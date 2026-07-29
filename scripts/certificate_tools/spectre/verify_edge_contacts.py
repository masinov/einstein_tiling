#!/usr/bin/env python
"""Independent arithmetic verifier for the Spectre edge-patch bridge."""

from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path

from einstein.tilings.substitution import SPECTRE_TILE_BOUNDARY
from einstein.geometry.cyclotomic import madd, mneg, norm2_pair
from einstein.tilings.spectre.geometry import UNIT_DIRECTIONS


def verify(path):
    artifact = json.loads(Path(path).read_text())
    if (
        artifact.get("schema") != "einstein.w3.spectre-edge-patch-bridge"
        or artifact.get("version") != 1
        or artifact.get("status") != "UNRESTRICTED_EDGE_PATCH_BRIDGE_PROVED"
    ):
        return False, "unsupported schema or status"
    analysis = artifact["analysis"]
    unit_index = {vector: index for index, vector in enumerate(UNIT_DIRECTIONS)}
    directions = []
    for start, end in zip(
        SPECTRE_TILE_BOUNDARY,
        SPECTRE_TILE_BOUNDARY[1:] + SPECTRE_TILE_BOUNDARY[:1],
    ):
        vector = madd(end, mneg(start))
        if norm2_pair(vector) != (4, 0) or vector not in unit_index:
            return False, "non-unit primitive boundary edge"
        directions.append(unit_index[vector])
    angles = []
    for index, outgoing in enumerate(directions):
        turn = (outgoing - directions[index - 1] + 6) % 12 - 6
        angles.append(6 - turn)
    runs = []
    start = 0
    while start < len(directions):
        end = start + 1
        while end < len(directions) and directions[end] == directions[start]:
            end += 1
        runs.append((end - start, angles[start], angles[end % len(directions)]))
        start = end
    if not (
        len(directions) == 14
        and set(directions) == set(range(12))
        and sorted(length for length, _, _ in runs) == [1] * 12 + [2]
        and min(angles) == 3
        and all(not (left == right == 3) for _, left, right in runs)
    ):
        return False, "boundary angle/side hypotheses changed"

    words = ((1,), (2,), *product((1, 2), repeat=2))
    patterns = [(left, right) for left in words for right in words
                if sum(left) == sum(right)]
    if len(patterns) != 10:
        return False, "interface pattern count changed"
    stored = analysis["finite_correspondence"]
    stored_words = [(
        tuple(row["left_side_lengths"]),
        tuple(row["right_side_lengths"]),
    ) for row in stored["patterns"]]
    if stored_words != patterns:
        return False, "stored interface atlas changed"
    for row in stored["patterns"]:
        total = row["total_primitive_length"]
        if row["primitive_vertices"] != list(range(total + 1)):
            return False, "noncanonical primitive subdivision"
        if sum(row["left_side_lengths"]) != total:
            return False, "left length mismatch"
        if sum(row["right_side_lengths"]) != total:
            return False, "right length mismatch"

    for deformation in analysis["even_odd_deformation_control"]:
        vertices = [tuple(point) for point in deformation["vertices"]]
        if len(vertices) != 14 or len(set(vertices)) != 14:
            return False, "deformed boundary vertex count changed"
        vectors = [madd(end, mneg(start)) for start, end in zip(
            vertices, vertices[1:] + vertices[:1]
        )]
        parity = deformation["scaled_direction_parity"]
        norms = [norm2_pair(vector) for vector in vectors]
        expected = [
            (12, 0) if direction % 2 == parity else (4, 0)
            for direction in directions
        ]
        if norms != expected:
            return False, "even/odd deformation norms changed"
    theorem = analysis["theorem"]
    if not (
        theorem["unrestricted_contacts_reduce_to_primitive_edge_to_edge"]
        and theorem["T_junctions_are_exactly_primitive_vertices"]
    ):
        return False, "bridge theorem flags are false"
    return True, "14 primitive edges; 13 sides; 10/10 interface patterns"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    args = parser.parse_args()
    ok, message = verify(args.artifact)
    print(("PASS" if ok else "FAIL") + ": " + message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
