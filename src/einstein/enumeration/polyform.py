"""A0 -- substrate enumeration of free polyforms.

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

from einstein.substrate import kitegrid

OEIS_A057786 = [
    1, 2, 4, 10, 27, 85, 262, 873, 2917, 10011, 34561, 120815, 424468,
    1501441, 5334181, 19035075, 68167472, 244928324, 882555803,
]


def enumerate_free_polykites(n_max: int) -> Iterator[tuple[int, set[tuple]]]:
    """Yield (n, set-of-canonical-forms) for n = 1 .. n_max."""
    level = {kitegrid.canonical_form([(0, 0, 0)])}
    yield 1, level
    for n in range(2, n_max + 1):
        nxt = set()
        for shape in level:
            occupied = set(shape)
            grown = set()
            for cell in shape:
                for nb in kitegrid.cell_neighbors(cell):
                    if nb not in occupied and nb not in grown:
                        grown.add(nb)
                        nxt.add(kitegrid.canonical_form(shape + (nb,)))
        level = nxt
        yield n, level


def count_free_polykites(n_max: int) -> list[int]:
    return [len(forms) for _, forms in enumerate_free_polykites(n_max)]
