#!/usr/bin/env python3
"""Cold-verify source-native envelope translation certificates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_interchangeable_pair_periodicity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pairs", type=Path)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    verify_interchangeable_pair_periodicity(
        json.loads(args.artifact.read_text()),
        json.loads(args.pairs.read_text()),
    )
    print("interchangeable-pair periodicity: VERIFIED")


if __name__ == "__main__":
    main()
