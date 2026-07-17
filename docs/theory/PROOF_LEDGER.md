# Proof and certificate ledger

This is the claim-status authority for the theory track. Evidence does not
become a theorem by accumulation; each row closes only through its stated
proof or certificate route.

## Foundations

| ID | Statement | Scope | Status | Dependencies | Proof/certificate |
|---|---|---|---|---|---|
| F0.1 | Grid-aligned tilings by a fixed finite polykite form a \(\mathbb Z^2\) SFT | grid-aligned, fixed finite tile | proof-draft | finite tile diameter; finite point group | `01_periodic_completion.md` |
| T0.1 | Any tiling with a nonzero period implies existence of a fully periodic tiling containing that period | grid-aligned, arbitrary nonzero lattice vector | proof-draft | F0.1; periodic-point lemma for 1D SFTs | `01_periodic_completion.md` |
| C0.1 | Weak and strong translational aperiodicity coincide in this scope | grid-aligned, fixed finite tile | proof-draft | T0.1 | `01_periodic_completion.md` |
| E0.1 | Arbitrarily large disk tileability implies existence of a plane tiling | grid-aligned, finite local complexity | proposed/citation | compactness/diagonal argument | roadmap §1.3; full proof or canonical citation pending |

## Finalist obligations

| ID | Obligation | Current status | What closes it | Evidence that does *not* close it |
|---|---|---|---|---|
| O1 | No fully periodic tiling | open | universal W2 obstruction, exhaustive quotient theorem, or W3 recognizability | finite HNF sweeps, regardless of size |
| O3 | Existence of a tiling | open | W3 substitution/growth certificate or a uniform all-radii theorem + E0.1 | any finite collection of disk patches |
| O5 | Every geometric tiling is grid-aligned | open | W4 contact-rigidity theorem | grid-aligned SAT and torus results |
| EIN-G | Grid-aligned einstein property | open | O1 + O3, using T0.1 | diffraction or nested-core evidence |
| EIN-U | Unconditional geometric einstein property | open | EIN-G + O5 | any grid-aligned theorem alone |

Retired identifiers O2 and O4 remain aliases of O1 under T0.1 so that older
notebooks stay readable.

## Workstream theorems

| ID | Target | Status | Validation gate | Intended artifact |
|---|---|---|---|---|
| T1.1 | Decide whether one explicit nonzero vector is a period of some tiling | proof-draft; positive and negative certificate paths implemented | known periodic controls; hat negative controls | `02_transfer_certificates.md`; cycle + A1 torus certificate, or complete graph manifest checked by `transfer_verify.py` |
| T1.2-25 | Finalist has no nonzero period vector with \(Q(v)\le25\) | machine-verified | T1.1; exact D6 orbit enumeration including nonprimitive vectors | `docs/notebook/assets/theory-w1-finalist-norm25.json` (11 certificates, 90 vectors) |
| T1.2-36 | Finalist has no nonzero period vector with \(Q(v)\le36\) | machine-verified | T1.2-25 plus four independently verified shell certificates | `docs/notebook/assets/theory-w1-finalist-norm26-36.json` (4 certificates, 36 vectors) |
| T1.2 | Exclude every nonzero period vector of norm at most general \(N\) | proposed family; established at N=25 for finalist | T1.1 controls; enumeration includes nonprimitive vectors | vector-orbit manifest and per-vector certificates |
| T1.3 | Classify tileable transverse widths for a fixed cylinder | proposed | compare with exact torus solver on small widths | SCC/cycle-length semilinear certificate |
| T1.4 | Resolve the finalist's 8/7 collar ambiguity | proposed | recover known Spectre/hat recognizability behavior | ambiguity transfer graph and collar verdict |
| T2.A | Area/sector congruence obstructions | machine-verified/elementary; zero false exclusions on 60,477 periodic certificates | verified periodic corpus | `03_w2_invariants.md`; `theory-w2-layer-a.json`; `invariants.py` |
| T2.B0 | An isolated nontrivial Fourier-character linear block cannot obstruct a torus cover | proof-draft/no-go | direct homogeneous-system proof | `03_w2_invariants.md` |
| T2.B | Character invariants exclude quotient families as originally formulated | refuted | T2.B0 | retain characters only as a decomposition tool for Layer C |
| T2.C0 | A modular left-cokernel witness excludes an integer quotient cover | proof-draft; GF(2) implementation machine-verified | zero false exclusions on 60,477 periodic certificates | `04_w2_cokernel.md`; `invariants.py` |
| T2.C1 | Finalist cannot tile HNF \((1,0,k)\) for any \(k\ge4\) | proof-draft; formula machine-checked for 4≤k≤100 | T2.C0; two exact thin placement profiles | `04_w2_cokernel.md`; `finalist_thin_gf2_support` |
| T2.C2 | Integer quotient feasibility is equivalent to equality of the placement lattice and its extension by the all-ones target | proof-draft; dual exact normal-form implementation | HNF/Smith equivalence; FLINT/SymPy cross-checks; periodic positive controls | `04_w2_cokernel.md`; `invariants.py` |
| T2.C | Full integer incidence-lattice classification through finalist index 60 | machine-verified finite negative result | T2.C2; 60,477 explicit periodic covers; dual-backend controls | 36/742 rank kills, exactly the GF(2) set; 706 integer-compatible; zero torsion-index kills |
| T2.C3 | Nonnegative rational quotient feasibility reduces exactly to a six-sector profile cone | proof-draft; exact producer/verifier implemented | translation averaging; conic Carathéodory | `04_w2_cokernel.md`; `nonnegative_cokernel_relaxation` |
| T2.C4 | A no-period-vector certificate excludes every quotient lattice containing that vector | proof-draft; compositional verifier implemented | T1.2-36; exact HNF membership | `05_w2_binary_holonomy.md`; `binary_families.py` |
| T2.C4-36 | Every finalist quotient lattice of index at most 36 is excluded by a certified period vector | machine-verified | T2.C4; exhaustive HNF shells; all 126 vectors in T1.2-36 | `theory-w2-binary-families.json` |
| T2.C5 | The three thin HNFs `(1,0,k)`, `(k,0,1)`, `(k,k-1,1)` are impossible for every k≥4 | proof-draft; symmetry maps machine-verified | T2.C1; exact D6 lattice action | `05_w2_binary_holonomy.md`; `finalist_thin_family_orbit` |
| T2.D0 | Conway--Lagarias p3 winding control is reproduced from boundary words | external theorem; machine-reproduced | primary paper Theorems 1.2/2.1; exact affine Cayley model | `holonomy.py`; `theory-w2-layer-d-phase0.json` |
| T2.D1 | A periodic tiling's connected boundary skeleton carries commuting finite-group holonomies | proof-draft | tile relators vanish; boundary-skeleton connectivity | `05_w2_binary_holonomy.md` |
| T2.D2 | UNSAT of every commuting finite-group twisted boundary-potential CSP excludes an exact torus cover | proof-draft; implementation and periodic controls pass | T2.D1; verified tile-boundary quotient; binary placement coupling | `05_w2_binary_holonomy.md`; `holonomy_csp.py` |
| T2.D2-40 | Finalist has no exact cover on any HNF torus of index at most 40 | machine-verified | area; T2.C4-36; T2.D2; 54 independently checked DRAT cores | `theory-w2-layer-d-proof-index40.json`; `verify_theory_w2_layer_d_proofs.py` |
| T2.D | Torus holonomy obstruction from tiling groups | in progress; first genuine finite shell closed | extend finite-group/HNF families beyond index 40 | S3 class exhaustion gives six killing maps for each of the three W1-surviving index-40 HNFs |
| T3.1 | C1–C5 certificate implies existence and universal nonperiodicity | proof-draft in roadmap | Spectre, then blind hat | certificate schema, verifier, complete proof |
| T4.1 | Positive-length contacts force a common kite-grid frame | proposed | exact contact enumeration; fault-line search | contact atlas and propagation proof |

## Preserved finalist evidence

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

## Next status transitions

1. T0.1: proof-draft → theorem-ready after literature/citation audit and an
   independent proof review.
2. T1.1: proof-draft → theorem-ready after adversarial proof review and
   literature audit. D-W1-P0 and D-W1-NEG now cover positive/A1 and complete
   negative certificate paths.
3. D-E1-OVERNIGHT: recovered checksummed evidence → machine-verified only after
   every recorded quotient is replayed or independently verified. The recovery
   manifest closes provenance and counting, not mathematical re-verification.
4. T3.1 stays proof-draft until C1–C5 are formalized and the exhaustive
   legality-language requirement is implemented, not sampled.
