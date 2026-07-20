"""Exact ``A4 = V4 semidirect C3`` coordinates for Layer-D analysis.

The canonical A4 implementation numbers permutations lexicographically.  This
module replaces those opaque indices by a two-bit Klein-four coordinate and a
ternary quotient coordinate.  It is an analysis layer only: the certified CNF
encoder continues to use the independent multiplication table.
"""

from __future__ import annotations

from dataclasses import dataclass

from einstein.theory.finite_groups import alternating_group


def v4_add(left: int, right: int) -> int:
    """Add two packed GF(2)^2 vectors."""
    if not 0 <= left < 4 or not 0 <= right < 4:
        raise ValueError("V4 coordinates must be packed two-bit values")
    return left ^ right


def c3_action(exponent: int, value: int) -> int:
    """Act on V4 by the order-three matrix M(x,y)=(y,x+y)."""
    if not 0 <= value < 4:
        raise ValueError("V4 coordinates must be packed two-bit values")
    exponent %= 3
    for _ in range(exponent):
        x, y = value & 1, (value >> 1) & 1
        value = y | ((x ^ y) << 1)
    return value


@dataclass(frozen=True)
class A4Coordinate:
    """An element ``v c^q`` with v in V4 and q in C3."""

    v: int
    q: int

    def __post_init__(self):
        if not 0 <= self.v < 4 or not 0 <= self.q < 3:
            raise ValueError("invalid A4 semidirect coordinate")


def coordinate_multiply(left: A4Coordinate, right: A4Coordinate) -> A4Coordinate:
    """Multiply using (v,q)(w,r)=(v+M^q w,q+r)."""
    return A4Coordinate(
        v4_add(left.v, c3_action(left.q, right.v)),
        (left.q + right.q) % 3,
    )


def coordinate_inverse(value: A4Coordinate) -> A4Coordinate:
    """Invert a semidirect coordinate."""
    q = (-value.q) % 3
    return A4Coordinate(c3_action(q, value.v), q)


class A4Semidirect:
    """Exact bijection between canonical A4 indices and semidirect coordinates."""

    def __init__(self):
        self.group = alternating_group(4)
        # Packed bits: 0 -> identity, 1 -> group element 3,
        # 2 -> group element 8, 3 -> their product 11.
        self.v4_elements = (0, 3, 8, 11)
        self.c3_generator = 1
        c2 = self.group.multiplication[self.c3_generator][self.c3_generator]
        self.c3_elements = (self.group.identity, self.c3_generator, c2)
        to_element = {}
        to_coordinate = {}
        for v, v_element in enumerate(self.v4_elements):
            for q, q_element in enumerate(self.c3_elements):
                element = self.group.multiplication[v_element][q_element]
                coordinate = A4Coordinate(v, q)
                if element in to_coordinate:
                    raise AssertionError("semidirect coordinates are not injective")
                to_element[coordinate] = element
                to_coordinate[element] = coordinate
        if len(to_coordinate) != self.group.order:
            raise AssertionError("semidirect coordinates do not cover A4")
        self._to_element = to_element
        self._to_coordinate = to_coordinate

    def coordinate(self, element: int) -> A4Coordinate:
        return self._to_coordinate[element]

    def element(self, coordinate: A4Coordinate) -> int:
        return self._to_element[coordinate]

    def edge_equation(
        self, displacement: int, start: int, label: int
    ) -> A4Coordinate:
        """Factor the Layer-D equation ``end = displacement * start * label``."""
        d = self.coordinate(displacement)
        x = self.coordinate(start)
        edge = self.coordinate(label)
        return A4Coordinate(
            d.v
            ^ c3_action(d.q, x.v)
            ^ c3_action((d.q + x.q) % 3, edge.v),
            (d.q + x.q + edge.q) % 3,
        )

    def commute(self, left: A4Coordinate, right: A4Coordinate) -> bool:
        """The exact affine fixed-point equation for a commuting twist pair."""
        return (
            left.v ^ c3_action(left.q, right.v)
            == right.v ^ c3_action(right.q, left.v)
        )


def canonical_a4_semidirect() -> A4Semidirect:
    return A4Semidirect()
