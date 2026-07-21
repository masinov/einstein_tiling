# Polykite and Hat--Turtle literature baseline

**Audit date:** 2026-07-20  
**Purpose:** define what this repository may call validation, independent
recovery, or discovery.

## Controlling primary sources

- Smith, Myers, Kaplan, Goodman-Strauss, [*An aperiodic monotile*](https://doi.org/10.5070/C64163843),
  *Combinatorial Theory* 4(1), 2024. Controlling source for the Hat,
  Turtle, the `Tile(a,b)` continuum, the finite polykite search horizon, and
  the alignment reduction.
- Smith, Myers, Kaplan, Goodman-Strauss,
  [*A chiral aperiodic monotile*](https://escholarship.org/uc/item/4xn41982),
  *Combinatorial Theory* 4(2), 2024. Controlling source for `Tile(1,1)` under
  orientation-preserving motions and for the Spectre constructions.
- Kaplan, [*The Path to Aperiodic Monotiles*](https://arxiv.org/abs/2509.12216),
  2025. Author review used only for the later large-search report and the
  statement of open directions; it is not substituted for the two proofs
  above.

## Claim matrix

| ID | Claim | Evidence class | Consequence here |
|---|---|---|---|
| LIT-PK-01 | Up to scale, the positive `Tile(a,b)` polygons form a one-parameter family. For `a,b>0`, `a!=b`, their tilings are combinatorially equivalent to Hat tilings and the tiles are strongly aperiodic. | Peer-reviewed theorem: Section 6, especially Theorem 6.1, plus the Hat aperiodicity theorem. | Hat and Turtle are representatives, not isolated discoveries. |
| LIT-PK-02 | `Tile(a,a)`, `Tile(a,0)`, and `Tile(0,b)` admit periodic tilings. | Peer-reviewed constructions and Section 6 conclusion. | These are the exceptional similarity classes. |
| LIT-PK-03 | Hat is `Tile(1,sqrt(3))`; Turtle is `Tile(sqrt(3),1)`. | Peer-reviewed definition in Section 6. | Exact canonical anchors are required in the code. |
| LIT-PK-04 | `Tile(1,k sqrt(3))` and `Tile(k sqrt(3),1)` are polykites for every positive odd integer `k`. | Peer-reviewed statement in Section 6. | The known polykite family is infinite; a finite named-key registry can never be a complete deduplicator. |
| LIT-PK-05 | No other aperiodic `n`-kites occur for `n <= 24`, as verified by the authors' computer search. | Published exhaustive-computation report in Section 6. The paper states `24`, not `21`. | Every repository result through `n=24` is validation, census reproduction, or method development—not a new-polykite discovery. |
| LIT-PK-06 | If a finite polykite set admits a tiling with one of the listed periodicity properties, it admits one aligned to a common Laves grid (apart from the explicitly handled monokite/half-turn presentation). | Peer-reviewed Appendix A, Lemmas A.1, A.3, and A.5. Lemma A.6 further proves every Hat tiling aligned. | The planned W4 alignment bridge is not a missing prerequisite for excluding periodic polykite tilings. Stronger claims that *every* tiling of an arbitrary polykite is aligned remain separate. |
| LIT-CH-01 | `Tile(1,1)` has a mixed-handed periodic tiling, but every orientation-preserving tiling is nonperiodic. | Peer-reviewed chiral paper. | It is weakly chiral aperiodic, not an ordinary Einstein when reflections are allowed. |
| LIT-CH-02 | Replacing the edges of `Tile(1,1)` by suitable non-straight smooth paths yields families of strictly chiral Spectres; the paper does not characterize all Spectres. | Peer-reviewed Lemma 2.1 and Theorem 2.2. | “Spectre” denotes a construction family/combinatorial tiling class, not one isolated geometry. The paper leaves some path regularity cases open. |
| LIT-PK-07 | A later search of about 500 billion polykites found no unusual behavior beyond the Hat--Turtle anomaly. | Kaplan 2025 author review, not a complete published certificate corpus. | Naively starting at `n=25` is technically beyond the proved finite horizon but does not establish a credible unexplored computational frontier. |
| LIT-OPEN-01 | The cited work does not classify polykites of arbitrary size and does not prove that every aperiodic polykite belongs to `Tile(a,b)`. | Logical scope of LIT-PK-05 and Kaplan's open-problem discussion. | General polykite classification remains open. |

## Current-literature snapshot

Targeted searches on 2026-07-20 for new Euclidean planar aperiodic monotiles,
aperiodic polykites, and post-Spectre independent families found subsequent
work on proofs, dynamics, diffraction, physical realizations, applications,
and group monotiles, but no published proof of a combinatorially independent
connected unmarked Euclidean-plane family. This is a dated search result, not
a theorem of nonexistence, and must be refreshed before any novelty claim.

The 2025 paper
[*Graph Theoretic Analyses of Tessellations of Five Aperiodic Polykite Unitiles*](https://doi.org/10.3390/math13182982)
lists Hare, Red Squirrel, and Gray Squirrel as periodic in its Table 5. It is
useful as a secondary pointer for those named shapes, but its terminology and
table also mix periodic and nonperiodic examples in ways unsuitable for a
controlling classification source. Those shapes must not be treated as new
Einsteins on that paper's title or prose alone.

## Mandatory promotion checks

For a polykite survivor, record all of the following before using “new
candidate” language:

1. canonical key and exact geometry;
2. cell count and comparison with the published `n<=24` horizon;
3. exact comparison with named anchors;
4. membership test against the infinite polykite part of `Tile(a,b)`;
5. allowed isometry group (reflections allowed or forbidden);
6. a current primary-source literature search with dated queries;
7. whether the result is theorem, machine certificate, finite evidence, or
   heuristic prioritization.

The production gate in `src/einstein/e1_candidates.py` is intentionally
fail-closed: `n<=24` is ineligible, and `n>24` remains blocked until the
`Tile(a,b)` family audit is supplied.

## Program impact

- E1 remains valuable as a blind validation experiment. Its whole `n<=16`
  corpus is inside a published classified range.
- The frozen E2 plan (`n approximately 22--24`, described as beyond the known
  horizon) is factually invalid and is superseded by ERR-004.
- Existing Turtle W1--W3 computations remain exact independent-control and
  certificate-method results. They are not evidence for a new tile.
- The W2 parity/cokernel layer has now been compared with classical generalized
  coloring and torus tile-homology sources
  (`conway-lagarias-tiling-groups-1990`,
  `lidjan-baralic-flat-surface-homology-2021`). Its thin Turtle formula is a
  worked control, not a new invariant method or a new aperiodicity theorem.
- W4 may study stronger all-tilings rigidity or extensions to other
  substrates, but it is no longer the missing bridge for polykite periodicity.
