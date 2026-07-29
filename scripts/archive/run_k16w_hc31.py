#!/usr/bin/env python
"""Externally supervise the two fixed HC-31 K16W cells sequentially."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time

from einstein.db import code_version
from einstein.theory.k16w_exact import CELLS


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "docs/notebook/assets"
LOGS = ROOT / "logs"
MANIFEST = ASSETS / "k16w-hc31-manifest.json"
EXTERNAL_SECONDS = 4 * 60 * 60
KILL_GRACE_SECONDS = 60


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    records = []
    for cell in CELLS:
        stem = f"k16w-hc31-{cell}"
        formula = ASSETS / f"{stem}.smt2"
        result = ASSETS / f"{stem}-result.json"
        log_path = LOGS / f"{stem}.log"
        started = time.monotonic()
        with log_path.open("wb") as log:
            completed = subprocess.run(
                [
                    "/usr/bin/timeout",
                    "--signal=TERM",
                    f"--kill-after={KILL_GRACE_SECONDS}s",
                    str(EXTERNAL_SECONDS),
                    sys.executable,
                    str(ROOT / "scripts/run_k16w_cell.py"),
                    cell,
                ],
                cwd=ROOT,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )
        elapsed = time.monotonic() - started
        if result.exists():
            payload = json.loads(result.read_text())
            status = payload.get("status", "malformed_result")
        else:
            status = "resource_stop" if completed.returncode in (124, 137) else "no_result"
            payload = {
                "kind": "k16w-hc31-cell-result",
                "schema_version": 1,
                "date": "2026-07-23",
                "cell": cell,
                "status": status,
                "elapsed_seconds": elapsed,
                "external_returncode": completed.returncode,
                "external_wall_seconds": EXTERNAL_SECONDS,
                "external_kill_grace_seconds": KILL_GRACE_SECONDS,
                "formula": {
                    "path": str(formula.relative_to(ROOT)) if formula.exists() else None,
                    "sha256": sha256(formula.read_bytes()).hexdigest() if formula.exists() else None,
                },
                "claim_boundary": "no solver verdict; cell remains open/frozen",
                "model": None,
            }
            result.write_text(json.dumps(payload, indent=1) + "\n")
        records.append({
            "cell": cell,
            "status": status,
            "elapsed_seconds": elapsed,
            "external_returncode": completed.returncode,
            "result": str(result.relative_to(ROOT)),
            "log": str(log_path.relative_to(ROOT)),
        })
        print(json.dumps(records[-1]), flush=True)

    manifest = {
        "kind": "k16w-hc31-decomposed-manifest",
        "schema_version": 1,
        "date": "2026-07-23",
        "code_version": code_version(),
        "cell_order": list(CELLS),
        "external_seconds_per_cell": EXTERNAL_SECONDS,
        "kill_grace_seconds": KILL_GRACE_SECONDS,
        "records": records,
        "complete": len(records) == len(CELLS),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
