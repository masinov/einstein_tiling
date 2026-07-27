import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/sturmian-source/ahi-unit-apex-compiler.json"


def test_unit_apex_census_is_complete():
    result = json.loads(RESULT.read_text())
    assert result["macros"]["large_A"]["binary_word_count"] == 2**16
    assert result["macros"]["large_B"]["binary_word_count"] == 2**16


def test_all_inward_small_m_collapses():
    result = json.loads(RESULT.read_text())
    assert result["small_M_all_inward"]["doubled_area"] == 0
    assert result["small_M_all_inward"]["distinct_vertex_count"] < 8
