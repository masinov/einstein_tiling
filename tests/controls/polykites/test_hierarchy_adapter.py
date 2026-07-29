"""Exact kite-grid adapter and disk-core cover support for A6."""

import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.tilings.substitution import (
    canonical_cluster,
    frequent_nearest_templates,
)
from einstein.polykites.hierarchy import (
    cover_core_with_rule,
    contract_typed_core_cover,
    enumerate_core_covers,
    enumerate_typed_core_covers,
    frequent_hex_nearest_templates,
    hex_to_module,
    kite_op_sr,
    mine_joint_option_state_recursive_library,
    placement_poses,
    polykite_boundary,
    typed_core_backbone,
)
from einstein.geometry.kite_grid import (
    cell_vertices,
    transform_point,
)
from einstein.geometry.cyclotomic import apply_sr
from einstein.tilings.substitution import raw_hierarchy_level

ROOT = repository_root(Path(__file__))


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
    phases = enumerate_core_covers(poses, (1, 2), pair, pair)
    assert len(phases) == 2
    assert {phase.groups for phase in phases} == {
        (frozenset((0, 1)), frozenset((2, 3))),
        (frozenset((1, 2)),),
    }

    typed = enumerate_typed_core_covers(
        poses, range(4), (pair,), limit=2
    )
    assert len(typed) == 1
    contracted = contract_typed_core_cover(
        raw_hierarchy_level(poses), (pair,), typed[0]
    )
    assert contracted.types == (0, 0)
    assert len(contracted.level.poses) == 2
    assert typed_core_backbone(
        poses, range(4), (pair,), base_r2=100
    ) == {
        "satisfiable": True,
        "candidate_occurrences": 3,
        "candidate_bases": 3,
        "analyzed_bases": 3,
        "forced_bases": 2,
        "optional_bases": 0,
        "impossible_bases": 1,
        "all_analyzed_bases_forced": True,
        "allowed_type_profiles": {"": 1, "0": 2},
    }


def test_exact_hex_acceleration_matches_brute_nearest_mining():
    poses = placement_poses([
        (i % 12, 2 * i, 2 * (i % 3)) for i in range(12)
    ])
    fast = frequent_hex_nearest_templates(
        poses, min_size=4, max_size=4, top=5
    )[4]
    assert fast == frequent_nearest_templates(poses, size=4, top=5)


def test_joint_recursive_library_keeps_one_shared_state_alphabet():
    poses = placement_poses([
        (0, 0, 0), (0, 2, 0), (0, 4, 0), (0, 6, 0),
    ])
    alternating = {
        pose: ((0,) if i % 2 == 0 else (1,))
        for i, pose in enumerate(poses)
    }
    only_second_state = {pose: (1,) for pose in poses}
    result = mine_joint_option_state_recursive_library(
        [
            ("alternating", alternating),
            ("only-second", only_second_state),
        ],
        training_r2=100,
        forcing_r2=100,
        group_sizes=(2,),
    )
    assert result["satisfiable"] and result["all_samples_forced"]
    assert result["option_state_values"] == [[0], [1]]
    assert result["minimum_patterns"] == 2
    assert [
        sample["forced_inner_groups"]
        for sample in result["sample_results"]
    ] == [2, 2]
    assert {
        group["pattern"]
        for group in result["sample_results"][1]["forced_groups"]
    } == {1}


def test_hat_candidate_artifact_links_reproducible_svgs():
    result = json.loads(
        (ROOT / "docs/notebook/assets/a6-hat-screen-results.json").read_text()
    )
    assert result["status"] == "RULE-FAMILY"
    assert result["patch_tiles"] == 22_940
    assert len(result["candidates"]) == 2
    assert result["rule_family"]["covers_sampled"] == 20
    assert result["rule_family"]["cover_count_is_lower_bound"]
    assert result["rule_family"]["sampled_parent_anchor_sets_agree"]
    assert result["rule_family"]["interior_anchor_backbone"][
        "all_analyzed_bases_forced"
    ]
    recursive = result["rule_family"]["recursive_probe"]
    assert recursive["samples"] == 2
    assert recursive["minimum_patterns"] == 16
    assert recursive["selected_pattern_arities"] == {"7": 16}
    assert recursive["all_samples_forced"]
    first_samples = {
        sample["label"]: sample
        for sample in recursive["sample_results"]
    }
    assert {
        label: sample["forced_inner_groups"]
        for label, sample in first_samples.items()
    } == {
        "hat-r2-50000": 71,
        "hat-r2-100000": 72,
    }
    for sample in first_samples.values():
        assert sample["training_nodes"] == 430
        assert sample["optional_inner_groups"] == 0
        assert sample["inner_grouping_forced"]
        assert len(sample["forced_groups"]) == sample[
            "forced_inner_groups"
        ]
        assert all(
            0 <= group["pattern"] < recursive["minimum_patterns"]
            for group in sample["forced_groups"]
        )
        assert len({
            tuple(group["base"][:2]) + tuple(group["base"][2])
            for group in sample["forced_groups"]
        }) == sample["forced_inner_groups"]
    next_recursive = result["rule_family"]["next_recursive_probe"]
    assert next_recursive["samples"] == 2
    assert next_recursive["minimum_patterns"] == 15
    assert next_recursive["selected_pattern_arities"] == {"7": 6, "8": 9}
    assert next_recursive["all_samples_forced"]
    second_samples = {
        sample["label"]: sample
        for sample in next_recursive["sample_results"]
    }
    assert {
        label: (
            sample["training_nodes"],
            sample["forced_inner_groups"],
            sample["optional_inner_groups"],
        )
        for label, sample in second_samples.items()
    } == {
        "hat-r2-50000": (43, 8, 0),
        "hat-r2-100000": (41, 8, 0),
    }
    for sample in second_samples.values():
        assert all(
            0 <= group["pattern"] < next_recursive["minimum_patterns"]
            for group in sample["forced_groups"]
        )
    for candidate in result["candidates"]:
        svg = ROOT / candidate["svg"]
        text = svg.read_text()
        assert text.count("<polygon ") == 16
        assert text.count('stroke-dasharray="7 5"') == 1
