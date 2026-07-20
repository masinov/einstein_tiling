"""Pins for the ancestry-free Spectre D1 edge-to-edge entry certificate."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/notebook/assets/theory-w3-spectre-d1-entry.json"
PLOT = ROOT / "docs/notebook/assets/theory-w3-spectre-d1-entry.svg"


def test_non_l18_coronas_have_empty_radius_five_frontier():
    artifact = json.loads(ARTIFACT.read_text())
    assert artifact["status"] == "EDGE_TO_EDGE_L18_ENTRY_PROVED_RADIUS5"
    assert artifact["scope"][
        "ancestry_or_parent_data_used_in_ring_enumeration"
    ] is False
    assert artifact["physical_prefix"] == {
        "complete_first_coronas": 166,
        "radius2_surviving_types": 30,
        "radius3_surviving_types": 21,
        "L18_corona_types": 18,
        "non_L18_radius3_types": [33, 44, 155],
    }
    elimination = artifact["elimination"]
    assert elimination["decisive_radius"] == 5
    assert elimination["all_extra_coronas_eliminated"]
    assert [
        row["surviving_patches"] for row in elimination["radius_records"]
    ] == [89, 368, 282, 0]
    assert [
        list(row["survivors_by_root_corona"].values())
        for row in elimination["radius_records"]
    ] == [[2, 27, 60], [200, 144, 24], [72, 18, 192], [0, 0, 0]]


def test_d1_certificate_preserves_non_edge_to_edge_boundary():
    artifact = json.loads(ARTIFACT.read_text())
    assert artifact["scope"]["contact_model"] == "edge-to-edge unit-edge tilings"
    assert "separate theorem" in artifact["claim_boundary"]
    assert "non-edge-to-edge" in artifact["claim_boundary"]
    assert "radius-five frontier is empty" in artifact["theorem"]["logic"]
    svg = PLOT.read_text()
    assert "D1 physical entry" in svg
    assert "radius 5" in svg
