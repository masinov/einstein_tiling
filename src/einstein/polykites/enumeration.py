"""Enumerate free polykites on the exact kite grid.

Free = up to the full symmetry group of the substrate (rotations, reflections,
translations).  Enumeration is breadth-first by cell count with canonical-form
deduplication: every connected (n+1)-cell shape contains a connected n-cell
shape (remove a spanning-tree leaf), so growing each free n-form by one
exterior neighbor and canonicalizing reaches every free (n+1)-form.

Validation anchor: free polykites are OEIS A057786
1, 2, 4, 10, 27, 85, 262, 873, 2917, 10011, 34561, 120815, ...
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
import struct

from einstein.geometry import kite_grid

OEIS_A057786 = [
    1, 2, 4, 10, 27, 85, 262, 873, 2917, 10011, 34561, 120815, 424468,
    1501441, 5334181, 19035075, 68167472, 244928324, 882555803,
]

_COMPILED_HEADER = struct.Struct("<4sBBHQ")


def enumerate_free_polykites(n_max: int) -> Iterator[tuple[int, set[tuple]]]:
    """Yield (n, set-of-canonical-forms) for n = 1 .. n_max."""
    level = {kite_grid.canonical_form([(0, 0, 0)])}
    yield 1, level
    for n in range(2, n_max + 1):
        nxt = set()
        for shape in level:
            occupied = set(shape)
            grown = set()
            for cell in shape:
                for nb in kite_grid.cell_neighbors(cell):
                    if nb not in occupied and nb not in grown:
                        grown.add(nb)
                        nxt.add(kite_grid.canonical_form(shape + (nb,)))
        level = nxt
        yield n, level


def count_free_polykites(n_max: int) -> list[int]:
    return [len(forms) for _, forms in enumerate_free_polykites(n_max)]


def read_compiled_polykites(path: str | Path) -> Iterator[tuple]:
    """Stream canonical forms from `tools/a0_polykites.rs` binary output."""
    with open(path, "rb") as source:
        raw = source.read(_COMPILED_HEADER.size)
        if len(raw) != _COMPILED_HEADER.size:
            raise ValueError("truncated compiled A0 header")
        magic, version, n, reserved, count = _COMPILED_HEADER.unpack(raw)
        if magic != b"A0PK" or version != 1 or reserved != 0:
            raise ValueError("unsupported compiled A0 file")
        record = struct.Struct(f"<{n}H")
        for _ in range(count):
            raw = source.read(record.size)
            if len(raw) != record.size:
                raise ValueError("truncated compiled A0 record")
            cells = []
            for code in record.unpack(raw):
                cells.append((
                    2 * ((code >> 9) & 63),
                    2 * (((code >> 3) & 63) - 32),
                    code & 7,
                ))
            yield tuple(cells)
        if source.read(1):
            raise ValueError("trailing data in compiled A0 file")
