#!/usr/bin/env python
"""Exact-MIP probe of the T2.D7 placement-density conjecture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import highspy

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.circuits import build_v4_equation_system
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import PACKING_COLLISION_SEED
from einstein.holonomy.constraints import quotient_boundary_data


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def solve_density_mip(shape, hnf, row, time_limit=300.0):
    row = dict(row)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    instance, _, _ = quotient_boundary_data(shape, hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing = collision_orbit_clauses(shape, hnf, instance, target)

    highs = highspy.Highs()
    highs.silent()
    highs.setOptionValue("time_limit", time_limit)
    highs.setOptionValue("mip_rel_gap", 0.0)
    selected = [highs.addBinary(obj=1.0, name=f"p_{index}")
                for index in range(len(system.placements))]
    potential = [[
        highs.addBinary(name=f"v_{vertex}_{bit}") for bit in range(2)
    ] for vertex in range(len(system.vertices))]
    for placement, equations in enumerate(system.equations):
        enabled = selected[placement]
        for left, right, packed in equations:
            for bit in range(2):
                left_bit = potential[left][bit]
                right_bit = potential[right][bit]
                if (packed >> bit) & 1:
                    highs.addConstr(left_bit + right_bit - enabled >= 0)
                    highs.addConstr(left_bit + right_bit + enabled <= 2)
                else:
                    highs.addConstr(right_bit - left_bit + enabled <= 1)
                    highs.addConstr(left_bit - right_bit + enabled <= 1)
    for clause in packing:
        left, right = (-literal - 1 for literal in clause)
        highs.addConstr(selected[left] + selected[right] <= 1)
    highs.maximize(sum(selected))
    status = highs.getModelStatus()
    info = highs.getInfo()
    solution = highs.getSolution()
    chosen = [
        list(system.placements[index])
        for index, value in enumerate(solution.col_value[:len(selected)])
        if value > 0.5
    ] if solution.value_valid else []
    return {
        "hnf": list(hnf),
        "centers": hnf[0] * hnf[2],
        "status": highs.modelStatusToString(status),
        "objective": info.objective_function_value,
        "dual_bound": info.mip_dual_bound,
        "gap": info.mip_gap,
        "nodes": info.mip_node_count,
        "selected": chosen,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hnf", nargs=3, type=int, default=(4, 0, 4))
    parser.add_argument("--time-limit", type=float, default=300.0)
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    result = solve_density_mip(
        shape, tuple(args.hnf), payload["base_witnesses"][0], args.time_limit
    )
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
