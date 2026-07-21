# Proof and certificate ledger

This is the claim-status authority for the theory track. Evidence does not
become a theorem by accumulation; each row closes only through its stated
proof or certificate route.

> **Identity correction (ERR-003/D-0048):** every “finalist” row and artifact
> below concerns the already-known ten-kite Turtle. Finite statements and
> certificates remain valid; their logical use is control validation or
> independent Turtle certification, never novelty. O1/O3 are externally known.

## Foundations

| ID | Statement | Scope | Status | Dependencies | Proof/certificate |
|---|---|---|---|---|---|
| F0.1 | Grid-aligned tilings by a fixed finite polykite form a \(\mathbb Z^2\) SFT | grid-aligned, fixed finite tile | proof-draft | finite tile diameter; finite point group | `01_periodic_completion.md` |
| T0.1 | Any tiling with a nonzero period implies existence of a fully periodic tiling containing that period | grid-aligned, arbitrary nonzero lattice vector | proof-draft | F0.1; periodic-point lemma for 1D SFTs | `01_periodic_completion.md` |
| C0.1 | Weak and strong translational aperiodicity coincide in this scope | grid-aligned, fixed finite tile | proof-draft | T0.1 | `01_periodic_completion.md` |
| E0.1 | Arbitrarily large disk tileability implies existence of a plane tiling | grid-aligned, finite local complexity | proposed/citation | compactness/diagonal argument | roadmap §1.3; full proof or canonical citation pending |
| X0.1 | A periodic tiling by a finite polykite set under arbitrary Euclidean placements implies an aligned periodic tiling | geometric polykites | external peer-reviewed theorem | alignment property; Appendix-A component reduction | Smith et al., *An aperiodic monotile*, Lemmas A.1/A.3/A.5; literature baseline LIT-PK-06 |

## Turtle-control obligations (legacy “finalist” track)

| ID | Obligation | Current status | What closes it | Evidence that does *not* close it |
|---|---|---|---|---|
| O1 | No fully periodic Turtle tiling | externally proved; internal certificate partial | optional independent W2 theorem or W3 recognizability | finite HNF sweeps, regardless of size |
| O3 | Existence of a Turtle tiling | externally proved; internal certificate partial | optional independent W3 substitution/growth certificate | any finite collection of disk patches |
| O5 | Every geometric Turtle tiling is grid-aligned | optional stronger property; internal scope open and unnecessary for EIN-U | W4 contact-rigidity theorem | X0.1 proves only existence of an aligned counterpart with the same periodicity property |
| EIN-G | Grid-aligned Turtle einstein property | externally known; not internally re-proved | internal O1 + O3, using T0.1 | diffraction or nested-core evidence |
| EIN-U | Unconditional geometric Turtle einstein property | externally known | cited Hat/Turtle theorems; alternatively internal EIN-G + X0.1 | finite grid-aligned sweeps alone |

Retired identifiers O2 and O4 remain aliases of O1 under T0.1 so that older
notebooks stay readable.

External status anchor: Smith--Myers--Kaplan--Goodman-Strauss,
*An aperiodic monotile* (arXiv:2303.10798), proves the Hat/Turtle family;
Smith, *Turtles, Hats and Spectres* (arXiv:2403.01911), gives explicit Turtle
tilability and Ammann-bar nonperiodicity arguments. `tests/test_turtle.py`
proves that the repository's legacy finalist key is their exact ten-kite
Turtle under the production canonicalization.

## Workstream theorems

| ID | Target | Status | Validation gate | Intended artifact |
|---|---|---|---|---|
| T1.1 | Decide whether one explicit nonzero vector is a period of some tiling | proof-draft; positive and negative certificate paths implemented | known periodic controls; hat negative controls | `02_transfer_certificates.md`; cycle + A1 torus certificate, or complete graph manifest checked by `transfer_verify.py` |
| T1.2-25 | Turtle has no nonzero period vector with \(Q(v)\le25\) in the internal grid model | machine-verified | T1.1; exact D6 orbit enumeration including nonprimitive vectors | `docs/notebook/assets/theory-w1-finalist-norm25.json` (11 certificates, 90 vectors) |
| T1.2-36 | Turtle has no nonzero period vector with \(Q(v)\le36\) in the internal grid model | machine-verified | T1.2-25 plus four independently verified shell certificates | `docs/notebook/assets/theory-w1-finalist-norm26-36.json` (4 certificates, 36 vectors) |
| T1.2 | Exclude every nonzero period vector of norm at most general \(N\) | proposed family; established at N=36 for Turtle | T1.1 controls; enumeration includes nonprimitive vectors | vector-orbit manifest and per-vector certificates |
| T1.3 | Classify tileable transverse widths for a fixed cylinder | proposed | compare with exact torus solver on small widths | SCC/cycle-length semilinear certificate |
| T1.4 | Resolve the Turtle control's 8/7 collar ambiguity | proposed/optional | recover known Spectre/Hat/Turtle recognizability behavior | ambiguity transfer graph and collar verdict |
| T2.A | Area/sector congruence obstructions | machine-verified/elementary; zero false exclusions on 60,477 periodic certificates | verified periodic corpus | `03_w2_invariants.md`; `theory-w2-layer-a.json`; `invariants.py` |
| T2.B0 | An isolated nontrivial Fourier-character linear block cannot obstruct a torus cover | proof-draft/no-go | direct homogeneous-system proof | `03_w2_invariants.md` |
| T2.B | Character invariants exclude quotient families as originally formulated | refuted | T2.B0 | retain characters only as a decomposition tool for Layer C |
| T2.C0 | A modular left-cokernel witness excludes an integer quotient cover | classical generalized coloring/tile homology; GF(2) implementation machine-verified | Conway--Lagarias Section 5; zero false exclusions on 60,477 periodic certificates | `04_w2_cokernel.md`; `W2_ABELIAN_INVARIANTS.md`; `invariants.py` |
| T2.C1 | Turtle cannot tile HNF \((1,0,k)\) for any \(k\ge4\) | worked control; proof-draft formula machine-checked for 4≤k≤100 | T2.C0; two exact thin placement profiles; strict corollary of published Turtle aperiodicity | `04_w2_cokernel.md`; legacy `finalist_thin_gf2_support` |
| T2.C2 | Integer quotient feasibility is equivalent to equality of the placement lattice and its extension by the all-ones target | classical integer-module criterion; dual exact normal-form implementation | tile-homology/signed-tiling class; HNF/Smith equivalence; FLINT/SymPy cross-checks | `04_w2_cokernel.md`; `invariants.py` |
| T2.C | Full integer incidence-lattice classification for Turtle through index 60 | machine-verified finite negative result | T2.C2; 60,477 explicit periodic covers; dual-backend controls | 36/742 rank kills, exactly the GF(2) set; 706 integer-compatible; zero torsion-index kills |
| T2.C3 | Nonnegative rational quotient feasibility reduces exactly to a six-sector profile cone | elementary symmetry/cone reduction; exact producer/verifier implemented | translation averaging; conic Carathéodory | `04_w2_cokernel.md`; `nonnegative_cokernel_relaxation` |
| T2.C4 | A no-period-vector certificate excludes every quotient lattice containing that vector | proof-draft; compositional verifier implemented | T1.2-36; exact HNF membership | `05_w2_binary_holonomy.md`; `binary_families.py` |
| T2.C4-36 | Every Turtle quotient lattice of index at most 36 is excluded by a certified period vector | machine-verified | T2.C4; exhaustive HNF shells; all 126 vectors in T1.2-36 | `theory-w2-binary-families.json` |
| T2.C5 | The three thin HNFs `(1,0,k)`, `(k,0,1)`, `(k,k-1,1)` are impossible for every k≥4 | worked Turtle control; symmetry maps machine-verified | T2.C1; exact D6 lattice action; strict corollary of published Turtle aperiodicity | `05_w2_binary_holonomy.md`; `finalist_thin_family_orbit` |
| T2.D0 | Conway--Lagarias p3 winding control is reproduced from boundary words | external theorem; machine-reproduced | primary paper Theorems 1.2/2.1; exact affine Cayley model | `holonomy.py`; `theory-w2-layer-d-phase0.json` |
| T2.D1 | A periodic tiling's connected boundary skeleton carries commuting finite-group holonomies | proof-draft | tile relators vanish; boundary-skeleton connectivity | `05_w2_binary_holonomy.md` |
| T2.D2 | UNSAT of every commuting finite-group twisted boundary-potential CSP excludes an exact torus cover | proof-draft; implementation and periodic controls pass | T2.D1; verified tile-boundary quotient; binary placement coupling | `05_w2_binary_holonomy.md`; `holonomy_csp.py` |
| T2.D2-40 | Turtle has no exact cover on any HNF torus of index at most 40 | machine-verified | area; T2.C4-36; T2.D2; 54 independently checked DRAT cores | `theory-w2-layer-d-proof-index40.json`; `verify_theory_w2_layer_d_proofs.py` |
| T2.D2-45 | Turtle has no exact cover on any HNF torus of index at most 45 | machine-verified | T2.D2-40; area; 69 period-family kills and 9 holonomy kills at index 45; 162 independently checked DRAT cores | `theory-w2-layer-d-proof-index45.json`; generic proof verifier |
| T2.D2-50 | Turtle has no exact cover on any HNF torus of index at most 50 | machine-verified | T2.D2-45; area; index-50 split 75 W1 + 6 S3 + 12 A4; 576 independently checked A4 DRAT cores | `theory-w2-layer-d-a4-proof-index50.json`; `verify_theory_w2_layer_d_a4_proofs.py` |
| T2.D2-55 | Turtle has no exact cover on any HNF torus of index at most 55 | machine-verified | T2.D2-50; area; index-55 split 51 W1 + 21 A4; T2.D4; 336 independently checked V4-twist DRAT cores | `theory-w2-layer-d-a4-proof-index55.json`; `verify_theory_w2_layer_d_a4_proofs_index55.py` |
| T2.D2-60 | Turtle has no exact cover on any HNF torus of index at most 60 | machine-verified | T2.D2-55; area at 56--59; index-60 split 123 W1 + 42 map-7 twist unions + 3 T2.D6 packing kills; 45 cold-replayed DRAT cores | `theory-w2-layer-d-a4-proof-index60-{map7,packing}.json`; corresponding cold verifiers |
| T2.D3 | Layer-D satisfiability is invariant under the diagonal D6 action on period HNFs and contravariant boundary maps | proof-draft; exact action and index-45 covariance machine-checked | exact kite-grid action; T2.D2 model transport; inner-conjugacy reduction | `holonomy_symmetry.py`; `theory-w2-layer-d-symmetry.json` (4,212 checks) |
| T2.D4 | For A4 maps projecting to the geometric character ±(2x+y), exact-cover torus twists lie in V4, reducing 48 commuting pairs to 16 | proof-draft; exact semidirect tables and edge equations machine-checked | T2.D1 boundary connectivity; center-period character vanishes | `a4_semidirect.py`; `theory-w2-layer-d-a4-factor.json` |
| T2.D5 | Every finite product of the 16 distinct-tail V4 local invariants has an overlap-two countermodel on every HNF sublattice of `2 Lambda` | proof-draft; explicit base witnesses and 3,024 finite pullbacks cold-checked | T2.D4; locality under torus coverings | `a4_v4_{sft,lift,product}.py`; `theory-w2-layer-d-v4-{2lambda,product}.json` |
| T2.D6 | The three index-60 V4-SFT escapes fail after forbidding one exact D6 orbit of six-kite collisions | machine-verified finite theorem; 3/3 DRAT cores cold-replayed | T2.D4; unique surviving twist per signature map; collision clauses are a subset of exact nonoverlap | `a4_v4_packing.py`; `theory-w2-layer-d-a4-proof-index60-packing.json`; packing SVG |
| T2.D7 | One distinct-tail V4 signature plus the six-kite collision orbit forces placement density at most 1/2 on every area-admissible `L <= 2 Lambda` | frozen conjecture/control branch | finite controls only; no development authorized after D-0067 | `a4_v4_density.py`; notebook session 36 |
| T2.D7-H0 | Inclusion-minimal four-center Hall cores are connected, have deficiency 1 or 2, obey the private-center bound and exact curvature identity | proof-draft; executable profile checker and deterministic unit controls | elementary Hall minimality and incidence double count | `a4_v4_hall.py`; notebooks 37–38 |
| T2.D7-H | Every finite planar compatible nonoverlapping packing admits a two-to-one tile-to-center matching | **refuted** by a cold-verified 63-tile/125-center literal planar countermodel | exact matching/minimality; zero cell overlaps; XOR and independent CNF V4 compatibility; seam guard | `theory-w2-layer-d-v4-periodic-hall-catalog-full-packing.json`; notebook 38 |
| T2.D | Torus holonomy obstruction from tiling groups | closed as Turtle control branch; complete certified prefix through index 60 | D-0067 forbids further quotient/group/shell escalation; published Turtle aperiodicity is controlling | complementary S3/A4 exhaustion, twist-union DRAT proofs, saturation countermodels, and one-orbit packing lemma |
| T3.1 | C1–C5 certificate implies existence and universal nonperiodicity | frozen framework proposition; no current novelty authorization | a generic soundness theorem and at least two structurally independent systems are required by D-0070 | certificate schema and verifier remain reusable controls |
| T3.0 | Spectre W3 finite kernel is closed/deterministic and primitive of exponent 3; its exact geometry is a unimodular 16-coordinate recurrence matching all 32 vendor levels | machine-verified partial certificate | A6 v2 artifact; rank-four module; exact polygon signs | `06_w3_substitution_certificates.md`; `theory-w3-spectre-certificate-v0.json` |
| T3.0P | In the fixed-chirality edge-to-edge straight-Spectre model, the complete existential central-corona prefix has 166 radius-one types, 30 radius-two survivors and 21 radius-three survivors; 18 are substitution-observed and all three extras have radius-four witnesses | machine-verified finite proposition; not a whole-plane theorem | exact module geometry; SAT ring completion; generated controls | `spectre_patch_language.py`; `theory-w3-spectre-physical-language.json`; cold verifier |
| T3.0G | Conditional on the recovered 9/8 parent templates, coordinated buffered overlap eliminates corona types 33, 44 and 155 by radius four and leaves exactly the 18 generated controls | machine-verified finite conditional proposition; parent existence/uniqueness unproved | T3.0P; exact parent occurrences; coupled ring/grouping SAT | `spectre_parent_overlap.py`; `theory-w3-spectre-parent-overlap.json`; cold verifier |
| T3.0C | Every whole-plane tiling in the fixed-chirality edge-to-edge L18 domain has a unique full/missing 9/8 parent partition | machine-verified conditional theorem; contraction closure supplied by T3.0M | 418 exhaustive radius-three transducer cases; unique anchor map; zero common-core failures among 15,216 radius-six survivors | `spectre_component_language.py`; `theory-w3-spectre-component-language.json`; session 48 |
| T3.0I | Uncolored radius-one parent-corona overlap cannot eliminate the nine non-generated contracted states | machine-verified finite no-go | all 26 states have reciprocal-edge and triangle-consistent support; fixed-point pruning removes none | `spectre_parent_interface.py`; `theory-w3-spectre-parent-interface.json`; session 49 |
| T3.0J | Center type plus exact physical interface contacts cannot eliminate the non-generated contracted states | machine-verified finite no-go | complete radius-seven census gives 17 generated + 5 extra colored states; all 22 survive and form one closed SCC | `spectre_colored_interface.py`; `theory-w3-spectre-colored-overlap.json`; session 50 |
| T3.0K | Full/missing endpoint types plus exact contacts leave exactly three radius-nine defect states | machine-verified finite no-go/structure theorem | all 4,482 interfaces resolve; 17+3 states survive; exact one-star defect costs `[1,0,1]` | `theory-w3-spectre-two-sided-overlap.json`; `theory-w3-spectre-defect-propagation.json`; session 51 |
| T3.0L | Every extra two-sided state forces a typed extra state onto parent ring two | machine-verified finite propagation theorem | 131 pinned root stars; 128 UNSAT; 3 complete model sets of sizes 960/432/840; all 131 zero-outer variants independently SAT-refuted; forced map `A→C,B→C,C→A` | `spectre_parent_csp.py`; `theory-w3-spectre-radius2-defect.json`; session 52 |
| T3.0M | The unique L18 parent partition contracts only to the 17 generated colored states | machine-verified conditional closure theorem | 2,232 radius-three CSPs independently replayed; extra-root survivors `0,2,1`; every survivor of the latter roots contains the dead first state | `theory-w3-spectre-radius3-defect.json`; session 53 |
| T3.0N | Every complete tile corona in a whole-plane fixed-chirality edge-to-edge straight-Spectre tiling belongs to L18 | machine-verified finite exclusion theorem in the declared contact model | ancestry-free exact physical frontier `3→89→368→282→0`; independent one-hot SAT replay; decisive radius 5 | `spectre_d1_entry.py`; `theory-w3-spectre-d1-entry.json`; session 54 |
| T3.0O | Every unrestricted fixed-chirality straight-Spectre polygonal tiling reduces bijectively to the 14-segment primitive edge-contact model | machine-verified finite-atlas theorem plus elementary locally-finite interface argument | exact hypotheses: 13 maximal sides `12×1+1×2`, angles ≥90°, no side with two right-angle endpoints; 10/10 equal-length interface words share one unit subdivision; common 30-degree frame and rank-four anchor lock | `spectre_edge_patch_bridge.py`; `theory-w3-spectre-edge-patch-bridge.json`; session 55 |
| T3.0Q | The D4 colored-component/A6-collar correspondence and phase normalization form an exact finite equivalence kernel | machine-verified partial reconstruction; novelty branch closed | 17↔17 bijection on 310 controls; 17/17 boundary-owner round trips; two determinant-one maps and exact inverses; three generated level-pair round trips; bare SFT obstruction `3565→80` radius-two seeds | preserve artifact; D-0070 forbids another context expansion absent a generic theorem |
| T4.1 | Every tiling by a target polykite shares one kite-grid frame | optional stronger property; no longer a polykite periodicity gate | exact contact enumeration; fault-line search; compare Hat Lemma A.6 | contact atlas and propagation proof |

## Preserved Turtle-control evidence (legacy “finalist” identifiers)

| ID | Exact finite claim | Status | Artifact | Logical use |
|---|---|---|---|---|
| D-E1-NEST | A literal two-step nested core reaches an 18,386-tile disk | machine-verified | `docs/notebook/assets/e1-finalist-nested.json` | prioritization; not O3 |
| D-E1-A4 | The nested outer patch has rank-4/sixfold A4 signature | machine-verified numerical classification | same artifact | prioritization only |
| D-E1-HIER | 22,094-rule nearest-cluster screen leaves two ambiguous 8/7 variants and no forced recursive rule | machine-verified finite screen | `docs/notebook/assets/e1-finalist-hierarchy-screen.json` | negative result for that search class; not a no-substitution theorem |
| D-E1-A1-215 | No admissible torus quotient through index 215 tiles | machine-verified | `docs/notebook/assets/e1-finalist-periodicity.json` plus tests | finite prefix of O1 only |
| D-E1-OVERNIGHT | 9,135 quotient executions emitted exact UNSAT before interruption (9,099 generic HNFs plus 36 targeted jobs; deliberate reruns may overlap earlier evidence) | recovered, checksummed log evidence | `docs/notebook/assets/e1-overnight-recovered.json`; raw `logs/overnight-2026-07-17/` | finite O1 evidence only; independently replay before paper citation |
| D-W1-P0 | W1 phase-0 controls: 28 n≤3 vector cases, 102 bounded torus comparisons, 25 A1-verified cycles, four cycle-free hat vectors, zero disagreements/exhaustions | machine-verified finite validation | `docs/notebook/assets/theory-w1-phase0-controls.json`; `tests/test_theory_transfer.py` | validates reference behavior only; not a universal T1.1 or hat result |
| D-W1-NEG | Five complete cycle-free control manifests pass the separate verifier (two-kite non-tiler; four hat vectors) | machine-verified | `docs/notebook/assets/theory-w1-cycle-free-controls.json` | validates finite negative certificate completeness |
| D-W1-N25 | All 11 finalist vector-orbit representatives through \(Q=25\) are independently verified cycle-free | machine-verified | `docs/notebook/assets/theory-w1-finalist-norm25.json` | proves T1.2-25; not universal O1 |
| D-W1-N36 | Four further representatives cover \(25<Q\le36\), all independently verified cycle-free | machine-verified | `docs/notebook/assets/theory-w1-finalist-norm26-36.json` | combines with D-W1-N25 to prove T1.2-36 |
| D-W2-A | Layer A validates on 60,477 periodic certificates; finalist sector coloring adds zero kills beyond area | machine-verified finite validation/negative result | `docs/notebook/assets/theory-w2-layer-a.json` | directs effort to integral SNF rather than more equivalent colorings |
| D-W2-C2 | GF(2) cokernel validates on 60,477 periodic certificates and kills 36/742 finalist HNFs through index 60 | machine-verified finite validation | `docs/notebook/assets/theory-w2-layer-c-gf2.json` | exact modular UNSAT subset; survivors remain unknown |
| D-W2-C3 | Exact integral normal forms classify all 742 finalist HNFs through index 60 | machine-verified finite negative result | `docs/notebook/assets/theory-w2-layer-c-snf.json` | adds zero kills beyond GF(2); 706 integer-compatible relaxations are not tilings |
| D-W2-C4 | Exact nonnegative rational relaxation classifies all 742 finalist HNFs through index 60 | machine-verified finite negative result | `docs/notebook/assets/theory-w2-layer-c-nonnegative.json` | same 36 obstructions; all 706 survivors have verified fractional covers, not tilings |
| D-W2-C5 | W1 period vectors compose into 126 infinite quotient families; 2,941/8,864 admissible HNFs through 215 are covered | machine-verified compositional result | `docs/notebook/assets/theory-w2-binary-families.json` | exact binary exclusions; 5,923 survivors remain unknown to this class |
| D-W2-D0 | Primary p3 control passes; finalist has 2,556 S3 surjections but zero displacement-coset commutator obstructions | machine-verified phase-0/negative result | `docs/notebook/assets/theory-w2-layer-d-phase0.json` | requires coupling group potentials to selected binary boundary network |
| D-W2-D1 | Binary-coupled S3 CSP closes the three W1-surviving index-40 HNFs; all 54 selected map/twist UNSAT cores independently verify | machine-verified finite theorem | `docs/notebook/assets/theory-w2-layer-d-{coupled,s3-classes,proof-index40}.json`; compressed CNF/DRAT cores | with area and T2.C4-36, proves T2.D2-40; does not close O1 |
| D-W2-D2 | All 39 strong S3 classes are classified on the nine index-45 frontier HNFs; nine maps in three signature triples kill every HNF; 162 selected twist cores independently verify | machine-verified finite theorem | `theory-w2-layer-d-s3-index45.json`; `theory-w2-layer-d-proof-index45.json` | with D-W2-D1 and area, proves T2.D2-45; T2.D3 explains the finite symmetry pattern but does not make it an infinite-family theorem |
| D-W2-D3 | Exact diagonal D6 action partitions the index-45 9x39 matrix into 43 pair orbits with zero covariance failures | machine-verified structural result | `theory-w2-layer-d-symmetry.json`; `tests/test_theory_holonomy_symmetry.py` | sound symmetry reduction for later finite shells; does not itself exclude a new HNF |
| D-W2-D4 | At index 50, strong S3 Layer D excludes one six-HNF orbit while two six-HNF orbits survive all 39 maps | machine-verified mixed finite result | `theory-w2-layer-d-s3-index50.json`; 108 replayed DRAT cores in `theory-w2-layer-d-proof-index50.json`; 77 clause-verified SAT witnesses in `theory-w2-layer-d-sat-index50.json` | six new exact finite exclusions; proves S3 alone cannot close index 50; the then-prefix 45 is superseded by D-W2-D6 |
| D-W2-D5 | Adding coverage multiplicity at most two leaves the index-50 S3 polarity matrix unchanged | machine-verified negative result | `theory-w2-layer-d-overlap2-index50.json`; 77 independently clause-verified models in `theory-w2-layer-d-overlap2-sat-index50.json` | retires excess multiplicity and boundary connectivity as easy explanations of S3 saturation |
| D-W2-D6 | A4's strong V4-kernel classes exclude all 12 index-50 S3 survivors; the complete 75+6+12 shell decomposition is certified | machine-verified finite theorem | `theory-w2-layer-d-a4-index50.json`; 32 clause-verified SAT witnesses; 576 cold-replayed cores in `theory-w2-layer-d-a4-proof-index50.json`; exact V4 signature artifact | proves T2.D2-50; identifies a symbolic map signature but does not close O1 or an infinite HNF family |
| D-W2-D7 | The distinct-V4-tail A4 signature obstructs all 21 W1-surviving index-55 HNFs | machine-verified finite theorem | all 28 D6 pair orbits UNSAT for all 48 twists; map 7 has 336/336 cold-replayed V4-twist cores; exact semidirect reduction | proves T2.D2-55 with the 51+21 shell split; persistence is not yet an infinite-family theorem or O1 |
| D-W2-D8 | The V4 local SFT reaches its first structured escape at index 60 and has an infinite `2 Lambda` blind family | machine-verified negative/structural result | map 7 kills 42/45 frontier HNFs; a three-HNF D6 orbit survives all 16 maps; 16 base + 3,024 pullback assignments and the full 16-map overlap-two product replay clausewise | prevents false promotion to index 60; proves the current relaxation needs packing, not more products of the same quotient signature |
| D-W2-D9 | One of 40 local D6 collision orbits makes the full 16-layer product UNSAT on all three index-60 escapes | machine-verified finite packing result | exact orbit reconstruction gives 720/22,680 nonoverlap clauses per torus; three independently checked and cold-replayed DRAT cores | proves T2.D6 and isolates a small packing mechanism; the 42 non-escape HNFs still need independent proof packaging before T2.D2-60 promotion |
| D-W2-D10 | All 42 map-7-obstructed index-60 HNFs have complete 16-twist selector-union certificates | machine-verified finite theorem | 42 Glucose proofs represent 672 direct cases; raw/core checks during production and 42/42 cold replay; 123+42+3 shell accounting | combines with D-W2-D9, W1 and area to prove T2.D2-60; still finite and not O1 |
| D-W2-D11 | The T2.D6 packing mechanism survives every area-admissible `L <= 2 Lambda` HNF through index 120, and each of the 16 signature maps suffices alone | reproducible finite UNSAT search; census/provenance verified, no DRAT promotion | 193 HNFs for the product; 3,088 single-map cases; zero countermodels | motivates T2.D7; does not prove the infinite family, O1, or even the UNSAT cases independently |

## Next status transitions

1. T0.1: proof-draft → theorem-ready after literature/citation audit and an
   independent proof review.
2. T1.1: proof-draft → theorem-ready after adversarial proof review and
   literature audit. D-W1-P0 and D-W1-NEG now cover positive/A1 and complete
   negative certificate paths.
3. D-E1-OVERNIGHT: recovered checksummed evidence → machine-verified only after
   every recorded quotient is replayed or independently verified. The recovery
   manifest closes provenance and counting, not mathematical re-verification.
4. T3.1 and the 80-context D4 frontier are frozen by D-0070. Reopening requires
   a generic certificate-soundness proposition, explicit control of spurious
   abstract states, and validation on structurally independent systems; merely
   completing the known Spectre reconstruction is not a status transition.
