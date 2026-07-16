"""A3 large-patch construction: disk cover, both engines, certificates.

External anchor situation: no published polykite patch data exists, so A3
is validated by internal cross-checks that the two independent engines
(pure-Python greedy filler, SAT/CaDiCaL) agree with each other and with
the A1/A2 verdicts: tilers fill disks, the non-tiling 2-kite is refuted,
and certificates survive only untampered.
"""

import pytest

from einstein.enumeration.polyform import enumerate_free_polykites
from einstein.funnel.a1_torus import find_periodic_tiling
from einstein.funnel.a3_patch import (
    disk_region,
    grow_patch,
    sat_grow_patch,
    verify_patch_certificate,
)
from einstein.substrate.kitegrid import (
    canonical_form,
    cell_centroid4,
    cells_in_polygon,
    norm2,
    transform_cell,
)
from tests.test_hat import HAT_OUTLINE

KITE = [(0, 0, 0)]
HEXAGON = [(0, 0, d) for d in range(6)]


def _nontiler_2kite():
    for n, forms in enumerate_free_polykites(2):
        if n == 2:
            for shape in forms:
                if find_periodic_tiling(shape, k_max=6)[0] is None:
                    return shape
    raise AssertionError("unreachable")


def test_disk_region_smallest():
    # r2=2: exactly the six kites of the origin hexagon (their centroids
    # sit at distance sqrt(25)/4 = 1.25; the next hexagon's kites are
    # farther than sqrt(2)).
    assert disk_region(2) == [(0, 0, d) for d in range(6)]


def test_disk_region_is_symmetric_and_sorted():
    reg = disk_region(40)
    regset = set(reg)
    for op in range(12):
        assert {transform_cell(c, op) for c in reg} == regset
    dists = [norm2(cell_centroid4(c)) for c in reg]
    assert dists == sorted(dists)


def test_single_kite_fills_disk():
    res = grow_patch(KITE, 20)
    assert res["completed"] and res["tiles"] == len(disk_region(20))
    assert verify_patch_certificate(KITE, res["certificate"])


def test_hexagon_fills_disk():
    # the full hexagon is a trivially periodic tiler (A1-positive control)
    res = grow_patch(HEXAGON, 50)
    assert res["completed"]
    assert verify_patch_certificate(HEXAGON, res["certificate"])


def test_nontiler_refuted_by_both_engines():
    shape = _nontiler_2kite()
    res = grow_patch(shape, 20, node_budget=100_000)
    assert not res["completed"] and res["seed_pose_exhausted"]
    sat = sat_grow_patch(shape, 20, fix_seed=False)
    assert sat["refuted"] and not sat["completed"]


def test_hat_grows_disk_greedy():
    hat = canonical_form(cells_in_polygon(HAT_OUTLINE))
    res = grow_patch(hat, 150, node_budget=500_000, rng_seed=0)
    assert res["completed"]
    assert verify_patch_certificate(hat, res["certificate"])
    # the profile must show forced placements (options == 1 occurs)
    assert res["profile"]["options_hist"].get(1, 0) > 0


def test_hat_grows_disk_sat():
    hat = canonical_form(cells_in_polygon(HAT_OUTLINE))
    res = sat_grow_patch(hat, 500)
    assert res["completed"] and res["tiles"] > 100
    # sat_grow_patch verifies internally; re-check here anyway
    assert verify_patch_certificate(hat, res["certificate"])
    # both chiralities must occur (the hat cannot tile one-handedly)
    ops = {op for op, _, _ in res["certificate"]["placements"]}
    assert any(op >= 6 for op in ops) and any(op < 6 for op in ops)


def test_sat_phase_seed_still_produces_verified_patch():
    res = sat_grow_patch(HEXAGON, 30, phase_seed=7)
    assert res["completed"]
    assert res["stats"]["phase_seed"] == 7
    assert verify_patch_certificate(HEXAGON, res["certificate"])


def test_certificate_tamper_rejected():
    res = sat_grow_patch(HEXAGON, 30)
    cert = res["certificate"]
    assert verify_patch_certificate(HEXAGON, cert)

    dropped = dict(cert, placements=cert["placements"][1:])
    assert not verify_patch_certificate(HEXAGON, dropped)

    duplicated = dict(cert, placements=cert["placements"] + [cert["placements"][0]])
    assert not verify_patch_certificate(HEXAGON, duplicated)

    bad_op = dict(cert, placements=[[99] + cert["placements"][0][1:]] + cert["placements"][1:])
    assert not verify_patch_certificate(HEXAGON, bad_op)

    # non-center translation (breaks the grid alignment invariant)
    op0, tx0, ty0 = cert["placements"][0]
    shifted = dict(cert, placements=[[op0, tx0 + 1, ty0]] + cert["placements"][1:])
    assert not verify_patch_certificate(HEXAGON, shifted)


@pytest.mark.slow
def test_hat_chirality_ratio_sat():
    """In any hat tiling the two chiralities appear in ratio phi^4 : 1
    (Smith-Myers-Kaplan-Goodman-Strauss 2023), i.e. minority fraction
    1/(1+phi^4) ~ 0.1273.  A finite SAT-grown disk patch is not a tiling
    fragment guarantee, so allow a generous band."""
    hat = canonical_form(cells_in_polygon(HAT_OUTLINE))
    res = sat_grow_patch(hat, 2000)
    assert res["completed"]
    ops = [op for op, _, _ in res["certificate"]["placements"]]
    minority = min(sum(op >= 6 for op in ops), sum(op < 6 for op in ops))
    frac = minority / len(ops)
    assert 0.08 < frac < 0.18
