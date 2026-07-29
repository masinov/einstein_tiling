"""Regression pins for the session-03 A2 findings.

Full evidence lives in tests/fixtures/polykites-n8.sqlite (stage
'A2-heesch'); these tests
re-derive fast slices of it from scratch so code regressions surface.

Headline result being protected: among all 1,264 free polykites n <= 8, the
hat is the UNIQUE shape whose coronas keep growing (depth cap 4 reached);
six shapes have H_c = 2 exactly, first appearing at n = 7.
"""

import pytest

from einstein.db import deserialize_cells
from einstein.enumeration.polyform import enumerate_free_polykites
from einstein.funnel.a1_torus import find_periodic_tiling
from einstein.funnel.a2_heesch import heesch_search
from einstein.substrate.kitegrid import canonical_form, cells_in_polygon
from tests.test_hat import HAT_OUTLINE

# one of the six H_c = 2 polykites found in session 03 (shape id 502);
# its 7-cell subshape below (id 238) is the unique n=7 H_c = 2 polykite
H2_8KITE = deserialize_cells("0,0,0;0,0,1;0,0,2;0,0,3;2,2,4;2,2,5;4,-2,1;4,-2,2")
H2_7KITE = deserialize_cells("0,0,0;0,0,1;0,0,2;2,2,4;2,2,5;4,-2,1;4,-2,2")


def test_h2_8kite_exact():
    res = heesch_search(H2_8KITE, depth_cap=3, node_budget=2_000_000)
    assert res["depth"] == 2 and not res["reached_cap"] and not res["exhausted"]


def test_hat_reaches_depth_3():
    hat = canonical_form(cells_in_polygon(HAT_OUTLINE))
    res = heesch_search(hat, depth_cap=3, node_budget=2_000_000)
    assert res["reached_cap"] and res["depth"] == 3


@pytest.mark.slow
def test_heesch_census_n6():
    """Exact H_c distribution over all A1 survivors with n <= 6:
    H=0: 30 shapes, H=1: 16 shapes, nothing deeper."""
    dist: dict[int, int] = {}
    for n, forms in enumerate_free_polykites(6):
        for shape in forms:
            if find_periodic_tiling(shape, k_max=12)[0] is not None:
                continue
            res = heesch_search(shape, depth_cap=2, node_budget=500_000)
            assert not res["reached_cap"] and not res["exhausted"]
            dist[res["depth"]] = dist.get(res["depth"], 0) + 1
    assert dist == {0: 30, 1: 16}
