# Bent parity zipper and the congruent-packing cone

**Date:** 2026-07-29  
**Scope:** K70P simultaneous-packing obligation; exact deformation of the
K71T rooted contact complex  
**Status:** a simple algebraic bent host and an exact sufficient cone
criterion; one common polygon satisfying the cone criterion remains open

The straight K71T host makes the three `000` code neighbors congruent
translates along one line.  That is not an impossibility, but it is an
unnecessary packing constraint.  Phase continuity needs a constant sector
sum, not a straight host.  This note derives the full bending family and
selects a simple `30`-degree fan specialization.

## 1. K72F — the full bent-zipper family

Choose a constant `C` and two distinct incoming angles `lambda_0,lambda_1`
such that

```text
0 < lambda_0,lambda_1 < C < 2pi,
0 < C-lambda_0,C-lambda_1 < 2pi.                       (1.1)
```

Set

```text
L_p=lambda_p,                  R_p=C-lambda_p,          (1.2)
gamma=2pi-C.                                               (1.3)
```

Here `gamma` is the host's interior angle at every internal junction.  For
two consecutive code roles, or a delimiter and a code role,

```text
gamma+R_q+L_r=2pi        iff q=r.                       (1.4)
```

Indeed the matched sum is `gamma+C=2pi`; a mismatch differs by the nonzero
quantity `lambda_0-lambda_1`.  Therefore every proof in K70Z/K71T survives
with a polygonal host chain whose exterior turn at an internal junction is

```text
pi-gamma=C-pi.                                          (1.5)
```

The straight zipper is `C=pi`.  Values `C!=pi` spatially separate
successive neighbor poses while preserving exactly the same hidden
`Z/2` transducer and visible even-parity language.

This freedom does not contradict K70A: phase matching remains a discrete
two-state relation.  The real angle sum only implements equality of the
already distinct endpoint states.

## 2. K72S — one exact simple `30`-degree host chain

Take

```text
C=5pi/6,              gamma=7pi/6,
L_0=pi/3,             L_1=pi/4,
R_0=pi/2,             R_1=7pi/12.                      (2.1)
```

Matched endpoint sums are `5pi/6`; the mismatches are `3pi/4` and
`11pi/12`.  Adding the host angle gives respectively `2pi`, `23pi/12`, and
`25pi/12`.  Thus equality remains exact.

Use delimiter length four, code length one, and the directed host-chain edge
lengths

```text
4,1,1,1,4.                                             (2.2)
```

Traverse them at directions

```text
0, -pi/6, -pi/3, -pi/2, -2pi/3.                       (2.3)
```

The vertices are

```text
p_0=(0,0),
p_1=(4,0),
p_2=(4+sqrt(3)/2,-1/2),
p_3=(9/2+sqrt(3)/2,-(1+sqrt(3))/2),
p_4=(9/2+sqrt(3)/2,-(3+sqrt(3))/2),
p_5=(5/2+sqrt(3)/2,-(3+5sqrt(3))/2).                  (2.4)
```

This open chain is simple.  The first four edges have nonincreasing `y` and
nondecreasing `x`.  The relative interior of the last edge has
`y<y(p_4)`, whereas every earlier nonadjacent edge has `y>=y(p_4)`.  Hence no
nonadjacent pair meets.

For the delimiters, retain outer angle `pi/2`; their inner angles are now
`R_0=pi/2` on the left and `L_0=pi/3` on the right.  The terminal host/cap
star from K71T remains

```text
5pi/6+pi/2+2pi/3=2pi.                                 (2.5)
```

Thus (2.4), together with the endpoint table (2.1), is an exact
`Q(sqrt(3))` rooted host contact complex admitting precisely the four parity
words.  Even the word `000` now places its three identical `E_00` roles in
poses rotated successively by `pi/6`, rather than as unit translates.

## 3. K72C — a sufficient cone criterion for complete patch packing

For each edge `s_j=[p_j,p_(j+1)]` of the host chain, let `W_j` be a closed
pointed polygonal cone on the exterior side of that edge, truncated only in
one small neighborhood of its two endpoints.  Require:

1. the interiors of `W_0,...,W_4` are pairwise disjoint outside those
   endpoint neighborhoods;
2. the canonical copy using its selected delimiter/code side has all of its
   interior, except the shared side, in `int(W_j)`; and
3. each terminal cap copy lies in a further cone disjoint from all `W_j`
   except at its declared terminal star.

### Lemma

If one polygon satisfies these conditions for every delimiter/code role used
by a parity word, that complete K72S patch has pairwise-disjoint interiors.
If the same conditions hold uniformly for all four role choices at each
active position, all four parity patches exist.

### Proof

The host interior is on the opposite local side of every chain edge, so it is
disjoint from each neighbor interior.  Distinct neighbor interiors lie in
cones with disjoint interiors.  The only cone intersections are the declared
endpoint neighborhoods, where the exact sector equations (2.1) and (2.5)
partition the disk.  Caps are handled by condition 3.  Coverage of the host
chain is exact by the full-side placements.  QED.

K72C is sufficient, not necessary.  Interlocking polygons may pack without
separable cones.  Its purpose is to replace a global collection of pairwise
segment-intersection inequalities by one constructive geometric target.

## 4. The common-polygon cone problem

For a rooted code side `E_pq` of a proposed polygon `P`, put that side in a
canonical unit position with `P` on its inward side.  The **port cone** is any
pointed cone containing `P` in that canonical pose.  Under the isometry that
places `E_pq` on host slot `s_j`, the port cone moves with it.

K72C reduces simultaneous packing to the following finite question:

> Does one connected simple polygon carry the four K72F code germs and two
> delimiter germs so that each canonical remainder lies in a sufficiently
> narrow port cone, while its length-eleven host chain and cap germ remain
> part of the same boundary?

The `pi/6` pose separation in K72S gives positive angular room for such
cones; the straight specialization gave none.  K71B proves the germs can
coexist, but its large-tab construction does not control their port cones.
The next proof must strengthen K71B to a common narrow-body or multi-tip
embedding, or prove that the host/delimiter length requirements obstruct all
such embeddings.

## 5. Claim boundary

Established:

- the parity zipper has a continuous exact bending parameter;
- the explicit `30`-degree specialization has a simple algebraic host chain;
- all four parity words retain exact local sector legality;
- K72C is a finite sufficient condition for collision-free congruent patches.

Not established:

- a polygon satisfying the common port-cone conditions;
- necessity of the cone model;
- exclusion of other covers or contacts;
- a whole-plane tiling, source lift, periodicity result, or monotile.

The live constructive problem is now one common-polygon cone embedding, not
an unconstrained coordinate search.
