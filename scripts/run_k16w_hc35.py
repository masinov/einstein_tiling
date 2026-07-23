#!/usr/bin/env python
"""Run the user-authorized, fail-isolated HC-35 K16W batches.

The mathematical inputs are the immutable HC-34 formula files.  HC-35 only
changes process ownership: this supervisor is hosted by a transient user
service, and every cell starts a new session so a failed cell cannot signal a
sibling.  Screen is an optional log viewport and is not in this process tree.
"""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from einstein.db import code_version
from einstein.theory.k16w_exact import HC34_CELLS


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
LOGS = ROOT / "logs"
MANIFEST = ASSETS / "k16w-hc35-results.json"
LAUNCH_MANIFEST = ASSETS / "k16w-hc35-launch.json"
FORMULA_MANIFEST = ASSETS / "k16w-hc34-formulas.json"
EXTERNAL_SECONDS = 3 * 60 * 60
KILL_GRACE_SECONDS = 60
BATCHES = (HC34_CELLS[:3], HC34_CELLS[3:])


def result_path(cell: str) -> Path:
    # The single-cell runner consumes the frozen HC-34 namespace.  HC-34 wrote
    # no result, so these paths are required to be absent before HC-35 starts.
    return ASSETS / f"k16w-hc34-{cell}-result.json"


def stopped_payload(cell, formula, returncode, elapsed):
    status = "resource_stop" if returncode in (124, 137) else "no_result"
    return {
        "kind": "k16w-hc35-cell-result",
        "schema_version": 1,
        "date": "2026-07-24",
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "external_returncode": returncode,
        "external_wall_seconds": EXTERNAL_SECONDS,
        "external_kill_grace_seconds": KILL_GRACE_SECONDS,
        "formula": {
            "path": str(formula.relative_to(ROOT)),
            "sha256": sha256(formula.read_bytes()).hexdigest(),
        },
        "claim_boundary": "no solver verdict; cell remains open/frozen",
        "model": None,
    }


def launch_cell(cell: str, log) -> subprocess.Popen:
    """Start one externally supervised cell in an independent session."""

    return subprocess.Popen(
        [
            "/usr/bin/timeout", "--signal=TERM",
            f"--kill-after={KILL_GRACE_SECONDS}s",
            str(EXTERNAL_SECONDS), sys.executable,
            str(ROOT / "scripts/run_k16w_hc34_cell.py"), cell,
        ],
        cwd=ROOT,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )


def main() -> int:
    if not FORMULA_MANIFEST.exists():
        raise RuntimeError("cold formula manifest missing")
    formulas = json.loads(FORMULA_MANIFEST.read_text())
    if not formulas.get("complete") or formulas.get("cell_order") != list(HC34_CELLS):
        raise RuntimeError("cold formula manifest is incomplete or reordered")
    formula_records = {record["cell"]: record for record in formulas["records"]}
    for cell in HC34_CELLS:
        formula = ROOT / formula_records[cell]["path"]
        data = formula.read_bytes()
        if formula_records[cell]["bytes"] != len(data):
            raise RuntimeError(f"formula byte-count drift for {cell}")
        if formula_records[cell]["sha256"] != sha256(data).hexdigest():
            raise RuntimeError(f"formula hash drift for {cell}")
        if result_path(cell).exists():
            raise RuntimeError(f"stale cell result blocks fail-closed launch: {cell}")
    if MANIFEST.exists() or LAUNCH_MANIFEST.exists():
        raise RuntimeError("stale HC-35 manifest blocks fail-closed launch")

    ASSETS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    records = []
    launch = {
        "kind": "k16w-hc35-launch",
        "schema_version": 1,
        "date": "2026-07-24",
        "code_version": code_version(),
        "supervisor_pid": os.getpid(),
        "supervisor_process_group": os.getpgrp(),
        "ownership": "transient user service; screen is viewport only",
        "cell_isolation": "start_new_session=True",
        "cell_order": list(HC34_CELLS),
        "batches": [list(batch) for batch in BATCHES],
        "cells": [],
        "complete": False,
    }
    LAUNCH_MANIFEST.write_text(json.dumps(launch, indent=1) + "\n")

    for batch_index, batch in enumerate(BATCHES, 1):
        running = []
        for cell in batch:
            formula = ROOT / formula_records[cell]["path"]
            result = result_path(cell)
            log_path = LOGS / f"k16w-hc35-{cell}.log"
            log = log_path.open("xb")
            started = time.monotonic()
            process = launch_cell(cell, log)
            item = {
                "batch": batch_index,
                "cell": cell,
                "pid": process.pid,
                "process_group": os.getpgid(process.pid),
                "start_new_session": True,
                "formula_sha256": formula_records[cell]["sha256"],
                "log": str(log_path.relative_to(ROOT)),
            }
            launch["cells"].append(item)
            LAUNCH_MANIFEST.write_text(json.dumps(launch, indent=1) + "\n")
            running.append((cell, formula, result, log_path, log, started, process))

        # Reap every sibling before parsing any output.  A malformed or failed
        # cell therefore cannot make the supervisor abandon a live sibling.
        completed = []
        for item in running:
            *prefix, process = item
            returncode = process.wait()
            completed.append((*prefix, process, returncode))
        for cell, formula, result, log_path, log, started, process, returncode in completed:
            elapsed = time.monotonic() - started
            log.close()
            if result.exists():
                try:
                    payload = json.loads(result.read_text())
                except (json.JSONDecodeError, OSError):
                    payload = {"status": "malformed_result"}
            else:
                payload = stopped_payload(cell, formula, returncode, elapsed)
                result.write_text(json.dumps(payload, indent=1) + "\n")
            record = {
                "batch": batch_index,
                "cell": cell,
                "status": payload.get("status", "malformed_result"),
                "elapsed_seconds": elapsed,
                "external_returncode": returncode,
                "pid": process.pid,
                "process_group": process.pid,
                "result": str(result.relative_to(ROOT)),
                "log": str(log_path.relative_to(ROOT)),
            }
            records.append(record)
            print(json.dumps(record), flush=True)

    payload = {
        "kind": "k16w-hc35-decomposed-manifest",
        "schema_version": 1,
        "date": "2026-07-24",
        "code_version": code_version(),
        "formula_manifest": str(FORMULA_MANIFEST.relative_to(ROOT)),
        "cell_order": list(HC34_CELLS),
        "batches": [list(batch) for batch in BATCHES],
        "external_seconds_per_cell": EXTERNAL_SECONDS,
        "kill_grace_seconds": KILL_GRACE_SECONDS,
        "memory_limit_mib_per_cell": 32 * 1024,
        "cell_isolation": "start_new_session=True",
        "records": records,
        "complete": len(records) == len(HC34_CELLS),
    }
    MANIFEST.write_text(json.dumps(payload, indent=1) + "\n")
    launch["complete"] = True
    launch["result_manifest"] = str(MANIFEST.relative_to(ROOT))
    LAUNCH_MANIFEST.write_text(json.dumps(launch, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
