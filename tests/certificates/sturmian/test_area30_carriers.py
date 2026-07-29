import json
from pathlib import Path

from einstein.tilings.sturmian import verify_area30_carrier_classification


ARTIFACT = Path("data/sturmian-source/ahi-area30-carrier-classification.json")
ATLAS = Path("data/sturmian-source/ahi-section10-supports.json")


def test_area30_artifact_has_complete_fixed_scope():
    data = json.loads(ARTIFACT.read_text())
    assert data["schema"] == "ahi-sturmian-area30-carrier-classification-v1"
    assert data["support_count"] == len(data["supports"])
    assert data["G_embedding_count"] == sum(
        item["G_embedding_count"] for item in data["supports"]
    )
    assert data["G_bipartite_matching_count"] == sum(
        state["bipartite_matching_count"]
        for item in data["supports"]
        for state in item["G"]
    )
    assert data["Z_bipartite_matching_count"] == sum(
        item["Z"]["bipartite_matching_count"] for item in data["supports"]
    )
    assert data["area30_parity_survivor_count"] == (
        data["G_bipartite_matching_count"]
        + data["Z_bipartite_matching_count"]
    )


def test_area30_artifact_cold_rebuilds():
    verify_area30_carrier_classification(
        json.loads(ARTIFACT.read_text()), json.loads(ATLAS.read_text())
    )
