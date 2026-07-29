# Torsion-free interface no-go and the exact parity zipper

**Date:** 2026-07-29  
**Scope:** boundary-active carrier-local compilation of the exact AHI
three-rail relation  
**Status:** a general additive impossibility theorem and a positive exact
rooted T-junction contact complex; no one-polygon realization yet

K69A closes one ordinary vertex.  The same algebra is much broader: any
fixed-topology interface whose only joint tests are additive real lengths,
angles, displacements, areas, or closure vectors cannot recognize ternary
parity.  This note proves that family theorem, then gives the first exact
non-ordinary contact complex that does recognize the AHI relation: a
two-phase T-junction zipper.

The zipper is not a monotile and is not promoted as a polygon.  It is the
finite source-facing specification that a polygon must now realize.

## 1. K70A — torsion-free additive tests cannot recognize parity

Let `G` be an abelian group with no element of order two:

```text
2g=0  implies  g=0.                                      (1.1)
```

For three binary roles, let `f_A,f_B,f_C:{0,1}->G` be arbitrary maps.

### Theorem

If

```text
f_A(x)+f_B(y)+f_C(z)=g_*                                (1.2)
```

holds for all four even-parity triples, then it holds for all eight binary
triples.

### Proof

Put

```text
d_A=f_A(1)-f_A(0),
d_B=f_B(1)-f_B(0),
d_C=f_C(1)-f_C(0).
```

Subtract the `000` instance of (1.2) from the `011`, `101`, and `110`
instances.  This gives

```text
d_B+d_C=0,             d_A+d_C=0,             d_A+d_B=0.  (1.3)
```

The first two equations give `d_A=d_B`; the third gives `2d_A=0`.  By (1.1),
all three differences vanish.  Thus each contribution is independent of its
bit and (1.2) holds on the whole cube.  QED.

The theorem remains true for any finite collection of additive tests: take
their product group.  In particular it applies to `R^n`, `Q(sqrt(d))^n`, and
every torsion-free lattice.

## 2. N70T — fixed-topology additive T-junctions are insufficient

Consider a host boundary complex with three active neighbor roles.  Suppose
that:

1. the contact topology, cyclic order, and multiplicity of the three roles
   are fixed;
2. all unary and pairwise germ conditions are checked independently; and
3. every remaining joint condition is an additive equality of independent
   participant contributions—for example total covered length, sector-angle
   sum, vector closure, signed displacement, or area.

If the complex accepts all four AHI even-parity states, its unary and binary
conditions accept every projection because those projections are full.
K70A makes every additive equality bit-blind.  Therefore the complex also
accepts every odd state.

This closes, in one statement:

- one fixed-order subdivision with one interval per active bit;
- any fixed-multiplicity weighted variant;
- attempts to repair it by adding finitely many real closure or curvature
  equations; and
- the ordinary angle-star family K69A as the special case `G=R`.

It does **not** close a changing word topology, an order-sensitive finite
automaton, collision/nonintersection selection, a hidden state with
two-torsion, or a larger-radius all-tilings theorem.

The structural conclusion is important: the missing AHI bit cannot live in
ordinary Euclidean budgets.  It must live in discrete topology or in an
explicit finite auxiliary state.

## 3. K70Z — an exact two-phase parity zipper

Let the hidden junction phase be `q in Z/2`.  Introduce four directed code
side roles

```text
E_pq,                    p,q in {0,1},                  (3.1)
```

with visible bit

```text
x(E_pq)=p xor q.                                        (3.2)
```

All four code sides have the same length.  Give their left and right
endpoint sectors angles depending only on the incoming and outgoing phases:

```text
L_0=pi/3,          L_1=pi/4,
R_0=2pi/3,         R_1=3pi/4.                           (3.3)
```

At an internal subdivision point, a straight host contributes angle `pi`.
The right endpoint of one neighbor and the left endpoint of the next fill
the other half-disk exactly when

```text
R_q+L_r=pi  iff  q=r.                                  (3.4)
```

The matched sums are `pi`; the two mismatched sums are `11pi/12` and
`13pi/12`.  Thus the bare polygonal angle equation enforces exact phase
continuity at every internal T-junction.

Now take a rooted word of three code sides with boundary phases fixed to
zero:

```text
q_0=0,
E_(q_0,q_1), E_(q_1,q_2), E_(q_2,q_3),
q_3=0.                                                  (3.5)
```

Its visible word satisfies

```text
x_1 xor x_2 xor x_3
 = (q_0 xor q_1) xor (q_1 xor q_2) xor (q_2 xor q_3)
 = q_0 xor q_3
 = 0.                                                   (3.6)
```

Conversely every even word has the unique lift obtained by integrating from
`q_0=0`.  Hence eliminating the internal T-junction phases gives exactly

```text
{000,011,101,110}.                                     (3.7)
```

This is an exact rooted polygonal **contact complex**: the internal
T-junction angle equations have explicit rational multiples of `pi`, and no
painted state is used in (3.4).  The fixed endpoint phases in (3.5) are still
rooted terminal data; Section 5 states the geometric obligation for removing
them.

### Four code roles are necessary in this zipper model

All four transitions `00,01,10,11` occur in lifts of the even words:

```text
000 uses 00,
011 uses 00,01,10,
101 uses 01,11,10.
```

If a rooted side role determines both endpoint phases, those four transition
pairs require four distinguishable roles.  Thus (3.1) is minimal for the
phase-continuity model.  This is compatible with N6's independent four-state
lower bound, although the auxiliary state is distributed along the word
rather than placed at one central star.

## 4. Why K70Z escapes the no-gos

K70Z does not contradict K70A: its decisive datum is the `Z/2` transition
phase, and `Z/2` violates (1.1).  It does not contradict N5: the internal
division points are auxiliary variables.  It does not use the forbidden
absolute lattice residue of N8/N9: only phase equality across a physical
T-junction and the endpoint difference `q_0 xor q_3` appear.

It also sharpens K2C.  K2C supplied the symbolic boundary cocycle; K70Z
shows exactly how a non-edge-to-edge polygonal junction can enforce one
cocycle equation through sector angles.  The remaining issue is no longer
whether the finite relation has a local geometric semantics.  It is whether
one congruence class can realize all roles and force the terminals and the
whole-plane atlas without imitation.

## 5. K70P — one-polygon admission contract

A connected unmarked polygon realizes the K70Z hyperedge only if it supplies
all of the following.

1. **Host and code roles.** One intrinsically recognizable host maximal side
   and four intrinsically recognizable equal-length code sides with endpoint
   sectors exactly (3.3), including handed directed roles under the allowed
   isometries.
2. **Exact subdivision.** In every admitted host patch, exactly three code
   sides cover the active host interval with the internal T-junctions of
   (3.4), without sliding or overhang.
3. **Geometric terminals.** The two rooted phase-zero conditions in (3.5)
   are forced by bounded unmarked geometry—a delimiter, cap, or closed
   carrier contact cycle—not assigned as colors.  All odd endpoint-phase
   words are rejected.
4. **Patch existence.** All four lifted even words have exact placements of
   congruent copies with pairwise-disjoint interiors.
5. **Local-closure exactness.** Every possible contact involving the host,
   code roles, delimiters, other sides, reflections, point contacts, and
   maximal-segment subdivisions belongs to a finite atlas whose projection
   is exactly the intended phase relation.
6. **Source lift and period rejection.** The resulting whole-plane language
   maps totally to the K68V AHI relation and then to the full source; every
   candidate support passes the exact periodicity gates immediately.

Clauses 1--4 are a finite coordinate problem.  Clause 5 is the
no-spurious-tilings theorem and remains the load-bearing obligation.  Clause
6 connects the gadget to ST-M1 rather than treating a local parity patch as
the result.

## 6. Research consequence

The boundary-active carrier problem now has a positive finite kernel.  The
following are closed:

- boundary-neutral states (N68H);
- independent rails (N63R);
- independent two-body collars (K61R/N62S in their stated families);
- ordinary multi-tile vertices (N69O); and
- every fixed-topology interface based only on torsion-free additive budgets
  (N70T).

The constructive target is K70P, not another arbitrary carrier family.  A
failure should become a theorem about one of its clauses—especially terminal
forcing or local-closure exactness.  A success would be the first exact
nonseparable contact hyperedge capable of carrying the AHI source relation;
it would still require integration with the 31-state macro cover before any
monotile claim.
