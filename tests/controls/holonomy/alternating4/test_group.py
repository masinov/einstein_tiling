"""Exact controls for the A4 = V4 semidirect C3 factorization."""

from einstein.holonomy.alternating4.group import (
    A4Coordinate,
    c3_action,
    canonical_a4_semidirect,
    coordinate_inverse,
    coordinate_multiply,
)
from einstein.holonomy.boundary import KITE_EDGE_GENERATORS
from einstein.holonomy.finite_constraints import commuting_pairs


def test_semidirect_coordinates_reproduce_a4_tables():
    model = canonical_a4_semidirect()
    group = model.group
    assert c3_action(3, 1) == 1
    assert {c3_action(power, 1) for power in range(3)} == {1, 2, 3}
    for left in range(group.order):
        x = model.coordinate(left)
        assert model.element(x) == left
        assert model.element(coordinate_inverse(x)) == group.inverses[left]
        for right in range(group.order):
            y = model.coordinate(right)
            product = group.multiplication[left][right]
            assert model.element(coordinate_multiply(x, y)) == product
            assert model.commute(x, y) == (
                group.multiplication[left][right]
                == group.multiplication[right][left]
            )
    twists = commuting_pairs(group)
    assert len(twists) == 48
    assert tuple(
        index for index, pair in enumerate(twists)
        if all(model.coordinate(element).q == 0 for element in pair)
    ) == (0, 3, 8, 11, 18, 19, 20, 21, 34, 35, 36, 37, 44, 45, 46, 47)


def test_factorized_layer_d_edge_equation_and_map7_signature():
    model = canonical_a4_semidirect()
    group = model.group
    for displacement in range(group.order):
        for start in range(group.order):
            for label in range(group.order):
                expected = group.multiplication[
                    group.multiplication[displacement][start]
                ][label]
                assert model.element(model.edge_equation(
                    displacement, start, label
                )) == expected

    map7 = (1, 2, 1, 0, 3, 8)
    coordinates = tuple(model.coordinate(value) for value in map7)
    assert tuple(value.q for value in coordinates) == (1, 2, 1, 0, 0, 0)
    assert tuple((2 * x + y) % 3 for x, y in KITE_EDGE_GENERATORS) == (
        1, 2, 1, 0, 0, 0,
    )
    assert tuple(value.v for value in coordinates) == (0, 0, 0, 0, 1, 2)
    assert len({value.v for value in coordinates[3:]}) == 3
    assert all(value.q == 0 for value in coordinates[3:])
