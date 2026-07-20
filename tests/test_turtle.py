"""Exact primary-source identity anchor for the ten-kite Turtle.

The outline is transcribed from ``rawtileB`` in the source bundle of
Smith--Myers--Kaplan--Goodman-Strauss, *An aperiodic monotile*
(arXiv:2303.10798).  This regression prevents a known Turtle rediscovery from
again being promoted as a novel shape.
"""

from einstein.e1_candidates import (
    PUBLISHED_APERIODIC_POLYKITE_HORIZON,
    TURTLE_KEY,
    TURTLE_OUTLINE,
    aperiodic_discovery_status,
    decode_compiled_key,
    is_aperiodic_discovery_eligible,
    known_polykite_name,
)
from einstein.substrate.kitegrid import (
    canonical_form,
    cells_in_polygon,
    shoelace2,
)


def test_primary_source_turtle_is_ten_kites():
    cells = cells_in_polygon(TURTLE_OUTLINE)
    assert len(cells) == 10
    assert abs(shoelace2(TURTLE_OUTLINE)) == 40


def test_blind_e1_survivor_is_exactly_the_turtle():
    turtle = canonical_form(cells_in_polygon(TURTLE_OUTLINE))
    assert turtle == decode_compiled_key(TURTLE_KEY)
    assert known_polykite_name(TURTLE_KEY) == "turtle"


def test_literature_novelty_gate_is_fail_closed():
    unknown_key = "not-a-registered-key"
    assert PUBLISHED_APERIODIC_POLYKITE_HORIZON == 24
    assert (
        aperiodic_discovery_status(24, unknown_key)
        == "published-classified-horizon"
    )
    assert (
        aperiodic_discovery_status(25, unknown_key)
        == "tile-ab-audit-required"
    )
    assert not is_aperiodic_discovery_eligible(25, unknown_key)
    assert not is_aperiodic_discovery_eligible(
        25, unknown_key, tile_ab_member=True
    )
    assert is_aperiodic_discovery_eligible(
        25, unknown_key, tile_ab_member=False
    )
