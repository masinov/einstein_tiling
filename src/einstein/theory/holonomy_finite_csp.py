"""Generic finite-group form of the binary-coupled Layer-D torus CSP."""

from __future__ import annotations

import itertools

from pysat.formula import CNF
from pysat.solvers import Cadical195

from einstein.theory.holonomy_csp import (
    _append_cover_clauses,
    _cnf_sha256,
    quotient_boundary_data,
)


def commuting_pairs(group):
    return tuple(
        (left, right)
        for left in range(group.order) for right in range(group.order)
        if group.multiplication[left][right] == group.multiplication[right][left]
    )


def _power(value, exponent, group):
    if exponent < 0:
        value = group.inverses[value]
        exponent = -exponent
    out = group.identity
    for _ in range(exponent):
        out = group.multiplication[out][value]
    return out


def _deck_holonomy(deck, twists, group):
    return group.multiplication[
        _power(twists[0], deck[0], group)
    ][_power(twists[1], deck[1], group)]


def build_finite_boundary_holonomy_cnf(
    shape, hnf, images, twists, group, cover_mode="at-least"
):
    """Build the T2.D2 CSP for one exact finite target and twist pair."""
    if cover_mode not in {"at-least", "exact"}:
        raise ValueError("cover_mode must be 'at-least' or 'exact'")
    images = tuple(images)
    twists = tuple(twists)
    if len(images) != 6 or any(not 0 <= value < group.order for value in images):
        raise ValueError("invalid generator images")
    if twists not in commuting_pairs(group):
        raise ValueError("torus twists must commute")

    instance, vertices, boundaries = quotient_boundary_data(shape, hnf)
    cnf = CNF()
    placement_vars = tuple(range(1, len(instance.placements) + 1))
    next_var = len(placement_vars) + 1
    potential_vars = {}
    for vertex in vertices:
        variables = []
        for value in range(group.order):
            potential_vars[(vertex, value)] = next_var
            variables.append(next_var)
            next_var += 1
        cnf.append(variables)
        for left, right in itertools.combinations(variables, 2):
            cnf.append([-left, -right])
    _append_cover_clauses(cnf, instance, placement_vars, cover_mode)
    common_clause_count = len(cnf.clauses)

    for placement_var, edges in zip(placement_vars, boundaries):
        for start, start_deck, end, end_deck, letter in edges:
            left_deck = _deck_holonomy(start_deck, twists, group)
            right_deck_inverse = group.inverses[
                _deck_holonomy(end_deck, twists, group)
            ]
            displacement = group.multiplication[right_deck_inverse][left_deck]
            label = images[abs(letter) - 1]
            if letter < 0:
                label = group.inverses[label]
            for start_value in range(group.order):
                end_value = group.multiplication[
                    group.multiplication[displacement][start_value]
                ][label]
                cnf.append([
                    -placement_var,
                    -potential_vars[(start, start_value)],
                    potential_vars[(end, end_value)],
                ])
    metadata = {
        "target": group.name,
        "target_order": group.order,
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


def build_finite_boundary_holonomy_union_cnf(
    shape, hnf, images, group, cover_mode="at-least"
):
    """One selector CNF representing the disjunction of all commuting twists."""
    pairs = commuting_pairs(group)
    components = [
        build_finite_boundary_holonomy_cnf(
            shape, hnf, images, twists, group, cover_mode=cover_mode
        )
        for twists in pairs
    ]
    first, first_metadata = components[0]
    common_count = first_metadata["common_clauses"]
    common = first.clauses[:common_count]
    cnf = CNF(from_clauses=common)
    selector_start = first_metadata["variables"] + 1
    selectors = tuple(range(selector_start, selector_start + len(pairs)))
    cnf.append(list(selectors))
    for left, right in itertools.combinations(selectors, 2):
        cnf.append([-left, -right])
    component_specific_clauses = []
    for selector, (component, metadata) in zip(selectors, components):
        if metadata != first_metadata or component.clauses[:common_count] != common:
            raise AssertionError("twist components do not share a common prefix")
        specific = component.clauses[common_count:]
        component_specific_clauses.append(len(specific))
        for clause in specific:
            cnf.append([-selector, *clause])
    metadata = {
        **first_metadata,
        "kind": "finite-commuting-twist-union",
        "twist_pairs": len(pairs),
        "selector_variables": list(selectors),
        "variables": selectors[-1],
        "clauses": len(cnf.clauses),
        "component_specific_clauses": component_specific_clauses,
    }
    return cnf, metadata


def scan_finite_boundary_holonomy(
    shape, hnf, images, group, cover_mode="at-least", stop_on_sat=True
):
    pairs = commuting_pairs(group)
    rows = []
    for twists in pairs:
        cnf, metadata = build_finite_boundary_holonomy_cnf(
            shape, hnf, images, twists, group, cover_mode=cover_mode
        )
        with Cadical195(bootstrap_with=cnf) as solver:
            sat = solver.solve()
            stats = solver.accum_stats()
        rows.append({
            "twists": list(twists),
            "sat": sat,
            "cnf_sha256": _cnf_sha256(cnf),
            "metadata": metadata,
            "conflicts": stats.get("conflicts"),
        })
        if sat and stop_on_sat:
            break
    sat_count = sum(row["sat"] for row in rows)
    complete = len(rows) == len(pairs)
    return {
        "kind": "binary-coupled-finite-boundary-holonomy-scan",
        "target": group.name,
        "hnf": list(hnf),
        "commuting_twist_pairs": len(pairs),
        "twist_pairs_checked": len(rows),
        "sat_twist_pairs": sat_count,
        "scan_complete": complete,
        "verdict": (
            "holonomy-obstructed" if complete and sat_count == 0
            else "not-obstructed"
        ),
        "results": rows,
    }


def solve_finite_boundary_holonomy_union(
    shape, hnf, images, group, cover_mode="at-least"
):
    """Solve the all-twist disjunction in one learning-sharing CNF."""
    cnf, metadata = build_finite_boundary_holonomy_union_cnf(
        shape, hnf, images, group, cover_mode=cover_mode
    )
    with Cadical195(bootstrap_with=cnf) as solver:
        sat = solver.solve()
        stats = solver.accum_stats()
    return {
        "kind": "binary-coupled-finite-boundary-holonomy-union",
        "target": group.name,
        "hnf": list(hnf),
        "sat": sat,
        "verdict": "not-obstructed" if sat else "holonomy-obstructed",
        "cnf_sha256": _cnf_sha256(cnf),
        "metadata": metadata,
        "conflicts": stats.get("conflicts"),
    }


def solve_finite_boundary_holonomy_incremental(
    shape, hnf, images, group, cover_mode="at-least", start_twist=0
):
    """Share learning while fixing each union selector in turn."""
    cnf, metadata = build_finite_boundary_holonomy_union_cnf(
        shape, hnf, images, group, cover_mode=cover_mode
    )
    selectors = metadata["selector_variables"]
    sat_twist_index = None
    with Cadical195(bootstrap_with=cnf) as solver:
        for twist_index in range(start_twist, len(selectors)):
            selector = selectors[twist_index]
            if solver.solve(assumptions=[selector]):
                sat_twist_index = twist_index
                break
        stats = solver.accum_stats()
    sat = sat_twist_index is not None
    return {
        "kind": "binary-coupled-finite-boundary-holonomy-incremental",
        "target": group.name,
        "hnf": list(hnf),
        "sat": sat,
        "sat_twist_index": sat_twist_index,
        "twists_checked": (
            sat_twist_index - start_twist + 1 if sat
            else len(selectors) - start_twist
        ),
        "start_twist": start_twist,
        "verdict": "not-obstructed" if sat else "holonomy-obstructed",
        "cnf_sha256": _cnf_sha256(cnf),
        "metadata": metadata,
        "conflicts": stats.get("conflicts"),
    }


def solve_finite_boundary_holonomy_hybrid(
    shape, hnf, images, group, cover_mode="at-least"
):
    """Try the identity twist cheaply, otherwise solve the all-twist union."""
    identity_twists = (group.identity, group.identity)
    cnf, metadata = build_finite_boundary_holonomy_cnf(
        shape, hnf, images, identity_twists, group, cover_mode=cover_mode
    )
    with Cadical195(bootstrap_with=cnf) as solver:
        sat = solver.solve()
        stats = solver.accum_stats()
    if sat:
        return {
            "kind": "binary-coupled-finite-boundary-holonomy-hybrid",
            "target": group.name,
            "hnf": list(hnf),
            "mode": "identity-twist-shortcut",
            "sat": True,
            "verdict": "not-obstructed",
            "cnf_sha256": _cnf_sha256(cnf),
            "metadata": metadata,
            "conflicts": stats.get("conflicts"),
        }
    result = solve_finite_boundary_holonomy_incremental(
        shape, hnf, images, group, cover_mode=cover_mode, start_twist=1
    )
    return {**result, "mode": "incremental-selector-scan"}
