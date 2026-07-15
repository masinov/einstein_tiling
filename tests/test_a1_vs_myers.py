"""A1 external anchor: Joseph Myers' polykite tiling census.

Source: https://www.polyomino.org.uk/mathematics/polyform-tiling/ (fetched
2026-07-16). Myers' numbers use the SAME scope as our A1: tilings where all
tiles align to one underlying [3.4.6.4] Laves tiling.

Expected periodic-capable counts per n are derived from his table as
translation + 180-degree + isohedral + (anisohedral minus aperiodic):
the n=8 anisohedral entry is 3 = two 3-anisohedral (periodic) + the hat
(k = infinity, aperiodic).

The n <= 6 check runs in the fast suite; n = 7, 8 are marked slow.
"""

import pytest

from einstein.enumeration.polyform import enumerate_free_polykites
from einstein.funnel.a1_torus import find_periodic_tiling

# n -> number of polykites admitting a grid-aligned periodic tiling
MYERS_PERIODIC = {1: 1, 2: 1, 3: 4, 4: 5, 5: 1, 6: 71, 7: 55, 8: 39}


def _count_periodic(n_max):
    counts = {}
    for n, forms in enumerate_free_polykites(n_max):
        c = 0
        for shape in forms:
            cert, exhausted = find_periodic_tiling(shape, k_max=12)
            assert not exhausted, f"budget exhausted on {shape}"
            if cert is not None:
                c += 1
        counts[n] = c
    return counts


def test_periodic_counts_match_myers_n6():
    assert _count_periodic(6) == {n: MYERS_PERIODIC[n] for n in range(1, 7)}


@pytest.mark.slow
def test_periodic_counts_match_myers_n8():
    assert _count_periodic(8) == MYERS_PERIODIC
