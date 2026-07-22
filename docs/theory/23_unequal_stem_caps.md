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
