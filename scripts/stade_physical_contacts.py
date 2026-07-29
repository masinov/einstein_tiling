#!/usr/bin/env python3
"""Produce the preregistered exact Stade physical-contact quotient."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from einstein.tilings.stade.contacts import analyze_length


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ANCHOR = ROOT / "docs/literature/anchors/stade-stick-rules.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    anchor_bytes = SOURCE_ANCHOR.read_bytes()
    lengths = [analyze_length(n) for n in range(5, 13)]
    result = {
        "schema": "stade-physical-contact-quotient-v1",
        "arithmetic": "integer axial hex-cell coordinates",
        "motion_group": "orientation-preserving Euclidean isometries",
        "source_anchor_sha256": hashlib.sha256(anchor_bytes).hexdigest(),
        "tested_lengths": list(range(5, 13)),
        "lengths": lengths,
        "summary": {
            "separable_possible_lengths": [
                item["n"] for item in lengths if item["separable_erasure_possible"]
            ],
            "separable_impossible_lengths": [
                item["n"] for item in lengths if not item["separable_erasure_possible"]
            ],
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], sort_keys=True))
    for item in lengths:
        shortest = min(
            (len(hit["allowed_path"]) for hit in item["forced_forbidden_hits"]),
            default=None,
        )
        print(
            f"n={item['n']} ports={item['port_count']} "
            f"physical={item['physical_pair_count']} "
            f"allowed={item['allowed_physical_pair_count']} "
            f"forbidden={item['forbidden_physical_pair_count']} "
            f"hits={len(item['forced_forbidden_hits'])} shortest_path={shortest}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
