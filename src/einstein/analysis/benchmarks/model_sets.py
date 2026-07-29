"""Canonical projection references for the wider E4 diffraction gate.

Penrose vertices are obtained from Z^5 with five physical star vectors at
72-degree increments; the acceptance window is the projection of the
centered 5-cube into the three-dimensional internal space.  Ammann--Beenker
vertices are obtained analogously from Z^4 with four star vectors at
45-degree increments and a regular-octagon internal window.

The integer lattice identities are exact.  Cartesian/internal projections
and convex-window membership are numerical because these point sets exist
only as A4 calibration inputs (D-0010), never as search certificates.

Primary construction anchors:
  - Ammann--Beenker as a 4D cubic cut-and-project set:
    https://arxiv.org/abs/2103.08678
  - regular model sets and pure-point diffraction:
    https://arxiv.org/abs/1904.08285
"""

from __future__ import annotations

import itertools
import math
import random

import numpy as np


_SHIFTS = {
    "penrose": np.array([0.113, 0.184, 0.255, 0.326, 0.397]),
    "ammann-beenker": np.array([0.113, 0.184, 0.255, 0.326]),
}


def _cross2(o, a, b):
    return ((a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0]))


def _convex_hull_2d(points):
    pts = points[np.lexsort((points[:, 1], points[:, 0]))]
    lower = []
    for p in pts:
        while len(lower) >= 2 and _cross2(lower[-2], lower[-1], p) <= 1e-10:
            lower.pop()
        lower.append(p)
    upper = []
    for p in pts[::-1]:
        while len(upper) >= 2 and _cross2(upper[-2], upper[-1], p) <= 1e-10:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1])


def _halfspaces_2d(vertices):
    hull = _convex_hull_2d(vertices)
    normals = []
    offsets = []
    for p, q in zip(hull, np.roll(hull, -1, axis=0)):
        edge = q - p
        normal = np.array([edge[1], -edge[0]])
        normal /= np.linalg.norm(normal)
        normals.append(normal)
        offsets.append(normal @ p)
    return np.array(normals), np.array(offsets), len(hull)


def _halfspaces_3d(vertices):
    """Supporting planes of a small 3D convex hull (32 input vertices)."""
    facets: list[tuple[np.ndarray, float]] = []
    for a, b, c in itertools.combinations(range(len(vertices)), 3):
        p, q, r = vertices[a], vertices[b], vertices[c]
        normal = np.cross(q - p, r - p)
        norm = np.linalg.norm(normal)
        if norm < 1e-10:
            continue
        normal /= norm
        offset = float(normal @ p)
        side = vertices @ normal - offset
        if not (np.all(side <= 1e-9) or np.all(side >= -1e-9)):
            continue
        if np.all(side >= -1e-9):
            normal = -normal
            offset = -offset
        if any(normal @ old_n > 1.0 - 1e-8 and abs(offset - old_d) < 1e-8
               for old_n, old_d in facets):
            continue
        facets.append((normal, offset))
    return (np.array([n for n, _ in facets]),
            np.array([d for _, d in facets]), len(facets))


def _projection_data(kind):
    if kind == "penrose":
        n = 5
        angles = np.arange(n) * (2.0 * math.pi / 5.0)
    elif kind == "ammann-beenker":
        n = 4
        angles = np.arange(n) * (math.pi / 4.0)
    else:
        raise ValueError(f"unknown model set: {kind}")

    # Normalize so stacking physical and internal rows is orthogonal.
    physical = np.stack([np.cos(angles), np.sin(angles)]) * math.sqrt(2.0 / n)
    _, _, vh = np.linalg.svd(physical)
    internal = vh[2:]
    cube = np.array(list(itertools.product((-0.5, 0.5), repeat=n)))
    window_vertices = cube @ internal.T
    if internal.shape[0] == 2:
        normals, offsets, faces = _halfspaces_2d(window_vertices)
    else:
        normals, offsets, faces = _halfspaces_3d(window_vertices)
    return physical, internal, normals, offsets, window_vertices, faces


def model_set_metadata(kind):
    """Construction invariants used by tests and the E4 audit log."""
    physical, internal, _, _, window_vertices, faces = _projection_data(kind)
    return {
        "ambient_rank": physical.shape[1],
        "internal_dimension": internal.shape[0],
        "window_vertices": len({
            tuple(np.round(v, 10)) for v in window_vertices
        }),
        "window_facets": faces,
    }


def model_set_points(kind, bound: int, batch_size: int = 200_000):
    """Return a complete centered disk patch of a canonical model set.

    We enumerate integer identities in [-bound,bound]^n, accept those whose
    shifted internal projection lies in the projected-cube window, then clip
    to a disk that is provably inside the coefficient-box completeness radius.
    """
    physical, internal, normals, offsets, window_vertices, _ = (
        _projection_data(kind)
    )
    n = physical.shape[1]
    shift = _SHIFTS[kind]
    accepted = []
    batch = []

    def flush():
        if not batch:
            return
        z = np.asarray(batch, dtype=np.float64)
        internal_points = (z + shift) @ internal.T
        keep = np.all(internal_points @ normals.T <= offsets + 1e-9, axis=1)
        accepted.append(z[keep] @ physical.T)
        batch.clear()

    for identity in itertools.product(range(-bound, bound + 1), repeat=n):
        batch.append(identity)
        if len(batch) >= batch_size:
            flush()
    flush()

    points = np.concatenate(accepted)
    # Penrose has the integer relation sum(star vectors)=0; deduplicate the
    # rare coincident projections without erasing genuine close neighbors.
    unique = {tuple(np.round(p, 10)): p for p in points}
    points = np.array(list(unique.values()))

    window_radius = float(np.linalg.norm(window_vertices, axis=1).max())
    shift_radius = float(np.linalg.norm(internal @ shift))
    complete_radius = math.sqrt(
        max(0.0, (bound + 1) ** 2 - (window_radius + shift_radius) ** 2)
    )
    radius = 0.98 * complete_radius
    return points[np.linalg.norm(points, axis=1) <= radius]


def penrose_points(bound: int = 11):
    return model_set_points("penrose", bound)


def ammann_beenker_points(bound: int = 18):
    return model_set_points("ammann-beenker", bound)


def transform_points(points, angle: float = 0.0, shear: float = 0.0,
                     scale: float = 1.0):
    """Apply an invertible rotation/shear/scale for E4 covariance checks."""
    c, s = math.cos(angle), math.sin(angle)
    rotation = np.array([[c, -s], [s, c]])
    shear_matrix = np.array([[1.0, shear], [0.0, 1.0]])
    return np.asarray(points) @ (scale * rotation @ shear_matrix).T


def random_periodic_points(seed: int, radius: float = 13.0):
    """A random Bravais-lattice parallelogram tiling, represented by anchors.

    Rotation, aspect ratio, shear, scale and origin phase vary independently.
    Every returned control is exactly periodic (rank 2), while its finite disk
    window and reciprocal basis differ from every other seed.
    """
    rng = random.Random(seed)
    angle = rng.random() * math.pi
    c, s = math.cos(angle), math.sin(angle)
    aspect = math.exp(rng.uniform(-0.6, 0.6))
    shear = rng.uniform(-0.45, 0.45)
    scale = rng.uniform(1.4, 2.8)
    rotation = np.array([[c, -s], [s, c]])
    basis = rotation @ np.array([
        [scale * aspect, scale * shear],
        [0.0, scale / aspect],
    ])
    phase = np.array([rng.random(), rng.random()])
    min_singular = float(np.linalg.svd(basis, compute_uv=False).min())
    reach = math.ceil(radius / min_singular) + 2
    points = []
    for i in range(-reach, reach + 1):
        for j in range(-reach, reach + 1):
            point = (np.array([i, j]) + phase) @ basis.T
            if point @ point <= radius * radius:
                points.append(point)
    return np.asarray(points)
