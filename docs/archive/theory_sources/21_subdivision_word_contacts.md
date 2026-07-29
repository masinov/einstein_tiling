# K6O — subdivision-word contact capacity

**Date:** 2026-07-22

**Status:** exact contact-complex proof draft; no polygonal realization,
whole-plane forcing or monotile claim

## 1. Why partial contacts change the channel

N18 closes disjoint optional boundary ports because gapless coverage fills
every port. A subdivided host side uses that fact instead of fighting it.
Every point of one long side is filled, but several neighbors fill consecutive
subintervals. If their complete contact sides have unequal intrinsic lengths,
their left-to-right order is visible from the unmarked contact complex.

The construction is first studied as an interval complex. Realizing that
complex by congruent polygonal disks without overlap is a separate geometric
obligation.

## 2. The fixed subdivision-word model

Let `P` be a polygonal topological disk admitted under the full Euclidean
group. A **rooted `k`-subdivision patch** consists of one host occurrence `H`
and neighbor occurrences `N_1,...,N_k` such that:

1. `H` has an intrinsically identified straight host side `e` of length `L`;
2. `N_i` meets `e` in one whole side of intrinsic length `lambda_i>0`;
3. the `lambda_i` are pairwise distinct and
   `lambda_1+...+lambda_k=L`;
4. the contact intervals have disjoint relative interiors and cover `e`;
5. every internal division point has exactly the host and the two consecutive
   neighbors as participants; and
6. the host role and the `k` neighbor-side roles are recognizable from the
   contact patch, for example because their side lengths occur uniquely in
   `P`.

Reading from one endpoint of `e` gives a permutation
`sigma in S_k`. Since no orientation of the plane or endpoint of an unmarked
segment is distinguished, the intrinsic contact word is the reversal class

```text
[sigma] = {sigma, reverse(sigma)}.
```

Conditions 1 and 6 deliberately exclude a congruence that sends the host to a
different role. They are recognition hypotheses, not a claimed polygon.

## 3. K6O: exact order capacity

### ST-M1.K6O

For `k>=2`, the interval complexes of rooted `k`-subdivision words with
pairwise distinct role lengths have exactly

```text
k! / 2
```

classes under the full Euclidean group. Two words define the same class if
and only if one is the reverse of the other.

### Proof

Any Euclidean isometry carrying one rooted contact interval to another maps
its two endpoints to the two endpoints of the target interval. Its restriction
to that interval therefore either preserves or reverses linear order. Because
the contact lengths are pairwise distinct, the ordered list of subinterval
lengths recovers the role permutation exactly. Hence congruent interval
complexes have equal or reversed words.

Conversely, reflection in the perpendicular bisector of the host interval
reverses every subdivision word, so a word and its reverse are congruent.
For `k>=2` no permutation equals its own reversal: the first and last entries
would have to agree, contradicting distinctness. Reversal therefore acts
freely on `S_k`, giving `k!/2` orbits.  □

The theorem counts contact complexes. Additional polygon geometry can delete
words by overlap or angle incompatibility and can never increase the count.

## 4. N20: the three-occurrence junction is not binary

### ST-M1.N20

A host side partitioned into exactly two unequal whole neighbor sides has
only one state under full Euclidean isometry. It cannot by itself be an
intrinsic binary choice carrier.

### Proof

K6O gives `2!/2=1`. The apparent choices `(1,2)` and `(2,1)` are mirror
images of the complete unmarked patch.  □

This is the smallest gapless T-junction: three tile occurrences meet at its
one internal division point. It is useful as a rigid contact, but not as a
bit unless a second, independently visible structure or a one-handed motion
convention breaks the reflection. Under ordinary full-isometry monotile
semantics, post-hoc labels `left` and `right` do not do so.

## 5. The first surviving capacities

K6O gives:

| neighbors on one host side | raw orders | full-isometry order states |
|---:|---:|---:|
| 2 | 2 | 1 |
| 3 | 6 | 3 |
| 4 | 24 | 12 |

Thus a host with three unequal neighbors is the smallest bare subdivision
that carries more than one state. A host with four unequal neighbors has
exactly twelve abstract states, matching the twelve-state topology retained
by K5S. This is a capacity coincidence only. It does not show that one
polygon realizes all twelve patches or that neighboring hosts communicate
Wang colors.

If an eleven-state source is preferred, one may split one source state into
two symbolically identical copies before compilation: forgetting the copy
index maps every resulting tiling to the original aperiodic source. That
standard symbolic padding does not solve the geometric realization.

## 6. J0: endpoint-angle equations

Let one internal division point separate role `i` on the left from role `j`
on the right. Let `rho_i` be the interior angle of `N_i` at its right contact
endpoint and `ell_j` the interior angle of `N_j` at its left contact endpoint,
in their placed orientations.

### ST-M1.J0

Every exact three-participant internal T-junction satisfies

```text
rho_i + ell_j = pi.
```

### Proof

The point lies in the relative interior of the host side, so the host occupies
one straight sector of angle `pi`. The two neighbor interiors are disjoint and
gaplessly fill the other half-disk. Their two sectors therefore sum to the
remaining angle `pi`.  □

This elementary equation is a useful pre-geometry filter. In particular:

- if every code side has two right-angle endpoints, every order is locally
  angle-compatible without coordinating handedness;
- more generally, a common endpoint pair `{theta, pi-theta}` gives a
  sufficient locally compatible port vocabulary when orientations are chosen
  consistently; and
- if each role must use one fixed directed pose and every permutation for
  `k>=3` is admitted, then all left endpoint angles are equal, all right
  endpoint angles are equal, and the two common values sum to `pi`.

For the last claim, fix one role `i` and place it before any two other roles
`j,j'`; J0 gives `rho_i+ell_j=rho_i+ell_j'=pi`, hence
`ell_j=ell_j'`. With at least three roles this propagates to every left
angle. The symmetric argument fixes every right angle.

J0 is necessary only at the stated three-participant junction. Extra point
participants or an additional emanating contact change the sector equation
and belong to another class.

## 7. What the order channel does not enforce

The subdivision word makes one selected order visible **after** a legal patch
exists. It does not yet prove:

1. **polygonal realization:** congruent full copies can occupy all roles with
   disjoint interiors;
2. **word availability:** more than one non-reversal word survives the full
   polygon geometry;
3. **host forcing:** every occurrence uses exactly one host role and each
   host gets exactly `k` code neighbors;
4. **role exclusivity:** no other combination of boundary sides sums to `L`;
5. **FLC/contact completeness:** no slide, partial cover, extra participant or
   alternative T-junction occurs;
6. **communication:** external contacts expose the four source interfaces;
7. **whole-plane lift and converse:** at least one tiling exists and every
   unrestricted tiling decodes.

The order channel therefore does not reopen K5C or establish K4W. It is a
smaller exact primitive: unlike disjoint optional ports, every listed port is
occupied; unlike a fixed-successor ring, its state is an asymmetric finite
order rather than a transitive orbit.

## 8. HC-15 remaining question

Session 102 must decide the geometric part for the first surviving class:
one host plus three unequal whole-side neighbors. It must either give exact
coordinates for one polygon and two non-reversal, nonoverlapping contact
patches, or prove a scoped obstruction for that class. An interval diagram,
bounding-box sketch or assertion that thin arms can be added is not an exact
polygonal witness.

## 9. N21: convex complementary ports cannot realize the channel

The first geometric attempt gives every code side a complementary endpoint
pair. This includes the especially natural right-angle vocabulary suggested
by J0 and every fixed-directed-pose carrier that admits all permutations.

Call an irredundant convex polygon a **complementary-port carrier** when it
has a distinct host side and `k>=3` code sides, every code side's two interior
endpoint angles sum to `pi`, and the code-side lengths sum to the host length.
Consecutive collinear boundary segments are merged, so every exterior turn is
strictly positive.

### ST-M1.N21

No complementary-port carrier exists for `k>=3`.

### Proof

Write `delta_v=pi-alpha_v>0` for the exterior turn at a polygon vertex. A
code side with endpoint angles `alpha_u,alpha_v` has

```text
delta_u + delta_v
  = 2*pi - (alpha_u+alpha_v)
  = pi.                                      (1)
```

The code sides form one or more maximal path blocks in the polygon's boundary
cycle because the distinct host side is not a code side. Along a block of `r`
code sides, equation (1) makes the vertex turns alternate

```text
delta_0, pi-delta_0, delta_0, pi-delta_0, ... .
```

Hence a one-edge block consumes exactly `pi` exterior turn; a two-edge block
consumes `pi+delta_0>pi`; a three-edge block consumes exactly `2*pi`; and any
block of four or more edges consumes more than `2*pi` (the four-edge prefix
already consumes `2*pi+delta_0`).

Every convex polygon has total exterior turn `2*pi`. If there are two code
blocks and at least three code sides, one block contains at least two sides,
so the two blocks consume strictly more than `2*pi`. Three or more blocks
consume at least `3*pi`. A single block of four or more sides also consumes
more than `2*pi`.

The only remaining case is one block of exactly three code sides. Its four
vertices already consume the full `2*pi`, so strict positivity leaves no
other vertex. The polygon must be a quadrilateral consisting of those three
code sides and the host side. But a nondegenerate polygon side is strictly
shorter than the sum of all the other side lengths, whereas the carrier
requires

```text
length(host) = length(code_1)+length(code_2)+length(code_3).
```

The quadrilateral is therefore degenerate, a contradiction.  □

### Corollaries and scope

1. A convex right-angle-port realization of the three- or four-neighbor
   order channel is impossible.
2. In the fixed directed-pose model of Section 6, admitting every permutation
   forces a common complementary endpoint pair, so no convex universal-order
   carrier exists for any `k>=3`.
3. The twelve-state `k=4` capacity cannot be realized by merely placing four
   separated rectangular ports around a convex support.

N21 does **not** cover a nonconvex polygon, a junction with extra
participants, a code side whose orientation/handedness changes contextually,
or a carrier that deliberately realizes only a selected subset of words with
non-complementary endpoints. Those are precisely the harder geometries left
outside HC-15.

## 10. HC-15 disposition

The checkpoint has a useful positive and a decisive negative:

- K6O gives an exact fully occupied order channel with capacities
  `1,3,12,...`; and
- N21 closes its simplest convex, universally compatible geometric
  realization.

No exact nonconvex polygonal disk realizing two non-reversal three-neighbor
words was derived within the checkpoint. The HC-15 stop rule therefore fires.
Subdivision order is retained as a compiler-aware **search primitive**, not a
candidate tile or a reopened K5C proof.

Reopening requires, before computation, exact coordinates for one nonconvex
polygon and two proposed non-reversal patches, together with hand-checkable
proofs of side-role recognition, disjoint interiors and exact host coverage.
Only after that local witness survives may a separately authorized experiment
classify its unintended contacts or test whole-plane forcing.
