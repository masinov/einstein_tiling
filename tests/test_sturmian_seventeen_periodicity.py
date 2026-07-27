import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/sturmian-source/ahi-seventeen-rhombus-periodicity.json"


def test_one_copy_hnf_list_is_complete():
    data = json.loads(DATA.read_text())
    assert data["one_copy"]["forced_index"] == 17
    assert data["one_copy"]["hnf_count_tested"] == 18


def test_two_copy_certificates_are_pinned_to_exact_poses_and_lattices():
    data = json.loads(DATA.read_text())
    two = data["two_copy"]
    assert two["forced_index"] == 34
    assert two["edge_connected_union_count"] > 0
    assert two["translation_fundamental_domain_count"] == len(
        two["translation_fundamental_domains"]
    )
    for item in two["translation_fundamental_domains"]:
        assert item["translation_lattice"]["determinant"] == 34
