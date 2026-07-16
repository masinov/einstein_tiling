"""Pinned candidates promoted from the complete blind E1 n<=16 screen.

The compiled A0/A1/A2 streams are reproducible but intentionally git-ignored
because they occupy gigabytes.  Shape keys promoted into later funnel stages
are pinned here so A3/A4 artifacts remain reproducible from a clean checkout.
"""

SMALLEST_DEPTH3_KEYS = {
    10: (
        "0100010101020103030c030d0514051507020703",
        "010001010104010502f002f1030b030c04fa04fb",
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
