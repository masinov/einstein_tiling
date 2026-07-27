#!/usr/bin/env python3
"""Cold-verify the exact unit-apex compiler census."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import verify_unit_apex_compiler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("compiler", type=Path)
    args = parser.parse_args()
    verify_unit_apex_compiler(
        json.loads(args.compiler.read_text()),
        json.loads(args.atlas.read_text()),
    )
    print("unit-apex compiler census: VERIFIED")


if __name__ == "__main__":
    main()
