"""Pins for A4 ranking and exact-A1 overrides on the smallest A3 patches."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/notebook/assets"


def test_small_candidate_a4_results_respect_exact_periodic_overrides():
    payload = json.loads((ASSETS / "a4-small-candidate-results.json").read_text())
    assert len(payload["results"]) == 9
    periodic = [
        row for row in payload["results"]
        if row["exact_a1"]["verdict"] == "periodic"
    ]
    assert len(periodic) == 8
    assert {row["exact_a1"]["certificate_index"] for row in periodic} == {16}

    finalist = next(row for row in payload["results"] if row["n"] == 10)
    assert finalist["index"] == 2
    assert finalist["exact_a1"]["verdict"] == "no-periodic-at-budget"
    assert finalist["full"]["rank"] == finalist["full_confirm"]["rank"] == 4

    gallery = (ASSETS / "a4-small-candidate-spectra.svg").read_text()
    assert gallery.count("exact periodic · torus index 16") == 8
    for row in payload["results"]:
        assert (ASSETS / row["spectrum_png"]).is_file()
