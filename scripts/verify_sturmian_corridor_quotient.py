#!/usr/bin/env python3
"""Cold verifier for the exact AHI corridor quotient."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_corridor_quotient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("quotient", type=Path)
    args = parser.parse_args()
    verify_corridor_quotient(
        json.loads(args.quotient.read_text()),
        args.archive,
        json.loads(args.atlas.read_text()),
    )
    print("verified exact AHI 12-state corridor quotient")


if __name__ == "__main__":
    main()
