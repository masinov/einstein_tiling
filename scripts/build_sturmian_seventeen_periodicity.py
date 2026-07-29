#!/usr/bin/env python3
"""Test one/two-copy translation periods for the 17-rhombus compiler."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_seventeen_rhombus_periodicity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_seventeen_rhombus_periodicity(
        json.loads(args.atlas.read_text()),
        json.loads(args.kernel.read_text()),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "17-rhombus periodicity: "
        f"one={result['one_copy']['translation_fundamental_domain_count']} "
        f"two={result['two_copy']['translation_fundamental_domain_count']}"
    )


if __name__ == "__main__":
    main()
