#!/usr/bin/env python3
"""Exhaust the direct unit-apex edge substitution on the AHI source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_unit_apex_compiler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build_unit_apex_compiler(json.loads(args.atlas.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    counts = {
        name: macro["simple_word_count"]
        for name, macro in result["macros"].items()
    }
    print(
        f"simple_words={counts} common={result['common_simple_support_count']} "
        f"small_M_area={result['small_M_all_inward']['doubled_area']}"
    )


if __name__ == "__main__":
    main()
