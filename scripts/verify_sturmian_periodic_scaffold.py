#!/usr/bin/env python3
"""Cold verifier for the AHI periodic color-erasure scaffold."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import verify_periodic_scaffold


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("scaffold", type=Path)
    args = parser.parse_args()
    verify_periodic_scaffold(
        json.loads(args.scaffold.read_text()), json.loads(args.atlas.read_text())
    )
    print("verified exact AHI periodic color-erasure scaffold")


if __name__ == "__main__":
    main()
