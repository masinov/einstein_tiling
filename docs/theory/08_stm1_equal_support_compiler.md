# ST-M1.S0 — equal-support colored compiler and source gap

**Date:** 2026-07-21

**Status:** compiler and minimal source specialization proof-draft; entropy
transport unproved

**Primary source:** `akiyama-hamada-ito-sturmian-2026`, Sections 6, 8.1,
10.1--11

This note asks a narrower question than ST-M1: before colors can be encoded by
one unmarked shape, does the audited source actually provide a finite colored
system in which every tile already has one common support?

The answer has two parts. There is an elementary finite compiler from
connected macrotiles over a common cell to colored copies of that cell. The
source does not state the corresponding specialization for its
positive-entropy `sqrt(2)-1` system, but Definitions 4--5 and the explicit
templates suffice to derive the **minimal aperiodic colored specialization**.
They do not yet prove that positive entropy survives this recoding.

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

Accordingly, session 64 left S0C as a proof-draft lemma and E-infinity open.
The following section records the exact follow-up derivation rather than
silently attributing it to the source.

## 5. E-infinity derivation for the minimal target

### The common primitive cell

In the cabinet form, a rectangular cell is bounded by two consecutive lines
in each of two directions. Equidistancing replaces both possible corridor
widths by one common width. All rectangular supports therefore become one
parallelogram up to the three cyclic orientations. In the isometric form this
is the `60/120` rhombus of the trigonal lattice.

Definition 4 already cuts every `S_R` and `L_R` rhombus along the distinguished
diagonal into its two triangular cells. Split each `M_R` rhombus along the
same marked diagonal. This is compatible with the paper's systematic use of
the multiset `2M`. Every primitive support is now one equilateral triangle
`C_infinity`, up to isometry. The split only refines a colored source tile; it
does not assert that the unmarked triangle is aperiodic.

The same subdivision applies to the isometric cells in Section 10.1. The
construction is cyclic in `a,b,c`; at equal corridor width the three
orientations differ by rotations of the trigonal cellulation. Thus item 1 of
E-infinity holds with a nondegenerate periodic triangular cell.

### The three templates and the raw alphabet

Section 10.1 defines each `S` and `L` hexagonal patch as six triangular cells.
Both large prototile supports have composition `2S+L`, hence contain

```
2*6 + 1*6 = 18
```

primitive triangles. They are two different connected arrangements of the
same composition. The small `M` diamond contains the two halves of one
rhombus. Consequently the three connected templates transport to
`18,18,2` primitive cells. Before orientation, SAB, and collar refinements,
the macro-address alphabet has 38 states. Reflected occurrences are handled
as collared handed states of the same macro support. This proves item 2.

### Complete language transport

Take the complete finite one-corona atlas of the original subdivided
three-prototile system. It is finite because the source assumes edge-to-edge
FLC and has finitely many prototiles, cell addresses, SAB patterns, and
isometries modulo each support's stabilizer. Transport the following data to
`C_infinity`:

- macro type, handedness, and primitive-cell address;
- original `S/M/L` type and the half of a split `M` cell;
- the SAB segment and its continuation state;
- the complete collared source edge and vertex-star type.

Allow two colored triangles to meet only when their source collars agree on
the overlap. S0C then gives a unique finite-radius grouping into the two large
and one small macro templates. The vertex-star collar rules out a new flat
cycle that exists only after equidistancing. Conversely, transporting any
source tiling gives a legal colored triangular tiling. The two operations are
inverse at the level of the finite combinatorial tiling language. This proves
item 3 without claiming a bounded Euclidean displacement between the two
geometric realizations.

### Aperiodicity after the metric distinction is erased

The colors retain the virtual long/short corridor symbols. From any legal
colored triangular tiling, the transported atlas reconstructs the same
cabinet-cell incidence and SAB system as a legal source macrotiling. Both
large macro types contain `2S+L`, while `M` contains neither `S` nor `L`.
Consequently any periodic fundamental domain containing large macros has
exact count ratio `S:L=2:1`. For a virtual slope `beta`, the source cabinet
frequencies give

```
(1-beta)^2 / beta^2 = 2,
```

whose unique solution in `(0,1)` is `beta=sqrt(2)-1`. The all-`M` endpoint is
not on the source parabola and is excluded by the transported SAB atlas. This
is the projective composition restriction in this special case.

If the colored triangular tiling had a nonzero translational period, that
period would be a nonzero vector of the triangular cell lattice and would
periodically shift at least one of the three indexed corridor families. The
corresponding long/short bi-infinite word would be periodic. Its slope would
then be rational, contradicting `beta=sqrt(2)-1`. At least one colored
tiling exists by transporting the exhibited Section 10.1 tiling. This proves
item 4 and minimal aperiodicity.

### Disposition

E-infinity and ST-M1.S0 are therefore **proof-draft closed for the minimal
aperiodicity target**. This is our collared symbolic derivation, not a theorem
quoted from the paper. It uses external colors and atlas rules, so it is not a
monotile result.

No positive-entropy claim is made. Establishing it would require proving that
the interchangeable-pair construction transports with the correct areal
entropy normalization and that the colored triangular system covers the
complete Section 10.1 entropy-bearing language.

K1 is now logically admissible, but its input is the finite collared refinement
of the 38 raw macro-address states, not a three-symbol alphabet. Any proposed
unmarked carrier must encode this full state system or prove a smaller
aperiodicity-preserving quotient first.
