#!/usr/bin/env python3
"""Test one/two-copy periods of the three-P Figure 45 envelope."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_fiftyone_envelope_periodicity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pairs", type=Path)
    parser.add_argument("rep3", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_fiftyone_envelope_periodicity(
        json.loads(args.pairs.read_text()), json.loads(args.rep3.read_text())
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "51-rhombus macro periodicity: "
        f"one={result['one_copy']['translation_fundamental_domain_count']} "
        f"two={result['two_copy']['translation_fundamental_domain_count']}"
    )


if __name__ == "__main__":
    main()
