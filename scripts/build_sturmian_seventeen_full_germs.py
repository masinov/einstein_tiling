#!/usr/bin/env python3
"""Build the full bent-SAB germ test for the 17-rhombus relation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import (
    build_seventeen_rhombus_full_germs,
    dump_atlas,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_seventeen_rhombus_full_germs(
        args.archive,
        json.loads(args.atlas.read_text()),
        json.loads(args.kernel.read_text()),
    )
    dump_atlas(result, args.output)
    print(
        "full-germ equalizers:",
        [
            (
                item["legal_assignment_count_A"],
                item["legal_assignment_count_B"],
                item["matching_compatibility_pair_count"],
            )
            for item in result["equalizers"]
        ],
    )


if __name__ == "__main__":
    main()
