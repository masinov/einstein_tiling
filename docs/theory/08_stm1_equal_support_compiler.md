# ST-M1.S0 — equal-support colored compiler and source gap

**Date:** 2026-07-21

**Status:** conditional compiler and corrected minimal source specialization
are proof drafts; the session-65 attempt remains withdrawn by ERR-006

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
corridor decoding. At this stage there was no raw address count, collar
alphabet, or K1 table. Section 8 later resolves the support/count portion but
not the language. See ERR-006 and D-0076.

## 7. Actual-composition arithmetic that survives

The corrected compositions retain a useful source-level lemma. The paper
represents a patch `xS+yM+zL` by the homogeneous point `[x:2y:z]`, because an
`M` cell has weight two. Thus both optimized large prototiles represent

```
T_I = [12 : 12 : 6],
```

and the small prototile represents `T_II=M=[0:2:0]`. Let `L` be the
projective segment they span. The source's Sturmian-cell parabola is

```
C(beta) = [(1-beta)^2 : 2*beta*(1-beta) : beta^2],  0 <= beta <= 1.
```

### ST-M1.P0 (actual-composition intersection)

`L` intersects the Sturmian parabola in exactly
`C(sqrt(2)-1)`.

**Proof.** A point of `L` other than `M` has nonzero first and third
coordinates with ratio `12/6=2`. An interior point `C(beta)` therefore lies
on `L` only if

```
(1-beta)^2 / beta^2 = 2.
```

For `0<beta<1`, taking positive square roots gives
`(1-beta)/beta=sqrt(2)`, hence `beta=sqrt(2)-1`, uniquely. Neither endpoint
of the parabola is on `L`, and `M` itself is not on the parabola.

It remains to check that the algebraic solution is on the segment rather than
merely its projective line. Put

```
a = beta^2/6,
b = beta*(1-2*beta).
```

For `beta=sqrt(2)-1`, both are positive and

```
a*[12:12:6] + b*[0:2:0]
  = [(1-beta)^2 : 2*beta*(1-beta) : beta^2]
```

in homogeneous vector representatives. Thus the intersection exists and is
unique. \(\square\)

The two noncongruent large prototiles have the same composition; `a` is their
combined density, so P0 does not constrain how that density splits between
them. In a periodic source macrotiling, exact fundamental-domain counts give
the same `S:L=2:1` ratio, but periodicity is unnecessary for P0.

The source's complete SAB rule supplies the other half of its aperiodicity
argument: every admitted colored tiling lies on the Sturmian parabola. Hence
the original all-`M` configuration is excluded because `M` is not on that
parabola. This does **not** repair E-infinity. A recoded common-support system
may admit spurious all-`M`-like tilings unless its complete local language has
a total decoder into the source. P0 fixes the target slope but supplies no
support subdivision, collar atlas, or language-equivalence theorem.

## 8. Correct common-support geometry

The source's centroid definition is enough to close the geometric half of
E-infinity without assuming its language half. Work first in cabinet
coordinates, where the three line families have equations

```
a: x+y=-A,    b: x=B,    c: y=C.
```

The triangle determined by these lines has vertices
`(B,C)`, `(B,-A-B)`, and `(-A-C,C)`, so its centroid is

```
g(B,C;A) = ((2B-A-C)/3, (2C-A-B)/3).
```

Fix the `a` line used in the definition of `H^a_{j,k}`. If consecutive `b`
and `c` gaps are `p` and `q`, the four centroids are the translates generated
by

```
u_p = p*(2,-1)/3,    v_q = q*(-1,2)/3.
```

Hence `H^a_{j,k}` is a parallelogram whose two side scales are exactly the
two corridor widths. The linear map from cabinet to isometric coordinates is

```
A = [ -1/2    1/2 ]
    [ -sqrt(3)/2  -sqrt(3)/2 ].
```

It sends `(2,-1)` and `(-1,2)` to equal-length vectors with dot product equal
to minus one half the product of their lengths. Thus when `p=q` the cell is a
`60/120` rhombus. The cyclic `b` and `c` cell families are rotations of the
same calculation.

In `SL(kappa,beta)`, every gap is `kappa` or `kappa+1`. Rescale supports by
`1/kappa` and let `kappa` tend to infinity. Both normalized gaps tend to one,
so every `S`, `M`, and `L` isometric-cell parallelogram tends to the same
nondegenerate rhombus. The source's diagonal for splitting `S` and `L` is the
one not parallel to the omitted line family. In the limiting rhombus it is
the short diagonal; it divides the rhombus into two equilateral triangles.
Split each limiting `M` rhombus along the corresponding marked diagonal.

### ST-M1.G0 (equal-support geometry)

After normalized equidistancing and the marked `M` split, all constituent
supports of the actual optimized templates are congruent equilateral
triangles in a periodic triangular cellulation. The two large and one small
templates have raw primitive-address counts

```
12 + 2*6 + 6 = 30,    30,    2,
```

respectively.

**Justification of the cellulation and connectivity.** The centroid vertices
are affine functions of the gaps. The normalized finite-`kappa` cell tilings
therefore converge locally to the rank-two periodic polygonal complex just
described. Cell areas stay positive. Away from limiting boundaries, tile
membership stabilizes; hence no positive-area gap or overlap can appear in
the limit. Splitting rhombi does not change their union. The source's three
patch-tile supports are connected topological disks, and their constituent
edge adjacencies have positive limiting length, so the same finite adjacency
graphs give connected limiting templates. \(\square\)

This resolves the numerical uncertainty left by ERR-006 but does not restore
the withdrawn proof. Tiny triangles in the generating line arrangement
collapse to vertices in the equidistant limit, potentially adding point
contacts. G0 proves common supports and connected templates, not that every
locally legal colored triangular tiling lifts to the original SAB system.

Accordingly E-infinity now has a sharp remaining lemma:

### ST-M1.L0 (language transport; open)

Construct a finite colored edge/vertex atlas on the 62 addressed triangles
such that subdivision maps every source tiling into it and every tiling in its
full local closure groups uniquely and decodes to a legal source tiling.

L0 must explicitly control the new limiting point contacts, the bent SABs,
both large geometries and their reflected occurrence, and the split halves of
each `M`. Its all-tilings direction is the all-`M` exclusion. G0 does not
authorize an enumeration of this atlas.

## 9. Session-72 language closure

Theory note `10_stm1_limit_language.md` closes the sharp remaining lemma by a
different route from the withdrawn session-65 assertion. O0 transports the
auxiliary overlap incidence, I0 proves unique physical star provenance, and
D0 uses the exact triangular-frame index cocycle to prove global consistency.
Internal ports group the `30,30,2` addresses, repeated gap symbols propagate
to three bi-infinite sequences, and source edge/SAB rules decode every legal
configuration to the optimized irrational source language.

Thus E-infinity and the minimal colored S0 close at proof-draft level. The
claim is a finite period-reflecting symbolic specialization. It is not an MLD
or topological conjugacy statement between the finite-`kappa` and limiting
Euclidean embeddings, and it supplies no positive-entropy conclusion.
