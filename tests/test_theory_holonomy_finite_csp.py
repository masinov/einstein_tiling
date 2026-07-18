"""Generic finite-group coupled-CSP controls."""

from einstein.theory.finite_groups import alternating_group, symmetric_group
from einstein.theory.holonomy_csp import build_boundary_holonomy_cnf
from einstein.theory.holonomy_finite_csp import (
    build_finite_boundary_holonomy_cnf,
    build_finite_boundary_holonomy_union_cnf,
    commuting_pairs,
    scan_finite_boundary_holonomy,
    solve_finite_boundary_holonomy_hybrid,
    solve_finite_boundary_holonomy_incremental,
    solve_finite_boundary_holonomy_union,
)


def test_generic_s3_cnf_matches_specialized_encoding():
    group = symmetric_group(3)
    shape = ((0, 0, 0),)
    images = (0, 1, 2, 3, 4, 5)
    twists = commuting_pairs(group)[0]
    generic, _ = build_finite_boundary_holonomy_cnf(
        shape, (1, 0, 1), images, twists, group
    )
    specialized, _ = build_boundary_holonomy_cnf(
        shape, (1, 0, 1),
        tuple(group.labels[index] for index in images),
        tuple(group.labels[index] for index in twists),
    )
    assert generic.clauses == specialized.clauses


def test_periodic_single_kite_survives_a4_identity_map():
    group = alternating_group(4)
    assert len(commuting_pairs(group)) == 48
    result = scan_finite_boundary_holonomy(
        ((0, 0, 0),), (2, 0, 1), (0,) * 6, group
    )
    assert result["sat_twist_pairs"] > 0
    union = solve_finite_boundary_holonomy_union(
        ((0, 0, 0),), (2, 0, 1), (0,) * 6, group
    )
    assert union["sat"]
    incremental = solve_finite_boundary_holonomy_incremental(
        ((0, 0, 0),), (2, 0, 1), (0,) * 6, group
    )
    assert incremental["sat"]
    hybrid = solve_finite_boundary_holonomy_hybrid(
        ((0, 0, 0),), (2, 0, 1), (0,) * 6, group
    )
    assert hybrid["sat"] and hybrid["mode"] == "identity-twist-shortcut"
    cnf, metadata = build_finite_boundary_holonomy_union_cnf(
        ((0, 0, 0),), (2, 0, 1), (0,) * 6, group
    )
    assert cnf.nv == metadata["variables"]
    assert metadata["twist_pairs"] == 48
