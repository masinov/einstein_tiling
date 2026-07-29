#!/usr/bin/env python3
"""Test exact source-native envelopes as translation fundamental domains."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_interchangeable_pair_periodicity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pairs", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_interchangeable_pair_periodicity(
        json.loads(args.pairs.read_text())
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "translation FD counts: "
        + ", ".join(
            f"{item['rhombus_count']}:{item['translation_fundamental_domain_count']}"
            for item in result["results"]
        )
    )


if __name__ == "__main__":
    main()
