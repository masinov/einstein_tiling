#!/usr/bin/env python
"""Size exact ancestry-blind physical frontiers seeded by non-L18 coronas.

This is a resumable development probe for D1.  It assumes only the exact
fixed-chirality, edge-to-edge straight-Spectre geometry.  Each step covers
every exposed edge of every surviving patch by a complete nonoverlapping next
ring.  No parent template, substitution state, or generated-patch filter is
used.

Checkpoints live below ``data/w3-d1-physical/`` and are intentionally outside
the proof payload.  A finite empty frontier may later be packaged as a cold
certificate; a nonempty frontier is only experimental evidence.
"""

from __future__ import annotations

import argparse
import gzip
import json
import pickle
from pathlib import Path

from einstein.theory.spectre_d1_entry import (
    EXTRA_CORONA_INDICES,
    advance_frontier,
    initial_frontier,
)


ROOT = Path(__file__).resolve().parents[2]
CHECKPOINTS = ROOT / "data/w3-d1-physical"
def checkpoint_path(radius: int) -> Path:
    return CHECKPOINTS / f"radius{radius}.pkl.gz"


def summary_path(radius: int) -> Path:
    return CHECKPOINTS / f"radius{radius}-summary.json"


def save_checkpoint(radius, frontier, summary):
    CHECKPOINTS.mkdir(parents=True, exist_ok=True)
    with gzip.open(checkpoint_path(radius), "wb", compresslevel=3) as stream:
        pickle.dump(frontier, stream, protocol=pickle.HIGHEST_PROTOCOL)
    summary_path(radius).write_text(json.dumps(summary, indent=1) + "\n")


def load_frontier(radius):
    with gzip.open(checkpoint_path(radius), "rb") as stream:
        return pickle.load(stream)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-radius", type=int, default=3)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--resume-radius", type=int, default=1)
    args = parser.parse_args()
    if args.target_radius < 2 or args.resume_radius < 1:
        raise SystemExit("radii must satisfy target >= 2 and resume >= 1")
    frontier = (
        initial_frontier()
        if args.resume_radius == 1
        else load_frontier(args.resume_radius)
    )
    print(
        f"start r{args.resume_radius}: {len(frontier)} patches; "
        f"workers={args.workers}",
        flush=True,
    )
    for radius in range(args.resume_radius + 1, args.target_radius + 1):
        frontier, summary = advance_frontier(
            frontier, radius, workers=args.workers,
        )
        summary["scope"] = (
            "exact fixed-chirality edge-to-edge polygon rings; no parent "
            "or substitution data"
        )
        save_checkpoint(radius, frontier, summary)
        print(json.dumps(summary, sort_keys=True), flush=True)
        if not frontier:
            break


if __name__ == "__main__":
    main()
