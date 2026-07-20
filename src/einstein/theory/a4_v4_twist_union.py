"""Selector union for certifying complete A4/V4 torus-twist scans."""

from __future__ import annotations

from pysat.formula import CNF

from einstein.theory.a4_v4_sft import (
    MAP7,
    V4_TWIST_PAIRS,
    build_v4_coverability_cnf,
)


def build_v4_coverability_union_cnf(
    shape, hnf, images, cover_mode="at-least", twist_pairs=V4_TWIST_PAIRS
):
    """Build the exact disjunction of several V4-twist component CNFs.

    Components share placement and potential variables. A fresh selector
    activates each component's boundary implications, while cover clauses
    remain unconditional. At least one selector must be true; at-most-one is
    unnecessary. Thus one UNSAT proof certifies the complete twist scan.
    """
    twist_pairs = tuple(tuple(pair) for pair in twist_pairs)
    if not twist_pairs or any(pair not in V4_TWIST_PAIRS for pair in twist_pairs):
        raise ValueError("twist_pairs must be a nonempty V4-twist sequence")
    first, first_metadata = build_v4_coverability_cnf(
        shape, hnf, images, twists=twist_pairs[0], cover_mode=cover_mode
    )
    common_count = first_metadata["cover_clauses"]
    common = first.clauses[:common_count]
    cnf = CNF(from_clauses=common)
    selectors = tuple(
        range(first_metadata["variables"] + 1,
              first_metadata["variables"] + len(twist_pairs) + 1)
    )
    cnf.append(list(selectors))
    component_clause_counts = []
    for component_index, (selector, twists) in enumerate(zip(selectors, twist_pairs)):
        if component_index == 0:
            component, metadata = first, first_metadata
        else:
            component, metadata = build_v4_coverability_cnf(
                shape, hnf, images, twists=twists, cover_mode=cover_mode
            )
        if (metadata["cover_clauses"] != common_count
                or component.clauses[:common_count] != common
                or metadata["variables"] != first_metadata["variables"]):
            raise AssertionError("V4 twist components do not share a common prefix")
        suffix = component.clauses[common_count:]
        component_clause_counts.append(len(suffix))
        for clause in suffix:
            cnf.append([-selector, *clause])
    metadata = {
        "kind": "a4-geometric-c3-v4-local-coverability-twist-union",
        "images": list(images),
        "hnf": list(hnf),
        "cover_mode": cover_mode,
        "twist_pairs": [list(pair) for pair in twist_pairs],
        "twist_components": len(twist_pairs),
        "selectors": list(selectors),
        "cells": first_metadata["cells"],
        "placements": first_metadata["placements"],
        "vertices": first_metadata["vertices"],
        "potential_bits": first_metadata["potential_bits"],
        "common_clauses": common_count,
        "component_clause_counts": component_clause_counts,
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
    }
    return cnf, metadata


def build_map7_v4_coverability_union_cnf(
    shape, hnf, cover_mode="at-least", twist_pairs=V4_TWIST_PAIRS
):
    """Map-7 specialization of the exact V4-twist union."""
    return build_v4_coverability_union_cnf(
        shape, hnf, MAP7, cover_mode=cover_mode, twist_pairs=twist_pairs
    )
