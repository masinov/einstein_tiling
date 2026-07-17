#!/usr/bin/env python
"""Test exact tori inferred from strong finite-patch return vectors.

Every pair of independent high-overlap translation vectors determines a
candidate period lattice.  We convert it exactly to the repository's HNF
convention, discard area-incompatible quotients, rank by observed support,
and SAT-test the strongest distinct lattices.  Patch placements are solver
phase preferences only; every result retains ordinary exact SAT semantics.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import time
from pathlib import Path

from einstein.e1_candidates import SMALLEST_DEPTH3_KEYS, decode_compiled_key
from einstein.funnel.a1_torus import (
    _reduce,
    cell_to_lattice,
    solve_torus_sat,
)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/notebook/assets"
OUTPUT = ASSETS / "e1-finalist-translation-lattices.json"
KEY = SMALLEST_DEPTH3_KEYS[10][1]
SHAPE = decode_compiled_key(KEY)
PRODUCTION = json.loads(
    (ASSETS / "e1-finalist-results.json").read_text()
)["a3"]["certificate"]


def _egcd(a, b):
    if not b:
        return abs(a), 1 if a >= 0 else -1, 0
    g, x, y = _egcd(b, a % b)
    return g, y, x - (a // b) * y


def vectors_to_hnf(left, right):
    x1, y1 = left
    x2, y2 = right
    determinant = x1 * y2 - x2 * y1
    if not determinant:
        return None
    d, p, q = _egcd(y1, y2)
    if not d:
        return None
    index = abs(determinant)
    a = index // d
    b = (p * x1 + q * x2) % a
    hnf = (a, b, d)
    assert _reduce(x1, y1, *hnf) == (0, 0)
    assert _reduce(x2, y2, *hnf) == (0, 0)
    return hnf


def preferred_for(hnf):
    out = []
    for op, tx, ty in PRODUCTION["placements"]:
        u, v, _ = cell_to_lattice((tx, ty, 0))
        u, v = _reduce(u, v, *hnf)
        out.append((op, u, v))
    return out


def solve(row, budget):
    started = time.monotonic()
    hnf = tuple(row["hnf"])
    certificate, exhausted = solve_torus_sat(
        SHAPE,
        hnf,
        conflict_budget=budget,
        preferred_placements=preferred_for(hnf),
    )
    return {
        **row,
        "status": (
            "periodic" if certificate else "unknown" if exhausted else "refuted"
        ),
        "wall_seconds": round(time.monotonic() - started, 3),
        "certificate": certificate,
    }


def proposals(max_index):
    robustness = json.loads(
        (ASSETS / "e1-finalist-robustness.json").read_text()
    )
    observed = []
    profiles = [
        ("production", robustness["original_large_patch_translation_profile"]),
        *(
            (f"phase-{row['phase_seed']}", row["translations"])
            for row in robustness["results"]
        ),
    ]
    for source, profile in profiles:
        for rank, row in enumerate(profile, 1):
            observed.append({
                "source": source,
                "rank": rank,
                "vector": (row["du"], row["dv"]),
                "fraction": row["fraction"],
                "matched": row["matched"],
            })
    by_hnf = {}
    for i, left in enumerate(observed):
        for right in observed[i + 1:]:
            hnf = vectors_to_hnf(left["vector"], right["vector"])
            if hnf is None:
                continue
            index = hnf[0] * hnf[2]
            if not (216 <= index <= max_index):
                continue
            if (6 * index) % len(SHAPE):
                continue
            score = min(left["fraction"], right["fraction"]) * math.sqrt(
                left["matched"] * right["matched"]
            )
            row = {
                "hnf": list(hnf),
                "index": index,
                "score": score,
                "vectors": [list(left["vector"]), list(right["vector"])],
                "sources": [left["source"], right["source"]],
                "fractions": [left["fraction"], right["fraction"]],
                "matched": [left["matched"], right["matched"]],
            }
            if score > by_hnf.get(hnf, {}).get("score", -1):
                by_hnf[hnf] = row
    return sorted(
        by_hnf.values(), key=lambda row: (-row["score"], row["index"], row["hnf"])
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-lattices", type=int, default=64)
    parser.add_argument("--max-index", type=int, default=20_000)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--conflict-budget", type=int, default=10_000_000)
    args = parser.parse_args()
    selected = proposals(args.max_index)[:args.max_lattices]
    started = time.monotonic()
    results = []
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=min(args.jobs, len(selected))
    ) as pool:
        futures = {
            pool.submit(solve, row, args.conflict_budget): row for row in selected
        }
        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            results.append(row)
            print(
                f"hnf={tuple(row['hnf'])} index={row['index']}: "
                f"{row['status']} ({row['wall_seconds']:.1f}s)",
                flush=True,
            )
    results.sort(key=lambda row: (-row["score"], row["index"], row["hnf"]))
    payload = {
        "kind": "observed-return-vector-torus-search",
        "candidate": {"n": 10, "index": 2, "shape": KEY},
        "max_index": args.max_index,
        "conflict_budget_per_lattice": args.conflict_budget,
        "wall_seconds": round(time.monotonic() - started, 3),
        "results": results,
        "periodic_certificates": [
            row["certificate"] for row in results if row["certificate"]
        ],
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUTPUT.relative_to(ROOT))
    return 0 if payload["periodic_certificates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
