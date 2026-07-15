"""End-to-end anchor: the hat.

The hat (Smith-Myers-Kaplan-Goodman-Strauss 2023) is an 8-kite polykite.
Its outline below is taken verbatim from Kaplan's reference implementation
(hatviz, geometry.js, `hat_outline`), which uses the same hex-coordinate
convention as our kite grid (hexPt(x, y) = x*e1 + y*e2, hexagon side 2).

This test validates, end to end:
  - polygon embedding and exact point-in-polygon,
  - recovery of the hat's 8 kite cells from its outline,
  - union boundary reconstruction (must reproduce the outline),
  - area bookkeeping (8 kites),
  - that the enumerated free 8-kite polykites contain the hat.
"""

from einstein.enumeration.polyform import enumerate_free_polykites
from einstein.substrate.kitegrid import (
    boundary_cycle,
    canonical_form,
    cell_vertices,
    cells_in_polygon,
    remove_collinear,
    shoelace2,
)

# hatviz geometry.js: const hat_outline = [ hexPt(0,0), ... ]
HAT_OUTLINE = [
    (0, 0), (-1, -1), (0, -2), (2, -2), (2, -1), (4, -2), (5, -1),
    (4, 0), (3, 0), (2, 2), (0, 3), (0, 2), (-1, 2),
]


def _cyclic_variants(poly):
    n = len(poly)
    for seq in (poly, poly[::-1]):
        for i in range(n):
            yield tuple(seq[i:] + seq[:i])


def test_hat_is_8_kites():
    cells = cells_in_polygon(HAT_OUTLINE)
    assert len(cells) == 8
    # cells tile the outline exactly: areas match (one kite = 4)
    assert sum(shoelace2(list(cell_vertices(c))) for c in cells) == abs(shoelace2(HAT_OUTLINE)) == 32


def test_hat_boundary_matches_outline():
    cells = cells_in_polygon(HAT_OUTLINE)
    cyc = remove_collinear(boundary_cycle(cells))
    want = remove_collinear(list(HAT_OUTLINE))
    assert tuple(want) in set(_cyclic_variants(cyc))


def test_hat_found_by_enumeration():
    cells = cells_in_polygon(HAT_OUTLINE)
    hat_canon = canonical_form(cells)
    for n, forms in enumerate_free_polykites(8):
        if n == 8:
            assert hat_canon in forms
