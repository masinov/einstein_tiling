#!/usr/bin/env python
"""Serialize the six preregistered HC-34 cells without solving them."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.db import code_version
from einstein.theory.k16w_exact import HC34_CELLS, build_problem


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
MANIFEST = ASSETS / "k16w-hc34-formulas.json"


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    records = []
    for cell in HC34_CELLS:
        problem = build_problem(hc34_cell=cell)
        path = ASSETS / f"k16w-hc34-{cell}.smt2"
        path.write_text(problem.solver.to_smt2())
        records.append({
            "cell": cell,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
            "constraint_counts": problem.constraint_counts,
            "nonadjacent_pairs": len(problem.nonadjacent_pairs),
        })
    payload = {
        "kind": "k16w-hc34-formula-manifest",
        "schema_version": 1,
        "date": "2026-07-23",
        "code_version": code_version(),
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
