#!/usr/bin/env python
"""Run the two fixed concurrent batches of three HC-34 cells."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time

from einstein.db import code_version
from einstein.theory.k16w_exact import HC34_CELLS


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
LOGS = ROOT / "logs"
MANIFEST = ASSETS / "k16w-hc34-results.json"
FORMULA_MANIFEST = ASSETS / "k16w-hc34-formulas.json"
EXTERNAL_SECONDS = 3 * 60 * 60
KILL_GRACE_SECONDS = 60
BATCHES = (HC34_CELLS[:3], HC34_CELLS[3:])


def stopped_payload(cell, formula, returncode, elapsed):
    status = "resource_stop" if returncode in (124, 137) else "no_result"
    return {
        "kind": "k16w-hc34-cell-result",
        "schema_version": 1,
        "date": "2026-07-23",
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


def main() -> int:
    if not FORMULA_MANIFEST.exists():
        raise RuntimeError("cold formula manifest missing")
    formulas = json.loads(FORMULA_MANIFEST.read_text())
    if not formulas.get("complete") or formulas.get("cell_order") != list(HC34_CELLS):
        raise RuntimeError("cold formula manifest is incomplete or reordered")
    ASSETS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    records = []

    for batch_index, batch in enumerate(BATCHES, 1):
        running = []
        for cell in batch:
            stem = f"k16w-hc34-{cell}"
            formula = ASSETS / f"{stem}.smt2"
            result = ASSETS / f"{stem}-result.json"
            log_path = LOGS / f"{stem}.log"
            log = log_path.open("wb")
            started = time.monotonic()
            process = subprocess.Popen(
                [
                    "/usr/bin/timeout", "--signal=TERM",
                    f"--kill-after={KILL_GRACE_SECONDS}s",
                    str(EXTERNAL_SECONDS), sys.executable,
                    str(ROOT / "scripts/run_k16w_hc34_cell.py"), cell,
                ],
                cwd=ROOT,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
            running.append((cell, formula, result, log_path, log, started, process))

        for cell, formula, result, log_path, log, started, process in running:
            returncode = process.wait()
            elapsed = time.monotonic() - started
            log.close()
            if result.exists():
                payload = json.loads(result.read_text())
            else:
                payload = stopped_payload(cell, formula, returncode, elapsed)
                result.write_text(json.dumps(payload, indent=1) + "\n")
            record = {
                "batch": batch_index,
                "cell": cell,
                "status": payload.get("status", "malformed_result"),
                "elapsed_seconds": elapsed,
                "external_returncode": returncode,
                "result": str(result.relative_to(ROOT)),
                "log": str(log_path.relative_to(ROOT)),
            }
            records.append(record)
            print(json.dumps(record), flush=True)

    payload = {
        "kind": "k16w-hc34-decomposed-manifest",
        "schema_version": 1,
        "date": "2026-07-23",
        "code_version": code_version(),
        "cell_order": list(HC34_CELLS),
        "batches": [list(batch) for batch in BATCHES],
        "external_seconds_per_cell": EXTERNAL_SECONDS,
        "kill_grace_seconds": KILL_GRACE_SECONDS,
        "memory_limit_mib_per_cell": 32 * 1024,
        "records": records,
        "complete": len(records) == len(HC34_CELLS),
    }
    MANIFEST.write_text(json.dumps(payload, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
