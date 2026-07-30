#!/usr/bin/env python3
"""Run one admitted, reproducibly pinned experiment under external limits."""

from __future__ import annotations

import json
import os
import resource
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from einstein.repository import repository_root
from einstein.repository.research import (
    admission_record_path,
    git_head,
    load_admitted_experiment,
    sha256_file,
    tree_bytes,
)


ROOT = repository_root(Path(__file__))
POLL_SECONDS = 0.25
TIMEOUT_RETURN_CODE = 124
ARTIFACT_RETURN_CODE = 125
SUPERVISOR_RETURN_CODE = 126


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    """Terminate the complete externally supervised process group."""

    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=5)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()


def sizes(paths: list[Path]) -> dict[str, int]:
    return {path.relative_to(ROOT).as_posix(): tree_bytes(path) for path in paths}


def total_growth(current: dict[str, int], baseline: dict[str, int]) -> int:
    return max(0, sum(current.values()) - sum(baseline.values()))


def write_manifest(path: Path, document: dict) -> None:
    """Create, but never replace, the supervisor record."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(document, stream, indent=2, sort_keys=True)
        stream.write("\n")


def set_memory_limit(memory_bytes: int) -> None:
    """Install the address-space cap in the child before the target exec."""

    resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))


def classify_completed_process(
    *,
    prior_status: str,
    elapsed: float,
    wall_seconds: int,
    final_growth: int,
    max_growth: int,
    return_code: int,
) -> str:
    """Apply final fail-closed checks after the child has exited."""

    if prior_status != "completed":
        return prior_status
    if elapsed >= wall_seconds:
        return "resource_stop_wall"
    if final_growth > max_growth:
        return "resource_stop_artifact"
    if return_code != 0:
        return "process_error"
    return "completed"


def main(argv: list[str]) -> int:
    if len(argv) < 4 or argv[2] != "--":
        print(
            "usage: run_research.py <proposal.json> -- <exact command> ...",
            file=sys.stderr,
        )
        return 2

    proposal_path = Path(argv[1])
    if not proposal_path.is_absolute():
        proposal_path = ROOT / proposal_path
    if not proposal_path.is_file():
        print(f"gate: missing proposal: {proposal_path}", file=sys.stderr)
        return 2

    try:
        proposal = load_admitted_experiment(proposal_path, ROOT)
    except ValueError as exc:
        for error in str(exc).splitlines():
            print(f"gate: {error}", file=sys.stderr)
        return 1

    command = argv[3:]
    frozen_command = proposal["experiment"]["command"]
    if command != frozen_command:
        print("gate: command does not match proposal experiment.command", file=sys.stderr)
        return 1

    experiment = proposal["experiment"]
    budget = experiment["budget"]
    roots = [ROOT / item for item in budget["artifact_roots"]]
    record = experiment["run_record"]
    manifest_path = ROOT / record["manifest_path"]
    stdout_path = ROOT / record["stdout_path"]
    stderr_path = ROOT / record["stderr_path"]
    for output in (manifest_path, stdout_path, stderr_path):
        if output.exists():
            print(f"gate: run record already exists and will not be overwritten: {output}", file=sys.stderr)
            return 1
        output.parent.mkdir(parents=True, exist_ok=True)

    baseline = sizes(roots)
    peak_growth = 0
    max_growth = budget["max_new_artifact_bytes"]
    wall_seconds = budget["wall_time_seconds"]
    memory_bytes = budget["memory_bytes"]
    admission_path = admission_record_path(ROOT, proposal["id"])
    started_utc = utc_now()
    started = time.monotonic()
    execution_status = "completed"
    supervisor_error: str | None = None

    print(
        f"research gate: PASS [{proposal['id']}; wall={wall_seconds}s; "
        f"memory={memory_bytes}; artifact budget={max_growth} bytes]",
        flush=True,
    )

    return_code: int | None = None
    with stdout_path.open("xb") as stdout_stream, stderr_path.open("xb") as stderr_stream:
        try:
            process = subprocess.Popen(
                command,
                cwd=ROOT,
                start_new_session=True,
                stdout=stdout_stream,
                stderr=stderr_stream,
                preexec_fn=lambda: set_memory_limit(memory_bytes),
            )
        except (OSError, subprocess.SubprocessError) as exc:
            supervisor_error = f"could not launch under external limits: {exc}"
            execution_status = "supervisor_error"
        else:
            try:
                while execution_status == "completed" and process.poll() is None:
                    elapsed = time.monotonic() - started
                    current = sizes(roots)
                    growth = total_growth(current, baseline)
                    peak_growth = max(peak_growth, growth)
                    if elapsed >= wall_seconds:
                        execution_status = "resource_stop_wall"
                        terminate_group(process)
                        break
                    if growth > max_growth:
                        execution_status = "resource_stop_artifact"
                        terminate_group(process)
                        break
                    time.sleep(POLL_SECONDS)
            except KeyboardInterrupt:
                execution_status = "interrupted"
                terminate_group(process)

            if process.poll() is None:
                process.wait()
            return_code = process.returncode

    # A process can exit between polls.  Recheck both limits after exit so a
    # late successful return cannot outrun the declared boundary.
    elapsed = time.monotonic() - started
    final_sizes = sizes(roots)
    final_growth = total_growth(final_sizes, baseline)
    peak_growth = max(peak_growth, final_growth)
    execution_status = classify_completed_process(
        prior_status=execution_status,
        elapsed=elapsed,
        wall_seconds=wall_seconds,
        final_growth=final_growth,
        max_growth=max_growth,
        return_code=return_code if return_code is not None else SUPERVISOR_RETURN_CODE,
    )

    manifest = {
        "schema_version": 1,
        "proposal_id": proposal["id"],
        "proposal_path": proposal_path.relative_to(ROOT).as_posix(),
        "proposal_sha256": sha256_file(proposal_path),
        "admission_path": admission_path.relative_to(ROOT).as_posix(),
        "admission_sha256": sha256_file(admission_path),
        "pinned_code_revision": experiment["reproducibility"]["code_revision"],
        "launch_head_revision": git_head(ROOT),
        "command": command,
        "started_at": started_utc,
        "finished_at": utc_now(),
        "elapsed_seconds": round(elapsed, 6),
        "limits": {
            "wall_time_seconds": wall_seconds,
            "memory_bytes": memory_bytes,
            "max_new_artifact_bytes": max_growth,
        },
        "artifact_bytes": {
            "baseline": baseline,
            "final_before_manifest": final_sizes,
            "final_growth": final_growth,
            "peak_observed_growth": peak_growth,
            "poll_seconds": POLL_SECONDS,
        },
        "stdout_path": record["stdout_path"],
        "stdout_sha256": sha256_file(stdout_path),
        "stderr_path": record["stderr_path"],
        "stderr_sha256": sha256_file(stderr_path),
        "process_return_code": return_code,
        "execution_status": execution_status,
        "research_verdict": None,
        "supervisor_error": supervisor_error,
        "interpretation": "Execution completion or resource exhaustion is not a mathematical verdict.",
    }
    write_manifest(manifest_path, manifest)

    if execution_status == "resource_stop_wall":
        print(f"research stop: external wall limit reached after {elapsed:.3f}s", file=sys.stderr)
        return TIMEOUT_RETURN_CODE
    if execution_status == "resource_stop_artifact":
        print(
            f"research stop: artifact growth {final_growth} exceeds {max_growth}",
            file=sys.stderr,
        )
        return ARTIFACT_RETURN_CODE
    if execution_status in {"supervisor_error", "interrupted"}:
        if supervisor_error:
            print(f"research stop: {supervisor_error}", file=sys.stderr)
        return SUPERVISOR_RETURN_CODE
    return return_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
