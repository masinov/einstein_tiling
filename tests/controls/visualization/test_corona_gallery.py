"""Pins for the reproducible gallery of the smallest blind A2 candidates."""

import importlib.util
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
SPEC = importlib.util.spec_from_file_location(
    "corona_candidates", ROOT / "scripts/visualize/polykites/corona_candidates.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_small_candidate_gallery_is_complete_and_current():
    rows = list(MODULE.smallest_depth3_candidates())
    assert len(rows) == 10
    assert [n for n, _, _, _ in rows].count(10) == 2
    assert [n for n, _, _, _ in rows].count(12) == 8

    expected = MODULE.render(rows)
    path = ROOT / "docs/notebook/assets/a2-depth3-small-candidates.svg"
    assert path.read_text() == expected
    assert expected.count("<polygon ") == 116
    assert expected.count("Hc ≥ 3") == 10
    assert "known Turtle" in expected


def test_known_shapes_are_excluded_from_novelty_promotion():
    novel = list(MODULE.novel_smallest_depth3_candidates())
    assert novel == []

    unregistered = list(MODULE.unregistered_smallest_depth3_candidates())
    assert len(unregistered) == 9
    assert all(key != MODULE.TURTLE_KEY for _, _, key, _ in unregistered)
