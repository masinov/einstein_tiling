# K7A — selected-word nonconvex ports

**Date:** 2026-07-22

**Status:** exact local-angle proof draft; no polygonal disk, contact patch,
whole-plane forcing or monotile claim

## 1. HC-16 route fixed before geometry

HC-16 studies exactly one escape from N21:

- one nonconvex polygonal support;
- three unequal complete code sides `A,B,C`, whose lengths sum to one host
  side;
- fixed directed poses for the three roles;
- ordinary internal T-junctions with exactly three participants;
- two selected non-reversal subdivision words;
- no contextual handedness and no extra junction participant.

The non-complementary endpoint is part of the fixed code-side geometry.  It
is not an after-the-fact label.  Within three sessions this route must supply
exact coordinates and hand-checkable recognition, coverage and disjointness
for both patches, or it is frozen without a search.

## 2. Normal form for two selected words

For three distinct roles, a reversal class is determined by its middle role.
Given any two distinct reversal classes, reverse representatives if necessary
and relabel the roles so that they are

```text
A B C       and       A C B.                         (2.1)
```

Thus `A` is the common extreme role and `B,C` exchange the two remaining
positions.  Let `ell_X` and `rho_X` denote the interior angles at the left and
right endpoints of role `X` in its fixed directed pose.

J0 applied to the two internal divisions in each word gives

```text
rho_A + ell_B = pi,       rho_B + ell_C = pi,
rho_A + ell_C = pi,       rho_C + ell_B = pi.         (2.2)
```

## 3. K7A: exact two-of-three angle selector

### ST-M1.K7A

The two selected classes in (2.1) are locally compatible at every internal
T-junction if and only if, for some `theta in (0,pi)`,

```text
ell_B = ell_C = theta,
rho_A = rho_B = rho_C = pi-theta.                     (3.1)
```

The unused endpoint angle `ell_A` is unconstrained by those two words.  If
`ell_A != theta`, the third reversal class is locally impossible.  Hence
fixed endpoint geometry can select exactly two of the three K6O states.

### Proof

Subtract the first and third equations of (2.2) to obtain
`ell_B=ell_C`.  Calling the common value `theta`, every equation in (2.2)
then gives the three equal right angles in (3.1).  This proves necessity, and
substitution proves sufficiency.

The remaining reversal class has `A` as its middle role.  In either
orientation it contains an internal junction `B|A` or `C|A`.  Its angle sum
is

```text
(pi-theta) + ell_A,
```

which equals `pi` exactly when `ell_A=theta`.  J0 therefore excludes that
class precisely when `ell_A != theta`.  Reflection reverses a selected word
but does not change its reversal class, so allowing the full Euclidean group
adds no third state.  □

## 4. The exact orthogonal specialization

Set

```text
theta = pi/2,       ell_A = 3*pi/2.                   (4.1)
```

Then the directed endpoint pairs are

```text
A : (3*pi/2, pi/2),
B : (  pi/2, pi/2),
C : (  pi/2, pi/2).                                  (4.2)
```

Every internal junction in `ABC` and `ACB` is a `pi/2 + pi/2` junction.
The class with `A` in the middle would require a
`pi/2 + 3*pi/2 = 2*pi` junction and is impossible.  The reflex endpoint of
`A` forces the carrier itself to be nonconvex and is always at a host
endpoint in the two admitted words.  It becomes internal exactly in the
excluded class.

This is the smallest exact endpoint vocabulary presently known in the
branch: it uses only integer-coordinate-compatible orthogonal angles, gives
a genuine two-state selector under reflections, and escapes N21 through a
named reflex vertex rather than through vague nonconvexity.

## 5. What has and has not been earned

K7A proves a local selector.  It does **not** prove that one polygon possesses
the four required side roles, that three congruent neighbor copies are
disjoint away from the two internal junctions, or that either selected patch
exists.  In particular, the angle equations inspect only infinitesimal
sectors.  Long-range overlap can still kill both words.

The next geometric obligation is therefore exact and smaller than the HC-15
question.  Find one irredundant orthogonal polygonal disk with uniquely
recognizable side lengths

```text
|A|, |B|, |C| pairwise distinct,
|H| = |A|+|B|+|C|,
```

the endpoint types (4.2), and two explicit rooted patches `ABC` and `ACB`.
For each patch, coordinate inequalities must prove:

1. the three code sides cover `H` exactly;
2. all four occurrences have disjoint interiors;
3. no unlisted contact is used to repair a gap at an internal division; and
4. the two patches are not related by a full-plane isometry (equivalently,
   their subdivision words are not reversals).

No coordinate search, optimizer, SVG or candidate promotion is admitted by
this lemma.
