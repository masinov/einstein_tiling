#!/usr/bin/env python
"""Cold verifier for the Golden-Sturmian/Turtle-density control artifact."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from einstein.repository import repository_root

from einstein.polykites.known_shapes import TURTLE_KEY
from einstein.tilings.sturmian.turtle import (
    SOURCE_ID,
    central_word,
    golden_density_root_residual,
    minority_chirality_residual,
    minority_chirality_side,
    standard_word_table,
    verify_central_identities,
)


ROOT = repository_root(Path(__file__))
ARTIFACT = ROOT / "docs/notebook/assets/theory-w3-turtle-golden-sturmian.json"


def main() -> None:
    payload = json.loads(ARTIFACT.read_text())
    assert payload["source_id"] == SOURCE_ID
    assert payload["turtle_patch"]["canonical_key"] == TURTLE_KEY

    max_index = payload["sturmian"]["max_index"]
    assert payload["sturmian"]["central_checks"] == verify_central_identities(
        max_index
    )
    assert payload["sturmian"]["standard_words"] == standard_word_table(max_index)
    for row in payload["sturmian"]["central_words"]:
        word = central_word(row["index"])
        assert row["length"] == len(word)
        assert row["palindrome"] == (word == word[::-1])
        assert row["sha256"] == hashlib.sha256(word.encode()).hexdigest()

    assert golden_density_root_residual(-1) == (0, 0)
    assert golden_density_root_residual(1) == (0, 0)
    assert minority_chirality_residual() == (0, 0)

    patch_path = ROOT / payload["turtle_patch"]["source"]
    patch_bytes = patch_path.read_bytes()
    assert payload["turtle_patch"]["source_sha256"] == hashlib.sha256(
        patch_bytes
    ).hexdigest()
    source = json.loads(patch_bytes)
    assert source["candidate"]["shape"] == TURTLE_KEY
    placements = source["a3"]["certificate"]["placements"]
    counts = Counter(int(placement[0]) for placement in placements)
    preserving = sum(counts[op] for op in range(6))
    mirrored = sum(counts[op] for op in range(6, 12))
    observed = Fraction(min(preserving, mirrored), len(placements))
    assert payload["turtle_patch"]["placements"] == len(placements)
    assert payload["turtle_patch"]["orientation_preserving"] == preserving
    assert payload["turtle_patch"]["mirrored"] == mirrored
    assert payload["turtle_patch"]["minority_fraction"] == [
        observed.numerator,
        observed.denominator,
    ]
    assert payload["turtle_patch"]["side_of_exact_prediction"] == (
        minority_chirality_side(observed)
    )
    assert payload["verdict"] == "exact-combinatorial-and-density-control-pass"
    print("PASS: Golden Sturmian recurrence, density algebra, and Turtle patch count")


if __name__ == "__main__":
    main()
