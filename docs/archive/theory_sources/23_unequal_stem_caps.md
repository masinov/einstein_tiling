# N22 — unequal stems require a secondary participant

**Date:** 2026-07-22

**Status:** exact local-topology proof draft; no cap geometry, polygonal
witness, whole-plane forcing or monotile claim

## 1. HC-17 route fixed before cap design

HC-17 deliberately leaves K7C's equal-stem class. It retains K7A's two
selected words and ordinary three-participant primary junctions, but permits
the two neighbor sides leaving a primary junction to have unequal first
segment lengths. The shorter side ends first. The admitted route allows
exactly one additional congruent **cap occurrence** at that secondary vertex.

It does not allow contextual handedness, an unbounded cascade of new
junctions, or an unspecified contact atlas. Within three sessions the cap
must close as a finite exact contact complex or the route freezes without a
shape search.

## 2. N22: the secondary-participant necessity

### ST-M1.N22

Let two polygonal disk occurrences `X,Y` meet along the stem leaving an
ordinary internal host subdivision point. Suppose the boundary side of `X`
has first-vertex distance `u`, the coincident side of `Y` continues to
distance `v>u`, and the tiling is locally finite and gapless. Then at least
one occurrence other than `X,Y` contains the shorter-side endpoint `P`.

Thus unequal stems cannot remain a two-neighbor collar. They necessarily
create a secondary junction.

### Proof

From the primary junction to `P`, the two sides coincide and separate the
interiors of `X` and `Y`. At `P`, the irredundant boundary of `X` leaves the
continued line while the side of `Y` remains straight. In a sufficiently
small disk around `P`, `Y` occupies the half-disk on its side of that line.
The departing side of `X` cuts a nonzero sector from the opposite half-disk;
the complementary sector between that side and the continued line is outside
both `X` and `Y`.

Plane coverage fills this open sector. Local finiteness supplies an
occurrence `Z` whose closure contains `P`. Hence `P` has an additional
participant. □

If exactly one cap `Z` fills the sector and no other boundary ray emanates
from `P`, the continuing side of `Y` again supplies a straight `pi` sector.
Writing `alpha_X` and `alpha_Z` for the two angles on the other side gives

```text
alpha_X + alpha_Z = pi.                              (2.1)
```

In the orthogonal specialization both are `pi/2`. This is a second J0-type
equation, not a free socket into which an arbitrary cap can be inserted.

## 3. Consequence for the design space

N22 resolves the first HC-17 branch point:

- unequal stems with no new occurrence are impossible in a gapless tiling;
- a bounded one-cap mechanism remains logically possible; and
- the cap's entry angle is already fixed by (2.1).

The next task is finite algebra, not coordinates: assign directed first-stem
lengths to `A,B,C` so all four primary adjacencies in `ABC,ACB` create the
same recognizable excess and cap orientation. If that system has no
nontrivial solution, the route closes before any polygon is considered.

## 4. K8U: the uniform directed mismatch family

Write `r_X` for the first stem length leaving the right endpoint of role `X`
and `l_X` for the analogous left length. The four directed adjacencies in the
two selected words are

```text
E = {(A,B), (B,C), (A,C), (C,B)}.                    (4.1)
```

A **uniform left-short signature** has one `s>0` and one `Delta>0` such that,
at every `(X,Y) in E`, the stem from the spatially left occurrence `X` ends
at `s` while the stem of `Y` continues to `s+Delta`. The right-short
signature is its mirror.

### ST-M1.K8U

All four adjacencies have one uniform left-short signature if and only if

```text
r_A = r_B = r_C = s,
l_B = l_C = s+Delta.                                (4.2)
```

Up to reflection, (4.2) is the unique directed one-cap length assignment.

### Proof

The two adjacencies beginning with `A` give

```text
r_A=s,       l_B=l_C=s+Delta.
```

The adjacency `(B,C)` then gives `r_B=s`, and `(C,B)` gives `r_C=s`.
This proves necessity. Substitution in all four pairs proves sufficiency.
Reversing the complete patch interchanges left and right and gives the only
other uniform orientation. □

The unused `l_A` remains outside both selected words, exactly as in K7A. It
does not alter the mismatch sockets.

## 5. The exact socket left for geometry

With (4.2), each of the two internal divisions in either word has the same
local form:

1. a shared orthogonal stem of length `s`;
2. a secondary right-angle T-junction where the left occurrence turns;
3. an exposed straight continuation of the right occurrence of length
   exactly `Delta`; and
4. one cap occurrence entering that sector with angle `pi/2`.

If the cap uses one complete side along the exposed continuation, that side
must have intrinsic length `Delta`. This is necessary for the bounded socket
specified by HC-17; using only a proper subsegment would create another
T-junction before the longer stem ends and would already violate the
one-secondary-cap route.

K8U therefore removes all state-dependent length choices. Every admitted
host word creates two copies of one socket type. K7A still carries the binary
state; the cap is structural rather than another label.

What remains open is the lower endpoint of the cap side. When the longer
stem and the cap side end together, their next boundary pieces must close
using only the same local occurrences. If they separate and expose another
sector, N22 applies again and starts a tertiary cascade. Session 108 must
either provide a finite exact contact cycle closing this endpoint or fire the
HC-17 stop. An assertion that the cap “turns the corner” is not such a cycle.

## 6. N23: a one-edge cap transports the defect

The most economical proposed endpoint uses the existing K7A reflex vertex.
Orient the cap's `A` side vertically, with its convex `pi/2` endpoint at the
upper secondary T-junction and its reflex `3*pi/2` endpoint at the lower end
of the exposed continuation. If the longer neighbor has a convex `pi/2`
angle there, the two angles sum to `2*pi`.

That angle sum prevents an uncovered sector, but it does not terminate the
contact.

### ST-M1.N23

Let two polygonal disk occurrences `Y,Z` have disjoint interiors, share a
nondegenerate boundary segment ending at `Q`, and together cover a
neighborhood of `Q`. If no third occurrence contains `Q`, then their common
boundary continues through `Q` along another nondegenerate segment. Hence a
single complete cap side cannot absorb the unequal-stem defect at its lower
endpoint.

### Proof

Choose a disk around `Q` containing no other polygon vertex except `Q` and,
by local finiteness and the hypothesis, no other tile occurrence. The two
tile interiors are disjoint open subsets whose closures cover the disk. Their
common boundary is therefore the local separator between the two sides.

The incoming shared segment supplies one branch of that separator ending at
`Q`. A separator cannot end in the interior of the disk: a sufficiently small
circle about `Q` would otherwise contain one transition between the two open
interiors, whereas transitions on a circle occur in pairs. Polygonality then
supplies a second straight branch of positive length leaving `Q`, and that
branch belongs to both boundaries. □

For the `pi/2 + 3*pi/2` endpoint, N23 says exactly that the cap and longer
neighbor turn together and share their next sides. If those sides have
unequal lengths, N22 recurs at their first unequal endpoint. If they have
equal lengths, the common interface merely advances to the next pair of
vertices. Absorption requires an explicit finite multi-edge interface whose
two branches return to the original shorter occurrence. No such interface is
implied by K8U or by the angle sum.

## 7. HC-17 disposition

HC-17 produces a sharp positive/negative boundary:

- N22 proves that unequal stems necessarily introduce the secondary cap;
- K8U gives the unique uniform directed mismatch family; and
- N23 proves that the natural one-edge cap cannot terminate the mismatch.

No finite multi-edge cap cycle closing both interface branches back onto the
original shorter occurrence was derived. Introducing another occurrence at
the lower endpoint violates the one-cap route; following an unspecified
sequence of equal sides is precisely the unbounded contact atlas excluded at
admission.

The predeclared HC-17 stop therefore fires after session 108. This is not a
no-go theorem for all unequal-stem mechanisms: a future exact polygon might
contain a finite, recognizable multi-edge cap cycle. Reopening requires that
complete cyclic boundary word and its placement isometries before any
coordinate search. N22/K8U/N23 remain exact admission filters for such a
proposal.
