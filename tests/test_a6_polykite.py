"""Exact kite-grid adapter and disk-core cover support for A6."""

from einstein.funnel.a6_hierarchy import (
    canonical_cluster,
    frequent_nearest_templates,
)
from einstein.funnel.a6_polykite import (
    cover_core_with_rule,
    frequent_hex_nearest_templates,
    hex_to_module,
    kite_op_sr,
    placement_poses,
    polykite_boundary,
)
from einstein.substrate.kitegrid import (
    cell_vertices,
    transform_point,
)
from einstein.substrate.module12 import apply_sr


def test_kite_operations_embed_exactly_in_module12():
    points = [(0, 0), (1, 1), (4, -2), (-3, 5)]
    for op in range(12):
        s, r = kite_op_sr(op)
        for point in points:
            assert apply_sr(s, r, hex_to_module(point)) == hex_to_module(
                transform_point(point, op)
            )


def test_a3_placements_and_candidate_boundary():
    poses = placement_poses([(0, 4, -2), (7, -6, 8)])
    assert poses == (
        (0, 0, (4, 0, -2, 0)),
        (1, 8, (-6, 0, 8, 0)),
    )
    shape = ((0, 0, 0),)
    assert set(polykite_boundary(shape)) == {
        hex_to_module(point) for point in cell_vertices(shape[0])
    }


def test_core_cover_can_use_halo_but_requires_unique_core_composition():
    poses = placement_poses([(0, x, 0) for x in range(4)])
    pair = canonical_cluster(poses[:2])
    cover = cover_core_with_rule(poses, range(4), pair, pair)
    assert cover.n_solutions == 1
    assert cover.groups == (frozenset((0, 1)), frozenset((2, 3)))

    ambiguous = cover_core_with_rule(poses, (1, 2), pair, pair)
    assert ambiguous.n_solutions == 2


def test_exact_hex_acceleration_matches_brute_nearest_mining():
    poses = placement_poses([
        (i % 12, 2 * i, 2 * (i % 3)) for i in range(12)
    ])
    fast = frequent_hex_nearest_templates(
        poses, min_size=4, max_size=4, top=5
    )[4]
    assert fast == frequent_nearest_templates(poses, size=4, top=5)
