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

Session 58 subsequently derived the exact coordinate conversion and verified
a 116/116 per-shape bijection, including identical individual `H_c` values and
the three inconclusive identities. This strengthens the reproduction claim;
it does not restore any novelty claim.

## ERR-006 (2026-07-21) — The ST-M1 38-address source was misread

Sessions 65--66 claimed that the optimized `sqrt(2)-1` construction in
Akiyama--Hamada--Ito had two connected large templates of composition
`2S+L`, hence `18,18,2` common-triangle addresses. That claim is withdrawn.

The primary TeX distinguishes two constructions with the same slope. The
general construction in Section 9 has Type I composition `2S+L` and 26
possible large patch-tiles. The optimized three-prototile construction in
Section 10.1 instead has two Type I patch-tiles of composition
`12S+6M+6L`, plus one Type II `M`; this is stated explicitly in Table 1. The
six attached `M` cells in each connected large prototile were omitted when
the repository inferred `18,18,2` from the visible `2S+L` ratio.

More importantly, the later statement that cell supports can coincide at
`kappa=infinity` occurs in the separate Smith Turtle subsection. The source
does not apply that specialization to the optimized Section 10.1 system, give
a common-cell subdivision for its `12S+6M+6L` templates, or prove equivalence
of the resulting complete local languages. Replacing 38 by another guessed
integer would therefore not repair the proof.

Consequences:

- ST-M1.E-infinity and the instantiated ST-M1.S0 return to **blocked**;
- the conditional common-cell compiler ST-M1.S0C remains valid;
- the quotient criterion Q0 and the role-only/independent-rail no-go results
  N2/N1 remain valid as conditional symbolic statements;
- no raw addressed alphabet, collar/port table, or all-`M` exclusion has been
  established for the optimized system;
- the radius-one table authorized in D-0075 is halted before enumeration.

The affected historical notebooks are retained with correction notices. The
stable theory notes and proof ledger use this erratum as the controlling
status.

Session 69 subsequently resolved the geometry without undoing this erratum:
the centroid formulas give `30,30,2` common-triangle addresses after splitting
the six embedded `M` rhombi in each large template and the small `M` rhombus.
This is ST-M1.G0. Complete SAB/vertex-language transport remains open as L0,
so the withdrawn `18,18,2` proof and S0 closure remain withdrawn.

## ERR-007 (2026-07-22) — K7C settles the host footprint, not the whole strip

Theory note 22 originally claimed that K7C made the three neighbor interiors
in the entire strip `-d<y<0` exactly the three rectangles below the host.
That is false at the reflex endpoint of role `A`. With its code side directed
along positive `x`, interior below, and `ell_A=3*pi/2`, the `A` occurrence
contains a third-quadrant germ (`x<0,y<0`) outside the host footprint.

K7C proves exactly what the tail reduction needs: inside
`(0,L) x (-d,0)`, the open footprint below the host, the three interiors are
the disjoint rectangles below their code intervals. The reflex spillover is
part of the rooted tail `Q_A` and must be included in the tail-pair and
host-versus-tail intersection checks. References to the “complete strip” are
withdrawn and replaced by “host-footprint collar.”

At the same endpoint, if exactly the host and `A` occur and the neighborhood
is gaplessly covered, angle sum forces the host interior angle to be
`2*pi-3*pi/2=pi/2`. Any future K7W witness either has that right-angle host
corner or explicitly admits another participant there. K7A's selector and
K7C's stem equalities are otherwise unchanged.

## ERR-008 (2026-07-22) — Half-turn spine copies have complementary angles

Session 113's K10B role audit said that the paired copies of each `A,B,C`
length on the centrally symmetric shield spine were “the same role under
reversal.” That is false for the polygonal contact geometry being proposed.

If a carrier and its half-turn share the complete spine with disjoint
interiors, then at every paired spine vertex `p,-p` their two interior angles
sum to `2*pi`. Hence a convex intended code endpoint of angle `alpha` is
paired with a reflex auxiliary endpoint of angle `2*pi-alpha`, not another
copy of the same directed endpoint type. Length reflection alone therefore
does not recognize `A,B,C`.

Consequences:

- K10B's conditional half-turn docking lemma remains valid;
- the three mirror sides are auxiliary same-length sides, not declared code
  roles;
- intended code roles require length **and** convex endpoint context;
- the reflex copies cannot occupy an intended internal host junction because
  the host already contributes `pi` and their angle exceeds `pi`; and
- every future contact-completeness proof must nevertheless exclude other
  uses of those same-length auxiliary sides.

No coordinate or polygon claim depended on the incorrect role sentence.
The session-114 stop fires before the skeleton is promoted.

## ERR-009 (2026-07-22) — N26 does not apply at terminal spine vertices

ERR-008 and the original N26 proof correctly derive complementary carrier
angles at every **nonterminal** vertex of the shared K10B spine, where the two
half-turn occurrences locally fill a disk. They then incorrectly apply that
identity to both endpoints of all three paired code sides.

The `A` sides are the first and last edges of the spine. At their terminal
vertices `R,Q`, the two occurrences fill only the corner of the right-angle
guard lens. With `R=(-d/sqrt(2),0)` and
`Gamma=(0,d/sqrt(2))`, the vectors from `R` to `Gamma` and `-Gamma` are
perpendicular, so the paired terminal carrier angles sum to `pi/2`, not
`2*pi`. The internal endpoint of each paired `A` side still satisfies N26.
Both endpoints of `B,C` are nonterminal and still satisfy N26.

Consequences:

- K10B's half-turn docking and K11S's general atomic-root theorem survive;
- paired `B,C` sides are reflex at both endpoints when their intended mates
  are convex;
- paired `A` has one reflex internal endpoint and one convex terminal
  lens-corner endpoint, so it cannot be treated as a two-reflex atomic root;
- N27 remains valid endpoint by endpoint, but does not by itself settle the
  terminal `A` context; and
- K10B must be tested against K11S using complete root-cover data rather than
  the discarded shortest-reflex-side shortcut.

No polygon, coordinate or tiling claim had been promoted. The error was found
while applying the synchronization theorem, before any coordinate work.
