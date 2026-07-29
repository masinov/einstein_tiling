#!/usr/bin/env python
"""Launch six concurrent, externally bounded HC-38 tangent cells."""

from __future__ import annotations

from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import time

from einstein.polykites.database import code_version
from einstein.historical.thin_lens.exact import HC34_CELLS


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "docs/notebook/assets"
LOGS = ROOT / "logs"
FORMULA_MANIFEST = ASSETS / "k16w-hc38-tangent-formulas.json"
RESULT_MANIFEST = ASSETS / "k16w-hc38-tangent-results.json"
LIVE_MANIFEST = ASSETS / "k16w-hc38-tangent-live.json"
EXTERNAL_SECONDS = 48 * 60 * 60
KILL_GRACE_SECONDS = 60
MEMORY_MIB = 16 * 1024


def stopped_payload(cell, formula_record, returncode, elapsed):
    status = "resource_stop" if returncode in (124, 137) else "no_result"
    return {
        "kind": "k16w-hc38-tangent-cell-result",
        "schema_version": 1,
        "date": "2026-07-24",
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "external_returncode": returncode,
        "external_wall_seconds": EXTERNAL_SECONDS,
        "external_kill_grace_seconds": KILL_GRACE_SECONDS,
        "memory_limit_mib": MEMORY_MIB,
        "formula": {
            "path": formula_record["path"],
            "sha256": formula_record["sha256"],
        },
        "claim_boundary": "no solver verdict; cell remains open/frozen",
        "model": None,
    }


def write_live(records, complete=False):
    LIVE_MANIFEST.write_text(json.dumps({
        "kind": "k16w-hc38-tangent-live-manifest",
        "schema_version": 1,
        "date": "2026-07-24",
        "code_version": code_version(),
        "cell_order": list(HC34_CELLS),
        "external_seconds_per_cell": EXTERNAL_SECONDS,
        "kill_grace_seconds": KILL_GRACE_SECONDS,
        "memory_limit_mib_per_cell": MEMORY_MIB,
        "records": records,
        "complete": complete,
    }, indent=1) + "\n")


def main() -> int:
    manifest = json.loads(FORMULA_MANIFEST.read_text())
    if not manifest.get("complete") or manifest.get("cell_order") != list(HC34_CELLS):
        raise RuntimeError("cold tangent formula manifest is incomplete or reordered")
    if manifest.get("cvc5_version") != importlib.metadata.version("cvc5"):
        raise RuntimeError("cvc5 version drift at supervisor launch")
    formula_records = {record["cell"]: record for record in manifest["records"]}
    for cell in HC34_CELLS:
        record = formula_records[cell]
        formula = ROOT / record["path"]
        data = formula.read_bytes()
        if len(data) != record["bytes"] or sha256(data).hexdigest() != record["sha256"]:
            raise RuntimeError(f"formula provenance failure for {cell}")

    ASSETS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    running = {}
    live_records = []
    for cell in HC34_CELLS:
        stem = f"k16w-hc38-tangent-{cell}"
        stdout_path = LOGS / f"{stem}.stdout.log"
        stderr_path = LOGS / f"{stem}.stderr.log"
        stdout = stdout_path.open("wb")
        stderr = stderr_path.open("wb")
        command = [
            "/usr/bin/timeout", "--signal=TERM",
            f"--kill-after={KILL_GRACE_SECONDS}s",
            str(EXTERNAL_SECONDS), sys.executable,
            str(ROOT / "scripts/run_k16w_hc38_cell.py"), cell,
        ]
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=stdout,
            stderr=stderr,
            start_new_session=True,
        )
        started = time.monotonic()
        running[cell] = {
            "process": process,
            "started": started,
            "stdout": stdout,
            "stderr": stderr,
            "stdout_path": stdout_path,
            "stderr_path": stderr_path,
        }
        live_records.append({
            "cell": cell,
            "pid": process.pid,
            "status": "running",
            "formula_sha256": formula_records[cell]["sha256"],
            "stdout": str(stdout_path.relative_to(ROOT)),
            "stderr": str(stderr_path.relative_to(ROOT)),
        })
    write_live(live_records)
    print(json.dumps({"launched": live_records}, indent=1), flush=True)

    completed_records = []
    while running:
        for cell in list(running):
            state = running[cell]
            returncode = state["process"].poll()
            if returncode is None:
                continue
            elapsed = time.monotonic() - state["started"]
            state["stdout"].close()
            state["stderr"].close()
            result_path = ASSETS / f"k16w-hc38-tangent-{cell}-result.json"
            if result_path.exists():
                payload = json.loads(result_path.read_text())
                payload["external_returncode"] = returncode
                payload["external_wall_seconds"] = EXTERNAL_SECONDS
                payload["external_kill_grace_seconds"] = KILL_GRACE_SECONDS
                result_path.write_text(json.dumps(payload, indent=1) + "\n")
            else:
                payload = stopped_payload(cell, formula_records[cell], returncode, elapsed)
                result_path.write_text(json.dumps(payload, indent=1) + "\n")
            record = {
                "cell": cell,
                "status": payload.get("status", "malformed_result"),
                "elapsed_seconds": elapsed,
                "external_returncode": returncode,
                "result": str(result_path.relative_to(ROOT)),
                "stdout": str(state["stdout_path"].relative_to(ROOT)),
                "stderr": str(state["stderr_path"].relative_to(ROOT)),
            }
            completed_records.append(record)
            print(json.dumps(record), flush=True)
            del running[cell]
        live = []
        completed_by_cell = {record["cell"]: record for record in completed_records}
        for cell in HC34_CELLS:
            if cell in completed_by_cell:
                live.append(completed_by_cell[cell])
            else:
                state = running[cell]
                live.append({
                    "cell": cell,
                    "pid": state["process"].pid,
                    "status": "running",
                    "elapsed_seconds": time.monotonic() - state["started"],
                    "formula_sha256": formula_records[cell]["sha256"],
                })
        write_live(live, complete=not running)
        if running:
            time.sleep(5)

    by_cell = {record["cell"]: record for record in completed_records}
    ordered = [by_cell[cell] for cell in HC34_CELLS]
    RESULT_MANIFEST.write_text(json.dumps({
        "kind": "k16w-hc38-tangent-result-manifest",
        "schema_version": 1,
        "date": "2026-07-24",
        "code_version": code_version(),
        "cvc5_version": importlib.metadata.version("cvc5"),
        "cvc5_options": manifest["cvc5_options"],
        "cell_order": list(HC34_CELLS),
        "external_seconds_per_cell": EXTERNAL_SECONDS,
        "kill_grace_seconds": KILL_GRACE_SECONDS,
        "memory_limit_mib_per_cell": MEMORY_MIB,
        "records": ordered,
        "complete": len(ordered) == len(HC34_CELLS),
    }, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
