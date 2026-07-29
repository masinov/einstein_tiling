#!/usr/bin/env python3
"""Extract the exact normalized AHI Section 10.1 source supports."""

from __future__ import annotations

import argparse
from pathlib import Path

from einstein.tilings.sturmian import build_atlas, dump_atlas, verify_atlas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    atlas = build_atlas(args.archive)
    verify_atlas(atlas)
    dump_atlas(atlas, args.output)
    counts = {
        name: support["primitive_triangle_count"]
        for name, support in atlas["supports"].items()
    }
    print(f"verified AHI normalized supports: {counts}")


if __name__ == "__main__":
    main()
