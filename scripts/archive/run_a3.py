#!/usr/bin/env python
"""A3 large-patch construction for selected shapes (stage 'A3-patch').

Modes:
  grow SHAPE_ID R2      SAT-grow a disk patch, verify, store certificate
  refute SHAPE_ID R2    pose-free SAT refutation attempt at one radius
  ceiling SHAPE_ID      ladder of radii; record the largest coverable disk
                        and the smallest refuted one (finite-patch shapes)

Verdicts:
  patch-grown        certificate stored (verified before storage)
  disk-cover-refuted UNSAT with no seed constraint: no set of copies
                     covers the disk of the stated r2 at all (grid-aligned
                     scope, D-0006)
  unknown-budget     conflict budget exhausted without an answer

Usage: venv/bin/python scripts/archive/run_a3.py grow 635 5500
       venv/bin/python scripts/archive/run_a3.py ceiling 502
"""

import sys
import time

from einstein.db import ShapeDB, deserialize_cells
from einstein.funnel.a3_patch import sat_grow_patch

STAGE = "A3-patch"
CEILING_LADDER = [8, 20, 50, 100, 200, 400, 800, 1600]


def _shape(db, shape_id):
    row = db.conn.execute(
        "SELECT key FROM shapes WHERE id = ?", (shape_id,)).fetchone()
    if row is None:
        sys.exit(f"no shape with id {shape_id}")
    return deserialize_cells(row[0])


def grow(db, shape_id: int, r2: int, conflict_budget=None):
    shape = _shape(db, shape_id)
    t0 = time.time()
    res = sat_grow_patch(shape, r2, fix_seed=True,
                         conflict_budget=conflict_budget)
    dt = time.time() - t0
    budget = {"engine": "sat/cadical195", "r2": r2, "fix_seed": True,
              "conflict_budget": conflict_budget,
              "wall_seconds": round(dt, 1), **res["stats"]}
    if res["completed"]:
        db.record_verdict(shape_id, STAGE, "patch-grown",
                          res["certificate"], budget)
        print(f"shape {shape_id} r2={r2}: patch-grown, {res['tiles']} tiles "
              f"({dt:.1f}s)")
    elif res["refuted"]:
        # fix_seed=True refutations are pose-restricted; do not store them
        print(f"shape {shape_id} r2={r2}: UNSAT with fixed seed "
              f"(not stored; rerun in refute mode)")
    else:
        db.record_verdict(shape_id, STAGE, "unknown-budget", None, budget)
        print(f"shape {shape_id} r2={r2}: budget exhausted")
    db.commit()


def refute(db, shape_id: int, r2: int, conflict_budget=None, store=True):
    shape = _shape(db, shape_id)
    t0 = time.time()
    res = sat_grow_patch(shape, r2, fix_seed=False,
                         conflict_budget=conflict_budget)
    dt = time.time() - t0
    budget = {"engine": "sat/cadical195", "r2": r2, "fix_seed": False,
              "conflict_budget": conflict_budget,
              "wall_seconds": round(dt, 1), **res["stats"]}
    if store:
        if res["refuted"]:
            db.record_verdict(shape_id, STAGE, "disk-cover-refuted",
                              {"kind": "unsat-exhaustion", "r2": r2}, budget)
        elif res["completed"]:
            db.record_verdict(shape_id, STAGE, "patch-grown",
                              res["certificate"], budget)
        else:
            db.record_verdict(shape_id, STAGE, "unknown-budget", None, budget)
        db.commit()
    tag = ("refuted" if res["refuted"]
           else f"grown:{res['tiles']}" if res["completed"] else "unknown")
    print(f"shape {shape_id} r2={r2}: {tag} ({dt:.1f}s)")
    return res


def ceiling(db, shape_id: int, conflict_budget=1_000_000):
    """Find where a finite-patch shape stops covering disks."""
    largest_grown = None
    for r2 in CEILING_LADDER:
        res = refute(db, shape_id, r2, conflict_budget)
        if res["completed"]:
            largest_grown = r2
        elif res["refuted"]:
            print(f"shape {shape_id}: ceiling between r2={largest_grown} "
                  f"and r2={r2}")
            return
        else:
            print(f"shape {shape_id}: budget wall at r2={r2}")
            return
    print(f"shape {shape_id}: covered every ladder radius "
          f"(largest r2={largest_grown})")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    db = ShapeDB("data/shapes.sqlite")
    mode, shape_id = sys.argv[1], int(sys.argv[2])
    if mode == "grow":
        grow(db, shape_id, int(sys.argv[3]),
             int(sys.argv[4]) if len(sys.argv) > 4 else None)
    elif mode == "refute":
        refute(db, shape_id, int(sys.argv[3]),
               int(sys.argv[4]) if len(sys.argv) > 4 else None)
    elif mode == "ceiling":
        ceiling(db, shape_id)
    else:
        sys.exit(__doc__)
    db.close()


if __name__ == "__main__":
    main()
