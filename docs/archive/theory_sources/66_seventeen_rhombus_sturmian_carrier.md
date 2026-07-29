# The 17-rhombus Sturmian carrier: local compiler and composition obstruction

**Date:** 2026-07-27  
**Scope:** the fixed 16-gon `P17` with boundary

```text
(0,-2),(0,-1),(0,0),(1,1),(2,2),(3,2),(4,2),(4,1),
(4,0),(5,0),(5,-1),(4,-2),(3,-3),(2,-3),(2,-2),(1,-2).
```

Coordinates use the exact triangular-lattice basis of the source atlas.
`P17` is a connected unmarked polygonal disk containing 34 primitive
triangles, equivalently 17 common source rhombi.  This note decides a local
compiler question and a whole class of carrier-local decoders.  It does not
claim that `P17` tiles the plane or that every `P17` tiling has a source
decoder.

## 1. The actual AHI boundary rule

Akiyama--Hamada--Ito require an edge-to-edge patch tiling in which an SAB
continues across each patch boundary.  Their isometric-cell SABs are bent.
The source rule identifies the exposed endpoint; it does not state a tangent
color.

The pinned vector source provides a useful falsification control for any
stronger interpretation.  Across the 44 internal contacts of the two
published 15-rhombus macros, the two directed endpoint germs differ by
`1`, `3`, and `5` modulo six.  Thus exact straight tangency is not a source
matching condition.  At an edge-to-edge contact, the two marked arcs lie on
opposite sides of the common edge and share one endpoint; their union is
locally an embedded arc regardless of the two interior tangent directions.

Consequently the complete boundary datum used by the stated AHI rule is the
common edge and the SAB endpoint on it.  Exact tangent-germ equality is a
strictly stronger invented rule and is retained only as a diagnostic in the
machine artifact.

## 2. K60L — exact local compiler

For each of the four minimum equalizers in K54R, `P17` has two source-native
decompositions

```text
large_A + 2 singleton M,
large_B + 2 singleton M.
```

Every one of the 26 internal rhombus contacts continues, and the exposed
endpoint signature is identical because it is determined by the common
17-rhombus support.  The full vector audit gives four legal reflected-state
assignments for each pair of added singleton cells.  Hence `P17` is a genuine
finite local compiler block for the stated AHI endpoint rule.

This corrects K54S.  The `M+S` versus `L+S` labels described the components
in the two *large* macro decompositions; they did not prevent the two missing
geometric rhombi from being occupied by congruent singleton `M` tiles.

The result is local.  It neither partitions an entire source tiling into
`P17` blocks nor proves that a `P17` tiling admits any grouping.

## 3. N60C — composition-cone obstruction

Let a **carrier-local fusion decoder** be a finite-radius decoder from tilings
by one unmarked carrier `P` such that every occurrence of `P` is assigned one
of finitely many source patches, no decoded source tile crosses a carrier
boundary, and state `i` contains `p_i` large source tiles and `q_i` singleton
`M` tiles.

If such a decoder maps a carrier tiling to the AHI
`beta=sqrt(2)-1` source hull, then

```text
(a,b) belongs to cone{(p_i,q_i)},                 (3.1)
```

where the P0 coefficients are

```text
a = beta^2/6,
b = beta*(1-2*beta),
b/a = 6*(sqrt(2)-1).                              (3.2)
```

**Proof.** Count decoded source tiles in a disk of radius `R`.  Only carriers
meeting a fixed-width boundary annulus can contribute a boundary error, so
the error is `O(R)` while the number of interior carriers is `Theta(R^2)`.
Pass to a convergent subsequence of the finitely many carrier-state
frequencies.  The limiting source occurrence vector is a nonnegative linear
combination of `(p_i,q_i)`.  P0 fixes this vector projectively to `(a,b)`.
This proves (3.1).  Equation (3.2) follows exactly from the displayed P0
coefficients and `1/beta=sqrt(2)+1`.  □

In particular, any fixed-composition carrier state `(p,q)` with `p>0` forces
the rational ratio `q/p` and cannot realize this source.  The fixed
`large+2M` interpretation of `P17` has ratio `2`, while the required ratio is

```text
6*(sqrt(2)-1) > 2.
```

The same obstruction kills any carrier-local compiler whose complete state
library is drawn only from the presently transcribed 17-, 49-, and
51-rhombus large-containing kernels: their ratios are respectively `2`,
`4/3`, and `2`, so the cone has maximum slope `2`.

This is an impossibility theorem for a clearly defined realization family;
it is not an impossibility theorem for arbitrary finite-radius decoders whose
decoded source tiles may cross carrier boundaries.

## 4. N60V — the apparent all-M escape fails at one vertex

The support `P17` is itself tiled by 17 common rhombi.  At the exposed-
endpoint level these appear to give a second composition state

```text
Z = (0,17).                                           (4.1)
```

This is not a state of the complete twelve-state source language.  One must
not assume the inherited rhombus subdivision: the unmarked 34-triangle
support could in principle have another lozenge tiling.  The complete
primitive-triangle adjacency graph has exactly 60 perfect matchings.  In
every one, some physical vertex is surrounded by three rhombi of axes
`a,b,c`; equivalently, every long-diagonal graph contains an odd cycle.  The
shortest certified cycle has length three.

At such a vertex write the three corridor-gap bits as `x_a,x_b,x_c`.  If all
three rhombi were singleton `M` cells, their ordered transverse pairs would
require

```text
x_b != x_c,       x_c != x_a,       x_a != x_b.     (4.2)
```

No three binary values are pairwise unequal.  This is exactly the source
vertex consistency retained by I0/D0; endpoint continuation alone had erased
it.  Therefore the apparent `Z` decomposition is not even a locally legal
source patch under any lozenge subdivision of P17.  The contradiction is
invariant under rotation and reflection.  The exact enumeration and an
independent cold rebuild are serialized in
`ahi-p17-all-m-obstruction.json`.  □

## 5. N60P — P17 carrier-local impossibility

There is no carrier-local fusion decoder from one unmarked `P17` tile to the
exact AHI source system.

**Proof.** A decoded large source patch occupies 15 rhombi and a decoded
singleton occupies one.  Since a carrier has area 17 rhombi and decoded
source tiles do not cross its boundary, it contains at most one large patch.
If it contains one, the remaining area is exactly two singleton cells, so its
composition is `G=(1,2)`.  If it contains none, its composition is the
putative `Z=(0,17)`, which N60V excludes locally.  Thus every carrier would
have the fixed composition `G`.  N60C excludes that composition because
`2 != 6(sqrt(2)-1)`.  □

This is a complete impossibility result for the clearly defined
carrier-local family: finite state choices, exact source patches wholly
contained in each carrier, and the full twelve-state vertex/SAB language.
It does not exclude a bounded decoder whose reconstructed 15-rhombus source
patches cross `P17` boundaries, nor a different carrier with a larger
vertex-legal composition library.

## 6. Periodicity gates already closed

`P17` is not a one-copy triangular-lattice translation fundamental domain.
Among all 132 edge-connected interior-disjoint two-copy full-isometry unions,
none is a translation fundamental domain at index 34.  The 51-rhombus
Figure 45 envelope partitions into three `P17` copies in both displayed
panels, but it is not a norm-three inflation of `P17`; neither one nor two
copies of that envelope is a translation fundamental domain.

These are exact finite exclusions only.  They do not rule out another
periodic tiling of `P17`.
