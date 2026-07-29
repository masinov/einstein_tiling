# Outward parity fan and the port-curvature obstruction

**Date:** 2026-07-29  
**Scope:** K70P patch packing; exact comparison of the two K72F bend
branches and a family-level obstruction to convex port embeddings  
**Status:** an outward-divergent exact host fan and a proved no-go for every
unbroken convex-flank realization; a reflex-reset polygon remains open

K72F permits either sign of the host turn.  The specialization in K72S is a
simple contact skeleton, but its right-hand exterior normals converge: it is
not the useful branch for a narrow-body construction.  Reversing the sign of
the bend preserves the zipper language and produces a strictly convex host
arc whose exterior normals diverge.  The price is visible in the total
turning of the six port germs.  They cannot all lie on a convex carrier or on
unbroken convex wedge tips.  This note makes both statements exact.

## 1. K73F — the outward-bending exact zipper

In K72F take

```text
C=7pi/6,                 gamma=5pi/6,
L_0=2pi/3,               L_1=3pi/4,
R_0=pi/2,                R_1=5pi/12.                   (1.1)
```

For equal phases, `R_q+L_q=7pi/6`; the two unequal sums are

```text
R_0+L_1=5pi/4,           R_1+L_0=13pi/12.             (1.2)
```

Adding the host angle `5pi/6` gives respectively

```text
2pi,                     25pi/12,       23pi/12.       (1.3)
```

Thus the sector equation still accepts exactly phase equality.  Give the
left delimiter inner angle `R_0=pi/2`, the right delimiter inner angle
`L_0=2pi/3`, and retain outer delimiter angle `pi/2`.  The terminal equation
is unchanged:

```text
5pi/6+pi/2+2pi/3=2pi.                                  (1.4)
```

With lengths `4,1,1,1,4`, traverse the host chain at directions

```text
0, pi/6, pi/3, pi/2, 2pi/3.                            (1.5)
```

Its exact vertices are

```text
p_0=(0,0),
p_1=(4,0),
p_2=(4+sqrt(3)/2,1/2),
p_3=(9/2+sqrt(3)/2,(1+sqrt(3))/2),
p_4=(9/2+sqrt(3)/2,(3+sqrt(3))/2),
p_5=(5/2+sqrt(3)/2,(3+5sqrt(3))/2).                   (1.6)
```

This is the reflection of the K72S coordinate chain and is simple by the
same monotonicity argument.  More importantly, with the host polygon on the
left of the directed chain, every internal host angle is `5pi/6`; the chain
is a strictly convex arc.  Its five exterior right normals have directions

```text
-pi/2, -pi/3, -pi/6, 0, pi/6.                          (1.7)
```

The supporting lines occur in their cyclic order, so the corresponding
outward normal rays have disjoint interiors.  This is the divergent branch.
In contrast, K72S has reflex host angles `7pi/6`; its right normal rays point
towards the concave side and can intersect.  K72S remains a valid local
zipper skeleton, but it supplies no divergence theorem.

## 2. The six required port germs

The minimal one-polygon alphabet carries one occurrence of each of the four
code roles and two delimiters as directed sides.  For the outward branch
their endpoint angles are

```text
E_00 : (2pi/3, pi/2),       E_01 : (2pi/3, 5pi/12),
E_10 : (3pi/4, pi/2),       E_11 : (3pi/4, 5pi/12),
D_L  : (pi/2, pi/2),        D_R  : (2pi/3, pi/2).       (2.1)
```

For a counterclockwise polygon, a vertex of interior angle `alpha`
contributes signed exterior turn `pi-alpha`.  The two prescribed endpoint
turns at the six germs therefore sum to

```text
E_00 : 5pi/6,       E_01 : 11pi/12,
E_10 : 3pi/4,       E_11 : 5pi/6,
D_L  : pi,          D_R  : 5pi/6,

total = 31pi/6.                                           (2.2)
```

If the six sides are pairwise nonadjacent, their twelve endpoints are
distinct.  Allowing adjacent roles barely changes the budget.  The left
endpoint angles in (2.1) belong to `{2pi/3,3pi/4,pi/2}`, while the right
endpoint angles belong to `{pi/2,5pi/12}`.  Equality at a shared polygon
vertex is possible only for a right `pi/2` endpoint followed by the left
`pi/2` endpoint of `D_L`.  Since the minimal alphabet contains `D_L` once,
at most one port--port vertex can be shared.  Such sharing removes only one
doubly counted turn `pi-pi/2=pi/2`; the distinct prescribed port vertices
still contribute at least

```text
31pi/6-pi/2 = 14pi/3.                                  (2.3)
```

## 3. N73W — no unbroken convex-flank port realization

Call a rooted port side **unbroken convex-flank** when the port and both of
its immediately adjacent boundary sides are supporting edges of the
polygon's convex hull.  Equivalently, the obvious wedge bounded by the two
actual flank rays contains the entire polygon without a reflex reset.

### Theorem

No simple polygon contains one directed occurrence of every germ in (2.1)
as unbroken convex-flank ports, even when compatible port endpoints are
allowed to coincide.

### Proof

At an unbroken convex-flank port, both endpoint turns are turns between
successive supporting edges of the convex hull.  Count each distinct hull
vertex once.  The compatibility calculation above shows that these turns
sum to at least `14pi/3`.  But every subset of the convex hull's positive
turns sums to at most its total turning `2pi`.  This is a contradiction.
QED.

Consequently K72C cannot be discharged by making every port an ordinary
convex wedge whose actual adjacent flanks continue as the cone boundary.
The outward fan solves the *placement* direction, but the common polygon
must use nonconvex curvature resets behind its ports.

## 4. K73R — the exact reflex-curvature budget

The same calculation applies without the convex-flank hypothesis.  Every
counterclockwise simple polygon has total signed exterior turn `2pi`.
For the pairwise-nonadjacent K71B alphabet, the twelve fixed port endpoints
contribute `31pi/6`, so all remaining vertices together must contribute

```text
2pi-31pi/6 = -19pi/6.                                  (4.1)
```

Each vertex of a simple polygon has interior angle strictly below `2pi`, so
one reflex vertex contributes strictly more than `-pi`.  Three reflex
vertices can contribute more than only `-3pi=-18pi/6`, which is insufficient
for (4.1).  Hence every polygon carrying the outward zipper alphabet has at
least four reflex vertices outside the twelve port endpoints.

If compatible port adjacency is allowed, (2.3) instead forces residual turn
at most

```text
2pi-14pi/3 = -8pi/3.                                   (4.2)
```

Two reflex vertices contribute strictly more than `-2pi`, so even this
larger minimal family requires at least three reflex vertices away from the
distinct port vertices.  Thus sharing the only compatible endpoint cannot
restore a convex or one-/two-reset carrier.

This is a necessary condition, not a realization.  It also explains why a
convex carrier, a convex cap with all ports, or six independent triangular
port wedges cannot work.  A viable common body must specify where at least
four reflex resets occur and must show that their transformed copies remain
inside the five divergent exterior corridors.

## 5. Exact next object

The remaining finite construction is no longer an unspecified narrow body.
It is a **reflex-reset comb**:

1. the five K73F host slots use the divergent normal order (1.7);
2. each selected port begins with its prescribed convex germ;
3. connector chains supply total signed turn `-19pi/6` and funnel the body
   into the slot's exterior corridor; and
4. the same connector chains work for all six canonical port poses of one
   polygon.

A positive result must give the complete cyclic boundary word, exact
coordinates, and all four disjoint placement tables.  A negative result may
close a named reflex-reset topology, but cannot be inferred from N73W alone.

## 6. Claim boundary

Established:

- the outward-bending phase zipper has the same exact even-parity language;
- its host is a simple strictly convex algebraic fan with divergent exterior
  normal order;
- every all-convex/unbroken-flank realization of its six ports is impossible;
- the retained pairwise-nonadjacent alphabet needs at least four reflex
  vertices, with exact residual signed turn `-19pi/6`; even the only possible
  adjacent-port relaxation needs at least three.

Not established:

- a reflex-reset comb or any common polygon;
- complete patch packing or contact closure;
- source lift, tilability, aperiodicity, or a monotile.
