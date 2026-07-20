#!/usr/bin/env python
"""Build the pair-circuit orbit hypergraph and solve its clause dual."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_circuit_hypergraph import (
    affine_pair_circuit_orbits,
    packing_circuit_orbits,
    solve_orbit_clause_dual,
)
from einstein.theory.a4_v4_circuits import build_v4_equation_system
from einstein.theory.a4_v4_lift import induced_v4_twists


ROOT = Path(__file__).resolve().parents[1]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = dict(payload["base_witnesses"][0])
    hnf = (4, 0, 4)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    packing = packing_circuit_orbits(shape, system)
    affine = affine_pair_circuit_orbits(system)
    orbits = (*packing, *affine)
    result = solve_orbit_clause_dual(system, orbits)
    print(f"packing orbits: {len(packing)}")
    print(f"affine pair orbits: {len(affine)}")
    print(f"dual status: {result['model_status']}")
    print(f"dual density bound: {result['objective']:.12g}")
    print(f"nonzero orbit weights: {len(result['nonzero'])}")
    print(f"operation activity: {result['operation_activity']}")


if __name__ == "__main__":
    main()
