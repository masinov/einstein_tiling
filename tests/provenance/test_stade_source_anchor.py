"""Durable primary-source anchors for the Stade stick-rule obstruction."""

import hashlib
import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
ANCHOR = ROOT / "docs/literature/anchors/stade-stick-rules.json"
PDF = ROOT / "data/literature/papers/2506.11628-two-tiling-undecidable.pdf"
TEXT = ROOT / "data/literature/text/2506.11628-two-tiling-undecidable.txt"


def test_stade_rule_anchor_pins_the_forbidden_rectangle():
    anchor = json.loads(ANCHOR.read_text())
    assert anchor["source_id"] == "stade-two-tiling-2025"
    assert anchor["fixed_rule_9"] == {
        "left": "z1",
        "right_family": "b_i",
        "index_range": "1 <= i <= n-1",
        "status": "forbidden",
    }
    assert anchor["stable_rectangle"] == {
        "allowed": [["z1", "a2"], ["a1", "a2"], ["a1", "b1"]],
        "forbidden": [["z1", "b1"]],
    }
    assert anchor["later_forbidden_type_families"] == [
        ["a", "y"],
        ["c", "y"],
        ["a", "x1"],
        ["b", "z2"],
    ]


def test_cached_stade_primary_source_matches_anchor_when_present():
    anchor = json.loads(ANCHOR.read_text())
    if PDF.is_file():
        assert hashlib.sha256(PDF.read_bytes()).hexdigest() == anchor["pdf_sha256"]
    if TEXT.is_file():
        source = " ".join(TEXT.read_text().split())
        for fragment in (
            "(z1 , bi ) for 1 ≤ i ≤ n − 1",
            "(an−i , y2 )",
            "(ci+1 , y1 )",
            "(an−i , x1 )",
            "(bn−1−i , z2 )",
        ):
            assert fragment in source
