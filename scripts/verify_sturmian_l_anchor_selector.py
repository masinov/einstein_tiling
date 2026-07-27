#!/usr/bin/env python3
"""Cold-verify the exact AHI binary L-anchor selector artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import verify_l_anchor_selector


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("selector", type=Path)
    args = parser.parse_args()
    verify_l_anchor_selector(
        json.loads(args.selector.read_text()),
        json.loads(args.atlas.read_text()),
    )
    print("L-anchor selector: VERIFIED")


if __name__ == "__main__":
    main()
