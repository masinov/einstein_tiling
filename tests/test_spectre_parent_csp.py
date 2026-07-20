"""Pinned radius-two Spectre parent-state CSP result."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/notebook/assets/theory-w3-spectre-radius2-defect.json"


def test_all_three_defects_propagate_through_parent_radius_two():
    artifact = json.loads(ARTIFACT.read_text())
    assert artifact["status"] == (
        "RADIUS2_FORCES_TYPED_OUTER_DEFECT_FOR_ALL_THREE_STATES"
    )
    assert artifact["conclusion"]["minimum_outer_extras"] == [1, 1, 1]
    assert artifact["conclusion"]["all_zero_outer_problems_unsatisfiable"]
    assert [root["root_star_witnesses"] for root in artifact["roots"]] == [
        28, 100, 3,
    ]
    assert [root["satisfiable_witnesses"] for root in artifact["roots"]] == [
        1, 1, 1,
    ]
    assert [root["minimum_nonroot_extras"] for root in artifact["roots"]] == [
        3, 2, 3,
    ]
    assert [root["complete_assignment_count"] for root in artifact["roots"]] == [
        960, 432, 840,
    ]
    assert [root["forced_outer_extra_state_ids"] for root in artifact["roots"]] == [
        ["2f1d7f0fac5b9704"],
        ["2f1d7f0fac5b9704"],
        ["288091b49587a4b2"],
    ]


def test_radius_two_best_witnesses_have_one_outer_defect():
    artifact = json.loads(ARTIFACT.read_text())
    for root in artifact["roots"]:
        assignment = root["best_assignment"]
        assert sum(row["ring"] == 0 for row in assignment) == 1
        assert sum(
            row["ring"] == 2 and row["source"] == "extra"
            for row in assignment
        ) == 1
