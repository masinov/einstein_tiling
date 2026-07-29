#!/usr/bin/env python3
"""Build the exact closest-common-support kernel of the two AHI macros."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_common_support_kernel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_common_support_kernel(json.loads(args.atlas.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        f"triangle_overlap={result['best_primitive_triangle_overlap']} "
        f"rhombus_overlap={result['best_rhombus_overlap_at_that_support_overlap']} "
        f"one_rhombus_equalizers={result['one_rhombus_equalizer_count']}"
    )


if __name__ == "__main__":
    main()
