#!/usr/bin/env python
"""Run the single preregistered HC-27 K16W QF_NRA decision."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time

import z3

from einstein.polykites.database import code_version
from einstein.historical.thin_lens.exact import build_problem


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
SMT2 = ASSETS / "k16w-exact-qfnra.smt2"
RESULT = ASSETS / "k16w-exact-result.json"
VERIFY = ASSETS / "k16w-exact-verification.json"
TIMEOUT_MS = 8 * 60 * 60 * 1000


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


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    z3.set_param("memory_max_size", 96 * 1024)
    problem = build_problem(timeout_ms=TIMEOUT_MS)
    smt = problem.solver.to_smt2()
    SMT2.write_text(smt)

    started = time.monotonic()
    answer = problem.solver.check()
    elapsed = time.monotonic() - started
    status = str(answer)
    payload = {
        "kind": "k16w-exact-qfnra-result",
        "schema_version": 1,
        "date": "2026-07-22",
        "status": status,
        "elapsed_seconds": elapsed,
        "timeout_ms": TIMEOUT_MS,
        "memory_limit_mib": 96 * 1024,
        "z3_version": z3.get_version_string(),
        "code_version": code_version(),
        "formula": {
            "path": str(SMT2.relative_to(ROOT)),
            "sha256": sha256(SMT2.read_bytes()).hexdigest(),
            "constraint_counts": problem.constraint_counts,
            "normalization": "u=1",
            "unit_chart": "tangent half-angle; t0 in (0,1), t1*t2 nonzero",
            "simplicity": "exact closed-segment nonintersection on all 120 nonadjacent pairs",
        },
        "claim_boundary": {
            "sat": "requires separate exact cold verification before K16W reopens",
            "unsat": "solver evidence only without independently replayable exact certificate",
            "unknown": "K16W remains frozen; no budget or ordering escalation",
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
    RESULT.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps({
        "status": status,
        "elapsed_seconds": elapsed,
        "result": str(RESULT.relative_to(ROOT)),
        "formula_sha256": payload["formula"]["sha256"],
    }, indent=1), flush=True)

    if status == "sat":
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/verify_k16w_exact.py"), str(RESULT)],
            cwd=ROOT,
            check=False,
        )
        if not VERIFY.exists() or completed.returncode != 0:
            print("cold verification did not certify the SAT model", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

