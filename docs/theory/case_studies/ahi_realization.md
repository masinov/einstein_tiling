# AHI/Sturmian branch closure

**Date:** 2026-07-29  
**Status:** closed research branch; reusable results classified below  
**Scope:** work derived from the Akiyama--Hamada--Ito Section 10.1 source and
the subsequent one-support erasure attempts

## 1. The question and the outcome

The branch tried to replace one finite coloured AHI Sturmian-lattice system
by one connected unmarked polygon `P` such that:

1. `P` tiles the Euclidean plane;
2. every tiling in `X(P)` admits a finite-radius equivariant decoder into the
   chosen aperiodic source hull; and
3. therefore every translational period of a `P` tiling descends to an
   impossible source period.

It did **not** construct such a polygon and did **not** prove that none exists.
It also did not decide the general Sturmian-monotile problem. What it achieved
is a precise separation of the easy symbolic layer from the hard geometric
one, plus several complete no-go theorems for named erasure families.

## 2. Dependency graph

```text
external AHI aperiodic source
          |
          v
exact finite source presentation             CLOSED for the benchmark
(30,30,2 triangles; 31 rhombi; 12 states)
          |
          v
finite local relation compilation            CLOSED in general (K74A/K74R)
          |
          v
one connected unmarked support               OPEN
forcing all roles and contacts
          |
          v
total decoder on every unrestricted tiling   OPEN
          |
          v
period descent / aperiodic monotile           CONDITIONAL ONLY
```

Only the last two arrows are the monotile problem. The zipper work addressed
the already-closed middle arrow after K74A made its generality explicit.

## 3. Reusable source-independent results

These statements do not depend essentially on the AHI `31`-address atlas.

| Result | General content | Final disposition |
|---|---|---|
| Q0 / K1T | A decoder must be total on the full local closure; image-only agreement is insufficient | keep as proof/certificate contract; standard compact symbolic dynamics |
| N55 | A nonempty root-deterministic finite `Z^2` carrier is periodic, so it cannot factor to an aperiodic target | keep as a general no-go |
| U2 | Marked one-connected-polygon realization is undecidable via product with a fixed aperiodic source | keep, explicitly conditional on Stade's preprint/all-tilings weave converse; standard reduction |
| K61R | Complete independent two-participant port erasure realizes exactly biclique/rectangular compatibility relations | keep as a general classification; familiar jigsaw-color principle |
| K62P / N62S | For the audited stick relation, physical completion of independent profiles forces a periodic completion | keep as a scoped application, not a universal shape theorem |
| K69A | One ordinary participant-separable sector star cannot realize ternary parity | keep as a small general algebraic no-go |
| K70A | Torsion-free participant-wise additive tests cannot distinguish even parity from the binary cube | keep as the general form; angles/lengths/areas/displacements are corollaries |
| K74A / K74R | Rooted three-participant junctions with hidden finite state realize every finite fixed-arity relation | keep as the positive local normal form; standard finite-state construction |

Together these give the reusable local hierarchy:

```text
independent two-body profiles     -> biclique relations only
ordinary/additive joint tests     -> cannot detect torsion parity
rooted hidden-state T-junctions   -> every finite local relation
```

This hierarchy classifies local expressivity. It does not classify which
contact systems one unmarked polygon can force.

## 4. AHI-specific benchmark results

These are exact facts about one source presentation. They should remain as
benchmark fixtures, not be presented as a theory of all Sturmian tiles.

- The reconstructed Section 10.1 supports have `30,30,2` primitive triangles,
  `15,15,1` common rhombi, and 31 addressed rhombus roles.
- The twelve-state quotient is
  `Z/3 x {0,1} x {0,1}` with role map `S=00`, `M=01/10`, `L=11`.
- Both large macros have the source-native decomposition one `L` hexagon,
  two `S` hexagons and six `M` connectors.
- The direct Turtle center-spoke erasure has no common simple support in the
  exhaustively checked `2^16` polarity spaces.
- The best two-large-macro overlap gives a 17-rhombus union, but its role
  difference cannot be completed by the source singleton alone.
- Source Figure 45 provides exact contextual same-support flips of 51 and 49
  rhombi; their support symmetries erase any radius-zero unmarked bit.
- The P17 carrier is a genuine local retiling kernel but cannot realize the
  required carrier-local source frequencies; the apparent all-singleton state
  is locally impossible in all 60 lozenge subdivisions.
- Carrier-local exact decoding below area 30 is excluded, area 30 has a fixed
  normal form, and any finite-area carrier-local realization needs a
  count-changing trade that is boundary-active.
- A boundary-neutral count-changing trade is impossible because changed rail
  bits propagate along unbounded source strips.

The exact artifacts and cold verifiers supporting these claims remain useful
for regression tests and future source-presentation work.

## 5. Scoped erasure families that are closed

The following are mathematical exclusions, not failed searches:

1. separable complete two-participant profiles for the fixed source relation;
2. root-deterministic finite carriers;
3. carrier-local P17 decoding;
4. carrier-local source decoding below area 30;
5. carrier-local boundary-neutral count-changing states at any area;
6. one ordinary sector-star parity coupler;
7. fixed-topology participant-separable torsion-free additive parity tests;
8. the unbroken convex-flank realization of the outward zipper.

None of these statements excludes arbitrary connected unmarked polygons,
cross-carrier decoders, nonseparable contact hyperedges, or a source different
from the chosen AHI presentation.

## 6. Work that is retained only as a worked derivation

K70Z--K73R—the parity zipper, terminal erasure, bent host, outward fan, and
curvature/reset bounds—are exact local geometry. K74G shows that their
symbolic content is the generic `Z/2` automaton instance. Their remaining
polygon realization problem has no special connection to Sturmian order.

These notes may remain as derivations and test examples during the later
repository consolidation, but they are frozen as research directions. A new
reset count, comb, boundary word, or minor geometric relaxation would add no
goal-level information.

## 7. The actual unresolved theorem

Let `S` be a computably presented nonempty aperiodic planar FLC tiling system.
Determine whether there exists a connected unmarked polygonal disk `P` and a
total finite-radius translation-equivariant map

```text
pi : X(P) -> X(S).                                       (7.1)
```

For the existential version, it is enough that `pi` is total; a period of a
`P` tiling then descends to a source period. Surjectivity is a stronger target
and is required before transferring positive entropy from `S`.

The branch leaves three meaningful outcomes open:

- construct such a `P` for some aperiodic Sturmian source;
- prove nonexistence for an architecture-independent realization class; or
- prove undecidability for a clearly specified computable family of connected
  unmarked supports, while identifying decidable subfamilies.

## 8. Freeze and reopening rule

This AHI-specific branch is closed. No further source-address census,
carrier-area ladder, zipper, comb, reset topology, or local finite-state gadget
is admitted.

Reopening requires one of:

1. a theorem about the one-support erasure map applying to a source-independent
   family;
2. a reduction establishing undecidability for a precisely defined unmarked
   connected realization class;
3. an exact polygon accompanied from inception by the complete total-decoder
   and unintended-contact certificate contract; or
4. a new source-level structural theorem that changes the global realization
   problem, rather than another finite presentation of it.

## 9. Claim permissions

Permitted:

- the branch reconstructed and verified one finite AHI source presentation;
- it proved the scoped family exclusions listed above;
- it classified the local expressivity boundary up to arbitrary finite
  relations in a rooted coloured contact model;
- the one-connected-unmarked total-erasure problem remains open here.

Forbidden:

- a Sturmian monotile was found;
- all Sturmian monotiles were classified;
- an arbitrary unmarked polygon compiler was proved impossible;
- K74A or the zipper is a novel general simulation technique;
- accumulating further AHI carrier exclusions approaches the general theorem.
