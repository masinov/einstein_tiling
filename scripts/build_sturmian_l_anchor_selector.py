#!/usr/bin/env python3
"""Build the exact binary L-anchor selector of the AHI source atlas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_l_anchor_selector


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    selector = build_l_anchor_selector(json.loads(args.atlas.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(selector, indent=2, sort_keys=True) + "\n")
    bits = ", ".join(
        f"{name}:{item['selector_bit']}"
        for name, item in selector["macros"].items()
    )
    print(f"classes={len(selector['selector_alphabet'])} bits={{{bits}}}")


if __name__ == "__main__":
    main()
