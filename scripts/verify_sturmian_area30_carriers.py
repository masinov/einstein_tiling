#!/usr/bin/env python3
"""Cold-rebuild the exact K65 area-30 carrier classification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_area30_carrier_classification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--atlas",
        type=Path,
        default=Path("data/sturmian-source/ahi-section10-supports.json"),
    )
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    verify_area30_carrier_classification(
        data, json.loads(args.atlas.read_text())
    )
    print(
        "verified area-30 carrier classification:",
        f"supports={data['support_count']}",
        f"G_embeddings={data['G_embedding_count']}",
        f"G_matchings={data['G_perfect_matching_count']}",
        f"Z_matchings={data['Z_perfect_matching_count']}",
        f"survivors={data['area30_parity_survivor_count']}",
    )


if __name__ == "__main__":
    main()
