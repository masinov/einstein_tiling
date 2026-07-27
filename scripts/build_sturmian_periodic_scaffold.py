#!/usr/bin/env python3
"""Build the exact periodic color-erasure scaffold for the AHI source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import build_periodic_scaffold


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    scaffold = build_periodic_scaffold(json.loads(args.atlas.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scaffold, indent=2, sort_keys=True) + "\n")
    print(
        f"global_models={len(scaffold['global_affine_perfect_matching_models'])} "
        f"common_linear_parts={len(scaffold['common_linear_parts'])} "
        f"periodic_witness={scaffold['periodic_witness'] is not None}"
    )


if __name__ == "__main__":
    main()
