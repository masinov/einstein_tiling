"""A6 v0: exact blind immediate-composition mining."""

import subprocess
from pathlib import Path

import pytest

from einstein.funnel.a6_hierarchy import (
    SPECTRE_TILE_BOUNDARY,
    canonical_cluster,
    cover_with_rule,
    discover_composition,
    read_anchor_poses,
    read_hidden_parent_groups,
    recover_order2_recurrence,
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
