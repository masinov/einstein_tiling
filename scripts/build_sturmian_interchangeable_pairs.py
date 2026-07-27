#!/usr/bin/env python3
"""Transcribe AHI Figure 45 into exact normalized source assemblies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import build_interchangeable_pairs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_interchangeable_pairs(
        args.archive, json.loads(args.atlas.read_text())
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "interchangeable pairs: "
        + ", ".join(
            f"{pair['rhombus_count']} rhombi {pair['tile_census']}"
            for pair in result["pairs"]
        )
    )


if __name__ == "__main__":
    main()
