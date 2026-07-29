"""Controls for the bounded-overlap Layer-D relaxation."""

from pysat.solvers import Cadical195

from einstein.holonomy.boundary import s3_boundary_quotients
from einstein.holonomy.constraints import commuting_s3_pairs
from einstein.holonomy.overlaps import (
    build_bounded_overlap_holonomy_cnf,
    scan_bounded_overlap_holonomy,
)


def _mapping(shape):
    return s3_boundary_quotients(shape, keep=0)[
        "sample_surjections_by_displacement_kernel"
    ]["3"]


def test_periodic_single_kite_survives_double_cover_bound():
    shape = ((0, 0, 0),)
    result = scan_bounded_overlap_holonomy(
        shape, (2, 0, 1), _mapping(shape), maximum_coverage=2
    )
    assert result["sat_twist_pairs"] > 0


def test_bounded_overlap_encoding_is_deterministic_and_satisfiable_control():
    shape = ((0, 0, 0),)
    images = _mapping(shape)
    twists = commuting_s3_pairs()[0]
    left, left_metadata = build_bounded_overlap_holonomy_cnf(
        shape, (2, 0, 1), images, twists, maximum_coverage=2
    )
    right, right_metadata = build_bounded_overlap_holonomy_cnf(
        shape, (2, 0, 1), images, twists, maximum_coverage=2
    )
    assert left.clauses == right.clauses
    assert left_metadata == right_metadata
    assert left_metadata["maximum_coverage"] == 2
    with Cadical195(bootstrap_with=left) as solver:
        assert solver.solve()
