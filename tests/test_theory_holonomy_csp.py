"""Binary-coupled S3 boundary-holonomy CSP controls."""

from einstein.theory.holonomy import (
    s3_boundary_quotients,
    verify_s3_boundary_quotient,
)
from einstein.theory.holonomy_csp import (
    QuotientVertexReducer,
    build_boundary_holonomy_cnf,
    build_boundary_holonomy_union_cnf,
    build_cover_cnf,
    commuting_s3_pairs,
    scan_boundary_holonomy,
    solve_cover_control,
)


def _kernel3_mapping(shape):
    result = s3_boundary_quotients(shape, keep=0)
    images = result["sample_surjections_by_displacement_kernel"]["3"]
    assert verify_s3_boundary_quotient(shape, images, require_surjective=True)
    return images


def test_quotient_vertex_reducer_tracks_deck_translation():
    points = [(0, 0), (2, 2), (4, 4), (-2, 4)]
    reducer = QuotientVertexReducer((2, 0, 1), points)
    key0, deck0 = reducer.reduce((0, 0))
    key1, deck1 = reducer.reduce((4, 4))
    assert key0 == key1
    assert deck1[0] - deck0[0] == 1


def test_commuting_s3_pair_count():
    assert len(commuting_s3_pairs()) == 18


def test_periodic_single_kite_passes_all_coupled_encodings():
    shape = ((0, 0, 0),)
    images = _kernel3_mapping(shape)
    for hnf in ((1, 0, 1), (2, 0, 1), (2, 1, 1)):
        relaxed = scan_boundary_holonomy(shape, hnf, images, cover_mode="at-least")
        exact = scan_boundary_holonomy(shape, hnf, images, cover_mode="exact")
        assert relaxed["sat_twist_pairs"] > 0
        assert exact["sat_twist_pairs"] > 0


def test_stored_periodic_multikite_passes_coupled_encodings():
    # Shape 392's independently verified A1 certificate has this fundamental
    # domain and three tile placements.  It exercises nontrivial boundary
    # gluing, unlike the one-kite identity control.
    shape = (
        (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3),
        (0, 0, 4), (0, 0, 5), (2, -4, 0), (2, -4, 1),
    )
    hnf = (2, 0, 2)
    images = _kernel3_mapping(shape)
    assert solve_cover_control(shape, hnf, "exact")["sat"]
    for cover_mode in ("at-least", "exact"):
        result = scan_boundary_holonomy(
            shape, hnf, images, cover_mode=cover_mode
        )
        assert result["sat_twist_pairs"] > 0


def test_cnf_is_deterministic():
    shape = ((0, 0, 0),)
    images = _kernel3_mapping(shape)
    twists = commuting_s3_pairs()[0]
    left, left_meta = build_boundary_holonomy_cnf(shape, (1, 0, 1), images, twists)
    right, right_meta = build_boundary_holonomy_cnf(shape, (1, 0, 1), images, twists)
    assert left.clauses == right.clauses
    assert left_meta == right_meta

    left, left_meta = build_cover_cnf(shape, (1, 0, 1))
    right, right_meta = build_cover_cnf(shape, (1, 0, 1))
    assert left.clauses == right.clauses
    assert left_meta == right_meta


def test_twist_union_has_same_small_control_polarity():
    from pysat.solvers import Cadical195

    shape = ((0, 0, 0),)
    images = _kernel3_mapping(shape)
    union, metadata = build_boundary_holonomy_union_cnf(
        shape, (1, 0, 1), images, cover_mode="exact"
    )
    assert metadata["twist_pairs"] == 18
    with Cadical195(bootstrap_with=union) as solver:
        assert solver.solve()
