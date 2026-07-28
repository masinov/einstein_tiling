# State of the art: planar aperiodic monotiles

**Snapshot:** 2026-07-28
**Scope:** connected, unmarked tiles in the Euclidean plane, with emphasis on
polykites, Hat--Turtle--Spectre systems, and methods usable by this repository.

This is a research map, not a claim that every cited paper has received a
line-by-line audit. Review depth is controlled by `SOURCES.json` and the
reading queue.

## 1. What is classified

The Hat paper classifies the one-parameter `Tile(a,b)` deformation family:
positive unequal parameters give strongly aperiodic monotiles with
combinatorially equivalent tilings; the equal and zero-parameter similarity
classes admit periodic tilings. The Hat and Turtle are distinguished
polykite representatives, and the family contains infinitely many further
polykites. The same paper reports an exhaustive finite search through 24
constituent kites, finding no aperiodic examples outside Hat and Turtle in
that range. These results do **not** classify all polykites
(`smkgs-hat-2024`; detailed claims in `POLYKITE_BASELINE.md`).

`Tile(1,1)` is periodic when both handednesses may mix, but aperiodic under
orientation-preserving motions. Boundary modifications that forbid opposite
handedness interactions produce strictly chiral Spectres. Thus weak
chirality, strict chirality, and ordinary aperiodicity must remain distinct
fields in every candidate record (`smkgs-chiral-2024`).

As of this dated search, no primary paper in the catalog proves a second,
combinatorially independent family of connected unmarked Euclidean-plane
aperiodic monotiles. That is a search snapshot, not a theorem of absence.
The reported search of roughly 500 billion polykites is evidence that naive
size extension is a poor strategy, not a classification theorem
(`kaplan-path-review-2025`).

## 2. Known proof mechanisms

### Forced hierarchy and recognisability

The original Hat and chiral-Spectre proofs force local clusters and then a
unique hierarchical decomposition. Chéritat gives a detailed local cluster
route for Spectre tilings and explicitly reaches unique hierarchy for
whole-plane tilings (`smkgs-hat-2024`, `smkgs-chiral-2024`,
`cheritat-spectre-clusters-2024`). The crucial logical separation is:

1. a substitution or recursion constructs at least one tiling;
2. local legality is inherited at every level;
3. every admitted whole-plane tiling desubstitutes;
4. supertile inradii diverge, excluding translational periods.

Our W3 certificate schema follows this separation. A generated large patch is
not a substitute for steps 2--4.

The adversarial method audit now closes W3 as a novelty branch. Smith et al.'s
original Spectre proof already uses generated local patch lists, iterative
overlap-based extendability pruning, and reduced 5-patches to force unique
parent assignment; Chéritat supplies the full all-whole-plane correspondence.
Goodman--Strauss/Vereshchagin and Tatham cover the general matching-rule and
finite-state encoding ideas. W3 remains an exact machine-readable partial
reconstruction, not a new aperiodicity theorem or demonstrated generic method.
See `reviews/W3_CERTIFICATE_METHOD.md`.

The first ancestry-blind straight-Spectre control now enumerates 166 complete
edge-to-edge central coronas. Exact ring completion leaves 30 through radius
two and 21 through radius three, while the substitution controls contain 18.
All three extras reach radius four, and none of the 21 survivors has a unique
isolated central parent. This rules out a naïve local-owner shortcut and
redirects recognisability toward coordinated overlap constraints.

That coordinated experiment now conditionally closes the finite discrepancy:
all 18 generated types admit buffered parent partitions, while the three
extras have no radius-four frontier under the recovered 9/8 parent language.
This does not yet reproduce Chéritat's all-tilings theorem because parent
existence is assumed by the filter rather than derived from arbitrary physical
tilings.

Walton supplies a general recognisability framework for compact Hausdorff
expansive `L`-sub pattern spaces (`walton-recognisability-2026`, preprint).
The focused audit establishes an important boundary: the theorem gives unique
composition modulo translation, while in return-discrete tiling spaces strict
injectivity is equivalent to already excluding periodic hull elements. It is
therefore a post-aperiodicity theorem/control, not a non-circular proof of
aperiodicity. Chéritat's all-whole-plane local grouping is the direct control
for that route. See `reviews/WALTON_RECOGNISABILITY.md` and
`reviews/CHERITAT_SPECTRE_CLUSTERS.md`.

Machine-readable certificates now also have an adjacent primary control.
Batle--Bednorz publish exact JSON data and a Python verifier for exhaustive
unique retiling of a 2,490-hat region (`batle-bednorz-qecc-2026`). That finite
local-recoverability result is not universal Spectre recognisability, but it
precludes broad novelty claims based only on the use of certificate files and
independent checking.

### Arithmetic and Sturmian structure

Akiyama--Araki derive Turtle tilings using Golden Hex substitutions, Golden
Sturmian patches and Ammann-bar-like structures. This gives a second route to
the known Turtle beyond the original metatile proof and makes Sturmian
arithmetic an actionable discovery feature (`akiyama-araki-turtle-2025`).
James Smith's rhombille-grid model is a related alternative representation
linking Turtle, Hat, and Spectre structures (`james-smith-rhombic-2024`,
preprint).

The full technical paper `Sturmian Lattices and Aperiodic Tile Sets`, not only
its July 2026 announcement, gives an algorithmic construction of aperiodic
tile sets from quadratic-irrational Sturmian data
(`akiyama-hamada-ito-sturmian-2026`; announcement
`akiyama-hamada-ito-announcement-2026`). These are tile sets rather than a new
monotile family, so any monotile consequence would require an additional
encoding theorem.

A full-text audit now sharpens that boundary. The construction treats color
and Ammann-bar adjacency as part of the tile, can produce disconnected
supports, and explicitly asks whether another monotile and disk-like tiles can
be obtained. Its optimized `sqrt(2)-1` example uses three topological-disk
prototiles and has positive entropy. Standard geometric matching rules,
one-prototile atlas rules, and poly-`K` groupification do not supply the missing
shape-only congruence theorem: they respectively preserve tile types, retain
external local rules, or preserve cardinality/change the acting group
(`goodman-strauss-matching-1998`, `fletcher-atlas-2010`,
`vereshchagin-matching-2026`, `coulbois-et-al-groups-2026`). The precise open
target is a finite-radius factor from every tiling by one unmarked disk into
the irrational Sturmian system; see
`reviews/STURMIAN_MONOTILE_ENCODING.md`.

### Geometric deformation and incommensurability

The Hat paper uses geometric deformation and irrational length relations as
an alternative to the forced-metatile route (`smkgs-hat-2024`). This method is
family-level: it explains why a continuum of noncongruent polygons can realize
the same combinatorial tiling system. It also warns against treating a new
outline as a new dynamical system.

### Symbolic dynamics and finite-state descriptions

Labbé--Selinger construct Hat tilings from a Markov partition for a toral
action, identify the associated shift of finite type, and state analogous
constructions for Turtle and Spectre/CASPr as open questions
(`labbe-selinger-markov-2026`, preprint). Tatham develops finite-state
transducers for substitution tilings, hierarchical addresses, and exact
remote-tile access, including unambiguous Hat systems
(`tatham-transducers-2026`, preprint).

These approaches suggest machine-checkable outputs stronger than an image:
a finite alphabet, transition/neighbor automata, address semantics, and a
proof that the coding covers the complete tiling hull.

### Geometry translated to groups

Poly-`K` tiles translate polyform tilings into finite-subset tilings of the
symmetry group of a periodic grid. The Hat yields an aperiodic monotile in a
virtually `Z^2` Coxeter group (`coulbois-et-al-groups-2026`). This makes group
subsets a principled candidate space, but geometric realization and novelty
relative to known tiling systems remain separate checks.

### Coloring, homology, and quotient obstructions

Conway--Lagarias identify additive cell colorings with homomorphisms into
abelian groups and package the strongest such information as tile homology
(`conway-lagarias-tiling-groups-1990`). Their boundary-word groups can be
strictly stronger than signed-tiling/coloring obstructions. Lidjan--Baralic
apply tile homology directly to finite grids on flat surfaces, including
explicit parity obstructions on tori
(`lidjan-baralic-flat-surface-homology-2021`).

The repository's GF(2) incidence null vectors and integer cokernels belong to
this classical abelian class. Its uniform Turtle thin-family support was not
found in the audited Turtle papers, but it proves only a small corollary of
known Turtle aperiodicity. W2 is therefore retained as a worked certificate
control and closed as a novelty branch; see
`reviews/W2_ABELIAN_INVARIANTS.md`.

## 3. Computational filtering

Kaplan's Heesch SAT method measures finite surround depth; his public
implementation later generalized the method to polykites, and its public
eight-kite artifact exactly matches our A1+A2 aggregate (`108` at `H_c=1`,
five at `H_c=2`, plus two periodic anisohedral cases and the Hat left
inconclusive). The exact coordinate crosswalk now also verifies a 116/116
per-shape bijection. His isohedral SAT method gives an exact test for extendable
isohedral surrounds in its stated polyform setting (`kaplan-heesch-2022`,
`kaplan-heesch-sat-code`, `kaplan-8kites-2023`,
`kaplan-isohedral-sat-2024`). These are valuable early rejection filters and
external controls. Neither failure to find an isohedral tiling nor arbitrarily
deep finite patch growth proves aperiodicity.

The isohedral criterion is now implemented as a compact control. Its complete
counts over all 1,264 free polykites through `n=8` match Myers exactly:
`1,1,4,4,0,70,52,37`. It produces cold-verifiable positive surrounds and
correctly leaves periodic anisohedral shapes for A1. An initial edge-only halo
gave two false positives at `n=7`; the external census exposed the error and
the required full vertex halo corrected it. See
`reviews/KAPLAN_ISOHEDRAL_SAT.md`.

Our A0--A4 funnel aligns with this literature only partially:

- A0 and canonical identity support exhaustive enumeration;
- A1 searches periodic quotient tori, broader than an isohedral-only filter
  within its aligned scope;
- A2 and A3 provide finite surround and disk-growth evidence;
- A4 prioritizes long-range-order signatures;
- A6/W3 attempts to extract a hierarchy.

The missing end-to-end feature is a source-aware identity/family gate followed
by a machine-readable proof and novelty dossier. `NOVELTY_PROTOCOL.md` makes
that the required output rather than an optional report.

## 4. Characterizing whether a system is genuinely different

The Hat deformation space contains noncongruent tiles whose hulls are
topologically conjugate. The CAP representative supports cohomology,
cut-and-project, and pure-point dynamical descriptions
(`baake-gaehler-sadun-hat-2025`). Spectre/CASPr has an analogous long-range
order analysis with cohomology and Rauzy-fractal windows
(`baake-et-al-spectre-order-2025`). Explicit diffraction and Fourier--Bohr
calculations add measurable long-range invariants
(`baake-et-al-diffraction-2025`).

Consequently, polygonal noncongruence is the weakest possible novelty notion.
A serious comparison should move through:

1. exact shape and parameter-family identity;
2. local-isomorphism and patch-language comparison;
3. mutual local derivability;
4. topological conjugacy or shape deformation;
5. substitution incidence and recognisability data;
6. cohomology, dynamical eigenvalues, Fourier module, and model-set data.

Failure of an early equivalence may establish geometric novelty, but
“independent aperiodic system” requires evidence at the later levels.

## 5. What our Turtle rediscovery achieved

The repository independently isolated the published ten-kite Turtle from the
complete smallest-survivor search, after periodicity, local-growth, disk-patch,
and diffraction filters. That is not shape discovery. It is a useful positive
control showing that the funnel can promote a known hard case from a large
blind corpus.

What is already demonstrated:

- exact blind recovery of the Turtle canonical geometry;
- strong separation from the other smallest local-growth survivors;
- finite periodic-quotient refutations, large exact patches, and rank-four
  diffraction consistent with the known system;
- exact certificate machinery developed against a known aperiodic control.

What is not yet demonstrated:

- automated recognition that Hat and Turtle share a tiling language;
- recovery of the Golden Hex/Sturmian description without literature input;
- a complete internally recovered recognisability/aperiodicity proof;
- a calibrated false-positive rate for hierarchy inference.

A first literature-driven control now closes part of this gap. The exact
standard-word and central-palindrome recurrences from Akiyama--Araki pass
through level 24. Their Ammann-bar length count implies minority handedness
`(3-sqrt(5))/6 = 0.127322...`; the independent 9,239-tile Turtle disk contains
`1181/9239 = 0.127828...` minority placements. This validates a structure the
patch generator was not given, but the forced-bar and Golden Hex geometry are
not yet internally reconstructed. See
`reviews/AKIYAMA_ARAKI_TURTLE.md`.

The correct methodological experiment is therefore a blinded, ablated Turtle
control, specified in `NOVELTY_PROTOCOL.md`, rather than another novelty
claim.

## 6. Open directions supported by this survey

The marked/unmarked computability boundary is now explicit.  Stade proves
that tileability by one connected polygon with finite edge-to-edge matching
rules is undecidable, with an all-tilings weave decoder; adding one staple
polygon converts those rules to bare geometry.  Taking the simulated Wang
system to be the product of the fixed AHI source with an arbitrary Wang shift
preserves a total local Sturmian factor, so the marked one-polygon Sturmian
realization problem is undecidable.  This does not transfer to one unmarked
polygon: removing the staple is exactly the unresolved color-erasure step.
See `reviews/MARKED_STURMIAN_UNDECIDABILITY.md` and theory note 67.

The HC-15 contact-complex audit adds a narrow geometric boundary.  The
Spectre paper's edge-patch lemma already treats finite multi-tile contacts and
their locally consistent transport, while
`hellouin-lutfalla-vanier-geometric-2026` shows that arbitrary finite symbolic
rules can be layered over any nonempty FLC geometric tiling space.  Those are
not one-support shape-erasure theorems: the former assumes a complete
correspondence and the latter uses labels/forbidden patterns (or several
machine-dependent shapes in its purely geometric construction).  The
`sugimoto-convex-edge-2015` scope boundary further shows that convex
edge-to-edge monohedral geometry cannot yield an unmarked aperiodic prototile.
Intentional non-edge-to-edge subdivision is therefore legitimate territory,
but T-junction atlases and FLC recodings themselves carry no novelty claim.
HC-15 subsequently proved the abstract subdivision-order capacity and
refuted the natural convex complementary-port realization; no nonconvex
polygon was constructed. See `reviews/TJUNCTION_CONTACT_COMPLEX.md` and
theory note 21.

- Attack self-stapling color erasure as a theorem, not another isolated
  carrier: replace the finite edge relation in the marked one-polygon
  compiler without Stade's second support, while retaining its all-tilings
  decoder.  A no-go must name the self-stapling family it closes.
- Preserve the W3 Spectre certificates as controls. Reopen them only for a
  generic, on-paper certificate theorem satisfying D-0070, not to eliminate
  another finite context frontier.
- Add exact `Tile(a,b)` family recognition, then broaden identity to local
  languages and symbolic factors.
- Extend the completed Kaplan isohedral control to new substrates only when a
  justified search family requires it.
- Mine Sturmian/Ammann-bar factors from patches as candidate-ranking features.
- Explore poly-`K` subsets on other grid symmetry groups rather than extending
  the same polykite census mechanically.
- Build canonical transducer/Markov representations that can compare tiling
  systems and generate remote tiles exactly.

Every direction must declare whether it seeks a new shape, a new proof, a new
algorithm, or a new dynamical system. Those are different research outcomes.
