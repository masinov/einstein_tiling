#!/usr/bin/env python
"""Exact local incidence ranks for planar Hall discharging windows."""

from __future__ import annotations

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

import highspy

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_circuits import (
    affine_compatible,
    build_v4_equation_system,
    minimal_affine_circuit,
)
from einstein.theory.a4_v4_lift import induced_v4_twists
from einstein.theory.a4_v4_marking import resource_offsets
from einstein.theory.a4_v4_packing import (
    canonical_collision_type,
    placement_lattice_cells,
)
from einstein.theory.a4_v4_packing_family import PACKING_COLLISION_SEED


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def solve(shape, row, radius, maximum_iterations=1000):
    hnf = (20, 0, 20)
    row = dict(row)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    lookup = {placement: variable for variable, placement in enumerate(
        system.placements, 1
    )}
    region = set(resource_offsets(radius))
    operation_supports = [
        {(u, v) for u, v, _sector in placement_lattice_cells(
            shape, (operation, 0, 0)
        )}
        for operation in range(12)
    ]
    placements = tuple(sorted({
        (operation, center[0] - offset[0] + 10,
         center[1] - offset[1] + 10)
        for operation in range(12)
        for center in region
        for offset in operation_supports[operation]
    }))
    supports = tuple(
        {(u - 10, v - 10) for u, v, _sector in placement_lattice_cells(
            shape, placement
        )}
        for placement in placements
    )
    weights = tuple(len(support & region) for support in supports)
    global_variables = tuple(lookup[p] for p in placements)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    conflicts = []
    for left, right in itertools.combinations(range(len(placements)), 2):
        left_cells = placement_lattice_cells(shape, placements[left])
        right_cells = placement_lattice_cells(shape, placements[right])
        packing = (
            bool(left_cells & right_cells)
            and canonical_collision_type(left_cells, right_cells) == target
        )
        if packing or not affine_compatible(
            system, (global_variables[left], global_variables[right])
        ):
            conflicts.append((left, right))

    model = highspy.Highs()
    model.silent()
    selected = [model.addBinary(obj=weights[index], name=f"x_{index}")
                for index in range(len(placements))]
    for left, right in conflicts:
        model.addConstr(selected[left] + selected[right] <= 1)
    model.setMaximize()
    learned = []
    learned_clauses = set()
    local_lookup = {placement: index for index, placement in enumerate(placements)}
    for iteration in range(maximum_iterations + 1):
        model.run()
        if model.getModelStatus() != highspy.HighsModelStatus.kOptimal:
            raise RuntimeError(model.modelStatusToString(model.getModelStatus()))
        values = model.getSolution().col_value[:len(selected)]
        chosen = tuple(index for index, value in enumerate(values) if value > 0.5)
        objective = round(model.getObjectiveValue())
        chosen_global = tuple(global_variables[index] for index in chosen)
        if affine_compatible(system, chosen_global):
            return {
                "status": "EXACT_LOCAL_RANK",
                "radius": radius,
                "region_centers": len(region),
                "half_density_target": 2 * len(region),
                "placements": len(placements),
                "pair_conflicts": len(conflicts),
                "rank": objective,
                "rank_excess": objective - 2 * len(region),
                "iterations": iteration,
                "learned_circuits": learned,
                "selected": [
                    {"placement": list(placements[index]), "weight": weights[index]}
                    for index in chosen
                ],
            }
        core = minimal_affine_circuit(system, chosen_global)
        indices = tuple(sorted(global_variables.index(variable) for variable in core))
        first = placements[indices[0]]
        orbit = set()
        for candidate in placements:
            if candidate[0] != first[0]:
                continue
            shift = candidate[1] - first[1], candidate[2] - first[2]
            translated = tuple(sorted(
                local_lookup.get((placements[index][0],
                                  placements[index][1] + shift[0],
                                  placements[index][2] + shift[1]), -1)
                for index in indices
            ))
            if -1 not in translated:
                orbit.add(translated)
        added = 0
        for translated in sorted(orbit):
            if translated in learned_clauses:
                continue
            model.addConstr(
                sum(selected[index] for index in translated)
                <= len(translated) - 1
            )
            learned_clauses.add(translated)
            added += 1
        learned.append({
            "size": len(indices),
            "translation_cuts_added": added,
            "placements": [list(placements[index]) for index in indices],
        })
        if iteration < 20 or iteration % 25 == 0:
            print(
                f"iteration={iteration} objective={objective} "
                f"selected={len(chosen)} core={len(indices)} "
                f"translated={added} "
                f"histogram={dict(sorted(Counter(x['size'] for x in learned).items()))}",
                flush=True,
            )
    return {
        "status": "ITERATION_LIMIT",
        "radius": radius,
        "iterations": maximum_iterations,
        "learned_circuits": learned,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", type=int, default=1)
    parser.add_argument("--maximum-iterations", type=int, default=1000)
    parser.add_argument("--output")
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = payload["base_witnesses"][0]
    result = solve(shape, row, args.radius, args.maximum_iterations)
    result["mapping_index"] = row["mapping_index"]
    text = json.dumps(result, indent=1) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text)
    return 0 if result["status"] == "EXACT_LOCAL_RANK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
