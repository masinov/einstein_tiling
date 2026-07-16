"""Taylor--Socolar triangular hierarchy reference for E4.

The centers of Taylor--Socolar hexagons form a triangular lattice, while
the decoration is a union of periodic level-n patterns with lattice constants
a_n = 2^n a_0.  Consequently the reciprocal scales are b_n = 2^-n b_0.

This generator partitions a triangular-lattice disk by the exact 2-adic
valuation of its lattice coordinates.  It is a diffraction calibration of
the published hierarchy (not a replacement for a full decorated-tile
renderer), and is fed to A4 as per-level orientation/decoration classes.

Primary anchors:
  https://arxiv.org/abs/1406.2905
  https://arxiv.org/abs/1207.6237
"""

from __future__ import annotations

import math


TRIANGULAR_RECIPROCAL_RADIUS = 4.0 * math.pi / math.sqrt(3.0)


def _v2(value: int):
    if value == 0:
        return 60
    value = abs(value)
    return (value & -value).bit_length() - 1


def taylor_socolar_hierarchy_classes(radius: float = 128.0,
                                     levels: int = 7):
    """Partition triangular-lattice sites into exact 2-adic levels."""
    classes = [[] for _ in range(levels)]
    reach = int(radius * 1.3) + 3
    for i in range(-reach, reach + 1):
        for j in range(-reach, reach + 1):
            x = i + 0.5 * j
            y = math.sqrt(3.0) / 2.0 * j
            if x * x + y * y > radius * radius:
                continue
            level = min(_v2(i), _v2(j), levels - 1)
            classes[level].append((x, y))
    return classes
