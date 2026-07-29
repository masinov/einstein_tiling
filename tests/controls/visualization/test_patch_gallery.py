"""Pins for the first A3 screen of genuinely new blind candidates."""

import importlib.util
import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.polykites.patches import verify_patch_certificate

ROOT = repository_root(Path(__file__))
ASSETS = ROOT / "docs/notebook/assets"
SPEC = importlib.util.spec_from_file_location(
    "patch_candidates", ROOT / "scripts/visualize/polykites/patch_candidates.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_small_candidate_a3_results_and_gallery():
    payload = json.loads((ASSETS / "a3-small-candidate-results.json").read_text())
    assert payload["counts"] == {
        "grown_to_max": 9,
        "refuted": 1,
        "unknown": 0,
    }
    assert len(payload["results"]) == 10
    finals = [result["ladder"][-1] for result in payload["results"]]
    assert sum(rung["status"] == "refuted" for rung in finals) == 1
    assert sum(
        rung["status"] == "grown" and rung["r2"] == 12800
        for rung in finals
    ) == 9

    for result in payload["results"]:
        shape = decode_compiled_key(result["shape"])
        assert verify_patch_certificate(shape, result["largest_certificate"])

    expected = MODULE.render(payload)
    assert (ASSETS / "a3-small-candidate-patches.svg").read_text() == expected
