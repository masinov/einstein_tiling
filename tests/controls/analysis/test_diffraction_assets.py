"""Pins for A4 ranking and exact-A1 overrides on the smallest A3 patches."""

import json
from pathlib import Path

from einstein.repository import repository_root

ROOT = repository_root(Path(__file__))
ASSETS = ROOT / "docs/notebook/assets"


def test_small_candidate_a4_results_respect_exact_periodic_overrides():
    payload = json.loads((ASSETS / "a4-small-candidate-results.json").read_text())
    assert payload["literature_scope"] == {
        "published_aperiodic_polykite_horizon": 24,
        "all_rows_are_validation_not_discovery": True,
        "controlling_correction": "ERR-004/D-0049",
    }
    assert len(payload["results"]) == 9
    periodic = [
        row for row in payload["results"]
        if row["exact_a1"]["verdict"] == "periodic"
    ]
    assert len(periodic) == 8
    assert {row["exact_a1"]["certificate_index"] for row in periodic} == {16}

    turtle = next(row for row in payload["results"] if row["n"] == 10)
    assert turtle["index"] == 2
    assert turtle["known_name"] == "turtle"
    assert turtle["novel"] is False
    assert turtle["exact_a1"]["verdict"] == "no-periodic-at-budget"
    assert turtle["full"]["rank"] == turtle["full_confirm"]["rank"] == 4

    gallery = (ASSETS / "a4-small-candidate-spectra.svg").read_text()
    assert "n=10 known Turtle" in gallery
    assert gallery.count("exact periodic · torus index 16") == 8
    for row in payload["results"]:
        assert (ASSETS / row["spectrum_png"]).is_file()
