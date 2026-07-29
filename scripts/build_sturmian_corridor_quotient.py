#!/usr/bin/env python3
"""Build the exact 12-state corridor quotient of the AHI source atlas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_corridor_quotient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    quotient = build_corridor_quotient(
        args.archive, json.loads(args.atlas.read_text())
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(quotient, indent=2, sort_keys=True) + "\n")
    counts = {
        name: macro["corridor_embedding_count"]
        for name, macro in quotient["macros"].items()
    }
    print(f"alphabet={len(quotient['alphabet'])} embeddings={counts}")


if __name__ == "__main__":
    main()
