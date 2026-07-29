"""Exact corona growth and Heesch-depth analysis for polykites.

Definitions follow Kaplan, "Heesch Numbers of Unmarked Polyforms"
(arXiv:2105.09438): a corona of a patch is a set of congruent copies of the
shape with pairwise disjoint interiors, each touching the patch (sharing at
least one boundary point), whose union with the patch contains a
neighborhood of the patch -- on the grid: every empty cell sharing at least
a vertex with the patch is covered.  We compute H_c: holes are forbidden in
every corona (each successive patch must have no bounded empty region;
emptiness-connectivity is via edge adjacency).  Heesch number H = maximum k
such that k nested coronas exist; tilers have H = infinity.

Search: depth-first over corona solutions (exact cover of the required ring,
optional outward cells at most once), backtracking across levels, with a
global node budget.  Verdicts:

  reached depth cap          -> "heesch >= cap"    (certificate attached)
  search complete, best = k  -> "heesch = k" exact (exhaustive refutation)
  budget exhausted, best = k -> "heesch >= k, unknown above"

Certificates record every corona's placements and are re-verified
independently (congruence via canonical forms, coverage, disjointness,
hole-freeness).  Exactness claims are exhaustion results, like UNSAT: they
carry the budget stamp, not a certificate.

Scope: grid-aligned placements only (D-0006).
"""

from __future__ import annotations

from einstein.geometry.kite_grid import (
    N_OPS,
    canonical_form,
    cell_neighbors,
    cell_vertices,
    cells_at_point,
    transform_cell,
)
from einstein.polykites.periodic_quotients import cell_to_lattice, lattice_to_cell

Cell = tuple[int, int, int]


class BudgetExhausted(Exception):
    pass


class Budget:
    def __init__(self, nodes: int):
        self.left = nodes

    def tick(self):
        self.left -= 1
        if self.left < 0:
            raise BudgetExhausted


def ring(patch: frozenset[Cell]) -> frozenset[Cell]:
    """Empty cells sharing at least one vertex with the patch."""
    out = set()
    for c in patch:
        for v in cell_vertices(c):
            for c2 in cells_at_point(v):
                if c2 not in patch:
                    out.add(c2)
    return frozenset(out)


def placements_touching(shape, patch: frozenset[Cell], required) -> list[frozenset[Cell]]:
    """All congruent copies of `shape` that cover at least one required cell
    and do not overlap the patch."""
    seen = set()
    out = []
    for op in range(N_OPS):
        img = [transform_cell(c, op) for c in shape]
        for r in required:
            for c in img:
                if c[2] != r[2]:
                    continue
                t = (r[0] - c[0], r[1] - c[1])
                placed = frozenset(
                    (cc[0] + t[0], cc[1] + t[1], cc[2]) for cc in img
                )
                if placed in seen:
                    continue
                seen.add(placed)
                if not placed & patch:
                    out.append(placed)
    return out


def has_hole(patch: frozenset[Cell]) -> bool:
    """Does the complement of the patch have a bounded (edge-)connected
    component?  Checked by flood fill from the boundary of a padded
    bounding box in lattice coordinates."""
    lat = {cell_to_lattice(c) for c in patch}
    us = [u for u, v, s in lat]
    vs = [v for u, v, s in lat]
    u0, u1 = min(us) - 2, max(us) + 2
    v0, v1 = min(vs) - 2, max(vs) + 2

    def in_box(u, v):
        return u0 <= u <= u1 and v0 <= v <= v1

    empty = {
        (u, v, s)
        for u in range(u0, u1 + 1)
        for v in range(v0, v1 + 1)
        for s in range(6)
        if (u, v, s) not in lat
    }
    # flood from box rim
    stack = [c for c in empty if c[0] in (u0, u1) or c[1] in (v0, v1)]
    reached = set(stack)
    while stack:
        c = stack.pop()
        for nb in cell_neighbors(lattice_to_cell(c)):
            nl = cell_to_lattice(nb)
            if nl in empty and nl not in reached and in_box(nl[0], nl[1]):
                reached.add(nl)
                stack.append(nl)
    return len(reached) != len(empty)


def corona_solutions(shape, patch: frozenset[Cell], budget: Budget):
    """Generate all coronas of `patch` (as lists of placements), depth-first.
    Ticks the budget per search node; raises BudgetExhausted."""
    required = ring(patch)
    placements = placements_touching(shape, patch, required)
    by_req: dict[Cell, list[frozenset[Cell]]] = {r: [] for r in required}
    for p in placements:
        for r in required:
            if r in p:
                by_req[r].append(p)

    chosen: list[frozenset[Cell]] = []
    used: set[Cell] = set()

    def bt():
        budget.tick()
        best_r, best_opts = None, None
        for r in required:
            if r in used:
                continue
            opts = [p for p in by_req[r] if not (p & used)]
            if best_opts is None or len(opts) < len(best_opts):
                best_r, best_opts = r, opts
                if len(opts) <= 1:
                    break
        if best_r is None:
            yield list(chosen)
            return
        for p in best_opts:
            chosen.append(p)
            used.update(p)
            yield from bt()
            used.difference_update(p)
            chosen.pop()

    yield from bt()


def heesch_search(shape, depth_cap: int = 2, node_budget: int = 100_000,
                  hole_free: bool = True):
    """Depth-first Heesch search.  Returns a dict:
       {depth, reached_cap, exhausted, certificate}
    depth = deepest corona level completed on any branch."""
    seed = frozenset(shape)
    budget = Budget(node_budget)
    state = {"depth": 0, "cert": None}
    chain: list[list[list[Cell]]] = []

    def extend(patch: frozenset[Cell], level: int) -> bool:
        for corona in corona_solutions(shape, patch, budget):
            cells = set()
            for p in corona:
                cells |= p
            newpatch = patch | cells
            if hole_free and has_hole(newpatch):
                continue
            chain.append([sorted(p) for p in corona])
            if level > state["depth"]:
                state["depth"] = level
                state["cert"] = [list(lv) for lv in chain]
            if level == depth_cap or extend(newpatch, level + 1):
                chain.pop()
                return True
            chain.pop()
        return False

    exhausted = False
    try:
        reached_cap = extend(seed, 1)
    except BudgetExhausted:
        exhausted = True
        reached_cap = state["depth"] >= depth_cap
    return {
        "depth": state["depth"],
        "reached_cap": reached_cap,
        "exhausted": exhausted,
        "certificate": state["cert"],
    }


def verify_heesch_certificate(shape, cert, hole_free: bool = True) -> bool:
    """Independent re-check that `cert` (list of coronas, each a list of
    placements given as cell lists) witnesses Heesch depth >= len(cert)."""
    shape_canon = canonical_form(shape)
    patch = frozenset(shape)
    for corona in cert:
        occupied = set(patch)
        for placement in corona:
            cells = [tuple(c) for c in placement]
            if canonical_form(cells) != shape_canon:
                return False  # not a congruent copy
            if any(c in occupied for c in cells):
                return False  # overlap
            occupied.update(cells)
        newpatch = frozenset(occupied)
        if ring(patch) - newpatch:
            return False  # some vertex-adjacent cell left uncovered
        if hole_free and has_hole(newpatch):
            return False
        patch = newpatch
    return True
