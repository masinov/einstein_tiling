#!/usr/bin/env python
"""Batch A1 (torus periodicity test) over all free polykites up to n_max.

Resumable: shapes with an existing A1-torus verdict in the database are
skipped, so interrupting and rerunning is safe. Every verdict carries its
budget and code version.

Usage: venv/bin/python scripts/archive/run_a1.py [n_max] [k_max]
Writes: data/shapes.sqlite
"""

import sys
import time

from einstein.db import ShapeDB
from einstein.enumeration.polyform import enumerate_free_polykites
from einstein.funnel.a1_torus import find_periodic_tiling

STAGE = "A1-torus"


def main(n_max: int = 8, k_max: int = 12, node_budget: int = 200_000):
    db = ShapeDB("data/shapes.sqlite")
    budget = {"k_max": k_max, "node_budget": node_budget}
    t0 = time.time()
    for n, forms in enumerate_free_polykites(n_max):
        stats = {"periodic": 0, "no-periodic-at-budget": 0,
                 "unknown-budget-exhausted": 0, "skipped": 0}
        for shape in sorted(forms):
            sid = db.add_shape(shape)
            if db.latest_verdict(sid, STAGE) is not None:
                stats["skipped"] += 1
                continue
            cert, exhausted = find_periodic_tiling(
                shape, k_max=k_max, node_budget=node_budget)
            if cert is not None:
                db.record_verdict(sid, STAGE, "periodic", cert, budget)
                stats["periodic"] += 1
            elif exhausted:
                db.record_verdict(sid, STAGE, "unknown-budget-exhausted",
                                  None, budget)
                stats["unknown-budget-exhausted"] += 1
            else:
                db.record_verdict(sid, STAGE, "no-periodic-at-budget",
                                  None, budget)
                stats["no-periodic-at-budget"] += 1
        db.commit()
        print(f"n={n:2d} total={len(forms):5d} {stats} "
              f"t={time.time() - t0:7.1f}s", flush=True)
    db.close()


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]]
    main(*args)
