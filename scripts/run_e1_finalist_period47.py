#!/usr/bin/env python
"""Exact period-47 cylinder escalation for the E1 finalist.

The production r²=50,000 patch repeats every `(du,dv)=(0,47)` on all 706
eligible interior placements.  This script tests whether that strip repeat
closes with a transverse period `(a,0)`.  Any SAT result is a verified periodic
plane tiling and retires the candidate immediately.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
from pathlib import Path

from einstein.e1_candidates import SMALLEST_DEPTH3_KEYS, decode_compiled_key
from einstein.funnel.a1_torus import _reduce, cell_to_lattice, solve_torus_sat

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs/notebook/assets/e1-finalist-period47.json"
KEY = SMALLEST_DEPTH3_KEYS[10][1]
SHAPE = decode_compiled_key(KEY)
PRODUCTION = json.loads(
    (ROOT / "docs/notebook/assets/e1-finalist-results.json").read_text()
)["a3"]["certificate"]


def solve(a, budget):
    started = time.monotonic()
    preferred = []
    for op, tx, ty in PRODUCTION["placements"]:
        u, v, _ = cell_to_lattice((tx, ty, 0))
        u, v = _reduce(u, v, a, 0, 47)
        preferred.append((op, u, v))
    certificate, exhausted = solve_torus_sat(
        SHAPE,
        (a, 0, 47),
        conflict_budget=budget,
        preferred_placements=preferred,
    )
    return {
        "a": a,
        "hnf": [a, 0, 47],
        "index": 47 * a,
        "status": (
            "periodic" if certificate else "unknown" if exhausted else "refuted"
        ),
        "wall_seconds": round(time.monotonic() - started, 3),
        "certificate": certificate,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a-min", type=int, default=30)
    parser.add_argument("--a-max", type=int, default=150)
    parser.add_argument("--jobs", type=int, default=16)
    parser.add_argument("--conflict-budget", type=int, default=10_000_000)
    args = parser.parse_args()
    # 6*(47*a) cells must be divisible by the ten cells per tile.
    widths = [
        a for a in range(args.a_min, args.a_max + 1)
        if (6 * 47 * a) % len(SHAPE) == 0
    ]
    started = time.monotonic()
    results = []
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=min(args.jobs, len(widths))
    ) as pool:
        futures = {
            pool.submit(solve, a, args.conflict_budget): a for a in widths
        }
        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            results.append(row)
            print(
                f"a={row['a']:3d} index={row['index']:5d}: "
                f"{row['status']} ({row['wall_seconds']:.2f}s)",
                flush=True,
            )
            if row["certificate"]:
                for other in futures:
                    other.cancel()
                break
    results.sort(key=lambda row: row["a"])
    payload = {
        "kind": "exact-period-47-cylinder-escalation",
        "candidate": {"n": 10, "index": 2, "shape": KEY},
        "translation": [0, 47],
        "width_range": [args.a_min, args.a_max],
        "conflict_budget_per_width": args.conflict_budget,
        "wall_seconds": round(time.monotonic() - started, 3),
        "results": results,
        "periodic_certificate": next(
            (row["certificate"] for row in results if row["certificate"]), None
        ),
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUTPUT.relative_to(ROOT))
    return 0 if payload["periodic_certificate"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
