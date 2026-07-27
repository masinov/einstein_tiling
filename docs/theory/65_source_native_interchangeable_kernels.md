# Source-native interchangeable kernels

Exact transcription of Akiyama--Hamada--Ito Figure 45 into the normalized
31-address atlas gives two local retiling relations:

```text
3 A + 6 M  <->  3 A + 6 M       (51 rhombi),
2 A + B + 4 M  <->  2 A + B + 4 M  (49 rhombi).
```

Each side is an interior-disjoint disk and the paired supports are congruent.
These are the first same-support relations found wholly inside the admitted
physical source language; unlike K54R they need no free `S` or `L` cells.

They do not by themselves give an unmarked state.  In both cases a symmetry
of the common support carries one typed decomposition to the other.  An
equivariant radius-zero decoder on an isolated occurrence therefore cannot
distinguish the flip.  The positive-entropy use in the source is contextual:
the surrounding Sturmian frame roots an occurrence and makes the two local
choices distinct relative to that frame.

The bare supports also pass a first negative periodicity screen: neither is a
fundamental domain for any translation sublattice of the triangular lattice.
This is a complete HNF statement at forced indices 51 and 49, but does not
exclude multi-copy or orientation-changing periodic tilings and does not prove
that either common support tiles the plane.

The constructive implication is precise.  A compiler may use one of these
flips only after a finite contact neighborhood geometrically fixes its root;
the root cannot be inferred from the isolated polygon.  That requirement is
part of total decoding, not a cosmetic marking.
