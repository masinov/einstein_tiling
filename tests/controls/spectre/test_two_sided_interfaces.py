"""Pinned two-sided colored-interface and defect results."""

import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
ASSETS = ROOT / "docs/notebook/assets"


def test_two_sided_interface_frontier_is_complete_and_survives():
    artifact = json.loads(
        (ASSETS / "theory-w3-spectre-two-sided-overlap.json").read_text()
    )
    assert artifact["status"] == "TWO_SIDED_OVERLAP_LEAVES_A_FRONTIER"
    assert artifact["extension"]["radius9_states"] == 4482
    assert artifact["extension"]["two_sided_unresolved"] == 0
    assert artifact["alphabet"]["generated_states"] == 17
    assert artifact["alphabet"]["new_radius9_states"] == 3
    assert artifact["fixed_point"]["surviving_extra_states"] == 3


def test_extra_state_local_cost_split_is_pinned():
    artifact = json.loads(
        (ASSETS / "theory-w3-spectre-defect-propagation.json").read_text()
    )
    assert artifact["status"] == (
        "LOCAL_DEFECT_SPLIT_ONE_ABSORBABLE_TWO_PROPAGATING"
    )
    costs = sorted(
        row["minimum_extra_neighbors"]
        for row in artifact["analysis"]["states"]
    )
    assert costs == [0, 1, 1]
