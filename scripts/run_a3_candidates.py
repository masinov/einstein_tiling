#!/usr/bin/env python
"""Pose-free A3 disk-growth ladder for the ten smallest blind candidates.

The two n=10 and eight n=12 shapes are the complete smallest witnessed
H_c >= 3 sets from E1.  Each candidate is tested at increasing squared disk
radii.  SAT certificates are independently verified inside sat_grow_patch;
pose-free UNSAT is an exact grid-aligned disk-cover refutation.

Usage:
  venv/bin/python scripts/run_a3_candidates.py
  venv/bin/python scripts/run_a3_candidates.py --jobs 10 --radii 200,800,3200,12800
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
from pathlib import Path

from einstein.e1_candidates import smallest_depth3_candidates
from einstein.funnel.a3_patch import sat_grow_patch

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "notebook" / "assets"
OUTPUT = ASSETS / "a3-small-candidate-results.json"


def run_one(candidate, radii, conflict_budget):
    n, index, key, shape = candidate
    ladder = []
    largest_certificate = None
    for r2 in radii:
        t0 = time.monotonic()
        result = sat_grow_patch(
            shape,
            r2,
            fix_seed=False,
            conflict_budget=conflict_budget,
        )
        elapsed = time.monotonic() - t0
        rung = {
            "r2": r2,
            "status": (
                "grown" if result["completed"]
                else "refuted" if result["refuted"]
                else "unknown"
            ),
            "tiles": result["tiles"],
            "wall_seconds": round(elapsed, 3),
            **result["stats"],
        }
        ladder.append(rung)
        if result["completed"]:
            largest_certificate = result["certificate"]
        else:
            break
    return {
        "n": n,
        "index": index,
        "shape": key,
        "ladder": ladder,
        "largest_certificate": largest_certificate,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=10)
    parser.add_argument("--radii", default="200,800,3200,12800")
    parser.add_argument("--conflict-budget", type=int, default=5_000_000)
    args = parser.parse_args()
    radii = tuple(int(value) for value in args.radii.split(","))
    if not radii or any(a >= b for a, b in zip(radii, radii[1:])):
        parser.error("--radii must be a strictly increasing comma-separated list")

    candidates = list(smallest_depth3_candidates())
    t0 = time.monotonic()
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=min(args.jobs, len(candidates))
    ) as pool:
        futures = {
            pool.submit(run_one, candidate, radii, args.conflict_budget):
            candidate[:3]
            for candidate in candidates
        }
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            final = result["ladder"][-1]
            print(
                f"n={result['n']} candidate {result['index']}: "
                f"{final['status']} at r2={final['r2']} "
                f"(largest patch "
                f"{result['largest_certificate']['tiles'] if result['largest_certificate'] else 0} "
                "tiles)",
                flush=True,
            )

    results.sort(key=lambda row: (row["n"], row["index"]))
    counts = {"grown_to_max": 0, "refuted": 0, "unknown": 0}
    for result in results:
        status = result["ladder"][-1]["status"]
        if status == "grown" and result["ladder"][-1]["r2"] == radii[-1]:
            counts["grown_to_max"] += 1
        elif status == "refuted":
            counts["refuted"] += 1
        else:
            counts["unknown"] += 1
    payload = {
        "kind": "pose-free-a3-candidate-ladder",
        "radii": radii,
        "conflict_budget": args.conflict_budget,
        "jobs": min(args.jobs, len(candidates)),
        "wall_seconds": round(time.monotonic() - t0, 3),
        "counts": counts,
        "results": results,
    }
    ASSETS.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUTPUT.relative_to(ROOT))
    print(counts)


if __name__ == "__main__":
    main()
