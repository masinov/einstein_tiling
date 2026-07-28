# Physical contact completion forces a periodic stick tiling

**Date:** 2026-07-28  
**Scope:** independent two-participant, endpoint-preserving collars on the
length-`n` Stade stick; every physically possible contact allowed by the marked
system must remain realizable

## 1. Why relation-exactness was too strong

K61R classified erasures whose geometric compatibility relation is exactly the
declared marked relation.  That leaves a genuine loophole: a fourth corner of a
forbidden rectangle is harmless when the two carrier copies overlap there.

Let `G subset E_plus x E_minus` be the endpoint-aligned contacts for which the
two unmodified carriers have disjoint interiors.  For a marked allowed relation
`R`, put

```text
A = G intersect R,          F = G minus R.
```

Only `A` must be preserved and only `F` can be a spurious physical contact.
The correct finite question is therefore a graph-sandwich question, not
rectangularity of `R` itself.

## 2. K62P — the physical graph-sandwich theorem

For any bipartite graph `A`, let `cl(A)` be the union of the complete
bipartite graphs on its nontrivial connected components.

### Theorem

For endpoint-preserving independent collars with exactly two participants:

1. every geometric compatibility relation containing `A` also contains
   `cl(A)`;
2. `cl(A)` itself is realizable by arbitrarily shallow rational polygonal
   profiles; and consequently
3. a geometric profile-compatibility relation `B` with

   ```text
   A subset B,             B intersect F = empty
   ```

   exists if and only if `cl(A) intersect F` is empty.

### Proof

Put a complete port in canonical rooted coordinates.  As in K61R, one fixed
endpoint-reversing isometry `J` places its mate on the other side.  If two
required contacts share a right endpoint,

```text
p_e = J(p_f) = p_e',
```

so equality propagates along every even path in `A`; the analogous statement
holds on the right.  Hence a connected component forces one profile on its
left vertices and the complementary profile on its right vertices.  Every
cross-pair in the component is therefore compatible, proving `cl(A) subset
B`.

Conversely, assign one distinct asymmetric rational zigzag to each component
and its `J`-complement to the opposite side, exactly as in K61R.  This realizes
`cl(A)`.  It avoids every forbidden physical pair exactly when `cl(A)` misses
`F`.  QED.

This is a physical weakening of the standard jigsaw-color classification, not
a novelty claim.

## 3. Exact Stade stick coordinates

Use axial hex-cell coordinates with counterclockwise neighbor vectors

```text
v0=(1,0), v1=(1,-1), v2=(0,-1),
v3=(-1,0), v4=(-1,1), v5=(0,1).
```

The carrier is

```text
S_n = {(k,0) : 0 <= k < n}.
```

The source figure gives the following port data:

| port | incident cell | outward direction |
|---|---:|---:|
| `b_i` | `n-1-i` | `v1` |
| `d_i` | `i` | `v4` |
| `a_i` | `n-i` | `v2` |
| `c_i` | `i-1` | `v5` |
| `z1` | `n-1` | `v1` |
| `z2` | `0` | `v4` |
| `x1` | `n-1` | `v5` |
| `x2` | `0` | `v2` |
| `y1` | `n-1` | `v0` |
| `y2` | `0` | `v3` |

If port `(i,d)` of the first copy meets port `(j,d')` of the second, the
second copy has cells

```text
(i,0) + v_d + (t-j) v_(d+3-d'),       0 <= t < n,       (3.1)
```

with direction subscripts taken modulo six.  Formula (3.1) gives a symbolic
all-`n` physical-contact test.

## 4. K62C — a stable spanning tree for every `n>=5`

Delete not only fixed forbidden rules 1--11, but every pair that any later
input-dependent rule can forbid:

```text
a-y,       c-y,       a-x1,       b-z2.                 (4.1)
```

The remaining physically possible allowed graph is still connected.  The
following contact families and their reversals form a spanning graph:

```text
b1 -- b_i, d_i, x1, x2, y1, y2       (1 <= i < n)
x2 -- c_i                             (1 <= i < n)
d1 -- z1
z1 -- a_i                             (1 <= i < n)
d_(n-1) -- z2.                                             (4.2)
```

They reach every label on both sides of the bipartite graph.  For example,
with root `L:b1`, the only paths longer than three edges have the form

```text
L:b1 - R:b1 - L:d1 - R:z1 - L:a_i.
```

### Physical feasibility

Substitution in (3.1) proves disjointness without a finite-length census:

| contact family | locus of the second stick |
|---|---|
| `b1-b_i`, `b1-d_i` | row `r=-1` |
| `b1-x1`, `b1-x2` | column `q=n-1`, with `r<=-1` |
| `b1-y1`, `b1-y2` | every cell has `r<=-1` |
| `x2-c_i` | row `r=-1` |
| `d1-z1` | row `r=1` |
| `z1-a_i` | column `q=n` |
| `d_(n-1)-z2` | row `r=1` |

Every locus misses `S_n`; reversing a contact applies an inverse isometry and
preserves disjointness.

### Rule legality

Rules 1--11 forbid none of (4.2).  In particular, rule 7 permits only the
terminal `d_(n-1)-z2` contact, and rule 9 forbids `z1-b_i` but not `z1-a_i`.
None of (4.2) belongs to a later family in (4.1).  Thus the spanning graph is
present for every input Wang system and every `n>=5`.  QED.

The preregistered finite reconstruction for `5<=n<=12` independently supports
the proof.  Its old N61S rectangle is partly nonphysical: `a1-b1` overlaps.
Nevertheless, every tested graph has one component and every physically
possible fixed-rule prohibition lies in its forced biclique completion.

## 5. N62S — contact-complete erasure is necessarily periodic

### General periodic-carrier lemma

Let a polygonal carrier `T` have an edge-to-edge periodic tiling.  Suppose a
separable endpoint-preserving collar replacement must realize a required
contact graph `A` that is connected and spans every directed port role used by
that periodic tiling.  Then the modified tile also admits a periodic tiling.

Indeed, K62P forces the complete bipartite compatibility relation on that
component.  Replace every carrier in the periodic tiling by the modified tile.
Every old full-edge contact now has complementary profiles.  Port endpoints
and corner sectors are unchanged, so no gap or overlap is introduced at
vertices.  The original translation lattice remains a period lattice.  QED.

### Application to the Stade stick

The unmodified length-`n` stick periodically tiles the hexagonal cellulation:
partition every axial row into the translates

```text
S_n + m(n,0) + k(0,1),          (m,k) in Z^2.            (5.1)
```

K62C says that preserving every physically possible marked-system contact
forces all directed ports into one compatibility component, even after every
possible later deletion (4.1).  Hence all contacts in (5.1) are compatible
after erasure.  The modified single polygon has the rank-two translation
lattice generated by `(n,0)` and `(0,1)`.

### Corollary

For every `n>=5`, no contact-complete independent two-body collar erasure of
Stade's one-stick marked system can be an aperiodic monotile.  This remains
true if the geometry is allowed to realize extra marked-forbidden contacts:
the obstruction is an explicit periodic tiling, not failure of
relation-exactness.

The corollary uses only the published port labels and rule table.  It does not
depend on the preprint's Lemma 4 weave-converse proof.

## 6. Exact boundary of the result

N62S closes a substantially larger family than N61S:

- physically impossible contacts are discarded;
- arbitrary extra two-body contacts are allowed;
- every input-dependent rule set is covered at once; and
- the conclusion is periodicity of the unmarked tile.

It still assumes **contact completeness**: every physically possible contact
that the marked presentation permits must survive geometrization.  A compiler
could try to preserve only a globally sufficient sublanguage of the fixed AHI
source.  To escape N62S it must prove all three of the following:

1. the retained source subsystem is nonempty and aperiodic;
2. its globally occurring required-contact graph is disconnected enough to
   avoid the periodic carrier completion; and
3. every tiling of the unmarked polygon decodes into that subsystem.

That is now the precise separable-language loophole.  The other escapes remain
genuinely nonseparable: a third participant, joint multi-port state, or
carrier--verifier fusion.  Repeating independent port-profile synthesis cannot
cross this boundary.
