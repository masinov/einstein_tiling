#!/usr/bin/env python3
"""Cold-rebuild the exact K64A sub-30 carrier classification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_sub30_carrier_classification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--atlas",
        type=Path,
        default=Path("data/sturmian-source/ahi-section10-supports.json"),
    )
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    atlas = json.loads(args.atlas.read_text())
    data = json.loads(args.input.read_text())
    verify_sub30_carrier_classification(data, atlas)
    print(
        "verified sub-30 carrier classification:",
        f"supports={data['support_count']}",
        f"matchings={data['perfect_matching_count']}",
        f"bipartite={data['bipartite_matching_count']}",
    )


if __name__ == "__main__":
    main()
