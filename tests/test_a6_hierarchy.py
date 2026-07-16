"""A6 v0: exact blind immediate-composition mining."""

import subprocess
from pathlib import Path

import pytest

from einstein.funnel.a6_hierarchy import (
    SPECTRE_TILE_BOUNDARY,
    _exact_cover_solutions,
    collar_label_validation,
    collared_substitution_rules,
    canonical_cluster,
    contracted_adjacency,
    contract_level,
    cover_with_rule,
    discover_composition,
    oriented_collar_colors,
    physical_edge_contacts,
    read_anchor_poses,
    read_hidden_node_labels,
    read_hidden_parent_groups,
    raw_hierarchy_level,
    recover_recursive_hierarchy,
    recover_order2_recurrence,
    refinement_isomorphism,
    template_occurrences,
    validate_against_hidden,
)
from einstein.substrate.module12 import (
    compare_quadratic,
    compose_pose,
    inverse_pose,
    relative_pose,
)

ROOT = Path(__file__).parent.parent
FIXTURE = ROOT / "tests" / "data" / "spectre-anchors-n3-delta.csv"
CORE = ROOT / "vendor" / "spectre" / "spectre-core"
IDENTITY = (0, 0, (0, 0, 0, 0))


def test_exact_pose_group():
    poses = [
        (0, 5, (3, -2, 7, 1)),
        (1, 9, (-4, 0, 2, 6)),
        (1, 0, (1, 1, -1, -1)),
    ]
    for pose in poses:
        assert compose_pose(inverse_pose(pose), pose) == IDENTITY
        assert compose_pose(pose, inverse_pose(pose)) == IDENTITY
        assert relative_pose(pose, pose) == IDENTITY


def test_exact_quadratic_comparison():
    assert compare_quadratic((2, 0), (1, 0)) > 0
    assert compare_quadratic((0, 1), (2, 0)) < 0  # sqrt(3) < 2
    assert compare_quadratic((7, -4), (0, 0)) > 0  # 7 > 4*sqrt(3)
    assert compare_quadratic((-7, 4), (0, 0)) < 0


def test_exact_template_occurrences():
    poses = [
        (0, 0, (0, 0, 0, 0)),
        (0, 0, (1, 0, 0, 0)),
        (0, 0, (4, 0, 0, 0)),
        (0, 0, (5, 0, 0, 0)),
    ]
    template = canonical_cluster(poses[:2])
    assert template_occurrences(template, poses) == (
        frozenset((0, 1)),
        frozenset((2, 3)),
    )


def test_disconnected_exact_cover_does_not_recurse_per_group():
    candidates = [frozenset((2 * i, 2 * i + 1)) for i in range(1500)]
    solutions = _exact_cover_solutions(3000, candidates)
    assert len(solutions) == 1
    assert len(solutions[0]) == 1500


def test_exact_colored_graph_isomorphism():
    left = (
        frozenset((1, 2)),
        frozenset((0, 2)),
        frozenset((0, 1)),
    )
    right = (
        frozenset((1, 2)),
        frozenset((0, 2)),
        frozenset((0, 1)),
    )
    mapping, _ = refinement_isomorphism(left, (0, 1, 2), right, (2, 0, 1))
    assert mapping == {0: 1, 1: 2, 2: 0}


def test_blind_spectre_immediate_composition():
    poses = read_anchor_poses(FIXTURE)
    rule, cover, diagnostics = discover_composition(
        poses, tile_boundary=SPECTRE_TILE_BOUNDARY
    )
    assert rule.full_size == 9
    assert (cover.n_full, cover.n_missing, cover.n_solutions) == (55, 8, 1)
    assert diagnostics["sizes"]["9"]["accepted"] == 2
    assert [
        (item["missing_internal_edges"], item["missing_exposed_edges"])
        for item in diagnostics["candidate_scores"]
    ] == [(34, 44), (32, 48)]
    assert diagnostics["selected"]["missing_adjacency"]["internal_edges"] == 34
    assert cover_with_rule(poses, rule.full, rule.missing) == cover


def test_physical_count_recurrence():
    result = recover_order2_recurrence([9, 71, 559, 4401])
    assert result == {"a": 8, "b": -1, "characteristic": [1, -8, 1]}


@pytest.mark.slow
def test_blind_partition_matches_withheld_ancestry(tmp_path):
    hierarchy = tmp_path / "hierarchy.csv"
    subprocess.run(
        [
            "cargo",
            "run",
            "--release",
            "--bin",
            "hierarchy",
            "--",
            "Delta",
            "3",
            hierarchy,
        ],
        cwd=CORE,
        check=True,
    )
    poses = read_anchor_poses(FIXTURE)
    rule, cover, _ = discover_composition(
        poses, tile_boundary=SPECTRE_TILE_BOUNDARY
    )
    hidden = read_hidden_parent_groups(hierarchy, poses)
    assert validate_against_hidden(cover.groups, hidden) == {
        "predicted": 63,
        "hidden": 63,
        "matched": 63,
        "precision": 1.0,
        "recall": 1.0,
        "exact": True,
    }


@pytest.mark.slow
def test_recursive_hierarchy_and_collar_labels(tmp_path):
    paths = {}
    for level in (4, 5):
        for binary in ("anchors", "hierarchy"):
            path = tmp_path / f"{binary}-{level}.csv"
            subprocess.run(
                [
                    "cargo",
                    "run",
                    "--release",
                    "--bin",
                    binary,
                    "--",
                    "Delta",
                    str(level),
                    path,
                ],
                cwd=CORE,
                check=True,
            )
            paths[(binary, level)] = path

    training = read_anchor_poses(FIXTURE)
    p4 = read_anchor_poses(paths[("anchors", 4)])
    p5 = read_anchor_poses(paths[("anchors", 5)])
    physical_rule, _, _ = discover_composition(
        training, tile_boundary=SPECTRE_TILE_BOUNDARY
    )
    hierarchy = recover_recursive_hierarchy(
        p4, p5, physical_rule, SPECTRE_TILE_BOUNDARY
    )
    assert [len(level.poses) for level in hierarchy.levels] == [496, 63, 8, 1]
    assert [
        (cover.n_full, cover.n_missing) for cover in hierarchy.covers
    ] == [(55, 8), (7, 1), (1, 0)]
    for depth, level in enumerate(hierarchy.levels, 1):
        hidden = read_hidden_parent_groups(
            paths[("hierarchy", 4)], p4, levels_up=depth
        )
        assert validate_against_hidden(level.leaves, hidden)["exact"]

    immediate = contract_level(raw_hierarchy_level(p5), physical_rule)
    adjacency = contracted_adjacency(
        physical_edge_contacts(p5, SPECTRE_TILE_BOUNDARY), immediate
    )
    colors = oriented_collar_colors(immediate, adjacency, radius=1)
    labels = read_hidden_node_labels(
        paths[("hierarchy", 5)], p5, immediate, levels_up=1
    )
    validation = collar_label_validation(
        colors,
        labels,
        (i for i, neighbors in enumerate(adjacency) if len(neighbors) == 6),
    )
    assert validation == {
        "nodes": 3109,
        "collar_classes": 17,
        "labels": 9,
        "mixed_classes": {},
        "pure": True,
    }
    first_rule = hierarchy.rules[0]
    first_cover = cover_with_rule(
        immediate.poses, first_rule.full, first_rule.missing
    )
    parent = contract_level(immediate, first_rule, first_cover)
    rules = collared_substitution_rules(
        immediate,
        parent,
        first_cover,
        physical_edge_contacts(p5, SPECTRE_TILE_BOUNDARY),
    )
    assert rules["eligible_parents"] == 310
    assert rules["child_collar_classes"] == 17
    assert rules["parent_collar_classes"] == 17
    assert rules["ambiguous_classes"] == {}
    assert rules["deterministic"]
