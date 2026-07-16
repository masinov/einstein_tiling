"""A4 diffraction fingerprint: unit pins + the E4 reference signatures.

The E4 12-fold/core calibration (four reference patches,
literature-anchored criteria) runs via scripts/run_e4.py; results live in
docs/notebook/assets/e4-results.json.  These tests pin the pieces cheaply
so regressions surface: the indexer on synthetic peak lists (known rank),
the symmetry vote, and (slow) the hat patch's rank-4/sixfold signature end
to end.  The wider reference/stability suite required by full E4 remains
tracked in docs/STATUS.md.
"""

import math
import random

import pytest

from einstein.funnel.a4_diffraction import (
    detect_peaks,
    fingerprint,
    index_peaks,
    power_spectrum,
    rotational_symmetry,
)

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
