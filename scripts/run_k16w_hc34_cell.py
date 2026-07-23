#!/usr/bin/env python
"""Run one preregistered bounded HC-34 K16W cell."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time

import z3

from einstein.db import code_version
from einstein.theory.k16w_exact import HC34_CELLS, build_problem
from run_k16w_cell import exact_value


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
TIMEOUT_MS = 3 * 60 * 60 * 1000
MEMORY_MIB = 32 * 1024


def main(argv=None) -> int:
    argv = sys.argv if argv is None else argv
    if len(argv) != 2 or argv[1] not in HC34_CELLS:
        print(f"usage: {argv[0]} {{{'|'.join(HC34_CELLS)}}}", file=sys.stderr)
        return 2
    cell = argv[1]
    stem = f"k16w-hc34-{cell}"
    formula_path = ASSETS / f"{stem}.smt2"
    result_path = ASSETS / f"{stem}-result.json"
    verify_path = ASSETS / f"{stem}-result-verification.json"

    z3.set_param("memory_max_size", MEMORY_MIB)
    problem = build_problem(timeout_ms=TIMEOUT_MS, hc34_cell=cell)
    serialized = problem.solver.to_smt2()
    if not formula_path.exists() or formula_path.read_text() != serialized:
        raise RuntimeError(f"formula drift for {cell}; cold serialization no longer matches")

    started = time.monotonic()
    answer = problem.solver.check()
    elapsed = time.monotonic() - started
    status = str(answer)
    payload = {
        "kind": "k16w-hc34-cell-result",
        "schema_version": 1,
        "date": "2026-07-23",
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "timeout_ms": TIMEOUT_MS,
        "memory_limit_mib": MEMORY_MIB,
        "z3_version": z3.get_version_string(),
        "code_version": code_version(),
        "formula": {
            "path": str(formula_path.relative_to(ROOT)),
            "sha256": sha256(formula_path.read_bytes()).hexdigest(),
            "constraint_counts": problem.constraint_counts,
            "normalization": "u=1",
            "cell_theorems": "N38/K29O + K31C + corrected N42 + K32S/K32A + N43/K33C",
            "simplicity": "all 120 exact closed-segment predicates retained",
        },
        "claim_boundary": {
            "sat": "requires exact cold verification; carrier geometry only",
            "unsat": "solver evidence only without replayable exact certificate",
            "unknown": "cell remains open/frozen; no rerun or escalation",
        },
        "model": None,
        "statistics": str(problem.solver.statistics()),
        "reason_unknown": problem.solver.reason_unknown() if status == "unknown" else None,
    }
    if status == "sat":
        model = problem.solver.model()
        payload["model"] = {
            name: exact_value(model.eval(variable, model_completion=True))
            for name, variable in problem.variables.items()
        }
    result_path.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps({
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "formula_sha256": payload["formula"]["sha256"],
    }, indent=1), flush=True)

    if status == "sat":
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/verify_k16w_exact.py"),
             str(result_path), cell],
            cwd=ROOT,
            check=False,
        )
        if not verify_path.exists() or completed.returncode != 0:
            print("cold verification did not certify the SAT model", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
