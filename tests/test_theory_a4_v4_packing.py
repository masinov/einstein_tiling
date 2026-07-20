"""Unit pins for the packing-sensitive Layer-D refinement."""

from pysat.formula import CNF
from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.holonomy_csp import quotient_boundary_data
from einstein.theory.a4_v4_packing import (
    add_placement_budget,
    canonical_collision_type,
    collision_orbit_clauses,
    collision_overlap,
    placement_lattice_cells,
    selected_placements,
)


KEY = "010001010104010502f002f1030b030c04fa04fb"


def test_placement_budget_uses_initial_variable_block():
    cnf = CNF(from_clauses=[[1, 2], [2, 3], [4]])
    bounded, metadata = add_placement_budget(cnf, placement_count=3, budget=1)
    with Cadical195(bootstrap_with=bounded) as solver:
        assert solver.solve()
        selected = selected_placements(solver.get_model(), 3)
    assert len(selected) == 1
    assert selected == (2,)
    assert metadata["placement_budget"] == 1
    assert metadata["budget_clauses"] > 0


def test_zero_budget_can_refute_cover_clause():
    cnf = CNF(from_clauses=[[1, 2]])
    bounded, _ = add_placement_budget(cnf, placement_count=2, budget=0)
    with Cadical195(bootstrap_with=bounded) as solver:
        assert not solver.solve()


def test_overlap_six_collision_orbit_is_exact_and_translation_covariant():
    shape = decode_compiled_key(KEY)
    left = placement_lattice_cells(shape, (3, 0, 0))
    right = placement_lattice_cells(shape, (5, 0, 1))
    target = canonical_collision_type(left, right)
    translated = canonical_collision_type(
        placement_lattice_cells(shape, (3, 7, -4)),
        placement_lattice_cells(shape, (5, 7, -3)),
    )
    assert target == translated
    assert collision_overlap(target) == 6


def test_overlap_six_orbit_is_subset_of_torus_nonoverlap_clauses():
    shape = decode_compiled_key(KEY)
    hnf = (10, 2, 6)
    instance, _, _ = quotient_boundary_data(shape, hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, (3, 0, 0)),
        placement_lattice_cells(shape, (5, 0, 1)),
    )
    clauses = collision_orbit_clauses(shape, hnf, instance, target)
    assert len(clauses) == 720
    for left, right in clauses:
        assert left < 0 and right < 0
        assert (instance.placements[-left - 1][1]
                & instance.placements[-right - 1][1])
