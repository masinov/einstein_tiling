"""Small-group and generic boundary-quotient controls."""

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.finite_groups import (
    alternating_group,
    dihedral_group_4,
    quaternion_group,
    symmetric_group,
)
from einstein.theory.holonomy_quotients import boundary_quotient_census


def test_small_group_tables():
    for group, order in (
        (symmetric_group(3), 6),
        (dihedral_group_4(), 8),
        (quaternion_group(), 8),
        (alternating_group(4), 12),
    ):
        assert group.order == order
        assert all(group.multiplication[value][group.inverses[value]] == 0
                   for value in range(order))
        assert all(group.multiplication[0][value] == value for value in range(order))
        assert all(
            group.multiplication[group.multiplication[left][middle]][right]
            == group.multiplication[left][group.multiplication[middle][right]]
            for left in range(order)
            for middle in range(order)
            for right in range(order)
        )


def test_generic_s3_census_reproduces_layer_d_counts():
    shape = decode_compiled_key("010001010104010502f002f1030b030c04fa04fb")
    census = boundary_quotient_census(shape, symmetric_group(3))
    assert census["homomorphisms"] == 3474
    assert census["surjections"] == 2556
    assert census["surjective_displacement_kernel_orders"] == {
        "3": 234, "6": 2322,
    }
    assert census["inner_conjugacy_classes_by_kernel"]["3"] == 39
