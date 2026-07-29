#!/usr/bin/env python
"""Cold verifier for a literal planar Hall-deficient V4 countermodel."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.circuits import affine_compatible, build_v4_equation_system
from einstein.holonomy.alternating4.matching import (
    hall_witness_profile,
    minimal_hall_witness,
    two_center_matching,
    verify_two_matching,
)
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import PACKING_COLLISION_SEED
from einstein.holonomy.alternating4.local_system import build_v4_coverability_cnf


ROOT = Path(__file__).resolve().parents[1]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def verify(payload):
    if payload.get("status") != "PLANAR_HALL_COUNTERMODEL":
        return False
    record = payload.get("countermodel")
    if not record or record.get("status") != "PLANAR_HALL_COUNTERMODEL":
        return False
    placements = tuple(tuple(p) for p in record["placements"])
    if len(set(placements)) != len(placements):
        return False
    shape = decode_compiled_key(KEY)
    supports = tuple(frozenset(
        (u, v) for u, v, _sector in placement_lattice_cells(shape, placement)
    ) for placement in placements)
    matching = two_center_matching(supports, range(1, len(placements) + 1))
    if matching.saturated or not verify_two_matching(supports, matching):
        return False
    minimal = minimal_hall_witness(supports, matching.deficient_tiles)
    if minimal.deficient_tiles != tuple(range(1, len(placements) + 1)):
        return False
    if tuple(map(tuple, record["centers"])) != minimal.deficient_centers:
        return False
    profile = json.loads(json.dumps(hall_witness_profile(supports, minimal)))
    if profile != record["minimal_hall_profile"]:
        return False

    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    cells = tuple(placement_lattice_cells(shape, placement)
                  for placement in placements)
    actual_overlaps = 0
    for left, right in itertools.combinations(range(len(placements)), 2):
        if not cells[left] & cells[right]:
            continue
        actual_overlaps += 1
        if canonical_collision_type(cells[left], cells[right]) == target:
            return False
    if actual_overlaps != record.get("actual_overlap_pairs"):
        return False
    if payload.get("packing_mode") == "full" and actual_overlaps:
        return False

    margin = 6
    min_u = min(u for _, u, _ in placements)
    min_v = min(v for _, _, v in placements)
    shifted = tuple((operation, u - min_u + margin, v - min_v + margin)
                    for operation, u, v in placements)
    side_u = max(u for _, u, _ in shifted) + margin + 2
    side_v = max(v for _, _, v in shifted) + margin + 2
    side_u += side_u % 2
    side_v += side_v % 2
    hnf = side_u, 0, side_v
    base = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())["base_witnesses"]
    row = dict(next(item for item in base
                    if item["mapping_index"] == payload["mapping_index"]))
    twists = induced_v4_twists(tuple(row["base_twists"]), hnf)
    row["twists"] = list(twists)
    system = build_v4_equation_system(shape, hnf, row)
    lookup = {placement: variable for variable, placement in enumerate(
        system.placements, 1
    )}
    variables = tuple(lookup[p] for p in shifted)

    # Explicitly guard the finite-plane interpretation: none of the selected
    # boundary equations reaches a quotient seam.
    used_vertices = set()
    for variable in variables:
        for left, right, _value in system.equations[variable - 1]:
            used_vertices.update((system.vertices[left], system.vertices[right]))
    if not all(1 < vertex[2] < side_u - 2
               and 1 < vertex[3] < side_v - 2 for vertex in used_vertices):
        return False
    if not affine_compatible(system, variables):
        return False

    # Independent CNF replay of the union-find compatibility verdict.
    cnf, metadata = build_v4_coverability_cnf(
        shape, hnf, tuple(row["images"]), twists=twists, cover_mode="at-least"
    )
    implications = cnf.clauses[metadata["cover_clauses"]:]
    with Cadical195(bootstrap_with=implications) as solver:
        if not solver.solve(assumptions=variables):
            return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    args = parser.parse_args()
    payload = json.loads(Path(args.artifact).read_text())
    ok = verify(payload)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
