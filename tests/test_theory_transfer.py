"""W1 exact cylinder-transfer reference controls."""

from einstein.enumeration.polyform import enumerate_free_polykites
from einstein.funnel.a1_torus import find_periodic_tiling, verify_certificate
from einstein.theory.transfer import (
    CylinderTransfer,
    basis_coordinates,
    cylinder_basis,
    decide_period_vector,
    lattice_hnf,
    vector_norm2,
    vector_orbit,
    vector_orbit_representatives,
)
from einstein.theory.transfer_verify import verify_cycle_free_manifest


def _nontiling_two_kite():
    for n, forms in enumerate_free_polykites(2):
        if n == 2:
            for shape in forms:
                if find_periodic_tiling(shape, k_max=6)[0] is None:
                    return shape
    raise AssertionError("Myers-validated n=2 non-tiler not found")


def test_cylinder_basis_roundtrip_including_nonprimitive_vector():
    for vector in [(1, 0), (0, -3), (6, 4), (-9, 6), (10, -15)]:
        p, g, u = cylinder_basis(vector)
        assert vector == (g * p[0], g * p[1])
        assert p[0] * u[1] - p[1] * u[0] == 1
        for alpha in range(-3, 4):
            for beta in range(-3, 4):
                q = (alpha * p[0] + beta * u[0], alpha * p[1] + beta * u[1])
                assert basis_coordinates(q, p, u) == (alpha, beta)


def test_lattice_hnf_generates_expected_indices():
    assert lattice_hnf((1, 0), (0, 1)) == (1, 0, 1)
    assert lattice_hnf((2, 0), (0, 3)) == (2, 0, 3)
    a, b, d = lattice_hnf((6, 4), (-2, 1))
    assert a * d == 14
    assert 0 <= b < a


def test_vector_orbits_cover_norm_ball_and_keep_nonprimitive_vectors():
    reps = vector_orbit_representatives(25)
    covered = {v for rep in reps for v in vector_orbit(rep)}
    expected = {
        (x, y)
        for x in range(-8, 9)
        for y in range(-8, 9)
        if (x or y) and vector_norm2((x, y)) <= 25
    }
    assert covered == expected
    assert (1, 0) in reps and (2, 0) in reps and (5, 0) in reps
    for rep in reps:
        assert all(vector_norm2(v) == vector_norm2(rep) for v in vector_orbit(rep))


def test_single_kite_cycle_reconstructs_a1_certificate():
    shape = ((0, 0, 0),)
    result = decide_period_vector(shape, (1, 0))
    assert result.verdict == "cycle"
    assert result.cycle
    assert result.certificate["index"] == 1
    assert verify_certificate(shape, result.certificate)


def test_nonprimitive_period_preserves_quotient_torsion():
    shape = ((0, 0, 0),)
    result = decide_period_vector(shape, (2, 0))
    assert result.verdict == "cycle"
    assert result.multiplicity == 2
    assert result.certificate["index"] == 2
    assert verify_certificate(shape, result.certificate)


def test_nonprimitive_vector_is_not_collapsed_to_primitive_direction():
    # This four-kite control has a (2,0)-periodic tiling but no tiling with
    # period (1,0).  It pins C0.3/W1's quotient-torsion requirement.
    shape = ((0, 0, 0), (0, 0, 1), (0, 0, 2), (2, 2, 3))
    primitive = decide_period_vector(shape, (1, 0))
    nonprimitive = decide_period_vector(shape, (2, 0))
    assert primitive.verdict == "cycle-free"
    assert nonprimitive.verdict == "cycle"
    assert nonprimitive.multiplicity == 2
    assert verify_certificate(shape, nonprimitive.certificate)


def test_same_hex_pair_positive_control():
    shape = ((0, 0, 0), (0, 0, 1))
    result = decide_period_vector(shape, (1, 0))
    assert result.verdict == "cycle"
    assert verify_certificate(shape, result.certificate)


def test_pose_free_refuted_two_kite_has_cycle_free_small_cylinder():
    shape = _nontiling_two_kite()
    result = decide_period_vector(shape, (1, 0))
    assert result.verdict == "cycle-free"
    assert result.graph_sha256
    manifest = CylinderTransfer(shape, (1, 0)).cycle_free_manifest()
    assert verify_cycle_free_manifest(manifest)


def test_cycle_free_manifest_rejects_incomplete_graph_and_bad_order():
    manifest = CylinderTransfer(_nontiling_two_kite(), (1, 0)).cycle_free_manifest()
    bad_states = dict(manifest)
    bad_states["states"] = manifest["states"][:-1]
    assert not verify_cycle_free_manifest(bad_states)
    bad_edges = dict(manifest)
    bad_edges["edges"] = manifest["edges"][:-1]
    assert not verify_cycle_free_manifest(bad_edges)
    bad_order = dict(manifest)
    bad_order["topological_order"] = manifest["topological_order"][:-1]
    assert not verify_cycle_free_manifest(bad_order)


def test_cycle_free_manifest_rejects_cyclic_instance():
    try:
        CylinderTransfer(((0, 0, 0),), (1, 0)).cycle_free_manifest()
    except ValueError as exc:
        assert "cyclic" in str(exc)
    else:
        raise AssertionError("cyclic graph was mislabeled cycle-free")


def test_resource_limit_has_no_negative_polarity():
    result = decide_period_vector(((0, 0, 0),), (3, 0), max_edges=0)
    assert result.verdict == "resource-exhausted"
    assert result.certificate is None
    assert result.limit["max_edges"] == 0
