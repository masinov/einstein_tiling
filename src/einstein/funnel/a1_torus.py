"""A1 -- fast periodicity rejection via torus (exact cover) search.

A *grid-aligned* periodic tiling of the plane by a polykite descends to an
exact cover of a torus: the quotient of the kite grid by a finite-index
sublattice L of the hexagon-center translation lattice.  Conversely any such
cover lifts to a genuine periodic tiling with period lattice L.  So:

  positive verdict  = machine-verified periodic-tiling certificate
                      (retires the shape from einstein candidacy);
  negative verdict  = "no grid-aligned periodic tiling with fundamental
                      domain of index <= k_max": a budget-stamped semi-
                      decision, never a proof of aperiodicity.

Scope limitation (recorded as D-0006): only grid-aligned placements are
considered, i.e. images of the shape under the kite grid's symmetry group
p6m = D6 (about a hex center) x center-lattice translations.  Polyform
tilings that break grid alignment exist in general and are invisible here.

Lattice bookkeeping: hexagon centers form a rank-2 lattice with basis
t1 = (2, 2), t2 = (-2, 4) in hex coordinates.  A cell (cx, cy, d) maps to
lattice coordinates (u, v, d) with u = (2*cx + cy) / 6, v = (cy - cx) / 6.
Sublattices of index k are enumerated in Hermite normal form: generators
(a, 0) and (b, d) with a*d = k, 0 <= b < a; every finite-index sublattice
appears exactly once.
"""

from __future__ import annotations

from einstein.substrate.kitegrid import N_OPS, transform_cell

Cell = tuple[int, int, int]


def cell_to_lattice(cell: Cell) -> tuple[int, int, int]:
    cx, cy, d = cell
    u, r1 = divmod(2 * cx + cy, 6)
    v, r2 = divmod(cy - cx, 6)
    if r1 or r2:
        raise ValueError(f"{cell} is not a valid hex-center cell")
    return (u, v, d)


def lattice_to_cell(uvd: tuple[int, int, int]) -> Cell:
    u, v, d = uvd
    return (2 * u - 2 * v, 2 * u + 4 * v, d)


def sublattices(k: int) -> list[tuple[int, int, int]]:
    """All index-k sublattices as HNF triples (a, b, d): generators
    (a, 0), (b, d) in (u, v) lattice coordinates."""
    out = []
    for a in range(1, k + 1):
        if k % a:
            continue
        d = k // a
        for b in range(a):
            out.append((a, b, d))
    return out


def _reduce(u: int, v: int, a: int, b: int, d: int) -> tuple[int, int]:
    """Canonical representative of (u, v) modulo the sublattice (a,0),(b,d)."""
    q, v = divmod(v, d)
    u -= q * b
    u %= a
    return u, v


class TorusInstance:
    """Exact-cover instance: tile the torus (quotient by one sublattice)."""

    def __init__(self, shape: tuple[Cell, ...], hnf: tuple[int, int, int]):
        self.shape = shape
        self.a, self.b, self.d = hnf
        self.k = self.a * self.d
        self.n_cells = 6 * self.k
        # torus cell index: (u, v, sector) -> bit
        self.index = {}
        for u in range(self.a):
            for v in range(self.d):
                for s in range(6):
                    self.index[(u, v, s)] = len(self.index)
        self.placements: list[tuple[tuple[int, int, int], int]] = []
        self._build_placements()

    def _build_placements(self):
        n = len(self.shape)
        seen_masks = {}
        for op in range(N_OPS):
            img = [cell_to_lattice(transform_cell(c, op)) for c in self.shape]
            for tu in range(self.a):
                for tv in range(self.d):
                    mask = 0
                    count = 0
                    for (u, v, s) in img:
                        uu, vv = _reduce(u + tu, v + tv, self.a, self.b, self.d)
                        bit = 1 << self.index[(uu, vv, s)]
                        if mask & bit:
                            break  # self-overlap through the quotient
                        mask |= bit
                        count += 1
                    if count == n and mask not in seen_masks:
                        seen_masks[mask] = (op, tu, tv)
                        self.placements.append(((op, tu, tv), mask))

    def solve(self, node_budget: int = 200_000):
        """Exact cover by backtracking on Python-int bitmasks.
        Returns (list of placements) or None; raises RuntimeError if the
        node budget is exhausted (result then unknown)."""
        full = (1 << self.n_cells) - 1
        by_cell = [[] for _ in range(self.n_cells)]
        for pl in self.placements:
            m = pl[1]
            i = 0
            mm = m
            while mm:
                if mm & 1:
                    by_cell[i].append(pl)
                mm >>= 1
                i += 1
        nodes = 0
        chosen: list[tuple[int, int, int]] = []

        def bt(cover: int) -> bool:
            nonlocal nodes
            nodes += 1
            if nodes > node_budget:
                raise RuntimeError("node budget exhausted")
            if cover == full:
                return True
            # branch on the uncovered cell with fewest available placements
            best_cell, best_opts = -1, None
            for i in range(self.n_cells):
                if not (cover >> i) & 1:
                    opts = [pl for pl in by_cell[i] if not (pl[1] & cover)]
                    if best_opts is None or len(opts) < len(best_opts):
                        best_cell, best_opts = i, opts
                        if not opts:
                            return False
                        if len(opts) == 1:
                            break
            for key, mask in best_opts:
                chosen.append(key)
                if bt(cover | mask):
                    return True
                chosen.pop()
            return False

        if bt(0):
            return list(chosen)
        return None


def find_periodic_tiling(shape, k_max: int = 12, node_budget: int = 200_000):
    """Sweep tori of index 1..k_max (smallest first).

    Returns (certificate, exhausted):
      certificate -- verified periodic-tiling certificate dict, or None;
      exhausted   -- True if any torus search hit the node budget (so a
                     None result means "unknown", not "refuted at budget").
    `shape` is a tuple of cells (any placement; canonical form is fine).
    """
    n = len(shape)
    exhausted = False
    for k in range(1, k_max + 1):
        if (6 * k) % n:
            continue
        for hnf in sublattices(k):
            inst = TorusInstance(tuple(shape), hnf)
            try:
                sol = inst.solve(node_budget=node_budget)
            except RuntimeError:
                exhausted = True
                continue
            if sol is not None:
                cert = {
                    "kind": "torus-exact-cover",
                    "hnf": list(hnf),
                    "index": k,
                    "tiles_per_domain": (6 * k) // n,
                    "placements": [list(p) for p in sol],
                }
                assert verify_certificate(shape, cert), "unverifiable certificate"
                return cert, exhausted
    return None, exhausted


def find_periodic_tiling_sat(
    shape,
    k_max: int = 100,
    conflict_budget: int | None = None,
    k_min: int = 1,
):
    """Exact torus sweep using CaDiCaL instead of recursive backtracking.

    This is the escalation engine for a small number of A3/A4 survivors.
    It supports arbitrary quotient sizes (Python integer masks), whereas the
    compiled bulk engine deliberately uses one u128 and stops at k=21.

    Returns ``(certificate, exhausted)`` with the same semantics as
    :func:`find_periodic_tiling`.
    """
    n = len(shape)
    exhausted = False
    if not (1 <= k_min <= k_max):
        raise ValueError("require 1 <= k_min <= k_max")
    for k in range(k_min, k_max + 1):
        if (6 * k) % n:
            continue
        for hnf in sublattices(k):
            certificate, instance_exhausted = solve_torus_sat(
                shape, hnf, conflict_budget=conflict_budget
            )
            if instance_exhausted:
                exhausted = True
                continue
            if certificate is not None:
                return certificate, exhausted
    return None, exhausted


def solve_torus_sat(shape, hnf, conflict_budget: int | None = None):
    """Solve one exact torus quotient with CaDiCaL.

    Returns ``(certificate, exhausted)``. A ``None, False`` result is an exact
    UNSAT proof for this quotient; ``None, True`` means the conflict budget
    was reached.
    """
    from pysat.solvers import Cadical195

    instance = TorusInstance(tuple(shape), hnf)
    covering = [[] for _ in range(instance.n_cells)]
    for variable, (_, mask) in enumerate(instance.placements, 1):
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            covering[bit.bit_length() - 1].append(variable)
            remaining ^= bit

    solver = Cadical195()
    for variables in covering:
        solver.add_clause(variables)
        for a in range(len(variables)):
            for b in range(a + 1, len(variables)):
                solver.add_clause([-variables[a], -variables[b]])
    if conflict_budget is None:
        sat = solver.solve()
    else:
        solver.conf_budget(conflict_budget)
        sat = solver.solve_limited()
    if sat is None:
        solver.delete()
        return None, True
    if not sat:
        solver.delete()
        return None, False
    model = {value for value in solver.get_model() if value > 0}
    solution = [
        list(placement)
        for variable, (placement, _) in enumerate(instance.placements, 1)
        if variable in model
    ]
    certificate = {
        "kind": "torus-exact-cover",
        "hnf": list(hnf),
        "index": hnf[0] * hnf[2],
        "tiles_per_domain": len(solution),
        "placements": solution,
    }
    solver.delete()
    assert verify_certificate(shape, certificate)
    return certificate, False


def verify_certificate(shape, cert) -> bool:
    """Independent re-check: the claimed placements exactly cover the torus."""
    a, b, d = cert["hnf"]
    idx = {}
    for u in range(a):
        for v in range(d):
            for s in range(6):
                idx[(u, v, s)] = len(idx)
    covered = 0
    for op, tu, tv in cert["placements"]:
        for c in shape:
            u, v, s = cell_to_lattice(transform_cell(tuple(c), op))
            uu, vv = _reduce(u + tu, v + tv, a, b, d)
            bit = 1 << idx[(uu, vv, s)]
            if covered & bit:
                return False
            covered |= bit
    return covered == (1 << (6 * a * d)) - 1
