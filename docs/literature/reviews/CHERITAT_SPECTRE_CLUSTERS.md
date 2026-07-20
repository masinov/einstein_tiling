# Chéritat: Spectre hex clusters and unique hierarchy

**Catalog ID:** `cheritat-spectre-clusters-2024`  
**Audited version:** arXiv:2407.05359v1, 2024-07-07  
**Audit date:** 2026-07-20  
**Status:** targeted audit of the equivalence and hierarchy theorem chain;
the long deferred local-case appendix was not independently rederived.

## Scope

The paper studies the undeformed straight-edged `Tile(1,1)` and calls it a
Spectre under an explicit convention: translations and rotations are allowed,
reflections are not. Every hierarchy statement is about **all whole-plane
tilings** admitted under that convention, not only patches produced by one
substitution.

This scope must stay explicit. It is not automatically a theorem about mixed
handedness tilings or about arbitrary edge-modified strict Spectres.

## Proof architecture

The argument creates a sequence of combinatorially equivalent descriptions:

```text
Spectres
  -> decorated D3/D2 tiling
  -> blue connected components plus interfaces
  -> marked triangular tiles
  -> unique yellow clusters and packs
  -> reflected higher-level component system
  -> repeat
```

Important junctions are:

- **Theorem 30:** every whole-plane Spectre tiling decomposes into the finite
  component/interface pieces of Figure 76.
- **Theorem 31:** a global arrangement satisfying four explicit covering,
  disjointness, interface and yellow-marking conditions reconstructs a
  Spectre tiling and covers the plane.
- **Proposition 34 and Proposition 38:** contraction and the retained dot data
  recover the relevant Spectre information bijectively.
- **Theorem 51:** the packed-piece and three triangular tileset descriptions
  are equivalent to whole-plane Spectre tilings.
- **Proposition 52:** yellow clusters correspond bijectively to vertices of a
  higher-level honeycomb with controlled orientation and adjacency.
- **Propositions 60--62** plus the deferred proofs classify the environments
  of all three higher-level yellow cluster types.
- **Corollary 63:** every whole-plane Spectre tiling without reflections is
  uniquely hierarchical. The proof explicitly says that every grouping and
  every equivalence correspondence is unique, so the construction repeats at
  the next level.
- **Proposition 64 and Corollary 65:** the arrows can be traversed in reverse;
  compactness/diagonal extraction gives existence of whole-plane Spectre
  tilings.

The paper then presents explicit equivalent substitutions in Section 2.13.
The logical order matters: a substitution that generates examples is not the
proof that every legal tiling admits the unique inverse grouping. Corollary 63
rests on the preceding whole-plane case classification.

## What a computational certificate must reproduce

Chéritat's result supplies a concrete checklist for a non-circular W3 route:

1. define the motion convention and the entire geometrically admitted
   whole-plane domain;
2. construct parent objects for every tiling in that domain;
3. prove the grouping unique, including boundary/interface ownership;
4. prove each representation change is faithful in both directions;
5. prove the parent description lies in the same domain, so the argument
   iterates indefinitely;
6. provide a local recognition radius or an exhaustive finite case table;
7. combine unique iteration with geometric scale growth to rule out every
   nonzero translational stabilizer;
8. separately construct at least one whole-plane tiling.

These are emitted as `D1`--`D7` by the W3 certificate audit. They refine C4
and C5 rather than replace C1--C5.

## Comparison with the recovered 17-state artifact

The current artifact has exact strengths:

- one deterministic child rule for each of 17 states;
- finite-alphabet closure and primitive incidence;
- 309 sampled complete contexts with unique composition;
- exact recurrent geometry and an all-level macro-side endpoint skeleton.

It does **not** yet reproduce Corollary 63:

- its collars were recovered from interiors of generated Delta patches;
- no formal language equals all geometrically legal whole-plane tilings;
- no exhaustive all-tilings parent-existence table is encoded;
- sampled ownership uniqueness does not establish boundary ownership;
- the correspondence between collared states and physical Spectre tilings is
  not proved bijective over the full hull;
- no finite uniform inverse radius or scale-period descent theorem is stored.

Accordingly, Chéritat proves the external Spectre result, while our W3
artifact remains an independently verified partial reconstruction.

## Independent finite comparison

The first ancestry-blind experiment is complete through an existential
three-ring prefix in the edge-to-edge model. Its 166 central coronas contract
to 30 at radius two and 21 at radius three; the generated substitution
language contains 18. The three extras all have exact radius-four witnesses.
Moreover, none of the 21 viable types has a unique central parent occurrence.
This is useful negative information: Chéritat's unique grouping cannot be
reproduced by choosing a parent for each central tile independently at this
radius.

The finite comparison has now encoded compatible parent occurrences jointly
on overlapping centers. A buffered exact-partition SAT
language preserves all 18 generated corona controls and eliminates all three
extras by radius four. Corona 33 has 200 coordinated third-ring frontier
states and corona 155 has 24; neither has a fourth-ring successor. Corona 44
has no coordinated third-ring frontier after all 27 second-ring branches are
handled. Boundary branches with no universally buffered target are expanded
physically rather than declared UNSAT.

Subsequent experiments have now removed that conditionality throughout the
fixed-chirality edge-to-edge model. The 18-corona physical language has a
418-case radius-three parent transducer and a unique 8/9 partition; contraction
closes to the 17 generated states after the radius-three defect CSP. Finally,
the three physical coronas outside L18 have complete ancestry-free frontier
`3→89→368→282→0`, proving that every whole-plane tiling in this contact model
enters L18.

The ten-case maximal-segment atlas now matches Chéritat's broader edge-patch
scope: arbitrary vertices on sides reduce to the primitive exact module
contacts used by L18. D4's finite correspondence kernel has also been made
explicit: 17 colored interfaces map bijectively to 17 A6 collars, every
component boundary round-trips, and determinant-one phase maps reconstruct
three consecutive generated physical levels. This reproduces the coordinate
role of the arrows in Figure 137, but not yet their whole-plane context
classification. The abstract radius-one state SFT admits 536 nonphysical
output-overlap stars; 80 seeds survive radius two. Eliminating or physically
identifying those 80 is the remaining independent analogue of Chéritat's
faithful all-tilings equivalence. See `SMKGS_CHIRAL_SPECTRE.md` for the original
paper's Theorem 3.1 route through aligned hat–turtle tilings.
