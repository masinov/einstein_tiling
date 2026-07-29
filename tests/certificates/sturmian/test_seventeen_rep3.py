import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
DATA = ROOT / "data/sturmian-source/ahi-seventeen-rhombus-rep3.json"


def test_similarity_has_norm_three_and_exact_area_ratio():
    data = json.loads(DATA.read_text())
    assert data["similarity_matrix_uv"] == [[1, 1], [-1, 2]]
    assert data["similarity_determinant"] == 3
    assert data["inflated_rhombus_count"] == 3 * data["small_rhombus_count"]


def test_each_published_51_rhombus_panel_has_a_three_tile_dissection_but_is_not_inflated():
    data = json.loads(DATA.read_text())
    assert [item["panel"] for item in data["panels"]] == [0, 1]
    assert all(item["similarity_witness_count"] == 0 for item in data["panels"])
    assert all(item["three_tile_partition_count"] > 0 for item in data["panels"])
