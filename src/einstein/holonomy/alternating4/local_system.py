"""The map-7 A4 obstruction as a two-bit local coverability SFT.

For an exact grid-aligned cover the tile-boundary skeleton is connected.  The
C3 coordinate of an A4 developing potential can therefore be normalized to
the geometric character ``chi(x,y)=2x+y mod 3``.  T2.D4 puts both deck twists
in V4.  What remains is a conditional affine system over GF(2)^2:

    v_end = v_deck + v_start + M^chi(start) v_label.

A placement variable asserts these equations on its boundary; at-least cover
requires every quotient cell to belong to an asserted placement.  Thus the
encoder is a four-colour local SFT and is a sound necessary condition for an
exact cover.  It is also the fixed-geometric-C3 factor of the map-7 A4 CNF.
"""

from __future__ import annotations

from pysat.formula import CNF
from pysat.solvers import Cadical195

from einstein.holonomy.alternating4.group import c3_action, canonical_a4_semidirect
from einstein.holonomy.constraints import (
    _append_cover_clauses,
    _cnf_sha256,
    quotient_boundary_data,
)


MAP7 = (1, 2, 1, 0, 3, 8)
V4_TWIST_PAIRS = tuple((left, right) for left in range(4) for right in range(4))


def _signed_coordinate(letter: int, images):
    if not 1 <= abs(letter) <= 6:
        raise ValueError("invalid signed kite-edge letter")
    model = canonical_a4_semidirect()
    element = images[abs(letter) - 1]
    if letter < 0:
        element = model.group.inverses[element]
    return model.coordinate(element)


def _map7_signed_coordinate(letter: int):
    return _signed_coordinate(letter, MAP7)


def _deck_v4(deck, twists) -> int:
    """V4 holonomy of an integral deck coordinate (all elements order two)."""
    return ((twists[0] if deck[0] % 2 else 0)
            ^ (twists[1] if deck[1] % 2 else 0))


def _append_implied_xor(cnf, enabled: int, left: int, right: int, value: int):
    """Append ``enabled -> (right = left XOR value)`` for one bit."""
    if value not in (0, 1):
        raise ValueError("XOR constant must be a bit")
    if value == 0:
        cnf.append([-enabled, -left, right])
        cnf.append([-enabled, left, -right])
    else:
        cnf.append([-enabled, -left, -right])
        cnf.append([-enabled, left, right])


def build_v4_coverability_cnf(
    shape, hnf, images, twists=(0, 0), cover_mode="at-least"
):
    """Build the phase-normalized two-bit factor of a geometric-C3 A4 map.

    ``twists`` are packed V4 coordinates in ``0..3``.  ``at-least`` is the
    local coverability SFT.  ``exact`` adds nonoverlap and remains useful as a
    control, although the relaxation is the theorem-producing polarity.
    """
    images = tuple(images)
    model = canonical_a4_semidirect()
    if len(images) != 6 or any(not 0 <= element < model.group.order for element in images):
        raise ValueError("images must be six canonical A4 element indices")
    coordinates = tuple(model.coordinate(element) for element in images)
    geometric = (1, 2, 1, 0, 0, 0)
    c3_values = tuple(value.q for value in coordinates)
    if c3_values == geometric:
        c3_sign = 1
    elif c3_values == tuple((-value) % 3 for value in geometric):
        c3_sign = -1
    else:
        raise ValueError("A4 map does not project to the geometric C3 character")
    twists = tuple(twists)
    if twists not in V4_TWIST_PAIRS:
        raise ValueError("twists must be an ordered V4 pair")
    if cover_mode not in {"at-least", "exact"}:
        raise ValueError("cover_mode must be 'at-least' or 'exact'")
    instance, vertices, boundaries = quotient_boundary_data(shape, hnf)
    cnf = CNF()
    placement_vars = tuple(range(1, len(instance.placements) + 1))
    next_var = len(placement_vars) + 1
    potential_bits = {}
    for vertex in vertices:
        potential_bits[vertex] = (next_var, next_var + 1)
        next_var += 2
    _append_cover_clauses(cnf, instance, placement_vars, cover_mode)
    cover_clause_count = len(cnf.clauses)

    for placement_var, edges in zip(placement_vars, boundaries):
        for start, start_deck, end, end_deck, letter in edges:
            label = _signed_coordinate(letter, images)
            q_start = (c3_sign * start[0]) % 3
            q_end = (c3_sign * end[0]) % 3
            if q_end != (q_start + label.q) % 3:
                raise AssertionError("geometric C3 character disagrees with edge label")
            displacement = _deck_v4(start_deck, twists) ^ _deck_v4(end_deck, twists)
            constant = displacement ^ c3_action(q_start, label.v)
            start_bits = potential_bits[start]
            end_bits = potential_bits[end]
            for bit in range(2):
                _append_implied_xor(
                    cnf, placement_var, start_bits[bit], end_bits[bit],
                    (constant >> bit) & 1,
                )

    metadata = {
        "kind": "a4-geometric-c3-v4-local-coverability-sft",
        "images": list(images),
        "c3_sign": c3_sign,
        "hnf": list(hnf),
        "cover_mode": cover_mode,
        "twists": list(twists),
        "cells": instance.n_cells,
        "placements": len(instance.placements),
        "vertices": len(vertices),
        "potential_bits": 2 * len(vertices),
        "variables": next_var - 1,
        "clauses": len(cnf.clauses),
        "cover_clauses": cover_clause_count,
    }
    return cnf, metadata


def build_map7_v4_coverability_cnf(shape, hnf, twists=(0, 0), cover_mode="at-least"):
    """Build the map-7 specialization of :func:`build_v4_coverability_cnf`."""
    return build_v4_coverability_cnf(
        shape, hnf, MAP7, twists=twists, cover_mode=cover_mode
    )


def scan_map7_v4_coverability(shape, hnf, cover_mode="at-least", stop_on_sat=True):
    """Scan all 16 exact-cover-relevant V4 deck-twist pairs."""
    rows = []
    for twist_index, twists in enumerate(V4_TWIST_PAIRS):
        cnf, metadata = build_map7_v4_coverability_cnf(
            shape, hnf, twists, cover_mode=cover_mode
        )
        with Cadical195(bootstrap_with=cnf) as solver:
            sat = solver.solve()
            stats = solver.accum_stats()
        rows.append({
            "twist_index": twist_index,
            "twists": list(twists),
            "sat": sat,
            "cnf_sha256": _cnf_sha256(cnf),
            "metadata": metadata,
            "conflicts": stats.get("conflicts"),
        })
        if sat and stop_on_sat:
            break
    complete = len(rows) == len(V4_TWIST_PAIRS)
    sat_count = sum(row["sat"] for row in rows)
    return {
        "kind": "map7-v4-local-coverability-sft-scan",
        "hnf": list(hnf),
        "twist_pairs": len(V4_TWIST_PAIRS),
        "twists_checked": len(rows),
        "sat_twist_pairs": sat_count,
        "scan_complete": complete,
        "verdict": (
            "holonomy-obstructed" if complete and sat_count == 0
            else "not-obstructed"
        ),
        "results": rows,
    }
