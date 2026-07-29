#!/usr/bin/env python
"""MIP-guided discovery of minimal planar Hall obstructions.

HiGHS maximizes ``2|S|-|N(S)|``.  Every positive model is reduced to an
inclusion-minimal Hall witness; if its V4 equations are inconsistent, the
complete in-window translation orbit of a minimal affine circuit is learned.
The final artifact is cold-checked by a separately reconstructed SAT master.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

import highspy

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_circuits import affine_compatible, minimal_affine_circuit
from einstein.theory.a4_v4_hall import (
    hall_witness_profile,
    minimal_hall_witness,
    two_center_matching,
)
from einstein.theory.a4_v4_plane_hall import (
    build_planar_hall_instance,
    local_translation_orbit,
    verify_planar_no_hall_certificate,
)


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def solve(instance, maximum_iterations=10000):
    model = highspy.Highs()
    model.silent()
    model.setOptionValue("threads", 16)
    selected = [model.addBinary(obj=2.0, name=f"x_{index}")
                for index in range(len(instance.placements))]
    used = [model.addBinary(obj=-1.0, name=f"y_{index}")
            for index in range(len(instance.centers))]
    center_index = {center: index for index, center in enumerate(instance.centers)}
    for left, right in instance.conflicts:
        model.addConstr(selected[left - 1] + selected[right - 1] <= 1)
    for variable, support in enumerate(instance.supports):
        for center in support:
            model.addConstr(selected[variable] <= used[center_index[center]])
    model.setMaximize()

    global_to_local = {variable: index for index, variable in enumerate(
        instance.global_variables, 1
    )}
    learned_clauses = set()
    learned_orbits = []
    for iteration in range(maximum_iterations + 1):
        model.run()
        if model.getModelStatus() != highspy.HighsModelStatus.kOptimal:
            raise RuntimeError(model.modelStatusToString(model.getModelStatus()))
        objective_float = model.getObjectiveValue()
        objective = round(objective_float)
        if abs(objective_float - objective) > 1e-6:
            raise AssertionError("integral Hall objective was not integral")
        values = model.getSolution().col_value[:len(selected)]
        chosen = tuple(index + 1 for index, value in enumerate(values)
                       if value > 0.5)
        if objective <= 0:
            return {
                "status": "NO_PLANAR_HALL_DEFICIENCY",
                "iterations": iteration,
                "maximum_deficiency": objective,
                "learned_orbits": learned_orbits,
                "learned_clauses": len(learned_clauses),
            }

        matching = two_center_matching(instance.supports, chosen)
        if matching.saturated:
            raise AssertionError("positive Hall objective had a saturated matching")
        matching = minimal_hall_witness(
            instance.supports, matching.deficient_tiles
        )
        profile = hall_witness_profile(instance.supports, matching)
        witness_global = tuple(
            instance.global_variables[variable - 1]
            for variable in matching.deficient_tiles
        )
        if affine_compatible(instance.system, witness_global):
            return {
                "status": "PLANAR_HALL_DEFICIENT_COUNTERMODEL",
                "iterations": iteration,
                "maximum_deficiency": objective,
                "witness_profile": profile,
                "deficient_tiles": [
                    list(instance.placements[variable - 1])
                    for variable in matching.deficient_tiles
                ],
                "deficient_centers": [list(c) for c in matching.deficient_centers],
                "learned_orbits": learned_orbits,
                "learned_clauses": len(learned_clauses),
            }

        core_global = minimal_affine_circuit(instance.system, witness_global)
        representative = tuple(sorted(global_to_local[variable]
                                      for variable in core_global))
        orbit = local_translation_orbit(instance, representative)
        added = 0
        for circuit in orbit:
            if circuit in learned_clauses:
                continue
            model.addConstr(sum(selected[variable - 1] for variable in circuit)
                            <= len(circuit) - 1)
            learned_clauses.add(circuit)
            added += 1
        if not added:
            raise AssertionError("minimal Hall witness relearned an affine orbit")
        learned_orbits.append({
            "size": len(representative),
            "orbit_size": len(orbit),
            "clauses_added": added,
            "hall_witness_profile": profile,
            "placements": [
                list(instance.placements[variable - 1])
                for variable in representative
            ],
        })
        if iteration < 20 or iteration % 25 == 0:
            print(
                f"iteration={iteration} maximum_deficiency={objective} "
                f"minimal={profile['center_count']}/{2 * profile['tile_count']} "
                f"core={len(representative)} orbit={len(orbit)} "
                f"clauses={len(learned_clauses)}",
                flush=True,
            )
    return {
        "status": "ITERATION_LIMIT",
        "iterations": maximum_iterations,
        "learned_orbits": learned_orbits,
        "learned_clauses": len(learned_clauses),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", nargs=2, type=int, default=(4, 4))
    parser.add_argument("--maximum-iterations", type=int, default=10000)
    parser.add_argument("--output")
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = payload["base_witnesses"][0]
    instance = build_planar_hall_instance(shape, row, *args.window)
    print(
        f"window={instance.width}x{instance.height} "
        f"placements={len(instance.placements)} centers={len(instance.centers)} "
        f"packing_pairs={len(instance.packing_pairs)} "
        f"affine_pairs={len(instance.affine_pairs)}",
        flush=True,
    )
    result = solve(instance, args.maximum_iterations)
    result.update({
        "window": list(args.window),
        "placements": len(instance.placements),
        "centers": len(instance.centers),
        "packing_pairs": len(instance.packing_pairs),
        "affine_pairs": len(instance.affine_pairs),
        "mapping_index": row["mapping_index"],
        "learned_core_size_histogram": dict(sorted(Counter(
            item["size"] for item in result["learned_orbits"]
        ).items())),
    })
    if result["status"] == "NO_PLANAR_HALL_DEFICIENCY":
        result["cold_verified"] = verify_planar_no_hall_certificate(
            instance, result
        )
        if not result["cold_verified"]:
            raise AssertionError("cold Hall certificate verification failed")
    text = json.dumps(result, indent=1) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text)
    return 1 if result["status"].endswith("COUNTERMODEL") else 0


if __name__ == "__main__":
    raise SystemExit(main())

