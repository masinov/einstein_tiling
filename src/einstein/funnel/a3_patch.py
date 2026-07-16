"""A3 -- large-patch construction (program section 4 A3, milestone M3).

Anomalies that survive A2 (coronas keep growing) are grown into large
patches here; A4 (diffraction) consumes the result.  The task is posed as
exact cover: cover every kite cell of a disk-shaped region with congruent
copies of the shape (copies may overhang the disk boundary).  Posing it as
region cover makes hole-freeness automatic: an enclosed empty cell is
itself an uncovered region cell, so it fails the cover instead of needing
a separate flood-fill check.

Two engines (D-0009):

* `sat_grow_patch` -- the workhorse.  CNF encoding (one variable per
  placement, at-least-one per region cell, pairwise conflicts for
  overlapping placements) handed to CaDiCaL.  CDCL's learned clauses and
  non-chronological backjumping handle the hat's long-range conflicts,
  which defeat greedy growth (measured: the pure-Python greedy filler
  stalls near ~250 tiles).  A model is decoded to placements and
  re-verified by our own exact verifier, so the external solver is never
  trusted.  UNSAT with no seed constraint is a *pose-free* refutation:
  no patch of copies covers this disk at all.

* `grow_patch` -- pure-Python greedy filler (most-constrained-first
  frontier, fail-first backtracking, escalating partial restarts).  Kept
  for the growth-rate *profile* the program wants as a feature
  (options-per-decision histogram; near-deterministic profiles signal
  forced, substitution-like structure) and as the no-dependency fallback.

Verdict semantics: constructive only, except SAT-UNSAT.  "grown" carries
a machine-verified certificate (placements as (op, tx, ty) acting on the
shape); "stalled" carries the budget stamp and profile and never claims a
larger patch is impossible.

Scope: grid-aligned placements only (D-0006).
"""

from __future__ import annotations

import heapq
import itertools
import random
import time
from math import isqrt

from einstein.funnel.a2_heesch import Budget, BudgetExhausted
from einstein.substrate.kitegrid import (
    N_OPS,
    cell_centroid4,
    cell_vertices,
    cells_at_point,
    is_center,
    norm2,
    transform_cell,
    translate_cell,
)

Cell = tuple[int, int, int]


def disk_region(r2: int) -> list[Cell]:
    """All kite cells whose centroid lies within squared Euclidean distance
    r2 of the origin, center-out order.  Exact: 4x the centroid is an
    integer point, so the test is norm2(centroid4) <= 16*r2."""
    lim = 2 * isqrt(r2) + 8
    out = []
    for cx in range(-lim, lim + 1):
        for cy in range(-lim, lim + 1):
            if not is_center((cx, cy)):
                continue
            for d in range(6):
                if norm2(cell_centroid4((cx, cy, d))) <= 16 * r2:
                    out.append((cx, cy, d))
    out.sort(key=lambda c: (norm2(cell_centroid4(c)), c))
    return out


def _images(shape):
    """Distinct point-group images of the shape, translation-normalized so
    the lex-min cell's center is the origin.  Entry (op, offx, offy, cells):
    the copy `cells + t` equals `transform_cell(shape, op) + (t + off)`,
    so its certificate record is (op, t + off)."""
    out = []
    seen = set()
    for op in range(N_OPS):
        raw = sorted(transform_cell(c, op) for c in shape)
        t0x, t0y = raw[0][0], raw[0][1]
        cells = tuple((cx - t0x, cy - t0y, d) for cx, cy, d in raw)
        if cells in seen:
            continue
        seen.add(cells)
        out.append((op, -t0x, -t0y, cells))
    return out


def grow_patch(shape, r2: int, node_budget: int = 5_000_000,
               restart_backtracks: int = 20_000, rng_seed: int = 0):
    """Grow a patch of congruent copies of `shape` exactly covering the
    disk of squared radius r2 (copies may overhang).  Returns a dict:

      completed           disk fully covered
      tiles               placements in the completed patch (0 otherwise)
      certificate         {"kind": "disk-patch", "r2", "tiles",
                           "placements": [[op, tx, ty], ...]} or None
      seed_pose_exhausted systematic search emptied without a solution
                          (only claimable before the first partial restart)
      exhausted           node budget ran out
      profile             region_cells, best_tiles, backtracks, restarts,
                          nodes, options_hist (options count -> frequency)

    restart_backtracks: how many backtrack steps without a new best patch
    size trigger a partial restart (unwind of half the trail, doubling on
    consecutive stalls up to a full reset).
    """
    region = disk_region(r2)
    region_set = frozenset(region)
    rdist = {c: norm2(cell_centroid4(c)) for c in region}
    imgs = _images(shape)
    budget = Budget(node_budget)
    rng = random.Random(rng_seed)
    counter = itertools.count()
    profile = {"region_cells": len(region), "best_tiles": 0,
               "backtracks": 0, "restarts": 0, "options_hist": {}}

    def attempt():
        covered: set[Cell] = set()
        uncovered = len(region)
        heap: list = []
        trail: list = []  # frames [options, index]; option = (op,tx,ty,cells)
        backtracks_seg = 0  # backtracks since the last restart / new best
        stall = 0           # consecutive restarts without a new best
        systematic = True   # no alternatives skipped yet

        def cand(r):
            rx, ry, rd = r
            out = []
            for op, offx, offy, img in imgs:
                for c in img:
                    if c[2] != rd:
                        continue
                    tx, ty = rx - c[0], ry - c[1]
                    cells = tuple((x + tx, y + ty, d) for x, y, d in img)
                    for cc in cells:
                        if cc in covered:
                            break
                    else:
                        out.append((op, tx + offx, ty + offy, cells))
            return out

        def place(pl):
            nonlocal uncovered
            for cc in pl[3]:
                covered.add(cc)
                if cc in region_set:
                    uncovered -= 1
            pts = set()
            for cc in pl[3]:
                pts.update(cell_vertices(cc))
            aff = set()
            for p in pts:
                for c2 in cells_at_point(p):
                    if c2 in region_set and c2 not in covered:
                        aff.add(c2)
            for c2 in aff:
                heapq.heappush(
                    heap, (len(cand(c2)), rdist[c2], next(counter), c2))

        def unplace(pl):
            nonlocal uncovered
            for cc in pl[3]:
                covered.discard(cc)
                if cc in region_set:
                    uncovered += 1
                    # optimistic key: recomputed when popped
                    heapq.heappush(heap, (0, rdist[cc], next(counter), cc))

        seed_pl = imgs[0]  # identity pose at the origin (symmetry breaking)
        place(seed_pl)
        if profile["best_tiles"] == 0:
            profile["best_tiles"] = 1
        while uncovered:
            budget.tick()
            r = opts = None
            while heap:
                k0, d0, _, c0 = heapq.heappop(heap)
                if c0 in covered:
                    continue
                o = cand(c0)
                if heap and len(o) > heap[0][0]:
                    heapq.heappush(heap, (len(o), d0, next(counter), c0))
                    continue
                r, opts = c0, o
                break
            if r is None:
                r = next(c for c in region if c not in covered)
                opts = cand(r)
            k = len(opts)
            profile["options_hist"][k] = profile["options_hist"].get(k, 0) + 1
            if opts:
                rng.shuffle(opts)
                trail.append([opts, 0])
                place(opts[0])
                if len(trail) + 1 > profile["best_tiles"]:
                    profile["best_tiles"] = len(trail) + 1
                    backtracks_seg = 0
                    stall = 0
                continue
            # dead end at r: fail-first -- keep r at the top of the heap so
            # it is re-examined right after every backtrack step
            heapq.heappush(heap, (0, rdist[r], next(counter), r))
            while True:  # chronological backtracking
                budget.tick()
                profile["backtracks"] += 1
                backtracks_seg += 1
                if backtracks_seg > restart_backtracks:
                    # partial restart: unwind an escalating fraction of the
                    # trail without trying alternatives (forfeits
                    # completeness), keep going with a fresh random order
                    stall += 1
                    systematic = False
                    keep = len(trail) >> min(stall, 32)
                    while len(trail) > keep:
                        o, i = trail.pop()
                        unplace(o[i])
                    backtracks_seg = 0
                    profile["restarts"] += 1
                    break
                if not trail:
                    if systematic:
                        return None  # seed-pose search space exhausted
                    break  # restart from the bare seed
                o, i = trail[-1]
                unplace(o[i])
                if i + 1 < len(o):
                    trail[-1][1] = i + 1
                    place(o[i + 1])
                    break
                trail.pop()
        return [seed_pl] + [o[i] for o, i in trail]

    placements = None
    exhausted = refuted = False
    try:
        placements = attempt()
        refuted = placements is None
    except BudgetExhausted:
        exhausted = True
    profile["nodes"] = node_budget - budget.left

    cert = None
    if placements is not None:
        cert = {"kind": "disk-patch", "r2": r2, "tiles": len(placements),
                "placements": [[op, tx, ty] for op, tx, ty, _ in placements]}
    return {
        "completed": placements is not None,
        "tiles": len(placements) if placements is not None else 0,
        "certificate": cert,
        "seed_pose_exhausted": refuted,
        "exhausted": exhausted,
        "profile": profile,
    }


def enumerate_placements(shape, region) -> list:
    """All distinct grid-aligned copies of `shape` covering at least one
    cell of `region`, as (op, tx, ty, cells)."""
    imgs = _images(shape)
    seen = set()
    out = []
    for r in region:
        rx, ry, rd = r
        for op, offx, offy, img in imgs:
            for c in img:
                if c[2] != rd:
                    continue
                tx, ty = rx - c[0], ry - c[1]
                key = (op, tx + offx, ty + offy)
                if key in seen:
                    continue
                seen.add(key)
                cells = tuple((x + tx, y + ty, d) for x, y, d in img)
                out.append(key + (cells,))
    return out


def sat_grow_patch(shape, r2: int, fix_seed: bool = True,
                   conflict_budget: int | None = None):
    """Cover the disk of squared radius r2 with copies of `shape` via SAT
    (CaDiCaL).  fix_seed pins the identity-pose copy at the origin
    (symmetry breaking; speeds up SAT runs but weakens UNSAT to
    "no patch containing that pose").  Returns a dict:

      completed    True (certificate attached, already re-verified)
      refuted      UNSAT; pose-free iff fix_seed was False
      exhausted    conflict budget hit before an answer
      stats        vars / clauses / region_cells / solve seconds
    """
    from pysat.solvers import Cadical195

    region = disk_region(r2)
    placements = enumerate_placements(shape, region)
    covering: dict[Cell, list[int]] = {}
    for i, pl in enumerate(placements):
        for cc in pl[3]:
            covering.setdefault(cc, []).append(i + 1)

    solver = Cadical195()
    n_clauses = 0
    for vs in covering.values():
        for a in range(len(vs)):
            for b in range(a + 1, len(vs)):
                solver.add_clause([-vs[a], -vs[b]])
                n_clauses += 1
    for cc in region:
        solver.add_clause(covering[cc])
        n_clauses += 1
    if fix_seed:
        seed_cells = _images(shape)[0][3]
        seed_var = next(
            i + 1 for i, pl in enumerate(placements) if pl[3] == seed_cells)
        solver.add_clause([seed_var])
        n_clauses += 1

    t0 = time.monotonic()
    if conflict_budget is not None:
        solver.conf_budget(conflict_budget)
        sat = solver.solve_limited()
    else:
        sat = solver.solve()
    dt = time.monotonic() - t0
    stats = {"vars": len(placements), "clauses": n_clauses,
             "region_cells": len(region), "solve_seconds": round(dt, 2)}

    result = {"completed": False, "refuted": False, "exhausted": False,
              "certificate": None, "tiles": 0, "stats": stats}
    if sat is None:
        result["exhausted"] = True
    elif sat is False:
        result["refuted"] = True
    else:
        model = set(v for v in solver.get_model() if v > 0)
        chosen = [pl for i, pl in enumerate(placements) if i + 1 in model]
        cert = {"kind": "disk-patch", "r2": r2, "tiles": len(chosen),
                "placements": [[op, tx, ty] for op, tx, ty, _ in chosen]}
        if not verify_patch_certificate(shape, cert):
            raise AssertionError("SAT model failed independent verification")
        result.update(completed=True, certificate=cert, tiles=len(chosen))
    solver.delete()
    return result


def certificate_cells(shape, cert) -> list[list[Cell]]:
    """The cells of each placement of a disk-patch certificate."""
    return [
        [translate_cell(transform_cell(c, op), (tx, ty)) for c in shape]
        for op, tx, ty in cert["placements"]
    ]


def verify_patch_certificate(shape, cert) -> bool:
    """Independent re-check of a disk-patch certificate: every placement is
    a valid grid-aligned copy of `shape` (op in range, center-lattice
    translation), placements are pairwise disjoint, and together they cover
    every cell of the disk region."""
    if cert.get("kind") != "disk-patch":
        return False
    covered: set[Cell] = set()
    for op, tx, ty in cert["placements"]:
        if not (0 <= op < N_OPS) or not is_center((tx, ty)):
            return False
        for c in shape:
            cc = translate_cell(transform_cell(c, op), (tx, ty))
            if cc in covered:
                return False
            covered.add(cc)
    return all(c in covered for c in disk_region(cert["r2"]))
