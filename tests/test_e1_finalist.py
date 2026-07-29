"""Pins for the blind E1 Turtle rediscovery (legacy "finalist" assets)."""

import json
from pathlib import Path

from einstein.polykites.known_shapes import TURTLE_KEY, decode_compiled_key
from einstein.polykites.patches import verify_patch_certificate

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/notebook/assets"


def test_e1_finalist_large_patch_and_spectrum_signature():
    payload = json.loads((ASSETS / "e1-finalist-results.json").read_text())
    assert payload["candidate"]["n"] == 10
    assert payload["candidate"]["index"] == 2
    assert payload["candidate"]["shape"] == TURTLE_KEY
    assert payload["candidate"]["known_name"] == "turtle"
    assert payload["candidate"]["novel"] is False

    a1 = payload["a1_extended"]
    assert a1["k_max"] == 100
    assert a1["certificate"] is None
    assert a1["exhausted_indices"] == []
    assert a1["indices_tested"][-1] == 100

    certificate = payload["a3"]["certificate"]
    assert certificate["r2"] == 50_000
    assert certificate["tiles"] == 9_239
    assert verify_patch_certificate(
        decode_compiled_key(payload["candidate"]["shape"]),
        certificate,
    )

    prior = payload["a4_prior_r2_12800"]
    large = payload["a4_r2_50000"]["result"]
    assert prior["rank"] == large["rank"] == 4
    assert large["symmetry"] == 6
    assert large["verdict"] == "quasicrystal-candidate"

    patch = (ASSETS / payload["patch_svg"]).read_text()
    assert patch.count("<polygon ") == 9_239
    spectrum = (ASSETS / payload["spectrum_png"]).read_bytes()
    assert spectrum.startswith(b"\x89PNG\r\n\x1a\n")
