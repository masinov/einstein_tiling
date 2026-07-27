#!/usr/bin/env python3
"""Exhaust P17 lozenge subdivisions and test the all-M source state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import (
    build_p17_all_m_obstruction,
    dump_atlas,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_p17_all_m_obstruction(
        json.loads(args.atlas.read_text()),
        json.loads(args.kernel.read_text()),
    )
    dump_atlas(result, args.output)
    print(
        f"matchings={result['perfect_matching_count']} "
        f"three_axis={result['matching_count_with_three_axis_vertex']} "
        f"bipartite={result['bipartite_long_diagonal_graph_count']}"
    )


if __name__ == "__main__":
    main()
