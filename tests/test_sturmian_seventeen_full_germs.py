from pathlib import Path

from einstein.theory.sturmian_source import (
    _sab_corridor_bits,
)


def test_corridor_bits_still_distinguish_reflected_m_paths():
    # Minimal exact synthetic paths in the two signed bend classes.
    first = ((0, 0), (12, 0), (18, 6), (30, 6))
    second = ((0, 0), (12, 0), (18, -6), (30, -6))
    assert _sab_corridor_bits(first) == (0, 1)
    assert _sab_corridor_bits(second) == (1, 0)


def test_full_germ_artifact_is_pinned_when_present():
    path = Path("data/sturmian-source/ahi-seventeen-rhombus-full-germs.json")
    if not path.exists():
        return
    import json

    data = json.loads(path.read_text())
    assert data["schema"] == "ahi-sturmian-seventeen-rhombus-full-germs-v1"
    assert data["published_macro_contact_counts"] == {
        "large_A": 22,
        "large_B": 22,
    }
    assert data["calibrated_germ_differences_mod_6"] == [1, 3, 5]
    assert len(data["equalizers"]) == 4
    assert all(item["source_endpoint_signature_equal"] for item in data["equalizers"])
    assert all(item["legal_assignment_count_A"] == 4 for item in data["equalizers"])
    assert all(item["legal_assignment_count_B"] == 4 for item in data["equalizers"])
