"""Contracted Spectre parent-interface overlap controls."""

import json
from pathlib import Path

from einstein.tilings.spectre.parent_interfaces import local_overlap_witnesses


ROOT = Path(__file__).resolve().parents[1]


def _states():
    artifact = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-parent-interface.json"
    ).read_text())["analysis"]
    return tuple(tuple(
        (row[0], row[1], tuple(row[2])) for row in record["corona"]
    ) for record in artifact["records"])


def test_all_uncolored_parent_coronas_have_triangle_overlap_support():
    states = _states()
    assert len(states) == 26
    assert all(local_overlap_witnesses(states, index, 1)
               for index in range(len(states)))


def test_no_go_artifact_retains_all_nine_extra_states():
    analysis = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-parent-interface.json"
    ).read_text())["analysis"]
    assert analysis["support_pruning_rounds"] == []
    assert analysis["surviving_states"] == list(range(26))
    assert analysis["surviving_extra_states"] == list(range(9))
