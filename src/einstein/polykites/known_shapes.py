"""Pinned shapes promoted from the complete blind E1 n<=16 screen.

The compiled A0/A1/A2 streams are reproducible but intentionally git-ignored
because they occupy gigabytes.  Shape keys promoted into later funnel stages
are pinned here so A3/A4 artifacts remain reproducible from a clean checkout.

Known-shape identity is recorded here as part of promotion.  In particular,
the shape historically called the "n=10 finalist" is exactly the Turtle of
Smith--Myers--Kaplan--Goodman-Strauss, not a new candidate.  Legacy artifact
filenames retain ``finalist`` so old certificates remain addressable.
"""

HAT_KEY = "0100010101020105030c030d04fa04fb"
TURTLE_KEY = "010001010104010502f002f1030b030c04fa04fb"

# Kaplan's published ``hat_outline`` in the same coordinate convention.
HAT_OUTLINE = (
    (0, 0), (-1, -1), (0, -2), (2, -2), (2, -1), (4, -2), (5, -1),
    (4, 0), (3, 0), (2, 2), (0, 3), (0, 2), (-1, 2),
)

# The exact vertex outline used by the primary Hat/Turtle paper's ``tileB``
# macro (arXiv:2303.10798, source file 00_macros.tex).  Coordinates use the
# same hex basis as ``substrate.kitegrid`` and Kaplan's hat reference data.
TURTLE_OUTLINE = (
    (0, 0), (-2, 1), (-2, 0), (-3, 0), (-2, -2), (2, -4), (3, -3),
    (4, -4), (5, -4), (4, -2), (2, -1), (2, 0), (1, 1),
)

KNOWN_POLYKITE_KEYS = {
    HAT_KEY: "hat",
    TURTLE_KEY: "turtle",
}

# Smith--Myers--Kaplan--Goodman-Strauss, *An aperiodic monotile*, Section 6:
# their exhaustive computer search found no other aperiodic n-kites for n<=24.
# This is a literature-governance boundary, not a certificate produced here.
PUBLISHED_APERIODIC_POLYKITE_HORIZON = 24

SMALLEST_DEPTH3_KEYS = {
    10: (
        "0100010101020103030c030d0514051507020703",
        TURTLE_KEY,
    ),
    12: (
        "010001010102010502f10308030b030c030d04fa04fb0703",
        "0100010101020103010502f1030b04f804f904fa04fb04fc",
        "0100010101020103010502f1030d04f904fa04fb04fc04fd",
        "010001010118011d0309030a030b030c04fa04fb05110512",
        "0100010101020105030c030d04fa04fb04fc04fd06e806e9",
        "0100010101020103030b030c04f904fa0701070207030704",
        "01000101010201030308030d04f904fa0702070307040705",
        "010001010102010502f102f2030a030b04f904fa04fb04fc",
    ),
}


def known_polykite_name(key: str) -> str | None:
    """Return the published name of a canonical key, if one is registered."""
    return KNOWN_POLYKITE_KEYS.get(key)


def is_novel_polykite_key(key: str) -> bool:
    """Return whether a key is absent from the small named-shape registry.

    This tests key identity only.  It is deliberately *not* sufficient for an
    aperiodic-monotile novelty claim; use ``aperiodic_discovery_status``.
    """
    return known_polykite_name(key) is None


def aperiodic_discovery_status(
    n: int,
    key: str,
    *,
    tile_ab_member: bool | None = None,
) -> str:
    """Fail-closed literature status for a polykite promotion.

    Above the finite published horizon, the infinite polykite subfamily of
    ``Tile(a,b)`` still has to be recognized.  Until a caller supplies that
    audit, the shape is not discovery-eligible.
    """
    known = known_polykite_name(key)
    if known is not None:
        return f"known-{known}"
    if n <= PUBLISHED_APERIODIC_POLYKITE_HORIZON:
        return "published-classified-horizon"
    if tile_ab_member is None:
        return "tile-ab-audit-required"
    if tile_ab_member:
        return "known-tile-ab-family"
    return "eligible"


def is_aperiodic_discovery_eligible(
    n: int,
    key: str,
    *,
    tile_ab_member: bool | None = None,
) -> bool:
    """Return true only after both finite-horizon and family deduplication."""
    return aperiodic_discovery_status(
        n, key, tile_ab_member=tile_ab_member
    ) == "eligible"


def decode_compiled_key(key: str):
    """Decode the fixed-width canonical key emitted by tools/a0_polykites."""
    cells = []
    for offset in range(0, len(key), 4):
        code = int(key[offset:offset + 4], 16)
        cells.append((
            2 * ((code >> 9) & 63),
            2 * (((code >> 3) & 63) - 32),
            code & 7,
        ))
    return tuple(cells)


def smallest_depth3_candidates():
    """Yield ``(n, one-based index, key, shape)`` in gallery order."""
    for n in sorted(SMALLEST_DEPTH3_KEYS):
        for index, key in enumerate(SMALLEST_DEPTH3_KEYS[n], 1):
            yield n, index, key, decode_compiled_key(key)


def novel_smallest_depth3_candidates():
    """Yield aperiodic-discovery-eligible shapes (currently none at n<=12)."""
    for row in smallest_depth3_candidates():
        if is_aperiodic_discovery_eligible(row[0], row[2]):
            yield row


def unregistered_smallest_depth3_candidates():
    """Yield shapes absent from the named-key registry, without novelty claims."""
    for row in smallest_depth3_candidates():
        if is_novel_polykite_key(row[2]):
            yield row
