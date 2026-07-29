#!/usr/bin/env python
"""Batch A2 (Heesch/corona depth) over A1 survivors in the shape database.

Sharp prediction (from Myers-validated A1 data): for n <= 8, every A1
survivor except the hat is a non-tiler, so all must have finite Heesch
depth; only the hat may keep growing at any cap.

Verdict vocabulary (stage 'A2-heesch'):
  heesch-ge-cap    reached the depth cap (certificate stored) -> escalate
  heesch-exact     exhaustive: depth is the shape's H_c (budget completed)
  heesch-ge-unknown budget exhausted at depth < cap: lower bound only

Usage: venv/bin/python scripts/archive/run_a2.py [n_max] [depth_cap] [node_budget]
Resumable; skips shapes with an existing A2-heesch verdict.
"""

import sys
import time

from einstein.polykites.database import ShapeDB, deserialize_cells
from einstein.polykites.coronas import heesch_search, verify_heesch_certificate

STAGE = "A2-heesch"


def main(n_max: int = 8, depth_cap: int = 2, node_budget: int = 100_000):
    db = ShapeDB("data/shapes.sqlite")
    budget = {"depth_cap": depth_cap, "node_budget": node_budget,
              "hole_free": True}
    rows = db.conn.execute(
        "SELECT s.id, s.key, s.n FROM shapes s JOIN verdicts v "
        "ON v.shape_id = s.id AND v.stage = 'A1-torus' "
        "WHERE v.verdict != 'periodic' AND s.n <= ? ORDER BY s.n, s.id",
        (n_max,),
    ).fetchall()
    print(f"{len(rows)} A1 survivors with n <= {n_max}")
    t0 = time.time()
    stats: dict[str, int] = {}
    done = 0
    for sid, key, n in rows:
        if db.latest_verdict(sid, STAGE) is not None:
            stats["skipped"] = stats.get("skipped", 0) + 1
            continue
        shape = deserialize_cells(key)
        res = heesch_search(shape, depth_cap=depth_cap,
                            node_budget=node_budget)
        cert = res["certificate"]
        if cert is not None:
            assert verify_heesch_certificate(shape, cert), (sid, key)
        if res["reached_cap"]:
            verdict = "heesch-ge-cap"
        elif not res["exhausted"]:
            verdict = "heesch-exact"
        else:
            verdict = "heesch-ge-unknown"
        db.record_verdict(sid, STAGE, verdict,
                          {"depth": res["depth"], "coronas": cert}, budget)
        stats[f"{verdict}:{res['depth']}"] = \
            stats.get(f"{verdict}:{res['depth']}", 0) + 1
        done += 1
        if done % 100 == 0:
            db.commit()
            print(f"  ...{done} done t={time.time() - t0:.0f}s", flush=True)
    db.commit()
    print(f"finished {done} shapes in {time.time() - t0:.0f}s")
    for k in sorted(stats):
        print(f"  {k:28s} {stats[k]}")
    db.close()


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]]
    main(*args)
