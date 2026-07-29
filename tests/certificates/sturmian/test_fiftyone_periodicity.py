import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
DATA = ROOT / "data/sturmian-source/ahi-fiftyone-envelope-periodicity.json"


def test_fiftyone_macro_one_and_two_copy_censuses_are_complete():
    data = json.loads(DATA.read_text())
    assert data["one_copy"]["forced_index"] == 51
    assert data["one_copy"]["hnf_count_tested"] == 72
    assert data["two_copy"]["forced_index"] == 102
    assert data["two_copy"]["edge_connected_union_count"] > 0


def test_any_periodic_macro_certificate_is_exactly_pinned():
    data = json.loads(DATA.read_text())
    for item in data["two_copy"]["translation_fundamental_domains"]:
        assert item["translation_lattice"]["determinant"] == 102
