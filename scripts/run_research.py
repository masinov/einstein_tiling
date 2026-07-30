#!/usr/bin/env python3
"""Launch the exact command frozen in an admitted experiment proposal."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from einstein.repository import repository_root
from einstein.repository.research import load_admitted_experiment, tree_bytes


ROOT = repository_root(Path(__file__))
POLL_SECONDS = 1.0
TIMEOUT_RETURN_CODE = 124
ARTIFACT_RETURN_CODE = 125


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

    budget = proposal["experiment"]["budget"]
    roots = [ROOT / item for item in budget["artifact_roots"]]
    baseline = sum(tree_bytes(path) for path in roots)
    max_growth = budget["max_new_artifact_bytes"]
    wall_seconds = budget["wall_time_seconds"]

    print(
        f"research gate: PASS [{proposal['id']}; wall={wall_seconds}s; "
        f"artifact budget={max_growth} bytes]",
        flush=True,
    )

    process = subprocess.Popen(
        command,
        cwd=ROOT,
        start_new_session=True,
    )
    started = time.monotonic()
    try:
        while process.poll() is None:
            elapsed = time.monotonic() - started
            if elapsed >= wall_seconds:
                terminate_group(process)
                print(
                    f"research stop: external wall limit reached after {elapsed:.1f}s",
                    file=sys.stderr,
                )
                return TIMEOUT_RETURN_CODE

            growth = max(0, sum(tree_bytes(path) for path in roots) - baseline)
            if growth > max_growth:
                terminate_group(process)
                print(
                    f"research stop: artifact growth {growth} exceeds {max_growth}",
                    file=sys.stderr,
                )
                return ARTIFACT_RETURN_CODE
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        terminate_group(process)
        raise

    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
