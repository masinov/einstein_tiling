# Directional composition law and the exact ceiling of corridor charges

**Date:** 2026-07-28  
**Scope:** arbitrary finite carrier-local patches of the exact AHI
`30,30,2` common-rhombus source; no carrier-area bound

## 1. K67O — lozenge-orientation counts belong to the support

Let a finite triangular-cell region admit a perfect matching of its primitive
triangles into common `60/120` rhombi. Number the three long-diagonal axes by
`j=0,1,2`, and let

```text
N_j = number of rhombi of axis j.                         (1.1)
```

Then `(N_0,N_1,N_2)` is independent of the perfect matching. In particular,
two source-macro decompositions of the same geometric support have the same
three numbers.

### Proof

Orient every primitive matching edge from the barycenter of an upward
triangle to the barycenter of its matched downward triangle. Its displacement
is one of three vectors `d_0,d_1,d_2`, with

```text
d_0+d_1+d_2=0                                             (1.2)
```

and no other linear relation. Summing over the matching gives

```text
N_0 d_0+N_1 d_1+N_2 d_2
  = sum(down-triangle barycenters)-sum(up-triangle barycenters), (1.3)
```

whose right side depends only on the region. The additional equation
`N_0+N_1+N_2=A`, where `A` is its rhombus area, removes the one-dimensional
kernel in (1.2). The three counts are therefore fixed. This is the standard
lozenge/dimer flux argument; no novelty is claimed. QED.

## 2. K67D — large-macro count is directional role deficit

For a source-macro state of the region, let `k` be its total number of large
macros (either published large type). Let `S_j,M_j,L_j` count source roles on
axis `j` after every macro is expanded into common rhombi.

The exact corridor quotient gives, for **both** large macro types,

```text
(S_j,L_j)=(2,1) for each j=0,1,2.                        (2.1)
```

The remaining six cells are `M`: the canonical large-A distribution is
`(0,3,3)` and the canonical large-B distribution is `(2,2,2)`, up to the
axis permutation induced by placement. A singleton contributes one `M` on
its own axis. Hence every state, in every pose, satisfies

```text
S_j = 2k,
L_j = k,
M_j = N_j-3k                     for j=0,1,2.            (2.2)
```

Consequently two decompositions of one support obey

```text
Delta M_0 = Delta M_1 = Delta M_2 = -3 Delta k.          (2.3)
```

This is stronger than the scalar area identity in K66T. A count-changing
trade cannot alter one rail direction independently: it must create or remove
the same number of mixed corridor cells in all three directions.

### Proof

Equation (2.1) is an extensional fact of the cold-verified source atlas. It
is unchanged by any Euclidean placement because a placement merely permutes
the three axes. Singletons have role `M`, so they add neither `S` nor `L`.
Summing (2.1) over the `k` large macros gives the first two equations of
(2.2); the third follows from `N_j=S_j+M_j+L_j`. K67O makes `N_j` common to
both decompositions, and subtraction gives (2.3). QED.

## 3. K67G — exact directional Gauss decomposition

Fix one axis `j` in a finite legal source patch and retain only the
axis-`j` long-diagonal edges of the corridor-occurrence graph. The published
SAB has the same axis on both endpoint arms, including the bent `M` case, so
source continuation pairs axis-`j` ends with axis-`j` ends. Every interior
vertex of this subgraph consequently has even degree; its odd-degree vertices
are exposed marked-boundary occurrences.

Each graph vertex carries its narrow/wide bit `c in {0,1}`. An edge has role
`M` exactly when its endpoint bits differ. The handshaking identity on the
bit-`1` vertices gives

```text
M_j = sum_v deg_j(v)c(v)                  (mod 2)
    = sum_{v exposed, deg_j(v) odd} c(v)  (mod 2).       (3.1)
```

Let `chi_j in {0,1}` be the last boundary sum. There is then a unique
nonnegative integer `p_j` such that

```text
M_j = chi_j+2p_j.                                      (3.2)
```

Combining (2.2) and (3.2) yields the exact all-area identity

```text
N_j-3k = chi_j+2p_j             for j=0,1,2.            (3.3)
```

Here `chi_j` is the Gauss charge read at the exposed axis-`j` occurrences,
whereas `p_j` counts transition pairs invisible to that charge.

### Corollaries

1. If two carrier states have the same marked corridor boundary, then their
   large-macro counts have the same parity.
2. Every odd-count AHI trade changes the boundary Gauss charge in **all
   three** directions.
3. A boundary-neutral trade changing `k` by `2r` must change the hidden
   transition-pair count by `3r` in each direction (with the sign fixed by
   the direction of the trade).

These statements allow contextual boundary states. They do not assume that
the unmarked carrier itself displays a radius-zero color.

## 4. N67C — corridor boundary charge cannot close even trades

No invariant depending only on the boundary of a binary corridor path can
recover its number of `M` edges beyond parity. On the same two-edge path,

```text
000 has 0 transitions,          010 has 2 transitions,   (4.1)
```

with identical endpoint bits. Inserting or deleting such an excursion
changes `p(P)` by one while preserving every endpoint datum. Conversely,
(3.1) proves that parity is the only endpoint-determined residue.

Therefore K66C's binary corridor potential, by itself, cannot prove N66R.
It excludes boundary-neutral odd-count trades, but it is intrinsically blind
to the transition-pair mechanism required by an even-count trade. This is a
method ceiling, not an existence result: (4.1) need not extend to a legal AHI
macro patch because the complete six-cell vertex and SAB rules have not been
used.

The result also explains the finite evidence without extrapolating from it.
The sub-30 cases require an odd exchange and fail already at the cut layer.
Area 30 includes the even `H/Z` exchange, which is invisible to boundary
parity and required the exact-cover classification. More parity checks at
larger area cannot settle the general branch.

## 5. The remaining all-area theorem

The carrier-local question is now sharper than N66R:

> Can the complete AHI vertex/SAB language create three synchronized pairs
> of internal corridor transitions while changing the large-macro count by
> two, or does its joint three-rail vertex rule conserve an additional
> integer or higher-modulus charge?

A negative answer closes every boundary-neutral carrier-local realization;
a positive finite patch is the first genuine even count-changing trade and
becomes constructive input. The next proof must use the coupled three-rail
vertex stars. Another per-axis parity argument or another carrier-area census
cannot answer it.
