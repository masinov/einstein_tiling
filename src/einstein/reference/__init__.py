"""Independent known-tiling/reference generators used by validation gates."""
"""Reference point sets and tilings used to calibrate A4."""

from .square_triangle import (
    random_square_triangle_patch,
    random_square_triangle_points,
)

__all__ = [
    "random_square_triangle_patch",
    "random_square_triangle_points",
]
