"""A4 diffraction fingerprint: unit pins + the E4 reference signatures.

The E4 12-fold/core calibration (four reference patches,
literature-anchored criteria) runs via scripts/run_e4.py; results live in
docs/notebook/assets/e4-results.json.  These tests pin the pieces cheaply
so regressions surface: the indexer on synthetic peak lists (known rank),
the symmetry vote, model-set and limit-periodic references, the random
square--triangle control, and the hat patch end to end.
"""

import math
import random

import numpy as np
import pytest

from einstein.funnel.a4_diffraction import (
    class_power_sum,
    detect_peaks,
    dyadic_scale_depth,
    fingerprint,
    index_peaks,
    power_spectrum,
    rotational_symmetry,
    sharp_peak_mass_fraction,
)
from einstein.reference.limit_periodic import (
    TRIANGULAR_RECIPROCAL_RADIUS,
    taylor_socolar_hierarchy_classes,
)
from einstein.reference.model_sets import (
    ammann_beenker_points,
    model_set_metadata,
    penrose_points,
    random_periodic_points,
    transform_points,
)
from einstein.reference.square_triangle import random_square_triangle_patch

PHI = (1 + math.sqrt(5)) / 2


def _combo_peaks(gens, bound, kmax):
    """All |integer combos| <= bound of gens within |k| <= kmax."""
    out = []
    def rec(i, kx, ky):
        if i == len(gens):
            if 0.05 < math.hypot(kx, ky) <= kmax:
                out.append((kx, ky, 1.0))
            return
        for c in range(-bound, bound + 1):
            rec(i + 1, kx + c * gens[i][0], ky + c * gens[i][1])
    rec(0, 0.0, 0.0)
    # dedup nearby
    ded = []
    for p in out:
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 1e-6 for q in ded):
            ded.append(p)
    return ded


def test_indexer_rank2_with_large_indices():
    g = [(0.31, 0.0), (0.0, 0.31)]
    peaks = _combo_peaks(g, 9, 2.5)  # indices up to 9 >> coeff_bound
    rank, gens, unindexed = index_peaks(peaks, tol=0.005, top=150)
    assert rank == 2 and unindexed == 0


def test_indexer_rank4_golden():
    b = [(0.4, 0.0), (0.0, 0.4)]
    g = b + [(PHI * x, PHI * y) for x, y in b]
    peaks = _combo_peaks(g, 2, 2.0)
    rank, gens, unindexed = index_peaks(peaks, tol=0.005, top=150)
    assert rank == 4 and unindexed == 0


def test_symmetry_vote():
    star = []
    for k in range(6):
        a = math.pi / 3 * k + 0.2
        star.append((math.cos(a), math.sin(a), 1.0))
    assert rotational_symmetry(star, tol=0.01) == 6
    assert rotational_symmetry(star[:5], tol=0.01) in (1, 2)


def test_extended_symmetry_vote():
    for order in (8, 10):
        star = []
        for k in range(order):
            a = 2 * math.pi / order * k + 0.17
            star.append((math.cos(a), math.sin(a), 1.0))
        assert rotational_symmetry(star, tol=0.01) == order


def test_sharp_peak_mass_rejects_broad_maximum():
    grid = 64
    k0 = grid // 2
    yy, xx = np.mgrid[:grid, :grid]
    sharp = np.zeros((grid, grid))
    sharp[k0, k0] = 1.0
    sharp[k0, k0 + 10] = 1.0
    broad = np.zeros((grid, grid))
    broad[k0, k0] = 1.0
    broad += np.exp(
        -((xx - (k0 + 10)) ** 2 + (yy - k0) ** 2) / (2.0 * 3.0 ** 2)
    )
    peaks = [(10.0, 0.0, 1.0)]
    assert sharp_peak_mass_fraction(
        sharp, peaks, 1.0, k0,
    ) > 5.0 * sharp_peak_mass_fraction(broad, peaks, 1.0, k0)


def test_model_set_construction_invariants():
    penrose = model_set_metadata("penrose")
    ab = model_set_metadata("ammann-beenker")
    assert penrose["ambient_rank"] == 5
    assert penrose["internal_dimension"] == 3
    assert penrose["window_facets"] == 20
    assert ab["ambient_rank"] == 4
    assert ab["internal_dimension"] == 2
    assert ab["window_facets"] == 8


@pytest.mark.slow
@pytest.mark.parametrize(
    ("builder", "symmetry"),
    [(penrose_points, 10), (ammann_beenker_points, 8)],
)
def test_rank4_model_set_references(builder, symmetry):
    points = builder()
    res = fingerprint(points=points, floor=0.03)
    assert res["verdict"] == "quasicrystal-candidate"
    assert res["rank"] == 4 and res["symmetry"] == symmetry


@pytest.mark.slow
def test_rank_is_stable_under_rotation_and_shear():
    points = ammann_beenker_points()
    for angle, shear in ((0.37, 0.0), (0.0, 0.18), (0.61, -0.13)):
        moved = transform_points(points, angle=angle, shear=shear)
        res = fingerprint(points=moved, floor=0.03)
        assert res["rank"] == 4


@pytest.mark.slow
def test_random_periodic_controls_do_not_look_quasicrystalline():
    for seed in range(100):
        points = random_periodic_points(seed)
        res = fingerprint(
            points=points, grid=192, floor=0.04, k_min=0.3, top=60,
        )
        assert res["verdict"] != "quasicrystal-candidate"


@pytest.mark.slow
def test_taylor_socolar_hierarchy_has_dyadic_reciprocal_scales():
    classes = taylor_socolar_hierarchy_classes()
    power, dk, k0 = class_power_sum(classes)
    peaks = detect_peaks(power, dk, k0, floor=0.02)
    depth = dyadic_scale_depth(
        peaks, TRIANGULAR_RECIPROCAL_RADIUS, tol=2.0 * dk,
    )
    assert depth >= 5

    # Erasing the hierarchy leaves the ordinary triangular center lattice.
    power, dk, k0 = class_power_sum([[p for group in classes for p in group]])
    peaks = detect_peaks(power, dk, k0, floor=0.02)
    assert dyadic_scale_depth(
        peaks, TRIANGULAR_RECIPROCAL_RADIUS, tol=2.0 * dk,
    ) == 1


@pytest.mark.slow
def test_random_square_triangle_growth_is_valid_and_mixed():
    patch = random_square_triangle_patch(7, target_tiles=500)
    assert len(patch.polygons) == 500
    assert len(patch.points) >= 20
    assert set(patch.tile_types) == {3, 4}
    assert patch.rejected_moves == 0
    edge_counts = {}
    for polygon in patch.polygons:
        assert len(polygon) in (3, 4)
        for a, b in zip(polygon, polygon[1:] + polygon[:1]):
            edge = (a, b) if a < b else (b, a)
            edge_counts[edge] = edge_counts.get(edge, 0) + 1
    assert max(edge_counts.values()) == 2


@pytest.mark.slow
def test_random_square_triangle_ensemble_is_diffuse_ordered():
    classes = [
        random_square_triangle_patch(
            10_000 + seed, target_tiles=1_000,
        ).points
        for seed in range(2)
    ]
    power, dk, k0 = class_power_sum(classes, grid=1024)
    peaks = detect_peaks(power, dk, k0, floor=0.005)
    rank, _, _ = index_peaks(peaks, 2.0 * dk, top=150)
    assert rank == 4
    assert rotational_symmetry(peaks, 2.0 * dk) == 12
    assert sharp_peak_mass_fraction(power, peaks, dk, k0) < 0.025


def test_periodic_point_set_is_crystal():
    # square lattice patch, single class
    pts = [(i * 3.0, j * 3.0) for i in range(-30, 31) for j in range(-30, 31)
           if (i * 3.0) ** 2 + (j * 3.0) ** 2 <= 90 * 90]
    res = fingerprint(points=pts, floor=0.05)
    assert res["verdict"] == "crystal" and res["rank"] == 2
    assert res["symmetry"] in (4, 2)


def test_random_point_set_is_diffuse():
    rng = random.Random(7)
    pts = []
    while len(pts) < 4000:
        x, y = rng.uniform(-90, 90), rng.uniform(-90, 90)
        if x * x + y * y <= 90 * 90:
            pts.append((x, y))
    p, dk, k0 = power_spectrum(pts)
    null = detect_peaks(p, dk, k0, floor=1e-12, max_peaks=3)
    ceiling = null[0][2]
    res = fingerprint(points=pts, floor=5 * ceiling)
    assert res["verdict"] == "diffuse"


@pytest.mark.slow
def test_hat_patch_is_rank4_sixfold():
    """E4's core positive: the funnel-grown hat patch fingerprints as a
    rank-4, sixfold quasicrystal candidate (Baake-Gaehler-Sadun give
    pure-point diffraction from a 4:2 cut-and-project scheme)."""
    from einstein.db import ShapeDB
    from einstein.render.svg import hex_to_xy

    db = ShapeDB("data/shapes.sqlite")
    cert = db.latest_verdict(635, "A3-patch")["certificate"]
    db.close()
    by_op: dict[int, list] = {}
    for op, tx, ty in cert["placements"]:
        by_op.setdefault(op, []).append(hex_to_xy((tx, ty)))
    res = fingerprint(classes=list(by_op.values()), floor=0.0327)
    assert res["verdict"] == "quasicrystal-candidate"
    assert res["rank"] == 4 and res["symmetry"] == 6
