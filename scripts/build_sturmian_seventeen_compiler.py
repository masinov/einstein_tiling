#!/usr/bin/env python3
"""Validate the exact A+2M / B+2M seventeen-rhombus source compiler."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_seventeen_rhombus_source_compiler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_seventeen_rhombus_source_compiler(
        json.loads(args.atlas.read_text()),
        json.loads(args.kernel.read_text()),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "17-rhombus compiler: "
        + ", ".join(
            "legal" if (
                item["all_A_plus_2M_contacts_continue"]
                and item["all_B_plus_2M_contacts_continue"]
                and item["outer_sab_signatures_equal"]
            ) else "illegal"
            for item in result["equalizers"]
        )
    )


if __name__ == "__main__":
    main()
