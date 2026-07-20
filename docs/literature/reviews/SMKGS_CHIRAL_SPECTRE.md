# Smith–Myers–Kaplan–Goodman-Strauss: chiral Spectre domain bridge

**Catalog ID:** `smkgs-chiral-2024`  
**Audited version:** *Combinatorial Theory* 4(2) (2024), #13 / arXiv:2305.17743  
**Audit date:** 2026-07-20  
**Status:** targeted full-text audit of Sections 2.2–5, especially Theorem 3.1

## Why this matters for D1

The paper's tiling convention is not restricted to edge-to-edge polygon
tilings. An edge patch is defined using an arbitrary connected intersection
arc of two tiles, so vertices on polygon sides and subdivided maximal segments
are included. Theorem 3.1 therefore supplies the published bridge from every
straight `Tile(1,1)` tiling to a discrete hat–turtle description.

The proof uses the following chain.

1. Adjacency propagates one common family of edge directions, so after one
   global rotation every tile has one of 24 orientations (12 rotations for
   each handedness).
2. The six directions split into even and odd classes. Direction-wise edge
   vector sums vanish, allowing all even or all odd unit edges to be changed
   to length `sqrt(3)` without changing the tiling's combinatorial complex.
3. The two choices produce combinatorially equivalent tilings by hats and
   turtles. Conversely, setting the long edges back to one recovers a
   `Tile(1,1)` tiling.
4. Hats and turtles align to one `[3.4.6.4]` Laves tiling, using the alignment
   result inherited from the Hat paper.
5. Lemma 2.3 establishes that the edge-patch correspondence extends globally;
   Theorem 3.1 states the bijection and preservation of translations and
   handedness.

The paper then reduces all homochiral hat–turtle tilings, groups them into the
marked clusters, and proves the unique hierarchy. Thus its published theorem
already covers the unrestricted-contact Spectre hull.

## What the certificate imports and verifies

The theorem is an external route for reducing unrestricted straight-Spectre
tilings to a discrete aligned complex and for preserving periodicity. Session
55 now encodes the local domain bridge independently:

- the 14 primitive edges merge into 13 sides with lengths `12×1+1×2`;
- the exact angle hypotheses bound each interface to two sides per half-plane;
- all ten ordered equal-length side words share one unique unit subdivision;
- the collinear 180-degree vertex resolves every apparent T-junction;
- adjacency locks one 30-degree frame and primitive endpoints lock rank-four
  module anchors;
- both even/odd `sqrt(3)` deformations close and remain simple exactly.

This composes the published unrestricted scope with the exact radius-five L18
entry theorem. D1/D2/D3/D5/D6 are now recorded over the full fixed-chirality
hull. D4's finite maps are now explicit as well: the 17 physical-interface
states and 17 A6 collars are bijective, all component boundaries round-trip,
and a determinant-one phase map reconstructs three consecutive generated
physical levels. Full D4 remains partial because the abstract state SFT is an
over-approximation; 80 radius-two context seeds still require comparison with
the physical-derived hull.

## Relation to the new radius-five result

The ancestry-free computation proves that the three non-L18 coronas have exact
physical frontier `3→89→368→282→0`. The ten-case bridge now composes this
finite theorem with the published unrestricted domain. Further blind
polygon-ring expansion is unnecessary; the next structural task is the pinned
D4 context comparison for those 80 seeds.
