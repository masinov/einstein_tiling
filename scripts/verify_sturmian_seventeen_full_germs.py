#!/usr/bin/env python3
"""Cold-verify the full bent-SAB germ test for the 17-rhombus relation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_seventeen_rhombus_full_germs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    verify_seventeen_rhombus_full_germs(
        json.loads(args.artifact.read_text()),
        args.archive,
        json.loads(args.atlas.read_text()),
        json.loads(args.kernel.read_text()),
    )
    print("17-rhombus full SAB-germ result: VERIFIED")


if __name__ == "__main__":
    main()
