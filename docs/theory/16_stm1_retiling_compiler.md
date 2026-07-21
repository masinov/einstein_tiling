# ST-M1.K3R — inverse retiling compiler

**Date:** 2026-07-21

**Status:** one rigidity lemma and one conditional compiler theorem in proof
draft; no polygon, search run, or novelty claim

## 1. Why the undeformed flag kite carries no state

Scale the K3F corner kite so its sides, cyclically from the `60`-degree
corner, have lengths

```
1, 1/sqrt(3), 1/sqrt(3), 1,
```

and its angles are `60,90,120,90` degrees. Its standard three-copy union is
an equilateral triangle of side `2`.

### ST-M1.N10 — three-copy rigidity

Every edge-to-edge tiling of that side-two equilateral triangle by three
congruent copies of the convex corner kite is the standard
centroid-and-midpoints dissection, up to a symmetry of the macrotriangle.

### Proof

Every kite angle is at least `60` degrees. A `60`-degree macro corner must
therefore contain exactly one kite corner, and that corner must be the unique
`60`-degree corner of its copy. The three macro corners use the three such
kite corners.

At a macro corner, the two incident kite sides coincide with the two macro
boundary rays. Both have length `1`; because the macro side has length `2`,
their endpoints are the midpoints of the adjacent macro sides. Hence the
placement of the kite at each macro corner is completely fixed. The three
fixed copies are precisely the corner regions meeting at the centroid, and
their interiors partition the macrotriangle. No alternative placement
remains. \(\square\)

The scope matters: this does not exclude a nonconvex deformation, more than
three copies, non-edge-to-edge macro contacts, or a different macrocell. It
does show that merely adding state names to the undeformed K3F support cannot
produce contextual geometry.

## 2. Retilings as symbols

The constructive alternative is to seek one compact polygonal disk `P` and
one periodically tileable macrocell `M` such that `M` has several exact
tilings by a fixed number `m` of congruent copies of `P`. A rooted retiling is
a symbol. The positions where constituent vertices meet the boundary of `M`
form its boundary signature; adjacent macrocells are compatible only when
their signatures and primitive contacts agree.

This differs from fixed fusion. The number `m` of physical copies per
macrocell is constant, but the source state is the **choice of retiling** and
its boundary signature. Irrational frequencies of source states are not
component-count ratios inside `P`.

For ST-M1 the intended macrocell may be the equilateral source triangle or a
larger fixed block of the K3F flag scaffold. N10 says `m=3` with the undeformed
convex corner kite supplies only one symbol, so a useful construction must
change at least one of support, multiplicity or contact topology.

## 3. Conditional compiler theorem

Let `R(P,M)` be a finite list of rooted exact `m`-copy retilings of `M` by
`P`. Assume the following.

- **R1 — geometric completeness.** Every whole-plane `P`-tiling admits a
  unique finite-radius partition into copies of `M`, and every macrocell uses
  one retiling in `R(P,M)`.
- **R2 — finite interface completeness.** Every primitive constituent
  contact, macro-boundary subdivision, macro vertex, point contact and
  T-junction belongs to a stated finite atlas. Neighboring retilings agree
  exactly when the atlas permits their common boundary signature.
- **R3 — source decoder.** The complete locally admitted retiling language has
  a finite-radius translation-equivariant decoder into S0 (or another proved
  aperiodic target), including the reflected branch.
- **R4 — chirality.** The atlas either forces one determinant sign on every
  connected tiling, with a reflected decoder for the other global branch, or
  directly covers every mixed-handed configuration in R3.
- **R5 — lift.** At least one compatible whole-plane source configuration has
  an exact `P`-tiling realization by the stated retilings.

### ST-M1.K3R

Under R1--R5, `P` is an aperiodic monotile for the full Euclidean isometry
group.

### Proof

R5 proves tileability. R1 and R2 turn every `P`-tiling into a configuration of
the complete finite retiling language; R3 maps it locally and equivariantly to
the aperiodic source. R4 makes this total under the declared full-isometry
semantics. A translational period of the `P`-tiling would transfer to its
source image, contradicting S0/Q0. \(\square\)

K3R is a sufficient contract, not a claim that arbitrary finite tile sets can
be compiled to one polygon.

## 4. Why this is a search improvement

Blind enumeration asks a shape to reveal tileability, aperiodicity and its
proof structure after the fact. Inverse retiling fixes the proof interface
first. A candidate must solve exact equations

```
union(g_1 P,...,g_m P) = M,
interior(g_i P) intersect interior(g_j P) = empty,
```

for several distinct transformation tuples, while their boundary signatures
realize a prescribed finite symbolic relation.

This gives cheap rejection layers before a whole-plane search:

1. at least two inequivalent exact retilings of `M`;
2. enough distinct boundary signatures to encode a selected source core;
3. exact compatibility with the K3F internal/midpoint/vertex relations;
4. no periodic macro configuration in the full local closure;
5. a plausible unique-macro marker and chirality guard.

Only survivors merit a complete primitive-contact atlas or witness lift. A
candidate generated this way tiles by construction once one compatible macro
configuration is supplied; the hard all-tilings burden remains R1--R4.

## 5. Full-edge deterministic no-go

A boundary deformation that preserves the K3F scaffold and gives every one
of the four sides exactly one full-side neighbor has no contextual state if
each complementary side pair has a unique relative placement. The rooted
contact star is then fixed by the carrier role and global handedness. Its
macro language is periodic and cannot factor onto S0.

Therefore a viable K3G/K3R geometry must deliberately include at least one of:

- multiple inequivalent exact retilings of a macrocell;
- more than one discrete full-side alignment;
- a **stated** contact subdivision/multi-neighbor interface; or
- a variable but uniquely recoverable macro scaffold.

This corrects “exclude T-junctions” to “classify every T-junction.” An
intentional subdivision can carry information; an unrecorded one invalidates
completeness.

## 6. Bounded HC-11 mechanism question

The remaining checkpoint asks whether a guarded macrocell can have several
exact retilings while still forcing unique whole-plane macro grouping. The
design must name:

1. the fixed macrocell `M` and multiplicity `m`;
2. the finite family of intended retilings;
3. which boundary subdivisions encode modes;
4. a local marker proving R1 rather than assuming a macro grid; and
5. why unintended partial contacts reduce to a finite atlas.

If no such on-paper template is available in the final HC-11 session, no
inverse-geometry run is admitted.
