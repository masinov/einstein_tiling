# Ordinary polygon vertices cannot enforce the AHI three-rail relation

**Date:** 2026-07-29  
**Scope:** boundary-active carrier interfaces whose only joint meeting is one
ordinary polygon vertex, with fixed passive participants and no T-junction,
overlap, hidden star state, or larger-radius exclusion  
**Status:** complete impossibility theorem for this realization family

N68H forces any carrier-local AHI compiler to export joint three-rail state.
The cheapest apparent mechanism is an ordinary multi-tile vertex: let the
incident polygon angles and pairwise boundary germs accept exactly the four
even-parity rail states.  This note closes that entire mechanism, including
state-dependent angle choices and any fixed number of passive sectors.

The algebra is elementary and no novelty claim is made.  Its value is the
architecture-level conclusion: a genuine contact hyperedge, a visible hidden
star state, or an all-tilings larger-radius theorem is necessary.

## 1. The ordinary-star family

Fix three distinguished cyclic participant roles `A,B,C` at one point.  Role
`A` has a binary state `x`, role `B` a state `y`, and role `C` a state `z`.
For each state, its rooted occurrence contributes one interior sector angle

```text
A_x,                       B_y,                       C_z.
```

Any other participants are passive: their states and cyclic positions are
fixed, and their angles have constant total `Gamma`.  Between consecutive
participants, geometric compatibility is a unary or pairwise condition on
the two incident rooted boundary germs.

The star is **ordinary** when a sufficiently small punctured disk around the
point is partitioned into those sectors.  In particular:

- no boundary terminates in the relative interior of another boundary arc;
- no participant occupies two separated sectors;
- no positive-length overlap or auxiliary cavity occurs; and
- the only joint coverage equation is that the sector angles sum to `2*pi`.

This definition allows arbitrary nonconvex polygons away from the vertex and
arbitrary state-dependent angles at the vertex.  It excludes exactly the
topologies—T-junctions, multi-arc fusion, and changing auxiliary stars—that
can carry information not visible in ordinary sector incidence.

## 2. K69A — angle sums do not realize ternary parity

### Theorem

No ordinary star has exact visible state relation

```text
E_3={000,011,101,110}.                                  (2.1)
```

### Proof

Every unary projection and every two-coordinate projection of `E_3` is
full.  Therefore every unary state and every pair of adjacent boundary-germ
states occurs in an accepted star.  No unary or pairwise compatibility rule
may reject any of the eight binary triples without also rejecting a member
of `E_3`.

It remains only the sector-sum equation.  Acceptance of the four words in
(2.1) gives

```text
A_0+B_0+C_0+Gamma = 2*pi,
A_0+B_1+C_1+Gamma = 2*pi,
A_1+B_0+C_1+Gamma = 2*pi,
A_1+B_1+C_0+Gamma = 2*pi.                              (2.2)
```

Put

```text
d_A=A_1-A_0,          d_B=B_1-B_0,          d_C=C_1-C_0.
```

Subtracting the first equation in (2.2) from the other three yields

```text
d_B+d_C=0,            d_A+d_C=0,            d_A+d_B=0.
```

These equations force `d_A=d_B=d_C=0`.  Hence the angle sum is identical for
all eight triples.  Since the unary and pairwise checks also accept all of
them, the four odd-parity triples are legal as well.  The star cannot realize
exactly `E_3`.  QED.

The proof is unchanged if `Gamma` is split among any fixed number of passive
participants, if the three active roles are not consecutive, or if rooted
reflections are included in the binary state names.

## 3. N69O — ordinary vertices cannot supply the missing AHI coupling

K68V identifies the local AHI mixedness relation with `E_3`.  Therefore a
boundary-active carrier compiler cannot enforce the complete three-rail
vertex rule using only:

1. independent two-participant boundary profiles;
2. ordinary corner compatibility between adjacent profiles; and
3. one ordinary gapless sector star, even with state-dependent angles and
   fixed guard occurrences.

K61R already classifies item 1, and N5 gives the abstract binary-projection
obstruction.  K69A closes the apparent geometric loophole that a multi-tile
angle sum might itself be a ternary parity check.

This is a family theorem, not a statement about a particular polygon or a
sampled contact atlas.

## 4. K69F — the exact remaining contact mechanisms

Combine K68R and N69O.  Any carrier-local one-support realization of the
exact AHI source must have a boundary-active joint relation, and at least one
of the following must be present in every total decoder:

1. **a visible auxiliary star state:** the local geometry has several
   distinguishable completions and existentially eliminating that state
   yields `E_3`; N6 proves that the direct product-box form needs at least
   four states;
2. **a non-ordinary contact hyperedge:** a T-junction, side subdivision,
   multi-arc cavity, or carrier--verifier fusion whose coverage is not a
   conjunction of pairwise germ compatibility and one angle sum; or
3. **a proved larger-radius exclusion:** the odd triples are locally
   possible at the immediate star but absent from every whole-plane tiling,
   with a total decoder proving that fact.

Pure pose does not furnish item 1 by N7, and an unanchored lattice residue
does not furnish it by N8/N9.  Edge-to-edge ordinary vertices do not furnish
item 2 by N69O.  Thus the minimal unresolved geometric object is a
non-ordinary, locally recognizable contact hyperedge (or an independently
visible four-state completion), together with an all-tilings converse.

This list is exhaustive under the carrier-local hypothesis.  It does not say
that one of the three mechanisms exists for one unmarked polygon.

## 5. Next theorem target

The next step is not another carrier support.  It is a classification of the
minimal non-ordinary interface:

> For one host boundary arc partitioned by several congruent neighbors, what
> finite relations are realizable on the full local closure of one connected
> polygon, and can one realize the AHI even-parity hyperedge without admitting
> an odd word or a periodic fault tiling?

A positive theorem must give an exact contact complex and a total lift.  A
negative theorem must name the T-junction/fusion family it closes.  The
ordinary-star family is now permanently retired.
