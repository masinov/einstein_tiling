#!/usr/bin/env python
"""Serialize the six preregistered HC-38 tangent cells without solving."""

from __future__ import annotations

from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path

from einstein.polykites.database import code_version
from einstein.historical.thin_lens.exact import HC34_CELLS
from einstein.historical.thin_lens.tangent import build_tangent_problem


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
MANIFEST = ASSETS / "k16w-hc38-tangent-formulas.json"
OPTIONS = {
    "produce-models": "true",
    "produce-proofs": "false",
    "nl-cov": "true",
    "nl-cov-var-elim": "true",
}


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    records = []
    for cell in HC34_CELLS:
        problem = build_tangent_problem(cell)
        path = ASSETS / f"k16w-hc38-tangent-{cell}.smt2"
        smt2 = problem.solver.to_smt2()
        if not smt2.startswith("(set-logic QF_NRA)\n"):
            smt2 = "(set-logic QF_NRA)\n" + smt2
        path.write_text(smt2)
        records.append({
            "cell": cell,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
            "solver_variables": list(problem.variables),
            "constraint_counts": problem.constraint_counts,
            "nonadjacent_pairs": len(problem.nonadjacent_pairs),
            "positive_homothety": "all physical coordinates multiplied by K35T T>0",
        })
    payload = {
        "kind": "k16w-hc38-tangent-formula-manifest",
        "schema_version": 1,
        "date": "2026-07-24",
        "code_version": code_version(),
        "cvc5_version": importlib.metadata.version("cvc5"),
        "cvc5_options": OPTIONS,
        "cell_order": list(HC34_CELLS),
        "records": records,
        "complete": len(records) == 6,
        "claim_boundary": "serialization only; no solver verdict",
    }
    MANIFEST.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps(payload, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
