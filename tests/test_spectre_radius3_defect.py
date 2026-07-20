"""Pinned radius-three Spectre defect-elimination theorem."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/notebook/assets/theory-w3-spectre-radius3-defect.json"


def test_radius_three_eliminates_all_extra_states_within_l18():
    artifact = json.loads(ARTIFACT.read_text())
    assert artifact["status"] == (
        "RADIUS3_ELIMINATES_ALL_EXTRA_STATES_WITHIN_L18"
    )
    assert artifact["scope"]["radius2_assignments_checked"] == 2232
    assert [root["radius2_assignments"] for root in artifact["roots"]] == [
        960, 432, 840,
    ]
    assert [root["radius3_satisfiable"] for root in artifact["roots"]] == [
        0, 2, 1,
    ]
    assert artifact["elimination"]["dead_root_state_ids"] == [
        "288091b49587a4b2",
    ]
    assert artifact["elimination"][
        "every_surviving_other_root_contains_a_dead_state"
    ]
    assert artifact["elimination"]["all_extra_states_eliminated"]
    assert artifact["elimination"]["conditional_contraction_closure"]


def test_every_recorded_survivor_contains_the_dead_state():
    artifact = json.loads(ARTIFACT.read_text())
    dead = set(artifact["elimination"]["dead_root_state_ids"])
    for root in artifact["roots"]:
        if root["root_state_id"] in dead:
            assert root["survivors"] == []
            continue
        assert root["survivors"]
        for survivor in root["survivors"]:
            assert dead & {
                defect["state_id"] for defect in survivor["fixed_defects"]
            }
