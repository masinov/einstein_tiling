"""Pins for the exact extended-period audit of the E1 finalist."""

import json
from pathlib import Path

from einstein.repository import repository_root

ROOT = repository_root(Path(__file__))
RESULTS = ROOT / "docs/notebook/assets/e1-finalist-periodicity.json"


def test_finalist_has_no_torus_through_index_215():
    payload = json.loads(RESULTS.read_text())
    assert payload["prior_completed_range"] == [1, 100]
    assert payload["completed_contiguous_extension"] == [105, 215]
    assert payload["area_compatible_step"] == 5
    assert payload["extension_status"] == "all-refuted-no-exhaustions"
    assert 235 in payload["additional_refuted_indices"]
    assert {
        row["status"] for row in payload["period_47_cylinders"]
    } == {"refuted"}
