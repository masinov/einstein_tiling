"""Bounded-overlap relaxations between Layer D and ordinary exact cover."""

from __future__ import annotations

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

from einstein.holonomy.constraints import (
    _cnf_sha256,
    build_boundary_holonomy_cnf,
    commuting_s3_pairs,
    quotient_boundary_data,
)


def build_bounded_overlap_holonomy_cnf(
    shape, hnf, images, twists, maximum_coverage=2
):
    """Require every quotient cell to be covered between 1 and ``q`` times."""
    if maximum_coverage < 1:
        raise ValueError("maximum coverage must be positive")
    cnf, metadata = build_boundary_holonomy_cnf(
        shape, hnf, images, twists, cover_mode="at-least"
    )
    instance, _, _ = quotient_boundary_data(shape, hnf)
    by_cell = [[] for _ in range(instance.n_cells)]
    for variable, (_, mask) in enumerate(instance.placements, 1):
        for cell in range(instance.n_cells):
            if (mask >> cell) & 1:
                by_cell[cell].append(variable)
    added_clauses = 0
    for variables in by_cell:
        if len(variables) <= maximum_coverage:
            continue
        cardinality = CardEnc.atmost(
            lits=variables,
            bound=maximum_coverage,
            top_id=cnf.nv,
            encoding=EncType.seqcounter,
        )
        cnf.extend(cardinality.clauses)
        added_clauses += len(cardinality.clauses)
    metadata = {
        **metadata,
        "cover_mode": "bounded-overlap",
        "maximum_coverage": maximum_coverage,
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "bounded_overlap_clauses": added_clauses,
    }
    return cnf, metadata


def scan_bounded_overlap_holonomy(
    shape, hnf, images, maximum_coverage=2, stop_on_sat=True
):
    """Scan commuting twists under a sound bounded-overlap relaxation."""
    rows = []
    for twists in commuting_s3_pairs():
        cnf, metadata = build_bounded_overlap_holonomy_cnf(
            shape, hnf, images, twists,
            maximum_coverage=maximum_coverage,
        )
        with Cadical195(bootstrap_with=cnf) as solver:
            sat = solver.solve()
            stats = solver.accum_stats()
        rows.append({
            "twists": [list(twists[0]), list(twists[1])],
            "sat": sat,
            "cnf_sha256": _cnf_sha256(cnf),
            "metadata": metadata,
            "conflicts": stats.get("conflicts"),
        })
        if sat and stop_on_sat:
            break
    sat_count = sum(row["sat"] for row in rows)
    complete = len(rows) == len(commuting_s3_pairs())
    return {
        "kind": "binary-coupled-s3-bounded-overlap-scan",
        "hnf": list(hnf),
        "maximum_coverage": maximum_coverage,
        "twist_pairs_checked": len(rows),
        "sat_twist_pairs": sat_count,
        "scan_complete": complete,
        "verdict": (
            "holonomy-obstructed" if complete and sat_count == 0
            else "not-obstructed"
        ),
        "results": rows,
    }
