"""Pinned finite result for the one-sided colored parent alphabet."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-overlap.json"


def test_colored_overlap_frontier_is_recorded_honestly():
    artifact = json.loads(ARTIFACT.read_text())
    assert artifact["status"] == "COLORED_RADIUS1_OVERLAP_LEAVES_A_FRONTIER"
    assert artifact["alphabet"] == {
        "combined_states": 22,
        "generated_control_states": 17,
        "generated_radius7_states": 17,
        "extra_radius7_states": 5,
        "control_equals_radius7_generated": True,
        "generated_extra_intersection": 0,
        "generated_occurrences": 51309,
        "extra_occurrences": 6280,
    }
    assert artifact["fixed_point"]["surviving_states"] == 22
    assert artifact["fixed_point"]["surviving_extra_states"] == 5
    assert artifact["fixed_point"]["removed_generated_state_ids"] == []
