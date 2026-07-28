#!/usr/bin/env python3
"""Build the exact K64A sub-30 carrier-local classification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import build_sub30_carrier_classification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--atlas",
        type=Path,
        default=Path("data/sturmian-source/ahi-section10-supports.json"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    atlas = json.loads(args.atlas.read_text())
    result = build_sub30_carrier_classification(atlas)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "sub-30 carriers:",
        f"supports={result['support_count']}",
        f"matchings={result['perfect_matching_count']}",
        f"bipartite={result['bipartite_matching_count']}",
    )


if __name__ == "__main__":
    main()
