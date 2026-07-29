#!/usr/bin/env python
"""Lift a pairwise-compatible torus extremizer and find its first Hall core.

This is a structural falsification/discovery probe, not an infinite proof.  It
shows how a locally admissible periodic pattern accumulates positive incidence
curvature in the plane and identifies the affine circuit that prevents the
first deletion-minimal Hall obstruction from being globally V4-compatible.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.circuits import (
    affine_compatible,
    build_v4_equation_system,
    minimal_affine_circuit,
)
from einstein.holonomy.alternating4.matching import (
    hall_deficiency,
    hall_witness_profile,
    minimal_hall_witness,
    two_center_matching,
)
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import PACKING_COLLISION_SEED


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"
PAIRWISE_4X4_EXTREMIZER = (
    (4, 0, 0), (6, 0, 1), (6, 1, 1),
    (9, 2, 0), (9, 3, 0),
    (11, 0, 0), (11, 1, 3), (11, 2, 2), (11, 3, 3),
)


def _supports(shape, placements):
    return tuple(frozenset(
        (u, v) for u, v, _sector in placement_lattice_cells(shape, placement)
    ) for placement in placements)


def first_hall_core(shape, maximum_periods):
    tested = []
    rectangles = sorted(
        itertools.product(range(1, maximum_periods + 1), repeat=2),
        key=lambda pair: (pair[0] * pair[1], max(pair), pair),
    )
    for width, height in rectangles:
        placements = tuple(
            (operation, u + 4 * i, v + 4 * j)
            for i in range(width)
            for j in range(height)
            for operation, u, v in PAIRWISE_4X4_EXTREMIZER
        )
        supports = _supports(shape, placements)
        matching = two_center_matching(supports, range(1, len(placements) + 1))
        tested.append({
            "period_rectangle": [width, height],
            "placements": len(placements),
            "whole_set_deficiency": hall_deficiency(
                supports, range(1, len(placements) + 1)
            ),
            "has_hall_deficient_subset": not matching.saturated,
        })
        if matching.saturated:
            continue
        minimal = minimal_hall_witness(supports, matching.deficient_tiles)
        return tested, placements, supports, minimal
    return tested, (), (), None


def analyze(shape, signature_row, maximum_periods=7):
    tested, placements, supports, witness = first_hall_core(
        shape, maximum_periods
    )
    if witness is None:
        return {
            "status": "NO_HALL_CORE_IN_SEARCH",
            "maximum_periods": maximum_periods,
            "tested": tested,
        }
    witness_placements = tuple(
        placements[variable - 1] for variable in witness.deficient_tiles
    )

    margin = 5
    min_u = min(u for _, u, _ in placements)
    min_v = min(v for _, _, v in placements)
    shift = margin - min_u, margin - min_v
    shifted = tuple((operation, u + shift[0], v + shift[1])
                    for operation, u, v in placements)
    max_u = max(u for _, u, _ in shifted) + margin + 1
    max_v = max(v for _, _, v in shifted) + margin + 1
    max_u += max_u % 2
    max_v += max_v % 2
    hnf = (max_u, 0, max_v)
    row = dict(signature_row)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    lookup = {placement: variable for variable, placement in enumerate(
        system.placements, 1
    )}
    shifted_witness = tuple(
        (operation, u + shift[0], v + shift[1])
        for operation, u, v in witness_placements
    )
    global_witness = tuple(lookup[p] for p in shifted_witness)

    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing_conflicts = 0
    affine_pair_conflicts = 0
    cells = tuple(placement_lattice_cells(shape, placement)
                  for placement in shifted_witness)
    for left, right in itertools.combinations(range(len(shifted_witness)), 2):
        if (cells[left] & cells[right]
                and canonical_collision_type(cells[left], cells[right]) == target):
            packing_conflicts += 1
        if not affine_compatible(
                system, (global_witness[left], global_witness[right])):
            affine_pair_conflicts += 1
    if packing_conflicts or affine_pair_conflicts:
        raise AssertionError("the lifted witness was not pairwise admissible")

    core = minimal_affine_circuit(system, global_witness)
    if not core:
        status = "PLANAR_HALL_COUNTERMODEL"
        core_placements = []
    else:
        status = "HALL_CORE_BLOCKED_BY_AFFINE_CIRCUIT"
        core_placements = [
            [operation, u - shift[0], v - shift[1]]
            for operation, u, v in (system.placements[variable - 1]
                                    for variable in core)
        ]
    return {
        "status": status,
        "source_torus": [4, 0, 4],
        "source_selected": [list(p) for p in PAIRWISE_4X4_EXTREMIZER],
        "maximum_periods": maximum_periods,
        "tested": tested,
        "first_period_rectangle": tested[-1]["period_rectangle"],
        "minimal_hall_profile": hall_witness_profile(supports, witness),
        "minimal_hall_placements": [list(p) for p in witness_placements],
        "packing_pair_conflicts": packing_conflicts,
        "affine_pair_conflicts": affine_pair_conflicts,
        "affine_compatible": not core,
        "minimal_affine_circuit_size": len(core),
        "minimal_affine_circuit": core_placements,
        "mapping_index": signature_row["mapping_index"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-periods", type=int, default=7)
    parser.add_argument("--output")
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    result = analyze(shape, payload["base_witnesses"][0], args.maximum_periods)
    text = json.dumps(result, indent=1) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text)
    return 1 if result["status"] == "PLANAR_HALL_COUNTERMODEL" else 0


if __name__ == "__main__":
    raise SystemExit(main())

