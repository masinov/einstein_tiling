"""A2 corona/Heesch engine validation.

Anchors: tilers must grow coronas to any requested depth (single kite, and
the hat -- aperiodic but a tiler, so its coronas never stop); the unique
non-tiling 2-kite must get a small exact Heesch number by exhaustion.
"""

from einstein.polykites.coronas import (
    has_hole,
    heesch_search,
    ring,
    verify_heesch_certificate,
)
from einstein.geometry.kite_grid import (
    cell_vertices,
    cells_at_point,
    cells_in_polygon,
    canonical_form,
)
from einstein.polykites.enumeration import enumerate_free_polykites
from einstein.polykites.periodic_quotients import find_periodic_tiling
from einstein.polykites.known_shapes import HAT_OUTLINE


def test_cells_at_point_consistency():
    for cell in [(0, 0, d) for d in range(6)] + [(2, 2, 1), (-2, 4, 5)]:
        for v in cell_vertices(cell):
            inc = cells_at_point(v)
            assert cell in inc
            assert len(inc) in (3, 4, 6)
            # every incident cell really has v as a corner
            for c2 in inc:
                assert v in cell_vertices(c2)


def test_ring_of_single_kite():
    r = ring(frozenset([(0, 0, 0)]))
    # 5 same-hex kites + kites of 3 neighboring hexes sharing the two short
    # edges and the vertex/midpoint corners; all share >= 1 vertex
    assert (0, 0, 1) in r and (0, 0, 5) in r
    assert all(c != (0, 0, 0) for c in r)
    # geometric constant: 5 same-hex kites + 2 at midpoint M0 (hex (2,2))
    # + 2 at midpoint M5 / vertex V0 (hex (4,-2)); verified by hand
    assert len(r) == 9


def test_hole_detection():
    # a full hexagon has no hole
    hexagon = frozenset((0, 0, d) for d in range(6))
    assert not has_hole(hexagon)
    # a hexagon missing one kite, surrounded by its ring, encloses that kite
    ring1 = ring(hexagon)
    punctured = (hexagon - {(0, 0, 3)}) | ring1
    assert has_hole(punctured)


def test_single_kite_grows_to_cap():
    res = heesch_search(((0, 0, 0),), depth_cap=2, node_budget=100_000)
    assert res["reached_cap"] and res["depth"] == 2
    assert verify_heesch_certificate(((0, 0, 0),), res["certificate"])


def test_nontiling_2kite_exact_heesch():
    forms2 = None
    for n, forms in enumerate_free_polykites(2):
        if n == 2:
            forms2 = forms
    nontilers = [s for s in forms2 if find_periodic_tiling(s, k_max=6)[0] is None]
    assert len(nontilers) == 1  # matches Myers
    res = heesch_search(nontilers[0], depth_cap=2, node_budget=200_000)
    assert not res["reached_cap"] and not res["exhausted"], "should be exact"
    assert res["depth"] in (0, 1)  # small; exact value recorded in notebook
    if res["certificate"]:
        assert verify_heesch_certificate(nontilers[0], res["certificate"])


def test_hat_grows_to_cap2():
    hat = canonical_form(cells_in_polygon(HAT_OUTLINE))
    res = heesch_search(hat, depth_cap=2, node_budget=300_000)
    assert res["reached_cap"], "the hat tiles the plane; coronas must not stop"
    assert verify_heesch_certificate(hat, res["certificate"])


def test_tampered_heesch_certificate_rejected():
    res = heesch_search(((0, 0, 0),), depth_cap=1, node_budget=50_000)
    cert = res["certificate"]
    bad = [cert[0][:-1]]  # remove one corona tile: ring uncovered
    assert not verify_heesch_certificate(((0, 0, 0),), bad)
