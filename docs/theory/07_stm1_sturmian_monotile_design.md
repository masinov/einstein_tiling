# ST-M1 — arithmetic carrier design for a Sturmian monotile

**Date:** 2026-07-21

**Status:** theorem design; construction blocked before geometry

**Primary source:** `akiyama-hamada-ito-sturmian-2026`, especially Theorem 4,
Sections 10.1--11

**Motion convention:** full Euclidean isometry group, including reflections

This note tests whether the audited Sturmian tile-set theorem can plausibly be
turned into one connected, unmarked topological-disk tile. It is deliberately
upstream of shape drawing, SAT, enumeration, or patch generation. Its job is
to expose the exact lemmas that would make such work meaningful and to stop
the branch if they cannot first be supported on paper.

## 1. The target is two theorems, not one

Fix \(\alpha=\sqrt 2-1\). Let \(X^{(3)}_\alpha\) denote the complete decorated
three-prototile tiling space constructed in Section 10.1 of the source. The
source proves that this system enforces irrational Sturmian lattices and has
positive topological entropy.

### ST-M1 (minimal target)

Construct a compact polygonal topological disk \(P_\alpha\) that tiles the
plane by full Euclidean isometries and a finite-radius,
translation-equivariant map

\[
  \pi:X(P_\alpha)\longrightarrow Y_\alpha,
\]

defined on **every** tiling by \(P_\alpha\), where every element of the target
tiling space \(Y_\alpha\) carries an irrational Sturmian lattice and hence has
no nonzero translational period. Here \(Y_\alpha\) includes the Euclidean
images, in particular the reflected branch, of the chosen oriented source.

Neither injectivity nor surjectivity is required. If \(T+v=T\), equivariance
gives \(\pi(T)+v=\pi(T+v)=\pi(T)\), contradicting aperiodicity of
\(Y_\alpha\). Existence of one \(P_\alpha\)-tiling and totality of \(\pi\)
therefore prove that \(P_\alpha\) is an aperiodic monotile.

The intended minimal source \(Y_\alpha\) is a finite colored equal-support
system suggested by the source's formal \(\kappa=\infty\) remark. This object
is **not yet available as a cited theorem**. Section 10.2 says only that the
supports then cease to differ and the patch tiles *may* be reduced to one up
to color. Deriving a complete finite colored system and proving that all its
tilings enforce irrational Sturmian lattices is therefore obligation S0
below, not an assumption.

### ST-M1+ (positive-entropy strengthening)

Construct \(P_\alpha\) together with a surjective finite-radius map

\[
  \pi_+:X(P_\alpha)\twoheadrightarrow X^{(3)}_\alpha.
\]

Then entropy monotonicity gives
\(h(X(P_\alpha))\geq h(X^{(3)}_\alpha)>0\). This would be qualitatively
stronger than merely producing another aperiodic monotile. This statement uses
the standard compact tiling topology; the finite-radius map is continuous,
and the intended finite frame/contact atlas supplies the required finite local
complexity modulo the global Euclidean pose.

The \(\kappa=\infty\) equal-support remark and the Section 10.1
positive-entropy construction are different source statements. No factor,
conjugacy, or entropy-preserving relation between them has been proved here.
Consequently the present design selects **minimal ST-M1 first**. ST-M1+ is
deferred unless either the three-prototile system is encoded directly or a
surjective bridge from the equal-support system is proved.

## 2. Why the obvious reductions fail

### Fixed macro fusion

One congruent macro-tile made from a fixed finite multiset of the source
prototiles has rational component ratios. The source tilings have irrational
Sturmian frequencies. Fixed fusion can therefore neither represent the full
source language nor supply the desired map. Source states must be encoded by
context, pose, or a variable locally forced decomposition.

### Forgetting colors

The \(\kappa=\infty\) remark says “one up to color,” not “one unmarked tile.”
Forgetting the colors and Sturmian Ammann bars enlarges the hull. Nothing in
the source excludes periodic or mixed-handed tilings in that larger hull.

### Three uncoupled rails

The source is assembled from three rotated line systems. It is tempting to
force each direction by a separate finite-state zipper and superimpose the
three results. The following elementary obstruction rules this out.

**ST-M1.N1 (independent-rail no-go).** Suppose the legal configurations of a
candidate carrier are exactly a nonempty product
\(Z_1\times Z_2\times Z_3\), where each \(Z_i\) is a one-dimensional sofic
shift indexed by an integral linear coordinate on a common rank-two lattice,
and suppose any three factor configurations superimpose compatibly to produce
a plane tiling. Then the carrier admits a periodic tiling.

**Proof.** A nonempty one-dimensional sofic shift is presented by a finite
labeled directed graph containing a bi-infinite walk. Some strongly connected
component on that walk contains a directed cycle; repeating the cycle gives a
periodic point of the shift. Choose a periodic point in each \(Z_i\). By the
product and compatibility hypotheses their superposition is legal. The
simultaneous kernel of the three integral coordinates modulo their finite
periods is a finite-index subgroup of the common rank-two lattice, so the
superposition is periodic. \(\square\)

Thus finite rail states are not themselves the problem; **independence** is.
A viable encoder must couple the directional sequences at their intersections
so that rational periodic choices cannot be made independently.

## 3. Chosen mechanism: a coupled contact-star carrier

The only mechanism retained for further theorem work is a single congruent
carrier whose source state is decoded from a finite contact star, rather than
from a tile in isolation.

The proposed logical layers are:

1. **Frame ports.** A finite family of asymmetric boundary ports forces all
   contacts onto one three-direction frame and excludes continuous sliding,
   arbitrary rotations, and unrecorded T-junctions.
2. **Directional zipper data.** Within that frame, relative offsets along a
   contact encode the finite color and Ammann-bar data of the proposed
   equal-support source.
3. **Corner couplers.** Ports meeting at carrier corners impose joint
   relations among all three directions. These relations must realize the
   source's actual cell-intersection rule and violate the product hypothesis
   of ST-M1.N1.
4. **Contextual state.** A radius-\(R\) contact star, not the absolute pose of
   one tile, determines one source cell state. Neighboring stars must agree on
   overlaps.
5. **Chirality guard.** Contacts between opposite determinant classes are
   impossible. A connected whole-plane tiling is consequently homochiral.
   The reflected global branch is allowed and decodes to the reflected source
   system.

This is a mechanism specification, not a geometric construction. Boundary
teeth do not become a proof merely by being drawable. A successful carrier
must supply a finite exact contact atlas and prove that the atlas is complete
for arbitrary polygonal tilings, including non-edge-to-edge contacts.

## 4. The three-state requirement

The Section 10.1 control has three patch-tile types up to isometry; Figure 38
also uses a reflected copy of one type. A single carrier must therefore encode
at least three locally recoverable states while tolerating the source's
reflection semantics.

A pose-only encoding would be possible only if the required colored boundary
patterns form an orbit of the carrier's finite pose action. That orbit
condition has not been extracted from the source and must be checked before
pose is used as a state variable. In general it is too restrictive: congruent
poses permute one fixed cyclic list of ports, whereas arbitrary source types
need not have boundary words in one dihedral orbit.

The contact-star design avoids assuming the orbit condition. Three states may
be represented by three distinct legal relative-offset patterns around the
same carrier. To count as an encoding, however, the following finite kernel
must be proved without geometric search:

- a finite set \(K\) of oriented contact symbols;
- three nonempty, disjoint sets \(C_1,C_2,C_3\) of legal rooted contact stars;
- a deterministic decoder assigning both a source state and its anchored
  source-cell placement to every star;
- overlap equations making adjacent decoded stars realize exactly the source
  contact and Ammann-bar rules;
- exact-cover equations proving the decoded source cells cover the plane
  without gaps or interior overlaps;
- intersection equations coupling the three line directions.

Nonemptiness says the carrier really expresses all three states; disjointness
and overlap consistency make the decoder a function. For minimal ST-M1 it is
enough that the image is an aperiodic subsystem. For ST-M1+ every source
configuration must lift, not merely the three isolated star types.

No such kernel is presently derived from the paper's figures and definitions.
That is the first substantive blocker.

## 5. Full-isometry and mixed-handedness obligation

Ordinary monotile tilings here allow every element of \(E(2)\). Restricting
placements to rotations and translations would prove only a weakly chiral
claim and would repeat the logical gap exposed by `Tile(1,1)`.

Let the sign of a placed carrier be the determinant of its isometry relative
to a reference copy. The desired chirality lemma is:

**ST-M1.C2 (chirality propagation).** Every contact in every tiling by
\(P_\alpha\) joins equal signs, and the tile-contact graph of every such
tiling is connected. Hence the sign is constant on the plane.

The equal-sign condition must follow from geometric incompatibility of every
opposite-sign contact, not from a declared matching rule. Connectivity cannot
simply be assumed: the proof must exclude positive-distance separation,
line-contact fault components, and contacts missed by the chosen primitive
atlas. If C2 holds, both global handednesses remain legal; reflection carries
one complete tiling branch to the other. The decoder is defined on one branch
and conjugated by reflection on the other.

If C2 cannot be proved, the theorem must be downgraded explicitly to the
orientation-preserving motion group. A mixed-handedness tiling may not be
ignored or assigned a source image ad hoc.

## 6. Conditional carrier theorem

The following packages exactly what remains between the mechanism and ST-M1.
It is useful because it makes future geometric work prove named hypotheses
instead of accumulating patches.

**ST-M1.C0 (conditional local-map theorem).** Let \(P\) be a compact polygonal
topological disk. Assume:

- **S0 — source:** a finite colored equal-support system \(Y_\alpha\) is
  completely specified and every tiling in it enforces an irrational
  Sturmian lattice;
- **C1 — contact completeness:** every tiling by \(P\) has a locally finite,
  connected contact graph and every interface belongs to a stated finite
  exact contact atlas;
- **C2 — chirality:** the atlas forbids opposite-sign adjacency, so each
  tiling is homochiral;
- **C3 — total local decoding:** for some fixed \(R\), every rooted radius-
  \(R\) contact star has exactly one state and one anchored source-cell
  placement;
- **C4 — overlap legality:** decoded neighboring stars agree on shared data
  and the decoded source cells form an exact plane tiling satisfying all
  source contact, bar-continuation, and three-direction intersection rules;
- **C5 — existence:** at least one source tiling lifts to a tiling by \(P\).

Assume also that \(Y_\alpha\) contains the Euclidean images of its oriented
source tilings. Then \(P\) is an aperiodic monotile under the full Euclidean
isometry group.

**Proof.** C5 gives tileability. By C1--C4, decoding every rooted star defines
a total finite-radius map from each homochiral component of \(X(P)\) into
\(Y_\alpha\). On the reflected component use the reflected decoder. Overlap
legality makes both definitions tiling maps, and translation equivariance is
immediate from their local definition. S0 makes every image aperiodic, so
period descent excludes a nonzero period of every \(P\)-tiling. \(\square\)

For ST-M1+, replace C5 by:

- **C6 — complete lifting:** every tiling in \(X^{(3)}_\alpha\) has a
  \(P\)-tiling preimage, and the decoder agrees with that preimage.

C6 is a surjectivity theorem. A generated example, arbitrary large patches,
or nonemptiness of each isolated state does not prove it.

## 7. Kill conditions before any geometry

The branch remains **blocked before construction**. It may proceed to a shape
only if all of the following paper obligations close or are replaced by a
comparably explicit route:

1. **S0:** derive the complete \(\kappa=\infty\) colored alphabet, contacts,
   Ammann-bar rules, and all-tilings aperiodicity statement. The source's
   strategy remark alone is insufficient.
2. **K1:** write the finite three-state contact-star kernel and prove its
   decoder total and unambiguous at the symbolic level.
3. **K2:** exhibit the joint intersection relation that couples the three
   directions and explain why ST-M1.N1 does not apply.
4. **K3:** state a realizable geometric chirality separator or accept, in
   advance, an orientation-preserving theorem only.
5. **K4:** state how frame locking and contact-atlas completeness will handle
   T-junctions, subdivided maximal segments, and sliding interfaces.
6. **K5:** prove a lift for at least one source tiling. For the entropy target,
   prove the stronger complete-lifting statement C6.

Failure of S0, K1, K2, or K3 closes the selected carrier mechanism without a
search. K4 and K5 are allowed to guide a later exact construction only after
the symbolic kernel exists. No radius escalation can repair a missing item in
this list.

## 8. Present disposition

This session does **not** establish ST-M1. It establishes:

- a clean separation between the minimal aperiodicity and positive-entropy
  targets;
- the elementary independent-rail no-go ST-M1.N1;
- a reflection-safe conditional local-map theorem ST-M1.C0;
- a finite list of falsifiable pre-geometric obligations.

The chosen coupled contact-star carrier is plausible only at the level of an
architecture. The paper does not yet supply S0, and the source contact data
have not yet been reduced to the finite kernel K1. Accordingly, drawing a
polygon or running a contact search now would be premature. The next action,
if separately authorized after checkpoint review, is a bounded source-lemma
derivation of S0 and K1 from the exact definitions in Sections 6--10—not a
computation.

## 9. Session-64 source-lemma result

The follow-up in `08_stm1_equal_support_compiler.md` proves an elementary
compiler S0C: any finite set of connected macrotiles over one congruent cell
can be replaced, with finite colors and local rules, by colored copies of that
cell, mutually locally derivable from the subdivided macro system.

This does not yet instantiate the Sturmian source. The `kappa=infinity`
passage is a strategy remark in the Turtle subsection, not an explicit
common-cell subdivision of the Section 10.1 three-prototile system. The exact
specialization E-infinity must still prove nondegenerate congruent cells,
connected transported templates, boundary/SAB-language preservation and
preservation of the irrational symbolic sequences. S0 therefore remains
blocked, and K1 was not begun. The eventual carrier must encode the full
addressed cell alphabet, not merely the three visible macro shapes.

## 10. Session-65 attempted E-infinity closure — withdrawn

Session 65 claimed a common-triangle system with `18,18,2` addresses. ERR-006
withdraws it: primary Table 1 gives the optimized large templates composition
`12S+6M+6L`, while `2S+L` belongs to the earlier 27-tile construction. The
one-support `kappa=infinity` remark is Turtle-specific and does not transport
the optimized local language. E-infinity and S0 are blocked again.

## 11. Session-66 symbolic quotient boundary

`09_stm1_symbolic_quotient.md` shows that a quotient must be tested on its
entire finite local closure, not only on images of intended source tilings.
The natural three-role reduction fails: after macro ownership and addresses
are erased, the remaining `{S,M,L}` cabinet system is exactly the source's
example admitting every slope, including rational periodic configurations.
Independent finite-state corridor rails fail separately by ST-M1.N1.

Conditional on a valid S0, Q0 still requires safety on the full local closure,
and the two no-go results still eliminate obvious reductions. There is,
however, no presently established addressed S0 alphabet to minimize. K1 is
blocked upstream of a collar table.

## 12. Session-67 primary-source correction

The planned radius-one table was halted before enumeration. A valid reopening
must first construct equal supports for the actual optimized templates and
prove the complete language transport required by S0. It may not substitute a
new guessed address count, a larger collar radius, or sampled intended
tilings for that theorem. The two-tile lower bound in the source applies to
its colored-tile category; a contextual unmarked carrier would lie outside
that category, but no such carrier is implied by the source remark.
