import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
PAIRS = ROOT / "data/sturmian-source/ahi-interchangeable-pairs.json"


def test_published_local_pairs_have_exact_source_censuses():
    data = json.loads(PAIRS.read_text())
    assert data["outline_count"] == 32
    assert [pair["tile_census"] for pair in data["pairs"]] == [
        {"large_A": 3, "small_M": 6},
        {"large_A": 2, "large_B": 1, "small_M": 4},
    ]


def test_published_local_pairs_are_same_support_but_unrooted_isometric():
    data = json.loads(PAIRS.read_text())
    assert [pair["rhombus_count"] for pair in data["pairs"]] == [51, 49]
    assert all(pair["same_support_under_full_isometry"] for pair in data["pairs"])
    assert not any(
        pair["decompositions_distinct_under_full_isometry"]
        for pair in data["pairs"]
    )
