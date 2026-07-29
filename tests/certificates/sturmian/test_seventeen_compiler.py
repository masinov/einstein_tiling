import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
DATA = ROOT / "data/sturmian-source/ahi-seventeen-rhombus-compiler.json"


def test_all_closest_equalizers_are_checked_as_source_decompositions():
    data = json.loads(DATA.read_text())
    assert data["equalizer_count"] == 4
    assert len(data["equalizers"]) == 4
    assert all(item["common_rhombus_count"] == 17 for item in data["equalizers"])
    assert all(
        item["added_singleton_count_per_side"] == 2
        for item in data["equalizers"]
    )


def test_source_compiler_legality_is_extensional():
    data = json.loads(DATA.read_text())
    for item in data["equalizers"]:
        assert item["all_A_plus_2M_contacts_continue"] == (
            item["failing_A_contacts"] == []
        )
        assert item["all_B_plus_2M_contacts_continue"] == (
            item["failing_B_contacts"] == []
        )
