"""Exact D6 covariance for Layer-D boundary quotients.

The finite-group obstruction is geometric: rotating or reflecting both the
torus period lattice and the six edge labels cannot change satisfiability.
This module makes that action explicit without changing the proof-producing
Layer-D implementation whose hashes are recorded in the experiment assets.
"""

from __future__ import annotations

from einstein.geometry.kite_grid import N_OPS, transform_point
from einstein.periodicity.binary_families import (
    _apply_action,
    _same_index_sublattice,
    lattice_action,
)
from einstein.holonomy.boundary import (
    KITE_EDGE_GENERATORS,
    S3,
    _conjugate_s3_images,
    _perm_inverse,
)


_SIGNED_EDGE = {
    vector: index + 1
    for index, vector in enumerate(KITE_EDGE_GENERATORS)
} | {
    (-vector[0], -vector[1]): -(index + 1)
    for index, vector in enumerate(KITE_EDGE_GENERATORS)
}


def inverse_d6_operation(op: int) -> int:
    """Inverse in the kite-grid convention ``rotation^k after mirror``."""
    if not 0 <= op < N_OPS:
        raise ValueError("D6 operation must be in range(12)")
    return (-op) % 6 if op < 6 else op


def signed_edge_action(op: int) -> tuple[int, ...]:
    """Images of the six positive edge generators under one D6 operation."""
    if not 0 <= op < N_OPS:
        raise ValueError("D6 operation must be in range(12)")
    return tuple(
        _SIGNED_EDGE[transform_point(vector, op)]
        for vector in KITE_EDGE_GENERATORS
    )


def canonical_s3_images(images):
    """Canonical representative of an S3 map modulo inner conjugacy."""
    images = tuple(tuple(image) for image in images)
    return min(_conjugate_s3_images(images, conjugator) for conjugator in S3)


def transform_s3_images(images, op: int):
    """Precompose a six-generator map with the geometric edge action."""
    images = tuple(tuple(image) for image in images)
    out = []
    for letter in signed_edge_action(op):
        image = images[abs(letter) - 1]
        out.append(image if letter > 0 else _perm_inverse(image))
    return tuple(out)


def pullback_s3_images(images, op: int):
    """Map transported contravariantly when the geometry is moved by ``op``."""
    return canonical_s3_images(
        transform_s3_images(images, inverse_d6_operation(op))
    )


def hnf_d6_image(hnf, op: int) -> tuple[int, int, int]:
    """Canonical HNF of a full-rank period lattice after a D6 operation."""
    a, b, d = map(int, hnf)
    if a <= 0 or d <= 0 or not 0 <= b < a:
        raise ValueError("invalid HNF")
    action = lattice_action(op)
    generators = (
        _apply_action(action, (a, 0)),
        _apply_action(action, (b, d)),
    )
    index = a * d
    matches = []
    for target_a in range(1, index + 1):
        if index % target_a:
            continue
        target_d = index // target_a
        for target_b in range(target_a):
            target = (target_a, target_b, target_d)
            if _same_index_sublattice(generators, target):
                matches.append(target)
    if len(matches) != 1:
        raise AssertionError(f"D6 image has {len(matches)} HNF representatives")
    return matches[0]


def orbit(values, action):
    """Return sorted finite orbits under the twelve supplied D6 actions."""
    remaining = set(values)
    out = []
    while remaining:
        seed = min(remaining)
        current = frozenset(action(seed, op) for op in range(N_OPS))
        if not current <= remaining:
            raise AssertionError("action does not preserve the supplied set")
        remaining.difference_update(current)
        out.append(tuple(sorted(current)))
    return tuple(out)
