import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / "data/sturmian-source/ahi-l-anchor-selector.json"


def test_l_anchor_selector_has_two_rooted_classes():
    selector = json.loads(SELECTOR.read_text())
    assert len(selector["selector_alphabet"]) == 2
    assert {item["selector_bit"] for item in selector["macros"].values()} == {0, 1}


def test_each_large_macro_is_one_l_two_s_six_m():
    selector = json.loads(SELECTOR.read_text())
    for macro in selector["macros"].values():
        assert len(macro["L_hexagon"]["addresses"]) == 3
        assert len(macro["S_hexagons"]) == 2
        assert all(len(item["addresses"]) == 3 for item in macro["S_hexagons"])
        assert len(macro["role_address_partition"]["M"]) == 6
