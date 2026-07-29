"""Pins for independent-solution robustness of the E1 finalist."""

import json
from pathlib import Path

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.polykites.patches import verify_patch_certificate

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/notebook/assets"


def test_finalist_signal_survives_independent_sat_phases():
    payload = json.loads(
        (ASSETS / "e1-finalist-robustness.json").read_text()
    )
    assert len(payload["results"]) == 4
    shape = decode_compiled_key(payload["candidate"]["shape"])
    for result in payload["results"]:
        assert verify_patch_certificate(shape, result["certificate"])
        assert result["a4"]["rank"] == 4
        assert result["a4"]["symmetry"] == 6
        assert result["a4_confirm"]["rank"] >= 4
        assert result["a4_confirm"]["verdict"] == "quasicrystal-candidate"

    assert max(
        overlap["jaccard"] for overlap in payload["pairwise_overlaps"]
    ) < 0.07
    boundary = payload["original_large_patch_boundary_audit"]
    assert boundary["missing_inside_certified_disk"] == 0
    assert boundary["certified_region_cells"] == 90_714
    assert boundary["overhang_cells"] == 1_676
    original = payload["original_large_patch_translation_profile"]
    period_47 = next(
        row for row in original if row["du"] == 0 and row["dv"] == 47
    )
    assert period_47["fraction"] == 1.0
    assert period_47["matched"] == period_47["eligible"] == 706

    sensitivity = payload["rank_top_sensitivity"]
    for top in ("20", "30", "40"):
        assert sensitivity["hat_control"]["rank_by_top"][top] == 2
        assert sensitivity["candidate"]["rank_by_top"][top] == 2
    for top in ("60", "100", "150", "250", "400"):
        assert sensitivity["periodic_control"]["rank_by_top"][top] == 2
        assert sensitivity["hat_control"]["rank_by_top"][top] == 4
        assert sensitivity["candidate"]["rank_by_top"][top] == 4
