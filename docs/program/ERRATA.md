# Errata and clarifications to the program document

The program document (`einstein_search_program.md`) is kept verbatim as the
specification. Factual errors found while implementing are recorded here,
with sources. Append-only.

## ERR-001 (2026-07-15) — "The hat being a 13-polykite" (§3.3)

The hat is an **8-kite** polykite on the Laves [3.4.6.4] grid; **13 is its
number of sides** (a tridecagon), not its cell count. Confirmed against the
SMKG paper ("An aperiodic monotile", arXiv:2303.10798) and verified
computationally in this repo: Kaplan's published hat outline contains exactly
8 kite cells (`tests/test_hat.py`). The document's later uses of polykite
horizons (§8 E1 "polykites n ≤ 16", E2 "n ≈ 22–24") are unaffected and remain
sensible budgets.

## ERR-002 (2026-07-17) — Independent disk covers are not patch growth (§4 A3)

The implementation initially treated a SAT cover of each larger disk as
evidence that a candidate "grew." That is weaker than the program's intended
frontier extension: independently solved disks may use incompatible interior
phases and sacrificial boundary crowns that cannot continue.

A3 evidence must therefore be nested. Exact placements from a smaller patch
are frozen inside a protected core while a larger region is solved. The
reported feature is the largest preserved core (and the discarded collar
depth), not merely the largest independently coverable circle. A complete
finite crown being non-extendable does not refute the tile; it refutes that
particular finite patch as a fragment of an infinite tiling.

## ERR-003 (2026-07-20) — The n=10 “finalist” is the known Turtle (§8 E1)

The shape historically promoted as “n=10 candidate 2” or the “E1 finalist,”
with compiled key
`010001010104010502f002f1030b030c04fa04fb`, is **exactly the Turtle** of
Smith--Myers--Kaplan--Goodman-Strauss, up to the canonical translation and
dihedral normalization already used by the enumerator. It is not a new shape.

This was checked without visual judgement. The primary paper's exact
`rawtileB` outline (arXiv:2303.10798 source, `00_macros.tex`) contains ten kite
cells; applying this repository's `cells_in_polygon` and `canonical_form`
produces the finalist key byte-for-byte. The identity is pinned by
`tests/test_turtle.py` and registered in `src/einstein/e1_candidates.py`.

The error was in promotion-time known-shape deduplication, not enumeration or
certificate verification. E1's specification explicitly expected the blind
funnel to surface both Hat and Turtle. The disk, diffraction, transfer,
cokernel, holonomy, and packing artifacts remain valid finite computations,
but their subject is now a **known aperiodic Turtle control**. Legacy filenames
containing `finalist` are retained for reproducibility and must be read as
aliases for Turtle.

Tilability and nonperiodicity are already established externally. In
particular, arXiv:2403.01911 gives a recursive Bricks-and-Mortar construction
and an Ammann-bar contradiction: periodicity would force rational `k/n` to
satisfy `q(1-q)=1/5`, hence `q=(5±sqrt(5))/10`. Internal W1--W3 work may seek
independent finite certificates for those known facts, but it is no longer a
proof obligation for a new-einstein claim. Novelty promotion must henceforth
classify every canonical key against the registered known-polykite anchors
before assigning candidate status.

## ERR-004 (2026-07-20) — E2 is not beyond the known polykite horizon (§8)

The program calls E2's `n≈22--24` polykite sweep “beyond the known horizon.”
That is false. Smith--Myers--Kaplan--Goodman-Strauss, *An aperiodic
monotile*, Section 6, explicitly report an exhaustive computer search with no
aperiodic `n`-kites other than Hat and Turtle for **`n≤24`**. This supersedes
ERR-001's statement that the original E2 horizon remained sensible.

The same section completely classifies the positive `Tile(a,b)` continuum:
every positive unequal pair is aperiodic and combinatorially equivalent to
Hat tilings; the three exceptional similarity classes `a=0`, `b=0`, and
`a=b` admit periodic tilings. It also identifies infinitely many polykites in
that continuum, namely `Tile(1,k√3)` and `Tile(k√3,1)` for every positive odd
integer `k`. Therefore named Hat/Turtle key comparison alone is not a
complete prior-art check even above `n=24`.

Appendix A also proves the periodic-alignment reduction the theory plan had
assigned to W4: if a polykite admits a periodic tiling under arbitrary
Euclidean placements, it admits a grid-aligned periodic tiling (Lemmas A.1,
A.3, A.5). Lemma A.6 proves the stronger statement that every Hat tiling is
aligned. W4 may still investigate stronger all-tilings rigidity or other
substrates, but it is not a missing bridge for polykite periodicity.

Consequences:

- E1 remains a validation experiment; none of its `n≤16` shapes can be a new
  aperiodic polykite under the published classification.
- E2, as frozen, is invalidated before launch and must be redesigned. Merely
  moving to `n=25` is not an adequate research justification: Kaplan's 2025
  review reports a later search of roughly 500 billion polykites with no
  other unusual behavior.
- New-polykite promotion is fail-closed pending both the finite-horizon check
  and recognition of the infinite polykite part of `Tile(a,b)`.

The controlling claim matrix and source tiers are recorded in
`docs/literature/POLYKITE_BASELINE.md`.

## ERR-005 (2026-07-21) — The A2 `n<=8` Heesch census is a reproduction

Session 03 stated that polykite Heesch numbers appeared uncharted and called
the six `H_c=2` cases through eight kites possibly novel. That prior-art claim
is withdrawn.

Kaplan's public `heesch-sat` implementation explicitly supports the polykite
grid. In an August 2023 comment on his official project page, he stated that
he had computed Heesch numbers of non-tiling polykites through roughly 16 or
17 cells. He also published a 116-page eight-kite artifact containing every
non-tiling 8-kite with positive Heesch number and three inconclusive cases.
Its aggregate counts are 108 with `H_c=1`, five with `H_c=2`, and three
inconclusive. Kaplan identifies the latter as two periodic anisohedral shapes
and the Hat. These numbers exactly match our A1+A2 partition.

The A2 implementation remains independent: it uses recursive exact-cover DFS
and cold-verifiable nested-corona certificates rather than Kaplan's monolithic
SAT encoding. Its result is therefore a useful exact reproduction and
pipeline benchmark, but not new census data. The source/algorithm crosswalk
and evidence tiers are recorded in
`docs/literature/reviews/KAPLAN_HEESCH_POLYKITES.md`.
