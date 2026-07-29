#!/usr/bin/env python3
"""Build the exact K65 area-30 carrier-local classification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_area30_carrier_classification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--atlas",
        type=Path,
        default=Path("data/sturmian-source/ahi-section10-supports.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_area30_carrier_classification(
        json.loads(args.atlas.read_text())
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "area-30 carriers:",
        f"supports={result['support_count']}",
        f"G_embeddings={result['G_embedding_count']}",
        f"G_matchings={result['G_perfect_matching_count']}",
        f"Z_matchings={result['Z_perfect_matching_count']}",
        f"survivors={result['area30_parity_survivor_count']}",
    )


if __name__ == "__main__":
    main()
