#!/usr/bin/env python3
"""Cold verifier for the exact Stade physical-contact quotient."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from einstein.tilings.stade.contacts import (
    analyze_length,
    physical_contact,
    polygonal_physical_contact,
    stick_ports,
)


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ANCHOR = ROOT / "docs/literature/anchors/stade-stick-rules.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    stored = json.loads(args.artifact.read_text())
    assert stored["schema"] == "stade-physical-contact-quotient-v1"
    assert stored["source_anchor_sha256"] == hashlib.sha256(SOURCE_ANCHOR.read_bytes()).hexdigest()
    assert stored["tested_lengths"] == list(range(5, 13))
    rebuilt = [analyze_length(n) for n in stored["tested_lengths"]]
    assert stored["lengths"] == rebuilt
    for n in stored["tested_lengths"]:
        ports = stick_ports(n)
        for left in ports:
            for right in ports:
                assert physical_contact(n, left, right) == polygonal_physical_contact(
                    n, left, right
                )
    possible = [item["n"] for item in rebuilt if item["separable_erasure_possible"]]
    impossible = [item["n"] for item in rebuilt if not item["separable_erasure_possible"]]
    assert stored["summary"] == {
        "separable_possible_lengths": possible,
        "separable_impossible_lengths": impossible,
    }
    print(
        f"verified {len(rebuilt)} lengths; "
        f"possible={possible}; impossible={impossible}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
