"""Rank-4 integer module for 12-fold geometry (program section 3.3).

A module vector (u0, u1, u2, u3) represents the plane point
u0*e0 + u1*e1 + u2*e2 + u3*e3 with e_k the unit vector at 30k degrees:
e0=(1,0), e1=(s3/2,1/2), e2=(1/2,s3/2), e3=(0,1).  Every vertex of every
Tile(1,1)/spectre substitution tiling lies on this module, and 30-degree
rotation, mirroring and translation act by integer maps -- the same
"exact arithmetic in the search path" discipline as the kite substrate
(D-0003 deferred this module until 12-fold geometry appeared; A4
diffraction indexing and the vendored spectre generator are that moment).

Conventions match vendor/spectre/gen_tables.py exactly, so anchor dumps
from the vendored generator embed verbatim.
"""

from __future__ import annotations

import math

Vec4 = tuple[int, int, int, int]
Pose = tuple[int, int, Vec4]

SQRT3_2 = math.sqrt(3.0) / 2.0  # output-time only


def rot30(v: Vec4) -> Vec4:
    """Rotate by +30 degrees: e_k -> e_{k+1} (e4 = e2 - e0)."""
    u0, u1, u2, u3 = v
    return (-u3, u0, u1 + u3, u2)


def mirror_y(v: Vec4) -> Vec4:
    """Mirror across the y-axis (x -> -x): e_k -> e_{6-k}."""
    u0, u1, u2, u3 = v
    return (-u0 - u2, -u1, u2, u1 + u3)


def apply_sr(s: int, r: int, v: Vec4) -> Vec4:
    """Apply MirrorY^s then Rot(30*r) -- the vendored generator's order."""
    if s:
        v = mirror_y(v)
    for _ in range(r % 12):
        v = rot30(v)
    return v


def madd(a: Vec4, b: Vec4) -> Vec4:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def mneg(v: Vec4) -> Vec4:
    return (-v[0], -v[1], -v[2], -v[3])


def compose_pose(a: Pose, b: Pose) -> Pose:
    """Compose exact plane isometries: apply ``b``, then ``a``."""
    sa, ra, ta = a
    sb, rb, tb = b
    return (
        sa ^ sb,
        (ra + (rb if sa == 0 else -rb)) % 12,
        madd(ta, apply_sr(sa, ra, tb)),
    )


def inverse_pose(p: Pose) -> Pose:
    """Return the exact inverse of a module-preserving pose."""
    s, r, t = p
    ri = (-r) % 12 if s == 0 else r % 12
    return (s, ri, apply_sr(s, ri, mneg(t)))


def relative_pose(origin: Pose, target: Pose) -> Pose:
    """Express ``target`` in ``origin``'s local coordinate frame."""
    return compose_pose(inverse_pose(origin), target)


def norm2_pair(v: Vec4) -> tuple[int, int]:
    """Return integers ``(a, b)`` with ``4*|v|² = a + b*sqrt(3)``.

    This representation permits exact distance ordering without projecting
    module points to floating-point Cartesian coordinates.
    """
    u0, u1, u2, u3 = v
    x0, x1 = 2 * u0 + u2, u1
    y0, y1 = 2 * u3 + u1, u2
    return (
        x0 * x0 + 3 * x1 * x1 + y0 * y0 + 3 * y1 * y1,
        2 * (x0 * x1 + y0 * y1),
    )


def compare_quadratic(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Compare exact values ``a0+a1*sqrt(3)`` and ``b0+b1*sqrt(3)``."""
    p, q = a[0] - b[0], a[1] - b[1]
    if q == 0:
        return (p > 0) - (p < 0)
    if p == 0:
        return (q > 0) - (q < 0)
    if (p > 0) == (q > 0):
        return 1 if p > 0 else -1
    # Opposite signs: compare |p| with |q|*sqrt(3), avoiding radicals.
    d = p * p - 3 * q * q
    if d == 0:
        return 0
    if p > 0:
        return 1 if d > 0 else -1
    return -1 if d > 0 else 1


def to_xy(v: Vec4) -> tuple[float, float]:
    """Cartesian projection (floats: output/analysis time only)."""
    u0, u1, u2, u3 = v
    return (u0 + SQRT3_2 * u1 + 0.5 * u2, 0.5 * u1 + SQRT3_2 * u2 + u3)
