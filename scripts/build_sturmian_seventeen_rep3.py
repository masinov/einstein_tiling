#!/usr/bin/env python3
"""Test the 17-rhombus compiler as the Figure 45 rep-3 tile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_seventeen_rhombus_rep3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    parser.add_argument("pairs", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_seventeen_rhombus_rep3(
        json.loads(args.atlas.read_text()),
        json.loads(args.kernel.read_text()),
        json.loads(args.pairs.read_text()),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "17-rhombus rep3: "
        + ", ".join(
            f"panel {item['panel']} similarities={item['similarity_witness_count']} "
            f"partitions={item['three_tile_partition_count']}"
            for item in result["panels"]
        )
    )


if __name__ == "__main__":
    main()
