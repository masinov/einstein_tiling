# K9 — controlled four-participant ports

**Date:** 2026-07-22

**Status:** exact local-angle/contact-topology proof draft; no polygonal
support, placement patch, all-tilings decoder or monotile claim

## 1. HC-18 route fixed before geometry

HC-18 studies one mechanism genuinely outside J0, K7C and K8U.  At each
internal division of a three-neighbor host word, a fourth congruent
occurrence `G` contributes a positive sector between the two code neighbors.
The host still contributes its straight `pi` sector.  The route requires:

1. one intrinsically recognizable guard vertex of angle `gamma`;
2. fixed directed poses for code roles `A,B,C` and the guard role;
3. exactly the two rooted word classes `ABC` and `ACB` at the primary stars;
4. a finite contact topology accounting for the two guard interfaces; and
5. no appeal to a coordinate search, optimizer or unspecified contact atlas.

Within three sessions the route must produce a state-bearing angle system
and a bounded residual contact topology, or freeze without a shape run.  A
topology that survives is only an admission target for later exact geometry.

## 2. The four-sector equation

At a primary division point, let role `X` lie on the spatial left, role `Y`
on the right, and `G` between them in the exterior half-plane of the host.
Write `rho_X` and `ell_Y` for their incident endpoint angles.  Gapless
coverage and disjoint interiors give

```text
rho_X + gamma + ell_Y = pi.                         (2.1)
```

This is not J0 with a decorative point label.  The positive `gamma` sector
separates `X` and `Y`; two distinct guard--neighbor boundary rays emanate
from the point.

The four directed adjacencies in the selected words are

```text
E = {(A,B), (B,C), (A,C), (C,B)}.                   (2.2)
```

## 3. K9A: exact four-participant selector

### ST-M1.K9A

All four adjacencies in (2.2) satisfy the same fixed-guard equation if and
only if there is a `theta>0` with `gamma+theta<pi` such that

```text
ell_B = ell_C = theta,
rho_A = rho_B = rho_C = pi-gamma-theta.              (3.1)
```

The unused `ell_A` is free.  The third reversal class, in which `A` is the
middle role, is compatible exactly when `ell_A=theta`.  Thus
`ell_A != theta` selects precisely `ABC` and `ACB`, even under the full
Euclidean group.

### Proof

Equations (2.1) for `(A,B)` and `(A,C)` give `ell_B=ell_C`; call the common
value `theta`.  Substitution in all four equations gives the common right
angle in (3.1).  This proves necessity, and direct substitution proves
sufficiency.

The remaining reversal class contains `B|A` or `C|A`.  Its sector sum is

```text
(pi-gamma-theta) + gamma + ell_A,
```

which equals `pi` exactly when `ell_A=theta`.  Reflection reverses a word but
does not change its reversal class, exactly as in K7A.  Hence no third state
appears when reflections are admitted.  □

## 4. What the extra sector buys

K7A needed a reflex endpoint in its orthogonal specialization.  K9A can
select two states with every angle in `(0,pi)`: choose any

```text
0 < gamma,theta,ell_A < pi,
gamma+theta < pi,       ell_A != theta.              (4.1)
```

For example, the primary equations alone admit

```text
gamma = theta = rho_X = pi/3,       ell_A = 2*pi/3.
```

This example is only local.  Section 6 below shows that its symmetric angle
choice cannot belong to a convex carrier.  The point is narrower: an extra
positive sector removes *local* nonconvexity from the selector algebra.  It
does not yet construct the occurrence that supplies that sector.

## 5. Clean guard spokes

Let `u_X` be the length of the first complete side leaving the right endpoint
of code role `X`, and `v_Y` the analogous length leaving the left endpoint of
role `Y`.  Let the two sides of `G` incident to its `gamma` vertex have
lengths `u,v` in the fixed guard pose.

If both guard interfaces are required to be complete clean contacts, the
four selected adjacencies force exactly

```text
u_A=u_B=u_C=u,       v_B=v_C=v.                       (5.1)
```

There is no equation `u=v`: the inserted guard separates the two code
neighbors, so K7C's common-stem equality no longer applies.  Conversely,
(5.1) makes the two primary spokes length-compatible in every selected
adjacency.  This closes only the first contacts; their remote endpoints still
need a finite topology.
