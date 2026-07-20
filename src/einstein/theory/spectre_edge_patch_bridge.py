"""Finite unrestricted edge-patch bridge for the straight Spectre.

Polygonal tilings need not initially be edge-to-edge: a polygon corner may
lie in the interior of another polygon side.  For Tile(1,1), however, the
published maximal-segment argument has finite hypotheses that can be checked
directly on the exact boundary.  All maximal sides have primitive length one
or two, every angle is at least 90 degrees, and no maximal side has 90-degree
angles at both endpoints.  Hence a straight interface uses at most two sides
on either side.  The resulting ten length patterns all have the same unique
unit subdivision on both sides.
"""

from __future__ import annotations

from itertools import product

from einstein.funnel.a6_hierarchy import SPECTRE_TILE_BOUNDARY
from einstein.substrate.module12 import Vec4, madd, mneg, norm2_pair
from einstein.theory.spectre_geometry import (
    EDGE_DIRECTIONS,
    UNIT_DIRECTIONS,
    UNIT_DIRECTION_INDEX,
    _segments_intersect,
)


def subtract(left: Vec4, right: Vec4) -> Vec4:
    return madd(left, mneg(right))


def boundary_directions(boundary=SPECTRE_TILE_BOUNDARY):
    directions = []
    for start, end in zip(boundary, boundary[1:] + boundary[:1]):
        vector = subtract(end, start)
        try:
            directions.append(UNIT_DIRECTION_INDEX[vector])
        except KeyError as exc:
            raise ValueError("boundary contains a non-unit primitive edge") from exc
    return tuple(directions)


def interior_angle_units(directions=EDGE_DIRECTIONS):
    """Interior angles in units of 30 degrees, including the 180 vertex."""
    angles = []
    for index, outgoing in enumerate(directions):
        incoming = directions[index - 1]
        turn = (outgoing - incoming + 6) % 12 - 6
        angles.append(6 - turn)
    return tuple(angles)


def maximal_sides(directions=EDGE_DIRECTIONS):
    """Merge consecutive collinear primitive edges into polygon sides."""
    angles = interior_angle_units(directions)
    sides = []
    start = 0
    while start < len(directions):
        end = start + 1
        while end < len(directions) and directions[end] == directions[start]:
            end += 1
        sides.append({
            "first_primitive_edge": start,
            "primitive_edges": end - start,
            "direction": directions[start],
            "start_angle_units30": angles[start],
            "end_angle_units30": angles[end % len(directions)],
        })
        start = end
    return tuple(sides)


def side_words():
    """All length words on one interface side under the two-side bound."""
    return ((1,), (2,), *product((1, 2), repeat=2))


def primitive_offsets(word):
    return tuple(range(sum(word) + 1))


def corner_offsets(word):
    total = 0
    result = []
    for length in word[:-1]:
        total += length
        result.append(total)
    return tuple(result)


def edge_patch_patterns():
    """The ten ordered maximal-segment subdivision patterns."""
    patterns = []
    for left in side_words():
        for right in side_words():
            if sum(left) != sum(right):
                continue
            total = sum(left)
            primitive = primitive_offsets(left)
            if primitive != primitive_offsets(right):
                raise AssertionError("unit subdivisions disagree")
            patterns.append({
                "left_side_lengths": list(left),
                "right_side_lengths": list(right),
                "total_primitive_length": total,
                "left_polygon_corners": list(corner_offsets(left)),
                "right_polygon_corners": list(corner_offsets(right)),
                "primitive_vertices": list(primitive),
                "T_junction_offsets": list(sorted(
                    set(corner_offsets(left)) ^ set(corner_offsets(right))
                )),
            })
    return tuple(patterns)


def sqrt3_direction(direction: int) -> Vec4:
    """Exact vector sqrt(3)*e_direction in the rank-four module."""
    return madd(
        UNIT_DIRECTIONS[(direction - 1) % 12],
        UNIT_DIRECTIONS[(direction + 1) % 12],
    )


def deformed_boundary(scale_parity: int):
    """Scale one direction parity by sqrt(3), as in Theorem 3.1."""
    if scale_parity not in (0, 1):
        raise ValueError("scale_parity must be zero or one")
    points = [(0, 0, 0, 0)]
    for direction in EDGE_DIRECTIONS[:-1]:
        vector = (
            sqrt3_direction(direction)
            if direction % 2 == scale_parity else UNIT_DIRECTIONS[direction]
        )
        points.append(madd(points[-1], vector))
    closing_direction = EDGE_DIRECTIONS[-1]
    closing = (
        sqrt3_direction(closing_direction)
        if closing_direction % 2 == scale_parity
        else UNIT_DIRECTIONS[closing_direction]
    )
    if madd(points[-1], closing) != (0, 0, 0, 0):
        raise ValueError("deformed boundary does not close")
    return tuple(points)


def polygon_is_simple(polygon):
    if len(set(polygon)) != len(polygon):
        return False
    edges = tuple(zip(polygon, polygon[1:] + polygon[:1]))
    for left, (a, b) in enumerate(edges):
        for right, (c, d) in enumerate(edges[:left]):
            if right in ((left - 1) % len(edges), (left + 1) % len(edges)):
                continue
            if {a, b} & {c, d}:
                continue
            if _segments_intersect(a, b, c, d):
                return False
    return True


def analyze_edge_patch_bridge():
    directions = boundary_directions()
    if directions != tuple(EDGE_DIRECTIONS):
        raise ValueError("boundary and reference direction word disagree")
    angles = interior_angle_units(directions)
    sides = maximal_sides(directions)
    patterns = edge_patch_patterns()
    deformations = []
    for parity in (0, 1):
        boundary = deformed_boundary(parity)
        deformations.append({
            "scaled_direction_parity": parity,
            "boundary_closes_exactly": True,
            "boundary_is_simple_exactly": polygon_is_simple(boundary),
            "vertices": [list(point) for point in boundary],
        })
    if not all(row["boundary_is_simple_exactly"] for row in deformations):
        raise ValueError("an even/odd deformation self-intersects")
    if any(norm2_pair(sqrt3_direction(d)) != (12, 0) for d in range(12)):
        raise ValueError("sqrt(3)-scaled direction has the wrong exact norm")
    side_lengths = sorted(side["primitive_edges"] for side in sides)
    no_double_right = all(
        not (
            side["start_angle_units30"] == 3
            and side["end_angle_units30"] == 3
        )
        for side in sides
    )
    if not (
        len(directions) == 14
        and set(directions) == set(range(12))
        and min(angles) >= 3
        and no_double_right
        and side_lengths == [1] * 12 + [2]
        and len(patterns) == 10
    ):
        raise ValueError("edge-patch bridge hypotheses changed")
    return {
        "primitive_boundary": {
            "edges": len(directions),
            "direction_word": list(directions),
            "all_edges_have_unit_exact_norm": all(
                norm2_pair(subtract(end, start)) == (4, 0)
                for start, end in zip(
                    SPECTRE_TILE_BOUNDARY,
                    SPECTRE_TILE_BOUNDARY[1:] + SPECTRE_TILE_BOUNDARY[:1],
                )
            ),
            "uses_all_12_directions": set(directions) == set(range(12)),
        },
        "maximal_sides": {
            "count": len(sides),
            "length_histogram": {"1": 12, "2": 1},
            "records": list(sides),
        },
        "angle_bound": {
            "interior_angles_units30": list(angles),
            "minimum_degrees": min(angles) * 30,
            "no_maximal_side_has_right_angles_at_both_ends": no_double_right,
            "consequence": (
                "a straight tiling interface has at most two polygon sides "
                "on either side"
            ),
            "proof": (
                "three or more sides would give a middle tile whose two side "
                "endpoints are both 90-degree corners; any additional "
                "point-only tile already exceeds the 180-degree half-plane"
            ),
        },
        "finite_correspondence": {
            "side_words": [list(word) for word in side_words()],
            "ordered_equal_length_patterns": len(patterns),
            "patterns": list(patterns),
            "all_reduce_to_identical_unit_subdivisions": True,
            "maximum_interface_primitive_length": max(
                row["total_primitive_length"] for row in patterns
            ),
        },
        "orientation_and_anchor_lock": {
            "relative_orientations_are_multiples_of_30_degrees": True,
            "reason": (
                "every adjacency equates two directions from the complete "
                "12-direction word; connectedness propagates one frame"
            ),
            "neighbor_anchor_difference_lies_in_rank4_module": True,
            "reason_anchor": (
                "matched primitive endpoints are exact boundary module points"
            ),
        },
        "even_odd_deformation_control": deformations,
        "theorem": {
            "unrestricted_contacts_reduce_to_primitive_edge_to_edge": True,
            "bijection": (
                "split every maximal-side word at all integer offsets; the ten "
                "patterns map uniquely to full primitive unit-edge contacts, "
                "and forgetting artificial 180-degree splits is the inverse"
            ),
            "T_junctions_are_exactly_primitive_vertices": True,
        },
    }
