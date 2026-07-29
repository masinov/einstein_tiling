# Exact AHI source and carrier-local theory

**Status:** integrated benchmark and scoped obstruction dossier
**Source:** Akiyama--Hamada--Ito Section 10.1 at
`beta=sqrt(2)-1`
**Claim boundary:** no unmarked monotile, no general Sturmian nonexistence
theorem, and no entropy transfer is established

This chapter replaces the chronological reading of source notes 58--78.  It
states the exact finite source, the general reductions extracted from it, and
the specialized carrier-local theorems in dependency order.  Full derivations
and coordinate tables remain in `docs/archive/theory_sources/` and are mapped
by `../reference/SOURCE_MAP.json`.

## 1. Exact finite source

At the optimized irrational parameter, the two large physical templates have
the same role composition

```text
12 S + 6 M + 6 L,
```

and the small template is one `M` rhombus.  Splitting each physical `M` cell
along its source-marked diagonal gives common primitive triangles.  Pairing
the triangles by the continuous SAB components produces one congruent
`60/120` rhombus support.

### Theorem AHI.1 — exact common-support atlas

The pinned Section 10.1 vector figure reconstructs, uniquely up to support
isometry, to three connected common-rhombus templates with component counts

```text
15, 15, 1
```

and primitive-triangle counts

```text
30, 30, 2.
```

The two large templates together contain 30 addressed rhombus roles and the
small template one, for 31 addresses total.  Their exact internal adjacency
kernel has 44 contacts.

This is the combined finite content of `SER1`, `G0`, `K50C` and `K51K`.
It is machine verified by the source-atlas and contact-kernel certificate
families.  It transcribes a published construction; it is not a new tile.

### Theorem AHI.2 — projective composition intersection

In the source convention `[x:2y:z]`, the segment joining the large-template
composition `[12:12:6]` and the small composition `[0:2:0]` meets the
Sturmian composition parabola at exactly

```text
beta = sqrt(2)-1.
```

Both mixture coefficients are positive.

#### Proof

The first-to-third coordinate ratio on the segment is `12/6=2`.  On the
Sturmian parabola it is `(1-beta)^2/beta^2`.  Hence

```text
(1-beta)^2 / beta^2 = 2,
```

whose unique solution in `(0,1)` is `sqrt(2)-1`.  Substitution into the
homogeneous coordinates gives positive coefficients.  This is `P0`. ∎

## 2. Total colored source decoder

The common-support atlas is still colored: addresses, diagonal axes, SAB
roles and vertex incidence remain part of its finite language.

### Theorem AHI.3 — overlap contraction

Contracting a locally finite FLC family of pairwise-disjoint auxiliary
overlap disks to points preserves the plane and retains, as vertex data, the
complete participant set and cyclic order.

This elementary quotient theorem (`O0`) separates the source's auxiliary
overlapping construction patches from its physical tiling.  It applies to
any such disk family, not only AHI.

### Theorem AHI.4 — physical incidence and holonomy

For source orders `s in {-1,0,1}`, the three centroid cosets are disjoint,
every decorated physical vertex has one prelimit lift, and no limiting edge
acquires an interior vertex.  The line-index increments integrate globally:
their sum around every face is zero, so simple connectivity kills all cycle
holonomy.  Gap-equality propagation recovers the three global narrow/wide
sequences.

Consequently every legal whole-plane tiling of the complete 31-address
colored language has a finite-radius, translation-equivariant decoder to an
irrational AHI/Sturmian configuration.  This is the proof-draft chain
`I0 + D0 + L0 + S0`.

The restriction on `s` is essential.  Unrestricted indices have the diagonal
ambiguity `(r,j,k) -> (r+1,j+1,k+1)`.

### Corollary AHI.5 — colored aperiodicity

The complete 31-address common-rhombus system is aperiodic by total-decoder
period descent.  This says nothing about forgetting its finite roles.

## 3. Lossless and compressed symbolic presentations

The addressed system admits two useful exact recodings.

### Theorem AHI.6 — lossless contact incidence

Every finite addressed triangular SFT has a finite contact-incidence
presentation in which each directed half-contact names its endpoint states
and side, the three half-contacts at a cell agree on one center state, and
legal cyclic corner words retain the vertex rule.  Encoding and decoding are
inverse radius-one maps on the full rule space.

This is `K1C`, a general higher-block recoding theorem.

### Theorem AHI.7 — safe quotient contract

A finite quotient is a total exact source presentation exactly when one
bounded local decoder, evaluated on every patch admitted by the quotient
local closure,

1. assigns a source state;
2. preserves every source adjacency; and
3. re-encodes to the original quotient patch on every overlap.

Injectivity on the intended compact image implies a finite-radius inverse
there, but does not prove totality on additional quotient configurations.
These are `K1R` and `K1T`.

### Theorem AHI.8 — twelve-state corridor quotient

The exact addressed atlas has a quotient

```text
Z/3 x {0,1} x {0,1}
```

with 12 source-native local states.  The `Z/3` coordinate records corridor
axis and the two bits record the ordered rail states.  One `L` hexagon, two
`S` hexagons and six `M` connectors occur in every large macro.  The rooted
large-macro arrangement has two full-isometry classes.

The quotient is a compact source benchmark and an exact-cover target.  Pure
pose cannot carry it: internal contacts change diagonal axis, binary
handedness has an odd-cycle obstruction, and affine orientation laws do not
recover macro ownership (`N53`, `N54`, `N56`).

## 4. Minimality prevents source-language pruning

For irrational slope, the underlying Sturmian lattice hull is minimal: the
dense phase-torus translation action has no proper nonempty closed invariant
subsystem.

### Theorem AHI.9 — factor-visible contacts are essential

If a nonempty tiling system has a total finite-radius factor onto the
irrational lattice hull, its image is the whole hull.  Therefore every finite
contact cylinder visible in that factor occurs in the realization language.
One cannot evade a difficult source contact by choosing a favorable proper
component.

### Theorem AHI.10 — finite separable component reduction

For any finite independent two-participant port realization, the biclique
classification decomposes the marked language into finitely many component
schemes.  Every viable scheme must still cover the whole minimal factor.

In particular an independent rail presentation of the three irrational
Sturmian length-two bigrams closes to a biclique containing the missing
constant corner; it admits a periodic constant rail.  Thus rail-separable
realizations cannot enforce the irrational source (`N63R`).

Arbitrary finite marked extensions remain undecidable by product with an
arbitrary Wang shift (`U3`); directed-graph and fixed-width auxiliary layers
remain decidable islands.

## 5. Carrier-local composition theory

A **carrier-local** realization is one in which every decoded AHI macro lies
entirely inside one equal-area common-rhombus carrier.  This is a strong,
explicit hypothesis; a general polygon decoder may cross carrier boundaries.

Write a carrier state as `(k,m)`, where `k` is the number of large macros and
`m` the number of singleton `M` cells.  Its area is

```text
A = 15 k + m.
```

The irrational source frequency lies strictly between rational composition
slopes.  Therefore a finite equal-area state library must straddle the unique
threshold in `k`.

### Theorem AHI.11 — all-area composition phase diagram

Write `A=15q+s`, `0<=s<15`.  Carrier-local composition is possible exactly
in the admitted band described by

```text
s/q < 6(sqrt(2)-1),
```

with the boundary cases interpreted as in source theorem `K66A`.  Every
viable finite state library contains states on both sides of the unique
irrational composition cut.

### Corollary AHI.12 — count-changing trade

At every area, a carrier-local compiler contains two states on one support
whose large-macro counts differ.  Equal area then exchanges exactly 15
singleton cells for each large macro.  Thus every such compiler contains a
finite count-changing AHI trade (`K66T`).

This replaces an unbounded search over carrier area by one structural
obligation: realize a legal same-support count-changing trade.

## 6. Exact finite lower bounds

The small-area classifications are applications of the phase diagram and a
source-native parity gate.

### Theorem AHI.13 — below area 30

Below 30, frequency permits only areas 15, 16 and 17, with both states
`(1,A-15)` and `(0,A)` essential.  The all-singleton state has a
long-diagonal continuation graph that must be bipartite.

The complete geometric superset contains 997 supports and 29,443 lozenge
subdivisions.  Every continuation graph is nonbipartite.  Hence no connected
common-rhombus carrier of area below 30 admits a carrier-local compiler to the
exact AHI source (`N64S`).

### Theorem AHI.14 — area 30

Every viable area-30 library contains `(2,0)` and at least one of `(1,15)` or
`(0,30)`.  Exhaustive full-isometry classification gives 65 two-large
supports, 164 contained-large embeddings, 3,390 residual `(1,15)` matchings
and 48,652 `(0,30)` matchings.  None passes the bipartite continuation gate.
Therefore area 30 is also impossible under carrier locality (`N65S`).

The finite censuses are machine verified.  They do not imply an area lower
bound for arbitrary unmarked monotiles.

## 7. Directional and boundary-active reduction

The all-area trade has additional structure.

### Theorem AHI.15 — matching-independent orientation counts

For a finite triangular-cell region admitting a lozenge matching, the counts
of lozenges in the three orientations depend only on the support, not on the
perfect matching.

#### Proof sketch

Sum the barycenter displacement vectors contributed by every matched pair.
The boundary region fixes the total displacement and area.  The three
orientation vectors have the single known linear dependence, while total
lozenge count supplies the remaining equation.  Hence the orientation count
vector is fixed.  This is the standard dimer-flux lemma `K67O`. ∎

### Theorem AHI.16 — synchronized directional deficit

For each axis `j`, an expanded AHI state satisfies

```text
S_j = 2k,       L_j = k,       M_j = N_j-3k.
```

A count-changing trade therefore changes all three directional `M` counts by
the same `-3 Delta k`.  SAB continuation decomposes

```text
N_j-3k = chi_j + 2p_j,
```

where `chi_j` is exposed binary Gauss charge and `p_j` counts hidden
transition pairs (`K67D`, `K67G`).

Per-axis parity cannot exclude even trades: a fixed-endpoint binary corridor
supports excursions changing transition count by two (`N67C`).

### Theorem AHI.17 — no boundary-neutral count trade

No two globally admissible same-support AHI patches with identical complete
marked boundary differ in large-macro count.  Replacing one by the other
would create a compactly supported difference in the global corridor fields,
but every changed rail bit propagates along an unbounded strip.  The
directional deficit then forces the macro counts to agree (`N68H`).

### Corollary AHI.18 — residual carrier-local class

Every surviving carrier-local realization must be simultaneously:

- boundary-active;
- joint across all three rails; and
- contextual rather than participant-separable.

This is a family reduction, not an existence theorem.

## 8. The exact parity hyperedge

At one indexed tiny-triangle vertex, the three rail bits form

```text
E_3 = {000,110,101,011}.
```

Its incidence lattice is the set of integer triples with even coordinate
sum.  This is `K68V`.

The general theory proves that ordinary sector stars and every finite family
of participant-wise additive tests over a two-torsion-free group accept the
whole cube whenever they accept `E_3`.  Therefore the remaining carrier-local
mechanism must use at least one of:

1. an independently visible auxiliary star state;
2. a non-ordinary multi-participant contact hyperedge; or
3. a proved larger-radius all-tilings exclusion.

Rooted T-junction automata can express `E_3`, but do not force their roles or
topology using one unmarked support.

## 9. What has and has not been classified

The integrated carrier-local conclusion is:

```text
sub-30 carriers                     impossible
area-30 carriers                    impossible
boundary-neutral trades, all areas  impossible
rail-separable schemes              periodic
ordinary/additive parity stars      insufficient
boundary-active contextual carriers open
```

No result here excludes decoders spanning carrier boundaries, a different
Sturmian source presentation, nonseparable contact complexes, or arbitrary
connected polygons.

## 10. Certificate and proof-source map

| Result family | Cold-verifiable artifact |
|---|---|
| Exact supports and SAB pairs | `data/sturmian-source/ahi-section10-supports.json` |
| Contact kernel | `data/sturmian-source/ahi-section10-contact-kernel.json` |
| Twelve-state quotient | `data/sturmian-source/ahi-corridor-quotient.json` |
| L-anchor selector | `data/sturmian-source/ahi-l-anchor-selector.json` |
| P17 obstruction | `data/sturmian-source/ahi-p17-all-m-obstruction.json` |
| Sub-30 census | `data/sturmian-source/ahi-sub30-carrier-classification.json` |
| Area-30 census | `data/sturmian-source/ahi-area30-carrier-classification.json` |

Exact scopes, dependencies and verifier commands remain in
`../reference/proof_ledger.md`.  Full proofs and corrected intermediate
calculations are preserved in source notes 58--78 under
`docs/archive/theory_sources/`.
