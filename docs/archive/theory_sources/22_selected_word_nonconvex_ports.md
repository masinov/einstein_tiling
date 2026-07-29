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

At that host endpoint the reflex sector spills outside the vertical
projection of the host. If no third occurrence participates there and the
neighborhood is gaplessly covered, the host corner is forced to have angle
`2*pi-3*pi/2=pi/2`. This endpoint condition is separate from the two internal
J0 equations.

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

## 6. K7C: the common clean-collar reduction

Angle compatibility alone does not prevent the two neighbor copies from
crossing farther from an internal division point.  The first positive-length
piece of their common boundary supplies the next exact datum.

For a directed code role `X`, let `s_X^L` and `s_X^R` be the lengths of the
polygon sides leaving the left and right contact endpoints, measured from the
code side to their first subsequent vertices.  Call a rooted subdivision
patch **clean to depth `d>0`** when, at every internal division:

1. the two leaving sides coincide for their complete length `d`;
2. neither has a vertex before distance `d`; and
3. no fourth occurrence meets the relative interior of that stem.

The endpoint `L` of `A` is external in both selected words and is omitted.

### ST-M1.K7C

Both `ABC` and `ACB` have a clean collar if and only if the five used stem
lengths agree:

```text
s_A^R = s_B^L = s_B^R = s_C^L = s_C^R = d.          (6.1)
```

In the orthogonal K7A specialization, after normalizing the host to
`[0,L] x {0}` and placing the neighbors below it, the three occurrence
interiors inside the open host footprint `(0,L) x (-d,0)` are exactly the
three disjoint open rectangles under their code intervals. Their order can
be `ABC` or `ACB` without overlap inside that footprint. The reflex germ of
`A` at `x<0` is not part of this conclusion and belongs to its rooted tail.

### Proof

At an internal junction the two non-host boundary sides leave along the same
ray, because their two right-angle sectors fill the exterior host half-disk.
A clean stem ends at the first vertex of both sides, so its two intrinsic
lengths are equal.

The word `ABC` gives

```text
s_A^R=s_B^L,       s_B^R=s_C^L,
```

and `ACB` gives

```text
s_A^R=s_C^L,       s_C^R=s_B^L.
```

Transitivity yields (6.1). Conversely, (6.1) makes every required pair of
leaving sides coincide completely. In the orthogonal frame these common
stems are perpendicular to the host. Consecutive stems bound exactly one
rectangle whose width is the intervening code length and whose depth is `d`.
The three rectangles have disjoint interiors and cover the host collar. □

If two stem lengths differ, the shorter side ends at a new boundary vertex
while the longer continues. Closing the resulting region requires another
partial contact, T-junction or participant. That is a different mechanism,
not a failure that HC-16 may silently repair by adding geometry.

## 7. Exact tail-packing formulation

Normalize one rooted occurrence for each role so its code interval is
`[0,lambda_X] x {0}` and its clean collar lies below the line. Remove the
open collar rectangle and call the remaining closed set the rooted tail
`Q_X`. With `a=|A|`, `b=|B|`, `c=|C|`, the two neighbor patches below depth
`d` are exactly

```text
ABC : Q_A,  Q_B+(a,0),    Q_C+(a+b,0),
ACB : Q_A,  Q_C+(a,0),    Q_B+(a+c,0).                (7.1)
```

Thus the coordinate problem has two independent proof layers:

- K7A/K7C already settle the host-footprint collar
  `(0,L) x (-d,0)`; and
- exact set-intersection inequalities for the six translated tail pairs in
  (7.1), together with host-versus-tail inequalities, settle everything
  below it.

This formulation prevents a picture from hiding an overlap just beneath a
valid collar. It also shows why an ordinary rectangular tooth is not enough:
the same rooted tails must pack after the `B,C` offsets change by `c` and
`b`, respectively.

## 8. HC-16 disposition

The checkpoint establishes two exact facts:

- K7A turns the three abstract K6O order classes into an intrinsic binary
  channel by one named reflex endpoint; and
- K7C proves the complete common collar and writes the two remaining rooted
  tail packings explicitly.

No exact orthogonal polygonal disk was derived whose rooted tails satisfy
both rows of (7.1) and avoid the host occurrence. In particular, valid local
right-angle sectors and a valid rectangular collar were not treated as
evidence for global disjointness. No proposed coordinate list passed the
paper obligation, so none is recorded as a candidate.

HC-16's predeclared stop therefore fires after session 105. The named route
is frozen at the tail-packing equations. This is not a nonexistence theorem:
it does not say that a nonconvex selected-word carrier is impossible. It says
that the branch has an exact symbolic/contact kernel but no geometric witness
and may not consume a search merely to compensate for that missing idea.

Reopening requires, before computation, one exact irredundant polygon and the
four placement isometries for each word, followed by hand proofs of every
intersection in (7.1) and every host-versus-tail intersection. A different
route using unequal stems, contextual handedness or extra participants needs
its own checkpoint because it changes the admitted mechanism.
