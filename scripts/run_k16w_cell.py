#!/usr/bin/env python
"""Run one preregistered HC-31 K16W decomposition cell."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time

import z3

from einstein.polykites.database import code_version
from einstein.historical.thin_lens.exact import CELLS, build_problem


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
TIMEOUT_MS = 4 * 60 * 60 * 1000


def exact_value(value):
    value = z3.simplify(value)
    if z3.is_rational_value(value):
        return {
            "kind": "rational",
            "numerator": value.numerator_as_long(),
            "denominator": value.denominator_as_long(),
            "smt2": value.sexpr(),
        }
    if z3.is_algebraic_value(value):
        return {
            "kind": "algebraic",
            "smt2": value.sexpr(),
            "decimal_80": value.as_decimal(80),
        }
    return {"kind": "expression", "smt2": value.sexpr()}


def main(argv=None) -> int:
    argv = sys.argv if argv is None else argv
    if len(argv) != 2 or argv[1] not in CELLS:
        print(f"usage: {argv[0]} {{{'|'.join(CELLS)}}}", file=sys.stderr)
        return 2
    cell = argv[1]
    stem = f"k16w-hc31-{cell}"
    smt_path = ASSETS / f"{stem}.smt2"
    result_path = ASSETS / f"{stem}-result.json"
    verify_path = ASSETS / f"{stem}-result-verification.json"

    z3.set_param("memory_max_size", 96 * 1024)
    problem = build_problem(timeout_ms=TIMEOUT_MS, cell=cell)
    smt_path.write_text(problem.solver.to_smt2())
    started = time.monotonic()
    answer = problem.solver.check()
    elapsed = time.monotonic() - started
    status = str(answer)
    payload = {
        "kind": "k16w-hc31-cell-result",
        "schema_version": 1,
        "date": "2026-07-23",
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "timeout_ms": TIMEOUT_MS,
        "memory_limit_mib": 96 * 1024,
        "z3_version": z3.get_version_string(),
        "code_version": code_version(),
        "formula": {
            "path": str(smt_path.relative_to(ROOT)),
            "sha256": sha256(smt_path.read_bytes()).hexdigest(),
            "constraint_counts": problem.constraint_counts,
            "normalization": "u=1",
            "cell_theorems": "N38 + N39 polarity + K29O",
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
