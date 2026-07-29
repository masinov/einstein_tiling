"""Independent verifier for W1 cycle-free transfer certificates.

This module intentionally does not call :class:`CylinderTransfer` or its state
and transition enumerators.  It recompiles placement masks from exact geometry,
re-enumerates crossing-state unions, reconstructs all exact-cover transitions,
and validates the supplied topological order and graph hash.
"""

from __future__ import annotations

from hashlib import sha256
import json
import math

from einstein.polykites.periodic_quotients import cell_to_lattice
from einstein.geometry.kite_grid import N_OPS, transform_cell


def _basis(vector):
    x, y = vector
    g = math.gcd(abs(x), abs(y))
    if not g:
        raise ValueError("zero period vector")
    p = (x // g, y // g)
    # Independent extended-Euclid implementation.
    def egcd(a, b):
        if b == 0:
            return abs(a), (1 if a >= 0 else -1), 0
        q, r = divmod(a, b)
        d, s, t = egcd(b, r)
        return d, t, s - q * t

    d, a, b = egcd(p[0], p[1])
    if d != 1:
        raise ValueError("primitive decomposition failed")
    u = (-b, a)
    if p[0] * u[1] - p[1] * u[0] != 1:
        raise ValueError("invalid transverse basis")
    return p, g, u


def _coordinates(q, p, u):
    return q[0] * u[1] - q[1] * u[0], p[0] * q[1] - p[1] * q[0]


def _compile_patterns(shape, vector):
    p, g, u = _basis(vector)
    raw = []
    span = 0
    for op in range(N_OPS):
        cells = []
        for cell in shape:
            x, y, sector = cell_to_lattice(transform_cell(cell, op))
            alpha, beta = _coordinates((x, y), p, u)
            cells.append((alpha, beta, sector))
        lo = min(beta for _, beta, _ in cells)
        hi = max(beta for _, beta, _ in cells)
        span = max(span, hi - lo)
        for shift in range(g):
            quotient = {
                (beta - lo, ((alpha + shift) % g) * 6 + sector)
                for alpha, beta, sector in cells
            }
            if len(quotient) == len(cells):
                raw.append((op, shift, lo, quotient))
    patterns = {}
    for op, shift, lo, cells in raw:
        masks = [0] * (span + 1)
        for layer, bit in cells:
            masks[layer] |= 1 << bit
        key = tuple(masks)
        patterns.setdefault(key, (op, shift, lo, key))
    return p, g, u, span, tuple(patterns[key] for key in sorted(patterns))


def _contributions(patterns, span):
    found = set()
    for _, _, _, masks in patterns:
        last = max(i for i, mask in enumerate(masks) if mask)
        for age in range(1, span + 1):
            if last >= age:
                contribution = tuple(
                    masks[layer + age] if layer + age < len(masks) else 0
                    for layer in range(span)
                )
                if any(contribution):
                    found.add(contribution)
    return tuple(sorted(found))


def _states(contributions, span):
    states = {(0,) * span}
    for contribution in contributions:
        additions = set()
        for state in states:
            if all(not (a & b) for a, b in zip(state, contribution)):
                additions.add(tuple(a | b for a, b in zip(state, contribution)))
        states |= additions
    return tuple(sorted(states))


def _targets(state, patterns, layer_size, state_set):
    """Independently enumerate all legal successor states.

    This verifier branches over the globally ordered placement list and prunes
    by the first uncovered current-layer cell; it records target sets only,
    while the producer records one placement witness per target.
    """
    full = (1 << layer_size) - 1
    occupied = list(state) + [0]
    by_bit = [[] for _ in range(layer_size)]
    for index, (_, _, _, masks) in enumerate(patterns):
        for bit in range(layer_size):
            if masks[0] & (1 << bit):
                by_bit[bit].append(index)
    targets = set()

    def visit():
        missing = full & ~occupied[0]
        if not missing:
            target = tuple(occupied[1:])
            if target in state_set:
                targets.add(target)
            return
        bit = (missing & -missing).bit_length() - 1
        for index in by_bit[bit]:
            masks = patterns[index][3]
            if any(a & b for a, b in zip(occupied, masks)):
                continue
            for layer, mask in enumerate(masks):
                occupied[layer] += mask
            visit()
            for layer, mask in enumerate(masks):
                occupied[layer] -= mask

    visit()
    return targets


def _graph_hash(states, adjacency, witnesses):
    serial = [
        [
            list(state),
            [
                [list(target), list(witnesses[(state, target)])]
                for target in sorted(adjacency[state])
            ],
        ]
        for state in states
    ]
    return sha256(json.dumps(serial, separators=(",", ":")).encode()).hexdigest()


def check_cycle_free_manifest(manifest: dict) -> None:
    """Raise ``ValueError`` unless ``manifest`` is a complete valid proof."""
    if manifest.get("kind") != "cylinder-cycle-free-certificate":
        raise ValueError("wrong certificate kind")
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported schema version")
    shape = tuple(tuple(cell) for cell in manifest["shape"])
    vector = tuple(manifest["vector"])
    p, g, u, span, patterns = _compile_patterns(shape, vector)
    basis = manifest["basis"]
    if (list(p), g, list(u)) != (
        basis["primitive"], basis["multiplicity"], basis["transverse"]
    ):
        raise ValueError("basis metadata mismatch")
    if manifest["layer_size"] != 6 * g or manifest["interaction_span"] != span:
        raise ValueError("layer/span metadata mismatch")
    recorded_patterns = tuple(
        (row["op"], row["alpha"], row["min_beta"], tuple(row["masks"]))
        for row in manifest["patterns"]
    )
    if recorded_patterns != patterns:
        raise ValueError("placement pattern enumeration is incomplete or altered")
    contributions = _contributions(patterns, span)
    if tuple(tuple(row) for row in manifest["crossing_contributions"]) != contributions:
        raise ValueError("crossing contribution enumeration mismatch")
    states = _states(contributions, span)
    recorded_states = tuple(tuple(row) for row in manifest["states"])
    if recorded_states != states:
        raise ValueError("state enumeration is incomplete or altered")

    adjacency = {state: set() for state in states}
    witnesses = {}
    for row in manifest["edges"]:
        try:
            source = states[row["source"]]
            target = states[row["target"]]
        except (IndexError, TypeError):
            raise ValueError("edge references an invalid state") from None
        key = (source, target)
        if key in witnesses:
            raise ValueError("duplicate graph edge")
        selected = tuple(row["patterns"])
        occupied = list(source) + [0]
        for index in selected:
            if not 0 <= index < len(patterns):
                raise ValueError("edge references an invalid pattern")
            masks = patterns[index][3]
            if any(a & b for a, b in zip(occupied, masks)):
                raise ValueError("edge witness overlaps")
            for layer, mask in enumerate(masks):
                occupied[layer] |= mask
        if occupied[0] != (1 << (6 * g)) - 1 or tuple(occupied[1:]) != target:
            raise ValueError("edge witness does not produce claimed transition")
        adjacency[source].add(target)
        witnesses[key] = selected

    state_set = set(states)
    for state in states:
        if adjacency[state] != _targets(state, patterns, 6 * g, state_set):
            raise ValueError("transition relation is incomplete or altered")

    order = manifest["topological_order"]
    if sorted(order) != list(range(len(states))):
        raise ValueError("topological order is not a state permutation")
    position = {state_index: rank for rank, state_index in enumerate(order)}
    for row in manifest["edges"]:
        if position[row["source"]] >= position[row["target"]]:
            raise ValueError("topological order does not prove acyclicity")
    counts = manifest["counts"]
    expected_counts = {
        "patterns": len(patterns),
        "crossing_contributions": len(contributions),
        "states": len(states),
        "edges": len(manifest["edges"]),
    }
    if counts != expected_counts:
        raise ValueError("certificate counts mismatch")
    if manifest["graph_sha256"] != _graph_hash(states, adjacency, witnesses):
        raise ValueError("graph hash mismatch")


def verify_cycle_free_manifest(manifest: dict) -> bool:
    try:
        check_cycle_free_manifest(manifest)
    except (KeyError, TypeError, ValueError):
        return False
    return True
