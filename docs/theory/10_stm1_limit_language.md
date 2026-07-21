# ST-M1.L0 — limiting language and overlap semantics

**Date:** 2026-07-21

**Status:** O0 auxiliary contraction and I0 physical incidence transport
proof drafts; full decoder D0 open

**Primary source:** `akiyama-hamada-ito-sturmian-2026`, Section 10.1 and the
general matching rule in Section 6

## 1. Two source objects must not be conflated

Section 10.1 uses two geometrically different systems.

1. The **physical isometric-cell tiling** consists of `S^*_{j}`, `M^*_{j}`
   and `L^*_{j}` cells. The source says these cells “provide a tiling.” The
   final three patch-tiles in Figure 37 are unions of these physical cells;
   the BD construction concludes that this tile set admits tilings of
   `R^2`. The global matching rule requires physical patch-tiles to meet
   edge-to-edge and their bent SABs to continue.
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
  those rules into `X_kappa`.

If I0 and D0 hold, the limit system is MLD with the subdivided physical source
system. P0 then fixes the irrational slope and excludes all-`M` through the
source decoder; S0 and E-infinity close for the minimal colored target.

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
Then every decorated limiting physical vertex star has exactly one prelimit
source-star lift. Cyclic families and global reflection give the corresponding
rotated/reflected lift, not a second lift of the same decorated star.

**Proof.** The coset calculation uniquely recovers the indexed generating
triangle at each vertex. Primitive edges recover the same physical incidence
graph as before the limit. The transported colors restore the corridor-width
symbols erased by equidistancing. Therefore the incident colored cells and
their cyclic order reconstruct one source star. A different lift would have
to change an index, order coset, edge incidence or retained color, all of
which are fixed. \(\square\)

I0 also sharpens the role of O0. Tiny auxiliary patches contract to decorated
vertices, but distinct **physical** cell vertices do not collapse together.
The remaining D0 problem is global/local-rule totality, not geometric
ambiguity of a point star.

## 6. Remaining D0 obligation

D0 must prove that internal address ports, source edge/SAB matches, O0
auxiliary decorations and I0 vertex stars define a finite local rule whose
every whole-plane configuration groups uniquely into the source physical
macrotiles. The proof must cover global consistency of the order-coset labels
without selecting an absolute origin and must show that every permitted local
star participates in one source lift. No enumeration is authorized.
