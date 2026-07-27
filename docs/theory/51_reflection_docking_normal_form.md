# Reflection-docking normal form

**Date:** 2026-07-27

**Status:** HC-39 theorem draft; exact two-copy topology, no polygonal
realization, placement patch, all-tilings converse or monotile claim

**Scope:** one symmetry-free irredundant polygonal disk, two congruent copies,
and a clean connected two-copy interface

## 1. Copy-exchanging isometries

Let `P` be a compact polygonal topological disk whose Euclidean symmetry group
is trivial.  Suppose `g(P)=P'!=P` and `g(P')=P`; thus the same isometry
exchanges the two occurrences rather than merely placing the second one.

### ST-M1.K43I

The nonidentity isometry `g` is either a half-turn about one point or a
reflection in one line.

### Proof

The exchange equations give `g^2(P)=P`.  Trivial symmetry forces `g^2=id` as
an isometry on the plane.  A nonidentity plane isometry of order two cannot
be a translation or glide reflection, whose square is a nonzero translation,
nor a rotation through an angle other than `pi`.  The remaining cases are a
rotation through `pi` and a line reflection. □

K42M/N46 classify the half-turn branch under complete clean spokes.  Hence a
line reflection is the only different copy-exchanging involution available
without giving the carrier an intrinsic symmetry.

## 2. Clean reflection interfaces

Fix reflection `R` in a line `L`.  Assume:

1. `P` and `R(P)` have disjoint interiors;
2. their intersection is one nondegenerate simple polygonal arc `W`;
3. `R(W)=W` and `W` is not contained in `L`; and
4. every relative-interior point of `W` has a neighborhood occupied only by
   the two copies, with no gap or third occurrence.

These are the **clean reflection-spine hypotheses**.  The endpoints may and,
by N23/N24, eventually must meet further occurrences; condition 4 concerns
the open spine.

### ST-M1.K43R

Under the clean reflection-spine hypotheses:

1. `R` exchanges the two endpoints of `W`;
2. `W` has exactly one fixed point under `R`;
3. that point lies in the relative interior of one side `H` perpendicular to
   `L`, never at an irredundant polygon vertex;
4. the side-length word of `W` is a palindrome centered on `H`; and
5. for every paired noncentral spine vertex `p,R(p)`, the carrier angles obey

```text
alpha(p)+alpha(R(p))=2*pi.                           (2.1)
```

### Proof

Reflection restricts to a homeomorphism of the interval `W`.  If it fixed the
two endpoints individually, this interval involution would be increasing; an
increasing involution of an interval is the identity.  Then every point of
`W` would lie on `L`, contrary to hypothesis 3.  Thus it exchanges the
endpoints.  A decreasing interval involution has exactly one fixed point.

If that fixed point were an internal spine vertex, reflection would give the
two incident copies equal sector angles there.  Clean two-copy coverage would
require `2*alpha=2*pi`, so `alpha=pi`, contradicting irredundancy.  The fixed
point therefore lies inside a side.  A reflection-invariant segment on which
the endpoints are exchanged is perpendicular to the mirror line; call it
`H`.

Away from `H`, reflection pairs sides and vertices in reverse order, proving
the palindromic length word.  At a paired vertex `p`, clean coverage makes
the sector of `P` and the reflected sector coming from `R(p)` disjoint and
collectively equal to the full disk.  Their angles sum to `2*pi`, which is
(2.1). □

## 3. Intrinsic polarity and directed vectors

### ST-M1.K43V

Every paired noncentral spine vertex is a convex/reflex pair: one of
`alpha(p),alpha(R(p))` is below `pi` and the other above `pi`.  Moreover, if
`e` is a spine edge vector in the first half, the paired traversal vector is

```text
e'=-R(e),                                             (3.1)
```

not `e` as in the half-turn carrier.

### Proof

Equation (2.1) and irredundancy exclude equality to `pi`, so exactly one
angle lies on each side of `pi`.  If first-half vertices are traversed toward
`H`, the reflected half is traversed away from `H`; reflection transforms the
unoriented edge by `R` and reversal contributes the minus sign, giving (3.1).
□

The polarity is measurable unmarked geometry, not a color.  Equation (3.1)
is also the precise escape from N33/N37/N38/N41: those thin-lens arguments
use centrally paired equal traversal vectors and a common long axis.  No
existence follows from dropping that hypothesis, but the reflection route is
not already covered by the half-turn no-gos.

## 4. Boundary of the result

K43I--K43V do not establish that a polygon with such a spine exists, that
the intended reflection is forced, or that all other contacts are excluded.
They classify the only surviving involution and state the exact local
geometry any realization must satisfy.  Mixed-handed occurrences are
explicitly admitted, as ordinary Euclidean monotiling requires.
