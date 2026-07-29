"""Pins for the exact extended-period audit of the smallest candidates."""

import json
from pathlib import Path

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.polykites.periodic_quotients import verify_certificate

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "docs/notebook/assets/a1-extended-small-candidate-results.json"


def test_extended_a1_retires_all_n12_candidates():
    payload = json.loads(RESULTS.read_text())
    assert payload["k_max"] == 21
    assert payload["periodic"] == 8
    assert payload["survivors"] == 2
    rows = payload["results"]
    assert len(rows) == 10

    periodic = [row for row in rows if row["verdict"] == "periodic"]
    assert {(row["n"], row["index"]) for row in periodic} == {
        (12, index) for index in range(1, 9)
    }
    assert {row["certificate"]["index"] for row in periodic} == {16}
    for row in periodic:
        assert verify_certificate(
            decode_compiled_key(row["shape"]), row["certificate"]
        )
