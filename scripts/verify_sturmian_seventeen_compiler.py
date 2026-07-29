#!/usr/bin/env python3
"""Cold-verify the exact seventeen-rhombus source compiler."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_seventeen_rhombus_source_compiler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    verify_seventeen_rhombus_source_compiler(
        json.loads(args.artifact.read_text()),
        json.loads(args.atlas.read_text()),
        json.loads(args.kernel.read_text()),
    )
    print("17-rhombus source compiler: VERIFIED")


if __name__ == "__main__":
    main()
