#!/usr/bin/env python
"""Targeted exact periodicity audit for the E1 n=10 finalist.

Tests:
  * every area-compatible torus index in a requested interval;
  * cylinders containing the exact (0,47) translation observed in the
    central domain of the first r2=50,000 SAT patch.

Usage:
  venv/bin/python scripts/run_e1_finalist_periodicity.py \
      --k-min 105 --k-max 300 --jobs 16
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
from pathlib import Path

from einstein.e1_candidates import (
    SMALLEST_DEPTH3_KEYS,
    decode_compiled_key,
)
from einstein.funnel.a1_torus import (
    find_periodic_tiling_sat,
    solve_torus_sat,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs/notebook/assets/e1-finalist-periodicity.json"
KEY = SMALLEST_DEPTH3_KEYS[10][1]
SHAPE = decode_compiled_key(KEY)


def sweep_index(k, conflict_budget):
    started = time.monotonic()
    certificate, exhausted = find_periodic_tiling_sat(
        SHAPE,
        k_min=k,
        k_max=k,
        conflict_budget=conflict_budget,
    )
    return {
        "index": k,
        "status": (
            "periodic" if certificate is not None
            else "unknown" if exhausted
            else "refuted"
        ),
        "wall_seconds": round(time.monotonic() - started, 3),
        "certificate": certificate,
    }


def cylinder(a, conflict_budget):
    hnf = (a, 0, 47)
    started = time.monotonic()
    certificate, exhausted = solve_torus_sat(
        SHAPE, hnf, conflict_budget=conflict_budget
    )
    return {
        "hnf": hnf,
        "index": a * 47,
        "status": (
            "periodic" if certificate is not None
            else "unknown" if exhausted
            else "refuted"
        ),
        "wall_seconds": round(time.monotonic() - started, 3),
        "certificate": certificate,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k-min", type=int, default=105)
    parser.add_argument("--k-max", type=int, default=300)
    parser.add_argument("--jobs", type=int, default=16)
    parser.add_argument("--conflict-budget", type=int, default=1_000_000)
    parser.add_argument("--cylinder-budget", type=int, default=5_000_000)
    args = parser.parse_args()
    indices = [
        k for k in range(args.k_min, args.k_max + 1)
        if (6 * k) % len(SHAPE) == 0
    ]
    started = time.monotonic()
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=min(args.jobs, len(indices))
    ) as pool:
        results = []
        futures = {
            pool.submit(sweep_index, k, args.conflict_budget): k
            for k in indices
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"k={result['index']}: {result['status']} "
                f"({result['wall_seconds']:.1f}s)",
                flush=True,
            )
    results.sort(key=lambda row: row["index"])
    cylinders = [
        cylinder(a, args.cylinder_budget)
        for a in (5, 10, 15, 20, 25)
    ]
    payload = {
        "kind": "exact-finalist-periodicity-escalation",
        "candidate": {"n": 10, "index": 2, "shape": KEY},
        "range": [args.k_min, args.k_max],
        "conflict_budget_per_hnf": args.conflict_budget,
        "wall_seconds": round(time.monotonic() - started, 3),
        "indices": results,
        "period_47_cylinders": cylinders,
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
