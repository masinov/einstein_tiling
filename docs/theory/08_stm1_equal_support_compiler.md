# ST-M1.S0 — equal-support colored compiler and source gap

**Date:** 2026-07-21

**Status:** conditional compiler proof-draft; source specialization blocked
and the session-65 attempt withdrawn by ERR-006

**Primary source:** `akiyama-hamada-ito-sturmian-2026`, Sections 6, 8.1,
10.1--11

This note asks a narrower question than ST-M1: before colors can be encoded by
one unmarked shape, does the audited source actually provide a finite colored
system in which every tile already has one common support?

The answer has one established part. There is an elementary finite compiler
from connected macrotiles over a common cell to colored copies of that cell.
The source does not state the corresponding specialization for its
positive-entropy `sqrt(2)-1` system, and the attempted repository derivation
misread the optimized template composition. The source-specific instance is
therefore still open.

## 1. Scope in the source

Section 6 defines a tile as `(support, color)`, lets the full isometry group act
on the support while preserving the color, and permits finite adjacency rules
such as Sturmian Ammann bars. Its aperiodic tile sets may have disconnected
supports in the general bounded-displacement construction.

Section 10.1 is better behaved. For `alpha=sqrt(2)-1` it explicitly gives
three prototiles up to isometry. Their supports are connected topological
disks: two large, noncongruent unions of isometric cells and one small diamond.
A reflected copy of one large tile also occurs. The construction proves
tileability, enforcement of the irrational Sturmian system, and positive
topological entropy.

Two later statements are easy to overread:

1. Section 8.1 uses `infinity^-1 SL(infinity,alpha)` as an artificial
   equidistanced/trigonal model for bounded-displacement calculations and says
   changing `kappa` preserves the combinatorial equivalence of cabinet-cell
   tilings.
2. At the end of the Turtle discussion, Section 10.2 suggests setting
   `kappa=infinity`: the supports of the cells then no longer differ, so the
   number of patch tiles *may* be reduced to one up to color.

Neither passage lists a colored common-cell alphabet for the Section 10.1
three-prototile system. Neither proves that its complete macro adjacency
language, reflected branch, or positive-entropy interchangeable pairs survive
that specialization. The word “may” is a research direction, not the missing
construction.

## 2. A general compiler that would finish the colored step

Let `C` be an edge-to-edge periodic cellulation of the plane by one polygonal
cell support, up to isometry. Let `A={A_1,...,A_m}` be a finite set of connected
macrotiles such that:

1. every `A_i` is a finite connected union of cells of `C`;
2. all legal `A` tilings use the same `C` frame, up to one global isometry;
3. macro-boundary legality is specified by a finite local atlas on exposed
   cell edges and vertex stars, including all decorations and reflected
   states.

The rule is allowed to be colored: this is an intermediate symbolic system,
not the desired unmarked monotile.

### ST-M1.S0C (equal-support compiler)

Under hypotheses 1--3 there is a finite colored prototile set `B` whose every
tile has support congruent to the single cell `C`, and the `B` tiling space is
mutually locally derivable from the subdivided `A` tiling space. In
particular, `A` is aperiodic if and only if `B` is aperiodic.

### Construction

Choose one canonical cell subdivision for every oriented/reflected macro
state. A color of `B` records:

- the macro type and handedness;
- the cell's finite address inside that macro;
- the directed internal ports leading to adjacent addresses in the same
  macro;
- on exposed cell edges, the complete original boundary and Ammann-bar data;
- enough finite collar data to identify the permitted source vertex star.

Give every internal port a unique complementary label containing the macro
type, the two cell addresses and the directed cell edge. An internal port can
therefore meet only the prescribed neighboring address. Boundary ports meet
exactly when the original collared macro-boundary rule permits them. Because
the source treats every exposed constituent edge as a patch-tile edge, no
unsynchronised maximal-segment convention is introduced by the subdivision.
The vertex collar prevents new vertex cycles made possible only by changing
the cell geometry.

The alphabet is finite because there are finitely many finite macro
templates, cell addresses, orientations modulo the finite cell point group,
and boundary labels.

### Proof

Subdividing an `A` tiling and applying the stated colors gives a legal `B`
tiling by construction. This map has radius zero once macro labels are
retained.

Conversely, start from any legal `B` tiling and one colored cell with macro
address `p`. Each internal port forces the unique adjacent address at the
unique neighboring cell. Following internal ports recovers every address in
the finite macro template because that template's cell-adjacency graph is
connected. Path independence follows from the directed address labels; two
different paths to one address demand the same cell position, while two
distinct cells there would have overlapping interiors. Boundary ports cannot
terminate an internal obligation or join two internal components.

Thus every colored cell belongs to one complete translated, rotated, or
reflected copy of its declared macro template. Different recovered copies
have disjoint interiors and cover the plane because the `B` cells do. Their
exposed ports satisfy precisely the original macro rule. Grouping is unique,
and its radius is bounded by the largest template diameter. Subdivision and
grouping are inverse local derivations.

A translational period is preserved in both directions by these local maps,
which proves the final aperiodicity equivalence. This argument also shows why
connectedness matters: the simple internal-port compiler does not locally tie
together separated components of a disconnected macro support.

## 3. What remains for the Sturmian source

To instantiate ST-M1.S0C on the Section 10.1 system, the following exact
specialization is required.

### ST-M1.E-infinity (common-cell specialization)

Construct a nondegenerate periodic cellulation `C_infinity` and subdivisions
of all three Section 10.1 prototiles such that:

1. every constituent support is congruent to the one cell of `C_infinity`;
2. all three macro templates remain finite connected cell unions, including
   the reflected large state;
3. the finite-kappa SAB and macro-boundary language transports bijectively to
   the new subdivisions;
4. every transported colored tiling still carries the irrational
   `sqrt(2)-1` Sturmian symbolic sequences, so a color-preserving translation
   cannot be a period.

Items 3--4 are necessary. Equidistancing the geometric corridors erases the
long/short metric distinction; it must survive in the colors and local rules.
Otherwise the common support is merely a periodic trigonal cellulation.

If E-infinity holds, applying S0C gives the finite colored equal-support
system required by ST-M1.S0. No entropy conclusion follows unless the
transport also preserves and covers the Section 10.1 interchangeable-pair
language.

## 4. Why E-infinity is not yet a source theorem

The source provides enough information to motivate each item, but not enough
to cite their conjunction:

- the equidistanced cabinet model is introduced for BD calculations;
- the optimized example uses isometric cells and a self-similar
  correspondence not generalized by the authors;
- the one-support sentence appears in the distinct Turtle subsection;
- no finite list of transported cell colors or contacts is given;
- no all-tilings equivalence between the finite-`kappa` optimized system and
  an infinite-`kappa` colored system is stated.

Accordingly, S0C is a proof-draft lemma and E-infinity remains open. Session
65 attempted a follow-up derivation; Section 5 retains its failure analysis.

## 5. Withdrawn E-infinity attempt

Session 65 conflated the earlier Section 9 construction with the optimized
Section 10.1 construction. The former has Type I composition `2S+L` and 26
large patch-tile possibilities. Primary Table 1 gives the latter's two large
prototiles composition `12S+6M+6L`, plus the small `M`. The computation
`2*6+1*6=18` therefore did not count either optimized connected template and
the derived `18,18,2`/38-address alphabet does not exist as proved data.

The attempted repair also applied the `kappa=infinity` one-support strategy
outside its source context. That statement occurs in the separate Turtle
subsection after a different construction. Nothing in the source establishes
that the optimized isometric cells become one congruent support while
preserving their complete SAB, vertex, and macro language. Merely splitting
more cells and announcing a revised address count would assume exactly the
language equivalence E-infinity is meant to prove.

The all-`M` exclusion was likewise circular: it invoked a “transported SAB
atlas” that had never been written or shown to be the complete local language.
It supplies no endpoint lemma independently of E-infinity.

## 6. Correct disposition

ST-M1.S0C remains a conditional proof draft. ST-M1.E-infinity and the
instantiated ST-M1.S0 are **blocked**. Their next admissible input would be an
exact source-independent construction for the actual two
`12S+6M+6L` templates and the `M` template, proving congruent constituent
supports, connectedness, complete local-language equivalence, and irrational
corridor decoding. Until then there is no raw address count, collar alphabet,
or K1 table. See ERR-006 and D-0076.
