"""Unrestricted-contact bridge into the 14-edge Spectre model."""

import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.tilings.spectre.edge_contacts import (
    analyze_edge_patch_bridge,
    edge_patch_patterns,
)


ROOT = repository_root(Path(__file__))
ARTIFACT = (
    ROOT / "docs/notebook/assets/theory-w3-spectre-edge-patch-bridge.json"
)


def test_exact_boundary_meets_the_maximal_segment_hypotheses():
    analysis = analyze_edge_patch_bridge()
    assert analysis["primitive_boundary"]["edges"] == 14
    assert analysis["primitive_boundary"]["uses_all_12_directions"]
    assert analysis["maximal_sides"]["length_histogram"] == {"1": 12, "2": 1}
    assert analysis["angle_bound"]["minimum_degrees"] == 90
    assert analysis["angle_bound"][
        "no_maximal_side_has_right_angles_at_both_ends"
    ]


def test_all_ten_edge_patch_patterns_have_one_unit_subdivision():
    patterns = edge_patch_patterns()
    assert len(patterns) == 10
    assert {row["total_primitive_length"] for row in patterns} == {1, 2, 3, 4}
    assert all(
        row["primitive_vertices"]
        == list(range(row["total_primitive_length"] + 1))
        for row in patterns
    )


def test_unrestricted_bridge_artifact_keeps_chirality_scope():
    artifact = json.loads(ARTIFACT.read_text())
    assert artifact["status"] == "UNRESTRICTED_EDGE_PATCH_BRIDGE_PROVED"
    assert artifact["scope"]["reflections_allowed"] is False
    assert artifact["analysis"]["theorem"][
        "unrestricted_contacts_reduce_to_primitive_edge_to_edge"
    ]
    assert artifact["analysis"]["finite_correspondence"][
        "ordered_equal_length_patterns"
    ] == 10
