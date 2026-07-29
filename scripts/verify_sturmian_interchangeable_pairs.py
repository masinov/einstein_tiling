#!/usr/bin/env python3
"""Cold-verify the exact AHI Figure 45 local-pair transcription."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_interchangeable_pairs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    verify_interchangeable_pairs(
        json.loads(args.artifact.read_text()),
        args.archive,
        json.loads(args.atlas.read_text()),
    )
    print("interchangeable pairs: VERIFIED")


if __name__ == "__main__":
    main()
