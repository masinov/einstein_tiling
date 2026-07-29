#!/usr/bin/env python
"""Cutting-plane search for a finite planar Hall discharging certificate.

A nonnegative center taper ``phi`` is a certificate when every compatible
T2.D6 packing has weighted incidence at most ``2 * sum(phi)`` in the taper's
support.  Summing all translates counts each selected tile four times per
unit taper mass and proves density at most one half.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path

import highspy
from scipy.optimize import linprog

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.circuits import (
    affine_compatible,
    build_v4_equation_system,
    minimal_affine_circuit,
)
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.markings import resource_offsets
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import PACKING_COLLISION_SEED


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _instance(shape, row, radius):
    ambient = max(20, 4 * radius + 12)
    ambient += ambient % 2
    hnf = (ambient, 0, ambient)
    origin = ambient // 2
    row = dict(row)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    global_lookup = {placement: variable for variable, placement in enumerate(
        system.placements, 1
    )}
    region = tuple(resource_offsets(radius))
    region_set = set(region)
    operation_supports = tuple(
        frozenset((u, v) for u, v, _sector in placement_lattice_cells(
            shape, (operation, 0, 0)
        ))
        for operation in range(12)
    )
    placements = tuple(sorted({
        (operation, center[0] - offset[0] + origin,
         center[1] - offset[1] + origin)
        for operation in range(12)
        for center in region
        for offset in operation_supports[operation]
    }))
    supports = tuple(frozenset(
        (u - origin, v - origin)
        for u, v, _sector in placement_lattice_cells(shape, placement)
        if (u - origin, v - origin) in region_set
    ) for placement in placements)
    global_variables = tuple(global_lookup[p] for p in placements)
    full_cells = tuple(placement_lattice_cells(shape, placement)
                       for placement in placements)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    conflicts = []
    conflict_types = {}
    for left, right in itertools.combinations(range(len(placements)), 2):
        left_placement = placements[left]
        right_placement = placements[right]
        relative = (
            left_placement[0], right_placement[0],
            right_placement[1] - left_placement[1],
            right_placement[2] - left_placement[2],
        )
        forbidden = conflict_types.get(relative)
        if forbidden is None:
            left_cells = full_cells[left]
            right_cells = full_cells[right]
            packing = (
                bool(left_cells & right_cells)
                and canonical_collision_type(left_cells, right_cells) == target
            )
            forbidden = packing or not affine_compatible(
                system, (global_variables[left], global_variables[right])
            )
            conflict_types[relative] = forbidden
        if forbidden:
            conflicts.append((left, right))
    return system, region, placements, supports, global_variables, conflicts


def solve(
    shape, row, radius, maximum_iterations=1000, seed_orbits=(), signed=False,
    signed_bound=8.0,
):
    (system, region, placements, supports,
     global_variables, conflicts) = _instance(shape, row, radius)
    print(
        f"radius={radius} centers={len(region)} placements={len(placements)} "
        f"pair_conflicts={len(conflicts)} seeded_orbits={len(seed_orbits)}",
        flush=True,
    )
    center_index = {center: index for index, center in enumerate(region)}

    separator = highspy.Highs()
    separator.silent()
    separator.setOptionValue("threads", 16)
    selected = [separator.addBinary(name=f"x_{index}")
                for index in range(len(placements))]
    for left, right in conflicts:
        separator.addConstr(selected[left] + selected[right] <= 1)
    separator.setMaximize()
    local_lookup = {placement: index for index, placement in enumerate(placements)}
    learned_circuits = set()
    learned_orbits = []

    def add_local_translation_orbit(core_placements):
        first = core_placements[0]
        orbit = set()
        for candidate in placements:
            if candidate[0] != first[0]:
                continue
            shift = candidate[1] - first[1], candidate[2] - first[2]
            translated = tuple(sorted(
                local_lookup.get((placement[0], placement[1] + shift[0],
                                  placement[2] + shift[1]), -1)
                for placement in core_placements
            ))
            if -1 not in translated:
                orbit.add(translated)
        added = 0
        for translated in orbit:
            if translated in learned_circuits:
                continue
            separator.addConstr(
                sum(selected[index] for index in translated)
                <= len(translated) - 1
            )
            learned_circuits.add(translated)
            added += 1
        return added

    for seed in seed_orbits:
        core_placements = tuple(tuple(p) for p in seed["placements"])
        if all(p in local_lookup for p in core_placements):
            added = add_local_translation_orbit(core_placements)
            learned_orbits.append({
                "size": len(core_placements),
                "cuts_added": added,
                "seeded": True,
                "placements": [list(p) for p in core_placements],
            })

    weights = [1.0 / len(region)] * len(region)
    patterns = []
    master_value = float("-inf")

    def exact_separator(center_weights):
        objective_scale = 1.0 / max(center_weights)
        placement_weights = tuple(
            objective_scale * sum(
                center_weights[center_index[c]] for c in support
            )
            for support in supports
        )
        for index, weight in enumerate(placement_weights):
            separator.changeColCost(index, weight)
        affine_rounds = 0
        while True:
            separator.run()
            if separator.getModelStatus() != highspy.HighsModelStatus.kOptimal:
                raise RuntimeError(separator.modelStatusToString(
                    separator.getModelStatus()
                ))
            values = separator.getSolution().col_value[:len(selected)]
            chosen = tuple(index for index, value in enumerate(values) if value > 0.5)
            chosen_global = tuple(global_variables[index] for index in chosen)
            if affine_compatible(system, chosen_global):
                degrees = [0] * len(region)
                for index in chosen:
                    for center in supports[index]:
                        degrees[center_index[center]] += 1
                return (separator.getObjectiveValue() / objective_scale, chosen,
                        tuple(degrees), affine_rounds)
            core = minimal_affine_circuit(system, chosen_global)
            core_indices = tuple(sorted(
                global_variables.index(variable) for variable in core
            ))
            core_placements = tuple(placements[index] for index in core_indices)
            added = add_local_translation_orbit(core_placements)
            learned_orbits.append({
                "size": len(core_indices),
                "cuts_added": added,
                "placements": [list(placements[index]) for index in core_indices],
            })
            affine_rounds += 1
            if affine_rounds <= 10 or affine_rounds % 5 == 0:
                print(
                    f"  affine refinement={affine_rounds} core={len(core_indices)} "
                    f"translated={added} total_clauses={len(learned_circuits)}",
                    flush=True,
                )

    for iteration in range(maximum_iterations + 1):
        value, chosen, degrees, affine_rounds = exact_separator(weights)
        violation = value - 2.0
        if violation <= 1e-8:
            fractions = tuple(Fraction(weight).limit_denominator(10**6)
                              for weight in weights)
            total = sum(fractions)
            if total != 1:
                fractions = tuple(value / total for value in fractions)
            # Re-separate the rationalized vector before declaring success.
            rational_value, rational_chosen, rational_degrees, _ = exact_separator(
                [float(value) for value in fractions]
            )
            if rational_value > 2.0 + 1e-9:
                weights = [float(value) for value in fractions]
                continue
            return {
                "status": "FINITE_TAPER_CERTIFICATE",
                "radius": radius,
                "region_centers": len(region),
                "placements": len(placements),
                "pair_conflicts": len(conflicts),
                "iterations": iteration,
                "learned_affine_orbits": learned_orbits,
                "learned_affine_clauses": len(learned_circuits),
                "maximum_weighted_incidence": rational_value,
                "taper": [
                    {"center": list(center), "weight": str(weight)}
                    for center, weight in zip(region, fractions)
                    if weight
                ],
                "tight_configuration": [list(placements[index])
                                        for index in rational_chosen],
                "tight_degrees": list(rational_degrees),
                "patterns": patterns,
            }

        if degrees in {tuple(pattern["degrees"]) for pattern in patterns}:
            # The separator has exposed the current master epigraph exactly.
            # A positive repeated violation is therefore a finite lower-bound
            # certificate that this taper support cannot prove density 1/2.
            return {
                "status": "NO_TAPER_ON_THIS_REGION",
                "radius": radius,
                "region_centers": len(region),
                "placements": len(placements),
                "pair_conflicts": len(conflicts),
                "iterations": iteration,
                "minimum_maximum_violation": master_value,
                "minimum_local_bound": 2.0 + master_value,
                "learned_affine_orbits": learned_orbits,
                "learned_affine_clauses": len(learned_circuits),
                "patterns": patterns,
            }
        patterns.append({
            "degrees": list(degrees),
            "placements": [list(placements[index]) for index in chosen],
        })
        center_count = len(region)
        master_result = linprog(
            c=[0.0] * center_count + [1.0],
            A_ub=[
                [degree - 2 for degree in pattern["degrees"]] + [-1.0]
                for pattern in patterns
            ],
            b_ub=[0.0] * len(patterns),
            A_eq=[[1.0] * center_count + [0.0]],
            b_eq=[1.0],
            bounds=([(-signed_bound, signed_bound)] if signed
                    else [(0.0, None)]) * center_count
            + [(None, None)],
            method="highs",
        )
        if not master_result.success:
            raise RuntimeError(master_result.message)
        weights = list(master_result.x[:center_count])
        master_value = float(master_result.fun)
        if iteration < 20 or iteration % 25 == 0:
            print(
                f"iteration={iteration} separator={value:.9g} "
                f"violation={violation:.9g} master="
                f"{master_value:.9g} selected={len(chosen)} "
                f"affine_rounds={affine_rounds}",
                flush=True,
            )
    return {
        "status": "ITERATION_LIMIT",
        "radius": radius,
        "iterations": maximum_iterations,
        "patterns": patterns,
        "learned_affine_orbits": learned_orbits,
        "signed": signed,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--maximum-iterations", type=int, default=1000)
    parser.add_argument("--seed-circuits")
    parser.add_argument("--signed", action="store_true")
    parser.add_argument("--signed-bound", type=float, default=8.0)
    parser.add_argument("--output")
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = payload["base_witnesses"][0]
    seed_orbits = ()
    if args.seed_circuits:
        seed_orbits = json.loads(Path(args.seed_circuits).read_text()).get(
            "learned_affine_orbits", ()
        )
    result = solve(
        shape, row, args.radius, args.maximum_iterations,
        seed_orbits=seed_orbits, signed=args.signed,
        signed_bound=args.signed_bound,
    )
    result["mapping_index"] = row["mapping_index"]
    text = json.dumps(result, indent=1) + "\n"
    if args.output:
        Path(args.output).write_text(text)
        print(json.dumps({
            key: result[key] for key in (
                "status", "radius", "region_centers", "placements",
                "pair_conflicts", "iterations",
            ) if key in result
        }, indent=1))
    else:
        print(text)
    return 0 if result["status"] == "FINITE_TAPER_CERTIFICATE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
