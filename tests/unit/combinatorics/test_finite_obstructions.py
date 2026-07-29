"""Architecture-independent controls for finite-obstruction primitives."""

import itertools

import pytest

from einstein.combinatorics.finite_obstructions import (
    deletion_minimal_obstruction,
    uniform_demand_matching,
    verify_uniform_demand_matching,
)


def test_deletion_minimizer_is_domain_independent_and_stable():
    forbidden = ({"b", "c"}, {"a", "d", "e"})

    def obstructed(items):
        return any(pattern <= set(items) for pattern in forbidden)

    assert deletion_minimal_obstruction(
        ("a", "b", "c", "d", "e", "a"), obstructed
    ) == ("b", "c")
    assert deletion_minimal_obstruction(("a", "b"), obstructed) == ()


def test_uniform_demand_matching_handles_arbitrary_demands():
    resources = tuple(range(7))
    supports = (
        frozenset((0, 1, 2, 3)),
        frozenset((2, 3, 4, 5)),
    )
    result = uniform_demand_matching(supports, (1, 2), demand=3)
    assert result.saturated
    assert result.matched == 6
    assert verify_uniform_demand_matching(supports, result)
    assert set(resource for _, assigned in result.assignment for resource in assigned) <= set(resources)


def test_uniform_demand_matching_returns_a_cold_hall_witness():
    supports = (
        frozenset(("p", "q", "r")),
        frozenset(("p", "q", "r")),
    )
    result = uniform_demand_matching(supports, (1, 2), demand=2)
    assert not result.saturated
    assert result.deficient_items == (1, 2)
    assert result.deficient_resources == ("p", "q", "r")
    assert verify_uniform_demand_matching(supports, result)


def test_matching_matches_exhaustive_hall_condition_for_demands_one_to_three():
    resources = range(4)
    support_choices = tuple(
        frozenset(resource for resource in resources if mask >> resource & 1)
        for mask in range(16)
    )
    for supports in itertools.product(support_choices, repeat=3):
        for demand in (1, 2, 3):
            expected = all(
                len(set().union(*(supports[index] for index in subset)))
                >= demand * len(subset)
                for size in range(1, 4)
                for subset in itertools.combinations(range(3), size)
            )
            result = uniform_demand_matching(
                supports, (1, 2, 3), demand=demand
            )
            assert result.saturated == expected
            assert verify_uniform_demand_matching(supports, result)


def test_uniform_demand_matching_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="positive"):
        uniform_demand_matching((frozenset((1,)),), (1,), demand=0)
    with pytest.raises(ValueError, match="out of range"):
        uniform_demand_matching((frozenset((1,)),), (2,), demand=1)
