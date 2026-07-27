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

## 4. K60V — the only local escape for `P17`

The support `P17` is itself tiled by 17 common rhombi.  At the endpoint-rule
level these may all be singleton `M` cells, giving a second local composition
state

```text
Z = (0,17).
```

Let `G=(1,2)` denote either large state.  If a whole-plane carrier-local
decoder uses only `G` and `Z`, N60C fixes their occurrence ratio exactly:

```text
frequency(Z) / frequency(G)
    = (6*(sqrt(2)-1)-2)/17
    = (6*sqrt(2)-8)/17.                            (4.1)
```

Thus `Z` is not an optional curiosity.  It must occur with the irrational
frequency (4.1).  Conversely, the composition obstruction no longer refutes
the two-state library because `(a,b)` lies in the cone generated by `G` and
`Z`.

This gives a precise total-decoder target for the fixed polygon:

1. construct at least one whole-plane `P17` tiling;
2. prove every `P17` tiling has a finite-radius `G/Z` grouping;
3. prove the resulting source patches satisfy the complete AHI vertex/SAB
   language, including reflections and non-edge-to-edge alternatives; and
4. prove the forced `Z/G` frequency is (4.1), or equivalently obtain period
   descent through the AHI source decoder.

Failure of item 2 or 3 is a counterexample to totality, not a near miss.

## 5. Periodicity gates already closed

`P17` is not a one-copy triangular-lattice translation fundamental domain.
Among all 132 edge-connected interior-disjoint two-copy full-isometry unions,
none is a translation fundamental domain at index 34.  The 51-rhombus
Figure 45 envelope partitions into three `P17` copies in both displayed
panels, but it is not a norm-three inflation of `P17`; neither one nor two
copies of that envelope is a translation fundamental domain.

These are exact finite exclusions only.  They do not rule out another
periodic tiling of `P17`.
