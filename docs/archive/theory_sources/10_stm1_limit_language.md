# ST-M1.L0 — limiting language and overlap semantics

**Date:** 2026-07-21

**Status:** O0 auxiliary contraction, I0 physical incidence transport and D0
global symbolic decoding are proof drafts; minimal L0 closed without an atlas
enumeration

**Primary source:** `akiyama-hamada-ito-sturmian-2026`, Section 10.1 and the
general matching rule in Section 6

## 1. Two source objects must not be conflated

Section 10.1 uses two geometrically different systems.

1. The **physical isometric-cell tiling** consists of `S^*_{j}`, `M^*_{j}`
   and `L^*_{j}` cells. The source says these cells “provide a tiling.” The
   final three patch-tiles in Figure 37 are unions of these physical cells;
   the BD construction concludes that this tile set admits tilings of
   `R^2`. The global matching rule requires physical patch-tiles to meet
   edge-to-edge and their bent SABs to continue. Here “bent SAB” is repository
   shorthand for the source's isometric-cell SAB construction in Figure 41,
   not terminology quoted from the paper.
2. The auxiliary patches `P1,P2,P3` are made from first-order **Sturmian
   triangles** and are used to construct and verify the BD correspondence.
   Only here does the source say that “tilings” is nonstandard and overlapping
   tiny triangles are permitted. Consistency on those intersections makes the
   substitution argument work.

Therefore the final finite-`kappa` physical tiling is not an overlapping
cover. The auxiliary overlap complex nevertheless carries construction data
that may be needed to identify the limiting vertex state.

## 2. ST-M1.O0 — overlap-to-decorated-vertex contraction

Let `A` be a locally finite planar family of closed polygonal auxiliary
patches. Assume:

1. distinct patch interiors intersect only in a locally finite family `D` of
   pairwise disjoint closed topological disks;
2. every nonempty positive-area intersection is one disk in `D`;
3. the family has finite local complexity, including participant identities
   and their cyclic order around each disk.

Collapse every `D in D` to a point. Decorate its image by the finite tuple
consisting of the incident auxiliary patch types, their addresses, and cyclic
order.

### Lemma O0

The quotient is homeomorphic to the plane. Images of distinct auxiliary
patches have disjoint interiors and meet at a contracted point exactly when
their preimages shared the corresponding overlap disk. The decorated point
determines the complete pre-contraction incidence. If the input family is
translation-equivariant and FLC, so is the decorated quotient.

### Proof

Choose pairwise interior-disjoint disk neighborhoods around the locally
finite disks of `D`. Within each neighborhood, a radial piecewise-linear map
contracts the inner disk to its center and is the identity on the outer
boundary. Local finiteness lets these maps be performed simultaneously; every
compact set meets only finitely many supports. The resulting quotient is a
plane because each modified neighborhood remains a disk and the maps agree
with the identity on its boundary.

Every positive-area overlap was contained in a contracted disk, so the image
patch interiors are disjoint. Conversely, the quotient identifies no points
outside those disks. Participant identities and cyclic order are recorded in
the vertex decoration, giving the inverse incidence relation. FLC leaves only
finitely many such decorations. Translation equivariance follows by choosing
the same local contraction rule for every translated disk type. \(\square\)

The source's tiny Sturmian triangles satisfy the intended hypotheses at the
combinatorial level: they are the named overlap components, form a locally
finite line-arrangement family, and have finitely many substitution incidence
types. The actual normalized `kappa` limit realizes the same contraction
geometrically because their diameters are `O(1/kappa)` while first-order
patch scales remain nonzero.

O0 does not say that the physical patch-tiles overlapped. It transports the
auxiliary coordination witness to a finite decorated vertex state.

## 3. Exact L0 factorization

Let `X_kappa` be the complete colored physical patch-tile space from Section
10.1, including edge-to-edge and bent-SAB matching. Split its six embedded
`M` rhombi and its small `M` rhombus as in G0, retaining macro addresses.

L0 factors into three obligations:

- **O0 — auxiliary contraction:** proved above. Any auxiliary BD incidence
  used by a physical macro assignment is retained at a decorated limiting
  vertex.
- **I0 — physical incidence transport:** normalized equidistancing must send
  every subdivided tiling in `X_kappa` to the G0 triangular cellulation and
  classify every new point contact by a unique prelimit edge/vertex/separated
  state. Conversely, each permitted decorated limiting star must reconstruct
  one physical source star.
- **D0 — full-language decoder:** a finite set of internal ports, edge labels,
  bent-SAB states and O0/I0 vertex decorations must force unique `30,30,2`
  macro grouping and define a total local map from **every** tiling satisfying
  those rules into the indexed source matching language.

If I0 and D0 hold, the limit system has a finite-radius period-reflecting map
to the indexed source language. P0 then fixes the irrational slope and
excludes all-`M` through the source decoder; S0 and E-infinity close for the
minimal colored target. This statement deliberately does not claim an MLD
map between the two Euclidean embeddings: changing corridor widths is a shape
deformation, not a position-preserving local derivation.

## 4. Stop conditions

The following are failures, not invitations to enlarge a radius:

- a limiting point star has two inequivalent prelimit source stars;
- the auxiliary participant/cyclic-order decoration does not determine the
  physical BD assignment;
- a split `M` half can terminate without completing its rhombus or macro;
- locally legal decorated stars admit a global configuration with no source
  lift;
- reflected large states make the decoder multivalued.

No finite atlas enumeration is authorized under HC-05. The next on-paper unit
is I0: classify point-contact provenance symbolically from the centroid/line
indices and decide whether the decorated limiting star has a unique prelimit
lift.

## 5. ST-M1.I0 — unique physical point-star provenance

The centroid formula also classifies the complete limiting vertex set. Write
the three indexed lines of a generating triangle as `a_r,b_j,c_k` and put
`s=r+j+k`. In the normalized equidistant cabinet limit, set `A=r`, `B=j`,
`C=k` in G0's formula:

```
g(r,j,k) = ((2j-r-k)/3, (2k-r-j)/3)
           = (j-s/3, k-s/3).
```

For `H^a_{j,k}`, the source takes `i+j+k=0`, fixes `r=i-1`, and uses the
four pairs `(j+epsilon,k+eta)` with `epsilon,eta in {0,1}`. Their orders are

```
s = -1 + epsilon + eta,
```

so the four vertices are

```
(j+1/3, k+1/3),  (j+1,k),  (j,k+1),  (j+2/3,k+2/3).
```

Globally, physical vertices therefore lie in three disjoint cosets:

```
V_-1 = Z^2 + (1/3,1/3),
V_0  = Z^2,
V_1  = Z^2 - (1/3,1/3).
```

The coset recovers `s`; then `(j,k)` and `r=s-j-k` are unique. Hence no two
distinct indexed source triangles collapse to one physical centroid.

The restriction to the physical order set is essential. On unrestricted
triples, `(r,j,k)` and `(r+1,j+1,k+1)` have the same centroid while their
orders differ by three. The physical vertices above have
`s in {-1,0,1}`; these are distinct modulo three, so the vertex coset selects
one actual integer `s` and removes exactly this diagonal ambiguity.

After the marked short-diagonal split, every limiting triangle edge has one
of the primitive cabinet differences

```
(2,-1)/3,  (-1,2)/3,  (1,1)/3
```

up to sign and cyclic rotation. No vertex from the three cosets lies in the
relative interior of such an edge: for the first two directions, equality of
the two fractional coordinates occurs only at an endpoint, and the third is
already the shortest step between its two endpoint cosets. Thus the limit has
no physical T-junction and no new edge crossing.

### Lemma I0

Retain on every limiting triangle its source `S/M/L` role, macro address,
split-`M` half and bent-SAB state, and retain the order class on each vertex.
Assume, as in the physical isometric-cell construction, that each generating
vertex has order `s in {-1,0,1}`. Then every decorated limiting physical
vertex star has exactly one prelimit source-star lift. Cyclic families and
global reflection give the corresponding rotated/reflected lift, not a
second lift of the same decorated star.

**Proof.** The restricted order hypothesis turns the residue class recovered
from the coset into the unique integer `s`; the calculation then recovers the
indexed generating triangle at each vertex. Primitive edges recover the same
physical incidence graph as before the limit. The transported colors restore
the corridor-width symbols erased by equidistancing. Therefore the incident
colored cells and their cyclic order reconstruct one source star. A different
lift would have to change an index, restricted order, edge incidence or
retained color, all of which are fixed. \(\square\)

I0 also sharpens the role of O0. Tiny auxiliary patches contract to decorated
vertices, but distinct **physical** cell vertices do not collapse together.
The remaining D0 problem is global/local-rule totality, not geometric
ambiguity of a point star.

## 6. Remaining D0 obligation

D0 must prove that internal address ports, source edge/SAB matches, O0
auxiliary decorations and I0 vertex stars define a finite local rule whose
every whole-plane configuration groups uniquely into source-labeled
macrotiles. The proof must cover global consistency of the order-coset labels
without selecting an absolute origin and must show that every permitted local
star participates in one indexed source lift. No enumeration is authorized.

## 7. The finite limiting presentation

Let `C_infinity` be the edge-to-edge equilateral-triangle cellulation obtained
in G0. An edge-to-edge whole-plane tiling by congruent equilateral triangles
has one global triangular frame: fixing one triangle forces the pose of every
edge-neighbor, and the dual graph is connected. Thus, up to one global
isometry, its vertices and faces have the cabinet indices of Section 5.

Define a finite color on a primitive triangle by retaining:

- the large/small macro state, its finite address and the split-`M` half;
- the directed internal-address ports of S0C;
- on exposed edges, the source patch-tile boundary and bent-SAB data;
- the line family, order coset, and narrow/wide gap symbols transported from
  the indexed source cell;
- at a contracted auxiliary vertex, the O0 participant and cyclic-order
  decoration.

The local rule has four parts. Internal ports meet only their unique
complements. Exposed ports satisfy the source edge-to-edge and SAB
continuation rule. At a vertex, order cosets and incident line families obey
the I0 star. Finally, two occurrences describing the same indexed corridor
gap carry the same narrow/wide symbol. The last equality propagates along the
connected strip of cells incident with that gap; it is a nearest-star rule,
not a global condition.

This is finite without listing a radius table. There are only three finite
macro templates (`30,30,2` addresses), finitely many directed constituent
edges, two gap values in each of three line families, finitely many SAB
segments, and finitely many O0 participant orders. Unlike a definition by
"all patches that happen to occur", every rule above is the direct transport
of specified source data or an exact address equality.

## 8. ST-M1.D0 — global symbolic lift

### Lemma D0

Every whole-plane tiling satisfying the finite presentation of Section 7
groups uniquely into complete limiting source macros and has a total,
finite-radius, translation-equivariant decoder to an indexed Section 10.1
source configuration. Its three narrow/wide corridor sequences and SABs form
a Sturmian lattice of the slope selected by the source macro system.

### Proof

Internal-address ports first recover every finite macro. The address graph of
each template is connected, so starting at any constituent triangle reaches
all `30` or `2` addresses. A second component cannot occupy the same address:
it would overlap a triangle interior. An internal obligation cannot terminate
at a macro boundary. This is exactly the S0C grouping argument, and its radius
is bounded by the largest template diameter.

It remains to show that the locally recovered source data have no global
holonomy. Choose one vertex as an index origin. Across the three primitive
edge directions, change `(r,j,k)` by the fixed integer increment read from
the cabinet frame. Around every triangular face these increments sum to zero.
Because the triangular cellulation is simply connected, every closed edge
path is a sum of face boundaries; hence its total increment is zero. The
indices obtained by path integration are therefore independent of the path.
Changing the chosen origin adds constants and changes no decoded state.

The three order-coset labels agree with these indices by I0. Gap-equality
ports make the bit between, for example, `a_r` and `a_(r+1)` independent of
the transverse cell used to read it. They therefore define three global
bi-infinite narrow/wide sequences. The exposed-edge rule makes every bent SAB
continue exactly as in the physical source, and the I0 vertex rule supplies
the same three-direction intersection state. Consequently the grouped macros,
gap sequences and SABs satisfy the source matching rule, not merely a sampled
list of its patches.

The source proves in Section 8.1 (the matching rule on pp. 39--43, followed
by the projective composition argument) that this edge-to-edge/SAB rule
produces a Sturmian lattice with some slope. The macro composition lies on
the segment spanned by
`[12:12:6]` and `[0:2:0]`; P0 shows that its only intersection with the
Sturmian parabola is `beta=sqrt(2)-1`. In particular, the apparent all-`M`
endpoint is not a decoded source configuration. Thus every legal limiting
tiling decodes to the irrational source language.

The conjugate alternative in source Theorem 4(2) adds no second slope here.
The algebraic conjugate of `beta=sqrt(2)-1` is `-1-sqrt(2)`, outside the
Sturmian parameter interval `[0,1]`. Equivalently, P0 already computed the
unique intersection on that interval.

The output attached to a rooted triangle—macro state/address, indexed source
cell, gap symbols and SAB state—is already present in a bounded neighborhood.
Grouping only adds the fixed maximum macro diameter. The decoder is therefore
finite-radius and commutes with translations of the regular frame. Reflection
transports all indices, ports and cyclic orders together. Reflected macro
states, including locally occurring reflected large macros permitted by the
source, are decoded according to their retained state; reflection does not
make that lift multivalued.
\(\square\)

## 9. Existence and period reflection

Take any physical Section 10.1 source tiling. Replace every indexed physical
cell by its G0 limiting rhombus, perform the marked split, and retain the
colors of Section 7. The exact index formula fills `C_infinity`; O0 and I0
preserve its auxiliary and physical incidences. Hence the finite limiting
system is nonempty.

Any translational period of a colored limiting tiling preserves the vertex
lattice and therefore induces a nonzero integral shift of `(r,j,k)`. D0 is
equivariant for this shift, so it would give a period of the decoded
irrational Sturmian configuration, which the source excludes. The limiting
colored system is therefore aperiodic.

This closes minimal L0, E-infinity and S0 at proof-draft level. It does **not**
prove ST-M1, produce an unmarked shape, or show positive entropy. In
particular, no topological conjugacy or surjection to the finite-`kappa`
Euclidean hull is asserted; the result is the period-reflecting colored source
needed by the minimal theorem.

The finite alphabet is specified functorially from the published finite
templates and their directed constituent edges; it has not been serialized as
an extensional collar table. Such a table would be useful for implementation
and independent checking, but its absence is why the result remains a proof
draft rather than a machine-verified certificate.

## 10. Boundary of the result

The next mathematical object would be K1: a smaller coupled contact-star
kernel whose complete local closure still decodes to this addressed system.
Q0, N1 and N2 show why simply erasing addresses or separating the three rails
is unsafe. D0 does not authorize a collar table, carrier drawing, geometric
contact search or experiment. Those require a new human checkpoint and a
separate finite proposition.
