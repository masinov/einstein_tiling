"""Binary-coupled finite-group torus holonomy CSP for W2.D."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import itertools

from pysat.formula import CNF
from pysat.solvers import Cadical195

from einstein.funnel.a1_torus import TorusInstance, lattice_to_cell
from einstein.substrate.kitegrid import boundary_edges, transform_cell
from einstein.theory.holonomy import (
    S3,
    S3_IDENTITY,
    _perm_compose,
    _perm_inverse,
    kite_edge_letter,
)


def _perm_power(value, exponent):
    if exponent < 0:
        value = _perm_inverse(value)
        exponent = -exponent
    out = S3_IDENTITY
    for _ in range(exponent):
        out = _perm_compose(out, value)
    return out


def commuting_s3_pairs():
    return tuple(
        (left, right)
        for left in S3 for right in S3
        if _perm_compose(left, right) == _perm_compose(right, left)
    )


def _point_type(point):
    x, y = point
    return (2 * x + y) % 6, (y - x) % 6


class QuotientVertexReducer:
    """Reduce kite vertices modulo an HNF and retain the deck translation."""

    def __init__(self, hnf, points):
        self.a, self.b, self.d = hnf
        by_type = {}
        for point in points:
            kind = _point_type(point)
            by_type.setdefault(kind, []).append(point)
        self.bases = {kind: min(values) for kind, values in by_type.items()}

    def reduce(self, point):
        kind = _point_type(point)
        base = self.bases[kind]
        dx, dy = point[0] - base[0], point[1] - base[1]
        u_num, v_num = 2 * dx + dy, dy - dx
        if u_num % 6 or v_num % 6:
            raise ValueError("vertex type did not differ by a center translation")
        u, v = u_num // 6, v_num // 6
        qv, rv = divmod(v, self.d)
        u -= qv * self.b
        qu, ru = divmod(u, self.a)
        return (kind[0], kind[1], ru, rv), (qu, qv)


def _placement_boundary(shape, placement):
    op, tu, tv = placement
    tx, ty, _ = lattice_to_cell((tu, tv, 0))
    cells = tuple(
        (cell[0] + tx, cell[1] + ty, cell[2])
        for cell in (transform_cell(source, op) for source in shape)
    )
    return boundary_edges(cells)


@lru_cache(maxsize=256)
def _quotient_boundary_data_cached(shape, hnf):
    instance = TorusInstance(shape, tuple(hnf))
    raw = []
    points = set()
    for placement, _ in instance.placements:
        edges = _placement_boundary(shape, placement)
        placement_rows = []
        for edge in edges:
            start, end = sorted(edge)
            points.update((start, end))
            placement_rows.append((start, end, kite_edge_letter(start, end)))
        raw.append(tuple(sorted(placement_rows)))
    reducer = QuotientVertexReducer(tuple(hnf), points)
    vertices = set()
    rows = []
    for placement_rows in raw:
        reduced = []
        for start, end, letter in placement_rows:
            start_key, start_deck = reducer.reduce(start)
            end_key, end_deck = reducer.reduce(end)
            vertices.update((start_key, end_key))
            reduced.append((start_key, start_deck, end_key, end_deck, letter))
        rows.append(tuple(reduced))
    return instance, tuple(sorted(vertices)), tuple(rows)


def quotient_boundary_data(shape, hnf):
    """All placement-boundary edges with quotient vertex/deck coordinates."""
    return _quotient_boundary_data_cached(
        tuple(tuple(cell) for cell in shape), tuple(hnf)
    )


def _edge_image(letter, images):
    image = images[abs(letter) - 1]
    return image if letter > 0 else _perm_inverse(image)


def _deck_holonomy(deck, twists):
    return _perm_compose(
        _perm_power(twists[0], deck[0]),
        _perm_power(twists[1], deck[1]),
    )


def _append_cover_clauses(cnf, instance, placement_vars, cover_mode):
    by_cell = [[] for _ in range(instance.n_cells)]
    for variable, (_, mask) in zip(placement_vars, instance.placements):
        for cell in range(instance.n_cells):
            if (mask >> cell) & 1:
                by_cell[cell].append(variable)
    for variables in by_cell:
        cnf.append(variables)
        if cover_mode == "exact":
            for left, right in itertools.combinations(variables, 2):
                cnf.append([-left, -right])


def build_cover_cnf(shape, hnf, cover_mode="at-least"):
    """Build the placement-only control CNF used by the coupled experiment."""
    if cover_mode not in {"at-least", "exact"}:
        raise ValueError("cover_mode must be 'at-least' or 'exact'")
    instance = TorusInstance(tuple(tuple(cell) for cell in shape), tuple(hnf))
    cnf = CNF()
    placement_vars = tuple(range(1, len(instance.placements) + 1))
    _append_cover_clauses(cnf, instance, placement_vars, cover_mode)
    metadata = {
        "hnf": list(hnf),
        "cover_mode": cover_mode,
        "cells": instance.n_cells,
        "placements": len(instance.placements),
        "variables": len(placement_vars),
        "clauses": len(cnf.clauses),
    }
    return cnf, metadata


def solve_cover_control(shape, hnf, cover_mode="at-least"):
    """Solve the placement-only control and return deterministic metadata."""
    cnf, metadata = build_cover_cnf(shape, hnf, cover_mode=cover_mode)
    with Cadical195(bootstrap_with=cnf) as solver:
        sat = solver.solve()
        stats = solver.accum_stats()
    return {
        "kind": "placement-only-cover-control",
        "hnf": list(hnf),
        "cover_mode": cover_mode,
        "sat": sat,
        "cnf_sha256": _cnf_sha256(cnf),
        "metadata": metadata,
        "conflicts": stats.get("conflicts"),
    }


def build_boundary_holonomy_cnf(
    shape,
    hnf,
    images,
    twists,
    cover_mode="at-least",
):
    """Build one twisted S3 boundary-potential CNF.

    ``at-least`` is the deliberate holonomy relaxation: every cell is covered
    by one or more selected placements. ``exact`` adds pairwise nonoverlap.
    Every genuine exact cover satisfies both encodings.
    """
    if cover_mode not in {"at-least", "exact"}:
        raise ValueError("cover_mode must be 'at-least' or 'exact'")
    images = tuple(tuple(image) for image in images)
    twists = tuple(tuple(value) for value in twists)
    if _perm_compose(*twists) != _perm_compose(twists[1], twists[0]):
        raise ValueError("torus twists must commute")

    instance, vertices, boundaries = quotient_boundary_data(shape, hnf)
    cnf = CNF()
    placement_vars = tuple(range(1, len(instance.placements) + 1))
    next_var = len(placement_vars) + 1
    potential_vars = {}
    for vertex in vertices:
        variables = []
        for value_index in range(len(S3)):
            potential_vars[(vertex, value_index)] = next_var
            variables.append(next_var)
            next_var += 1
        cnf.append(variables)
        for left, right in itertools.combinations(variables, 2):
            cnf.append([-left, -right])

    _append_cover_clauses(cnf, instance, placement_vars, cover_mode)
    common_clause_count = len(cnf.clauses)

    value_index = {value: index for index, value in enumerate(S3)}
    for placement_var, edges in zip(placement_vars, boundaries):
        for start, start_deck, end, end_deck, letter in edges:
            # Universal developing potentials obey P(end)=P(start)*label,
            # while deck translations act on the left: P(v+l)=H(l)*P(v).
            left_deck = _deck_holonomy(start_deck, twists)
            right_deck_inverse = _perm_inverse(
                _deck_holonomy(end_deck, twists)
            )
            displacement = _perm_compose(right_deck_inverse, left_deck)
            label = _edge_image(letter, images)
            for start_value_index, start_value in enumerate(S3):
                end_value = _perm_compose(
                    _perm_compose(displacement, start_value), label
                )
                cnf.append([
                    -placement_var,
                    -potential_vars[(start, start_value_index)],
                    potential_vars[(end, value_index[end_value])],
                ])

    metadata = {
        "hnf": list(hnf),
        "cover_mode": cover_mode,
        "cells": instance.n_cells,
        "placements": len(instance.placements),
        "vertices": len(vertices),
        "variables": next_var - 1,
        "clauses": len(cnf.clauses),
        "common_clauses": common_clause_count,
    }
    return cnf, metadata


def build_boundary_holonomy_union_cnf(
    shape,
    hnf,
    images,
    cover_mode="at-least",
):
    """Build one CNF whose models choose any commuting S3 twist pair.

    This is logically the disjunction of the 18 per-twist CNFs, with their
    placement and potential variables shared.  Its UNSAT polarity therefore
    certifies every commuting twist in one independently checkable proof.
    """
    twist_pairs = commuting_s3_pairs()
    components = [
        build_boundary_holonomy_cnf(
            shape, hnf, images, twists, cover_mode=cover_mode
        )
        for twists in twist_pairs
    ]
    first_cnf, first_metadata = components[0]
    common_count = first_metadata["common_clauses"]
    common = first_cnf.clauses[:common_count]
    cnf = CNF(from_clauses=common)
    selector_start = first_metadata["variables"] + 1
    selectors = tuple(range(selector_start, selector_start + len(components)))
    cnf.append(list(selectors))
    for left, right in itertools.combinations(selectors, 2):
        cnf.append([-left, -right])
    component_clause_counts = []
    for selector, (component, metadata) in zip(selectors, components):
        if metadata != first_metadata:
            raise AssertionError("twist components do not share metadata")
        if component.clauses[:common_count] != common:
            raise AssertionError("twist components do not share their prefix")
        specific = component.clauses[common_count:]
        component_clause_counts.append(len(specific))
        for clause in specific:
            cnf.append([-selector, *clause])
    metadata = {
        **first_metadata,
        "kind": "commuting-twist-union",
        "twist_pairs": len(twist_pairs),
        "selector_variables": list(selectors),
        "variables": selectors[-1],
        "clauses": len(cnf.clauses),
        "component_specific_clauses": component_clause_counts,
    }
    return cnf, metadata


def _cnf_sha256(cnf):
    digest = sha256()
    for clause in cnf.clauses:
        digest.update(" ".join(map(str, clause)).encode())
        digest.update(b" 0\n")
    return digest.hexdigest()


def scan_boundary_holonomy(
    shape,
    hnf,
    images,
    cover_mode="at-least",
    keep_proofs=False,
    stop_on_sat=False,
):
    """Solve every commuting S3 twist pair for one boundary quotient map."""
    rows = []
    first_model = None
    for twists in commuting_s3_pairs():
        cnf, metadata = build_boundary_holonomy_cnf(
            shape, hnf, images, twists, cover_mode=cover_mode
        )
        with Cadical195(bootstrap_with=cnf, with_proof=keep_proofs) as solver:
            sat = solver.solve()
            stats = solver.accum_stats()
            proof = solver.get_proof() if keep_proofs and not sat else None
            if sat and first_model is None:
                first_model = solver.get_model()
        rows.append({
            "twists": [[*twists[0]], [*twists[1]]],
            "sat": sat,
            "cnf_sha256": _cnf_sha256(cnf),
            "metadata": metadata,
            "conflicts": stats.get("conflicts"),
            "proof": proof,
        })
        if sat and stop_on_sat:
            break
    sat_count = sum(row["sat"] for row in rows)
    return {
        "kind": "binary-coupled-s3-boundary-holonomy-scan",
        "hnf": list(hnf),
        "cover_mode": cover_mode,
        "commuting_twist_pairs": len(commuting_s3_pairs()),
        "twist_pairs_checked": len(rows),
        "sat_twist_pairs": sat_count,
        "unsat_twist_pairs_checked": len(rows) - sat_count,
        "scan_complete": len(rows) == len(commuting_s3_pairs()),
        "verdict": (
            "holonomy-obstructed"
            if sat_count == 0 and len(rows) == len(commuting_s3_pairs())
            else "not-obstructed"
        ),
        "first_model_found": first_model is not None,
        "results": rows,
    }
