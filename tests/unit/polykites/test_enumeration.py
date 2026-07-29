"""A0 validation: free polykite counts must match OEIS A057786 exactly.

A057786 was computed independently (Brendan Owen; extended from Joseph
Myers' tables) -- agreement validates substrate adjacency, the symmetry
action, and canonical-form dedup all at once.
"""

import pytest

from einstein.polykites.enumeration import OEIS_A057786, count_free_polykites


def test_counts_match_oeis_through_n8():
    assert count_free_polykites(8) == OEIS_A057786[:8]


@pytest.mark.slow
def test_counts_match_oeis_through_n10():
    assert count_free_polykites(10) == OEIS_A057786[:10]
