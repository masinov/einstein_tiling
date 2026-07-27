#!/usr/bin/env python3
"""Cold-verify the 51-rhombus macro periodicity census."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.sturmian_source import verify_fiftyone_envelope_periodicity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pairs", type=Path)
    parser.add_argument("rep3", type=Path)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    verify_fiftyone_envelope_periodicity(
        json.loads(args.artifact.read_text()),
        json.loads(args.pairs.read_text()),
        json.loads(args.rep3.read_text()),
    )
    print("51-rhombus macro periodicity: VERIFIED")


if __name__ == "__main__":
    main()
