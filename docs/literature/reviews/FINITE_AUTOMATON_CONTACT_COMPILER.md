# Finite-automaton contact compiler: prior-art boundary

**Audit date:** 2026-07-29  
**Object audited:** K74A/K74R/K74G in theory note 82

## Decision

K74A is a useful repository abstraction, but it is not a method-novelty
claim. Finite automata, Wang presentations, coloured matching rules,
edge-patch correspondences, boundary-profile encodings, and finite local
recodings already provide the relevant symbolic machinery. The particular
one-line angle assignment is an elementary realization of state continuity
at a prescribed rooted T-junction chain.

The sources audited here still do not supply the stronger result this project
needs: one connected unmarked planar polygon whose unrestricted gapless
tiling space forces the compiler topology and admits a total finite-radius
decoder. Absence from this audit is not evidence that such a theorem is new or
that none exists.

## Primary-source comparison

### Edge patches already contain the local topology

Smith--Myers--Kaplan--Goodman-Strauss, *A chiral aperiodic monotile*, Section
2.2, define edge patches around connected tile intersections and allow
vertices with three or more participants. Lemma 2.3 promotes a complete,
locally consistent edge-patch correspondence to a correspondence of whole
tiling spaces preserving translational periodicity.

Therefore the rooted three-participant junction used by K74A is an instance
of an established local proof object. K74A supplies its own finite-state angle
semantics; it does not supply the complete edge-patch correspondence for one
unmarked support.

### Finite symbolic recoding is standard

Fletcher's atlas construction converts finite coloured matching systems into
finite allowed-corona rules on congruent supports. Hellouin de
Menibus--Lutfalla--Vanier simulate symbolic rules over FLC geometric tiling
spaces using labels and forbidden patterns, and separately obtain geometric
undecidability with finite shapesets. Ollinger's polyomino construction
already uses selectors, code words, wires, and an all-tilings converse for a
finite functional shapeset. Demaine et al. encode finite coloured systems in
the poses and boundary profiles of one polygon in a prescribed-lattice,
near-plane model with gaps.

These results preempt broad novelty claims for automaton states, delimiter
states, hidden state propagation, prefix tries, or geometric encoding of
finite relations. Their retained hypotheses—decorations, atlases, several
supports, gaps, prescribed lattice sites, or a finite fibre—are precisely why
they do not close the ordinary one-unmarked-polygon problem.

### Matching rules for hierarchical tilings

Vereshchagin's 2026 preprint proves local matching-rule presentations for FLC
substitution and hierarchical tiling families, using decorated tiles. This
reinforces the same distinction: a finite local rule presentation of a target
hull is not a one-support shape-only erasure theorem.

### Marked one-support and unmarked two-support boundaries

The repository's separate Stade audit records an undecidable marked
one-connected-polygon family and an unmarked two-polygon geometric
construction, conditional on the preprint's all-tilings weave converse. K74A
does not improve either support count; it only exposes why local finite-state
logic is easy once roles and contact topology are granted.

## Exact contribution retained

The repository may use K74A/K74R as:

- a compact normal form for finite rooted contact languages;
- a test fixture for contact-atlas verifiers;
- a reduction showing that another local automaton, zipper, delimiter, or
  parity gadget does not advance the monotile problem;
- the positive side of the local expressivity hierarchy
  `bicliques < hidden-state T-junction relations`.

It may not present the compiler as a new simulation paradigm.

## Permitted claims

- Under a prescribed rooted host/order/three-participant topology, distinct
  endpoint state angles realize every finite automaton at fixed word length.
- Prefix tries realize every finite fixed-arity relation in that model.
- The old AHI parity zipper is the finite-group instance `G=Z/2`, `n=3`.
- Local finite-relation expressivity is closed in the coloured contact model.
- The audited sources do not furnish the missing one-connected-unmarked,
  unrestricted-gapless, total-decoder theorem.

## Forbidden claims

- “Finite-state T-junction compilation is new.”
- “Every finite relation can be compiled into one unmarked polygon.”
- “The AHI system has been converted to a monotile.”
- “A local legal compiler patch implies every tiling decodes.”
- “No unmarked compiler exists because none appeared in this audit.”
- Any restart of zipper/comb/reset geometry justified only by K74A.

## Dated searches

Searches on 2026-07-29 included:

- `finite automaton T-junction tiling matching rules one polygon unmarked`;
- `geometric tilings finite automaton local rules single prototile 2026`;
- `one polygon simulate Wang tiles gapless unmarked tiling`;
- `matching rules hierarchical tilings finite decorations 2026`.

They recovered the audited edge-patch, Wang/jigsaw, atlas, geometric-tiling,
single-puzzle-piece, and hierarchical-matching-rule lines. No directly
supporting primary theorem was located for unrestricted gapless tilings by one
connected unmarked Euclidean polygon with a total decoder.

## Sources

- Smith, Myers, Kaplan, Goodman-Strauss, *A chiral aperiodic monotile*,
  arXiv:2305.17743, Section 2.2 and Lemma 2.3.
- Fletcher, *An atlas matching rule for substitution tilings*,
  arXiv:1003.4909.
- Hellouin de Menibus, Lutfalla, Vanier, *Decision problems on geometric
  tilings*, arXiv:2409.11739 / TCS 2026.
- Ollinger, *Tiling the plane with a fixed number of polyominoes*,
  arXiv:0904.1364 / LATA 2009.
- Demaine et al., *One tile to rule them all*, arXiv:1212.4756.
- Vereshchagin, *Matching Rules for Substitution and Hierarchical Tilings for
  any Substitution with Finite Local Complexity*, arXiv:2606.25005.
- Repository reviews `TJUNCTION_CONTACT_COMPLEX.md`,
  `K5C_SINGLE_TILE_SIMULATION.md`, and `MARKED_STURMIAN_UNDECIDABILITY.md`.
