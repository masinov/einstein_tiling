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


def to_xy(v: Vec4) -> tuple[float, float]:
    """Cartesian projection (floats: output/analysis time only)."""
    u0, u1, u2, u3 = v
    return (u0 + SQRT3_2 * u1 + 0.5 * u2, 0.5 * u1 + SQRT3_2 * u2 + u3)
