#!/usr/bin/env python3
"""Cold verifier for the exact 31-state source contact kernel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_contact_kernel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    args = parser.parse_args()
    verify_contact_kernel(
        json.loads(args.kernel.read_text()), json.loads(args.atlas.read_text())
    )
    print("verified exact AHI 31-state contact kernel")


if __name__ == "__main__":
    main()
