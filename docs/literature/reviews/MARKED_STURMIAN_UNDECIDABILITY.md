# Marked one-polygon Sturmian realization: the exact undecidability boundary

**Audit date:** 2026-07-28  
**Primary source:** Jack Stade, *Two Tiling is Undecidable*, arXiv:2506.11628  
**Catalog ID:** `stade-two-tiling-2025`  
**Cached PDF SHA-256:**
`765aa26361a2f1026333972e710b5ff2760401e5c1c0791ff374862bb66ecf2a`

## Question

Does the published one-prototile construction preserve enough of the
simulated tiling to strengthen ordinary tileability-undecidability to the
existence of a total local factor onto the fixed AHI Sturmian source?

## Source findings

The answer is yes **with finite edge-to-edge matching rules retained**.

1. Lemma 4 proves that every valid tiling by the connected stick prototile is
   a weave tiling.  This is an all-tilings converse, not merely a construction
   of one intended tiling.
2. Sections 2.3--2.5 recover a diagonal lattice of gaps.  A gap's state and
   its two bounded integer values are read from the bucket and its position.
   Lemmas 6--9 prove that these data exactly characterize the schematics.
3. Four locally recognizable encoding states store the simulated `A/B` tile
   index.  Lemmas 12 and 14 recover the alternating `A/B` tiling and its
   matching colors from every complete schematic.
4. Lemma 5 is the local Wang-to-`A/B` recoding.  The private color attached to
   a Wang-tile index forces the corresponding `A/B` pieces into its
   `S`-tetromino, so the Wang symbol is recovered locally.
5. Theorem 15 composes both directions and proves that the one marked stick
   tiles exactly when the input Wang system tiles.

All parameters in the construction are finite functions of the input tile
set.  Consequently the converse decoder has a finite, computable radius.
The paper phrases the last step after choosing row and column labels; this is
not a nonlocal origin choice.  Encoding-state rows and whether a gap stores an
`A` or `B` index are visible in the bounded schematic.  Changing the labels
only translates the recovered macrogrid.

The construction initially forbids reflections.  The end of Section 3 gives
an additional finite edge rule forcing all sticks to have common handedness,
so the result is unchanged if reflected copies are admitted.

## What follows and what does not

Given the fixed nonempty AHI source Wang presentation `Y` and an arbitrary
Wang shift `W`, apply Stade's construction to the product `Y x W`.  Every
valid marked-stick tiling then has a total finite-radius factor to `Y`, while
such a tiling exists exactly when `W` is nonempty.  This proves the marked
geometric undecidability theorem in theory note 67.

This is a corollary of standard product reduction plus Stade's construction,
not a method-novelty claim.

It does **not** remove the edge matching rules.  Stade simulates those rules
geometrically using a second, noncongruent staple polygon.  Therefore the
paper proves undecidability for:

- one connected polygon **with** finite edge rules; and
- two unmarked polygonal prototiles;

but not for one connected unmarked polygon.  Claiming the latter would assume
the color-erasure theorem sought by ST-M1.  The unmarked boundary is exact,
not terminological.
