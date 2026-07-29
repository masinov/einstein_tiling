import json
from pathlib import Path

from einstein.tilings.sturmian import (
    boundary_vertices,
    verify_atlas,
)


ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "data" / "sturmian-source" / "ahi-section10-supports.json"


def test_exact_source_support_artifact():
    data = json.loads(ARTIFACT.read_text())
    verify_atlas(data)
    assert {
        name: support["primitive_triangle_count"]
        for name, support in data["supports"].items()
    } == {"large_A": 30, "large_B": 30, "small_M": 2}


def test_source_boundary_words_are_pinned():
    data = json.loads(ARTIFACT.read_text())
    assert data["supports"]["large_A"]["boundary_directions"] == [
        1, 1, 0, 5, 0, 5, 0, 5, 4, 4, 3, 2, 3, 2, 3, 2
    ]
    assert data["supports"]["large_B"]["boundary_directions"] == [
        0, 1, 0, 5, 5, 0, 5, 4, 4, 3, 2, 3, 3, 2, 1, 2
    ]
    assert data["supports"]["small_M"]["boundary_directions"] == [3, 2, 0, 5]
    for support in data["supports"].values():
        assert boundary_vertices(tuple(support["boundary_directions"]))


def test_source_sab_components_are_exact_triangle_pairings():
    data = json.loads(ARTIFACT.read_text())
    assert {
        name: {
            role: sum(component["role"] == role for component in support["sab_components"])
            for role in {component["role"] for component in support["sab_components"]}
        }
        for name, support in data["supports"].items()
    } == {
        "large_A": {"S": 6, "M": 6, "L": 3},
        "large_B": {"S": 6, "M": 6, "L": 3},
        "small_M": {"M": 1},
    }
    assert {
        name: support["source_embedding_count"]
        for name, support in data["supports"].items()
    } == {"large_A": 2, "large_B": 2, "small_M": 1}
    assert all(
        support["source_embeddings_one_support_isometry_orbit"]
        for support in data["supports"].values()
    )
