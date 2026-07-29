#!/usr/bin/env python3
"""Cold verifier for the normalized AHI source-support artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_atlas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    data = json.loads(args.artifact.read_text())
    verify_atlas(data)
    print("verified exact AHI source-support artifact")


if __name__ == "__main__":
    main()
