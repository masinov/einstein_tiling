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
