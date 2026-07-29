#!/usr/bin/env python
"""Exact finite-window search for a planar two-center Hall obstruction."""

from __future__ import annotations

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_circuits import (
    affine_compatible,
    build_v4_equation_system,
    minimal_affine_circuit,
)
from einstein.theory.a4_v4_hall import (
    hall_witness_profile,
    minimal_hall_witness,
    two_center_matching,
    verify_two_matching,
)
from einstein.theory.a4_v4_lift import induced_v4_twists
from einstein.theory.a4_v4_packing import (
    canonical_collision_type,
    placement_lattice_cells,
)
from einstein.theory.a4_v4_packing_family import PACKING_COLLISION_SEED


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def search(shape, row, width, height, maximum_iterations=100000):
    # Six cells of margin keep every selected placement and its boundary away
    # from quotient seams.  The V4 oracle can therefore reuse the exact torus
    # equation extractor while all Hall supports remain unreduced planar sets.
    margin = 3
    ambient_width = width + 2 * margin
    ambient_height = height + 2 * margin
    # The induced V4 deck character is defined on sublattices of 2 Lambda.
    # Round the otherwise irrelevant ambient quotient dimensions up to even.
    ambient_width += ambient_width % 2
    ambient_height += ambient_height % 2
    hnf = (ambient_width, 0, ambient_height)
    row = dict(row)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    global_lookup = {
        placement: variable
        for variable, placement in enumerate(system.placements, 1)
    }
    placements = tuple(
        (operation, u, v)
        for operation in range(12)
        for u in range(margin, margin + width)
        for v in range(margin, margin + height)
    )
    global_variables = tuple(global_lookup[p] for p in placements)
    local_of_global = {variable: index for index, variable in enumerate(
        global_variables, 1
    )}
    supports = tuple(frozenset(
        (u, v) for u, v, _sector in placement_lattice_cells(shape, placement)
    ) for placement in placements)
    centers = tuple(sorted(set().union(*supports)))
    center_variables = {
        center: len(placements) + index
        for index, center in enumerate(centers, 1)
    }

    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    cnf = CNF()
    packing_pairs = 0
    affine_pairs = 0
    for left, right in itertools.combinations(range(len(placements)), 2):
        left_cells = placement_lattice_cells(shape, placements[left])
        right_cells = placement_lattice_cells(shape, placements[right])
        if (left_cells & right_cells
                and canonical_collision_type(left_cells, right_cells) == target):
            cnf.append([-(left + 1), -(right + 1)])
            packing_pairs += 1
        if not affine_compatible(
            system, (global_variables[left], global_variables[right])
        ):
            cnf.append([-(left + 1), -(right + 1)])
            affine_pairs += 1

    for variable, support in enumerate(supports, 1):
        for center in support:
            cnf.append([-variable, center_variables[center]])
    # 2*selected - used_centers >= 1.
    hall = CardEnc.atleast(
        lits=(list(range(1, len(placements) + 1)) * 2
              + [-center_variables[center] for center in centers]),
        bound=len(centers) + 1,
        top_id=max(cnf.nv, len(placements) + len(centers)),
        encoding=EncType.cardnetwrk,
    )
    cnf.extend(hall.clauses)
    print(
        f"window={width}x{height} placements={len(placements)} "
        f"centers={len(centers)} packing_pairs={packing_pairs} "
        f"affine_pairs={affine_pairs} variables={cnf.nv} "
        f"clauses={len(cnf.clauses)}",
        flush=True,
    )

    learned = []
    learned_clauses = set()
    with Cadical195(bootstrap_with=cnf) as solver:
        for iteration in range(1, maximum_iterations + 1):
            if not solver.solve():
                return {
                    "status": "NO_PLANAR_HALL_DEFICIENCY",
                    "iterations": iteration - 1,
                    "window": [width, height],
                    "placements": len(placements),
                    "centers": len(centers),
                    "packing_pairs": packing_pairs,
                    "affine_pairs": affine_pairs,
                    "learned": learned,
                    "learned_clauses": len(learned_clauses),
                }
            positive = {literal for literal in solver.get_model() if literal > 0}
            selected_local = tuple(
                variable for variable in range(1, len(placements) + 1)
                if variable in positive
            )
            matching = two_center_matching(supports, selected_local)
            if matching.saturated or not verify_two_matching(supports, matching):
                raise AssertionError("Hall encoding and matching disagree")
            matching = minimal_hall_witness(supports, matching.deficient_tiles)
            profile = hall_witness_profile(supports, matching)
            witness_global = tuple(
                global_variables[variable - 1]
                for variable in matching.deficient_tiles
            )
            if affine_compatible(system, witness_global):
                return {
                    "status": "PLANAR_HALL_DEFICIENT_COUNTERMODEL",
                    "iterations": iteration - 1,
                    "window": [width, height],
                    "selected": [list(placements[v - 1]) for v in selected_local],
                    "deficient_tiles": [
                        list(placements[v - 1]) for v in matching.deficient_tiles
                    ],
                    "deficient_centers": [list(c) for c in matching.deficient_centers],
                    "witness_profile": profile,
                    "learned": learned,
                }
            core_global = minimal_affine_circuit(system, witness_global)
            core_local = tuple(sorted(local_of_global[v] for v in core_global))
            clause = tuple(-variable for variable in core_local)
            if clause in learned_clauses:
                raise AssertionError("relearned the same affine circuit")
            solver.add_clause(list(clause))
            learned_clauses.add(clause)
            learned.append({
                "size": len(core_local),
                "hall_witness_profile": profile,
                "placements": [list(placements[v - 1]) for v in core_local],
            })
            if iteration <= 20 or iteration % 100 == 0:
                print(
                    f"iteration={iteration} selected={len(selected_local)} "
                    f"minimal_Hall={profile['center_count']}/"
                    f"{2 * profile['tile_count']} "
                    f"core={len(core_local)} histogram="
                    f"{dict(sorted(Counter(x['size'] for x in learned).items()))}",
                    flush=True,
                )
    raise AssertionError("unreachable")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", nargs=2, type=int, default=(4, 4))
    parser.add_argument("--maximum-iterations", type=int, default=100000)
    parser.add_argument("--output")
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = payload["base_witnesses"][0]
    result = search(shape, row, *args.window, args.maximum_iterations)
    result["mapping_index"] = row["mapping_index"]
    result["learned_core_size_histogram"] = dict(sorted(Counter(
        item["size"] for item in result["learned"]
    ).items()))
    text = json.dumps(result, indent=1) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text)
    return 1 if result["status"].endswith("COUNTERMODEL") else 0


if __name__ == "__main__":
    raise SystemExit(main())
