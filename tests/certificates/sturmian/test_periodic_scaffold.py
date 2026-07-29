import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.tilings.sturmian import verify_periodic_scaffold


ROOT = repository_root(Path(__file__))
ATLAS = ROOT / "data/sturmian-source/ahi-section10-supports.json"
SCAFFOLD = ROOT / "data/sturmian-source/ahi-periodic-scaffold.json"


def test_periodic_scaffold_cold_verifies():
    verify_periodic_scaffold(
        json.loads(SCAFFOLD.read_text()), json.loads(ATLAS.read_text())
    )


def test_affine_periodic_scaffold_is_exactly_refuted():
    scaffold = json.loads(SCAFFOLD.read_text())
    assert scaffold["periodic_witness"] is None
    assert scaffold["global_affine_perfect_matching_models"] == [
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 2],
    ]
    assert scaffold["macro_models"]["large_A"] == []
    assert scaffold["macro_models"]["large_B"] == []
