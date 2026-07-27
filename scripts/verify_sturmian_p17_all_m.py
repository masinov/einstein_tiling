#!/usr/bin/env python3
"""Cold-verify the exhaustive P17 all-M obstruction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import verify_p17_all_m_obstruction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    verify_p17_all_m_obstruction(
        json.loads(args.artifact.read_text()),
        json.loads(args.atlas.read_text()),
        json.loads(args.kernel.read_text()),
    )
    print("P17 all-M obstruction: VERIFIED")


if __name__ == "__main__":
    main()
