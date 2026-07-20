"""Products of geometric-C3 A4/V4 local coverability invariants."""

from __future__ import annotations

from pysat.formula import CNF

from einstein.theory.a4_semidirect import c3_action, canonical_a4_semidirect
from einstein.theory.a4_v4_sft import (
    V4_TWIST_PAIRS,
    _append_implied_xor,
    _deck_v4,
    _signed_coordinate,
)
from einstein.theory.a4_v4_lift import lift_2lambda_witness
from einstein.theory.holonomy_csp import _append_cover_clauses, quotient_boundary_data


def _layer_data(images, twists):
    images = tuple(images)
    twists = tuple(twists)
    model = canonical_a4_semidirect()
    if len(images) != 6 or any(not 0 <= element < model.group.order for element in images):
        raise ValueError("images must be six canonical A4 element indices")
    if twists not in V4_TWIST_PAIRS:
        raise ValueError("twists must be an ordered V4 pair")
    geometric = (1, 2, 1, 0, 0, 0)
    c3_values = tuple(model.coordinate(element).q for element in images)
    if c3_values == geometric:
        sign = 1
    elif c3_values == tuple((-value) % 3 for value in geometric):
        sign = -1
    else:
        raise ValueError("A4 map does not project to the geometric C3 character")
    return images, twists, sign


def build_v4_product_coverability_cnf(shape, hnf, layers, cover_mode="at-least"):
    """Build several V4 potential layers coupled to one placement cover."""
    layers = tuple(_layer_data(images, twists) for images, twists in layers)
    if not layers:
        raise ValueError("at least one V4 layer is required")
    if cover_mode not in {"at-least", "exact"}:
        raise ValueError("cover_mode must be 'at-least' or 'exact'")
    instance, vertices, boundaries = quotient_boundary_data(shape, hnf)
    cnf = CNF()
    placement_vars = tuple(range(1, len(instance.placements) + 1))
    next_var = len(placement_vars) + 1
    layer_bits = []
    for _ in layers:
        bits = {}
        for vertex in vertices:
            bits[vertex] = (next_var, next_var + 1)
            next_var += 2
        layer_bits.append(bits)
    _append_cover_clauses(cnf, instance, placement_vars, cover_mode)
    cover_clause_count = len(cnf.clauses)

    for placement_var, edges in zip(placement_vars, boundaries):
        for start, start_deck, end, end_deck, letter in edges:
            for (images, twists, sign), potential_bits in zip(layers, layer_bits):
                label = _signed_coordinate(letter, images)
                q_start = (sign * start[0]) % 3
                q_end = (sign * end[0]) % 3
                if q_end != (q_start + label.q) % 3:
                    raise AssertionError("geometric C3 character disagrees with edge label")
                displacement = _deck_v4(start_deck, twists) ^ _deck_v4(end_deck, twists)
                constant = displacement ^ c3_action(q_start, label.v)
                for bit in range(2):
                    _append_implied_xor(
                        cnf, placement_var,
                        potential_bits[start][bit], potential_bits[end][bit],
                        (constant >> bit) & 1,
                    )
    metadata = {
        "kind": "a4-v4-product-local-coverability-sft",
        "hnf": list(hnf),
        "cover_mode": cover_mode,
        "layers": [
            {"images": list(images), "twists": list(twists), "c3_sign": sign}
            for images, twists, sign in layers
        ],
        "cells": instance.n_cells,
        "placements": len(instance.placements),
        "vertices": len(vertices),
        "potential_bits": 2 * len(vertices) * len(layers),
        "variables": next_var - 1,
        "clauses": len(cnf.clauses),
        "cover_clauses": cover_clause_count,
    }
    return cnf, metadata


def semantic_product_witness(shape, model, n_layers):
    """Decode one base-HNF product model into shared placements and layer colors."""
    instance, vertices, _ = quotient_boundary_data(shape, (2, 0, 2))
    truth = {abs(literal): literal > 0 for literal in model}
    n_placements = len(instance.placements)
    selected = tuple(sorted(
        (op, tu % 2, tv % 2)
        for variable, ((op, tu, tv), _) in enumerate(instance.placements, 1)
        if truth[variable]
    ))
    layer_colors = []
    for layer in range(n_layers):
        offset = n_placements + layer * 2 * len(vertices)
        layer_colors.append(tuple(
            (vertex, int(truth[offset + 2 * index + 1])
             | (int(truth[offset + 2 * index + 2]) << 1))
            for index, vertex in enumerate(vertices)
        ))
    return selected, tuple(layer_colors)


def lift_product_witness(shape, hnf, base_twists, selected, layer_colors):
    """Pull back a shared-placement product witness from the 2-Lambda base."""
    instance, vertices, _ = quotient_boundary_data(shape, tuple(hnf))
    n_placements = len(instance.placements)
    values = {}
    induced_layers = []
    for layer, (twists, colors) in enumerate(zip(base_twists, layer_colors)):
        induced, single = lift_2lambda_witness(
            shape, hnf, twists, selected, colors
        )
        induced_layers.append(induced)
        if layer == 0:
            values.update({
                variable: single[variable]
                for variable in range(1, n_placements + 1)
            })
        single_offset = n_placements
        product_offset = n_placements + layer * 2 * len(vertices)
        for index in range(2 * len(vertices)):
            values[product_offset + index + 1] = single[single_offset + index + 1]
    return tuple(induced_layers), values
