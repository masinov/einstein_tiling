# Theory research program — periodicity obstructions, transfer automata, and substitution certificates for polykite families

> **Status:** living document, v0.2 (2026-07-17). Unlike
> `einstein_search_program.md` (frozen; corrections via `ERRATA.md`), this
> plan is edited in place; substantive redirections are logged in
> `docs/DECISIONS.md`. Companion to, not replacement of, the computational
> search program — the two share the substrate, the verification standards
> (exact arithmetic, D-0005 external anchors) and the artifact conventions.
>
> **Provenance:** distilled from a joint design discussion (Mario ↔ codex ↔
> Claude, 2026-07-17) triggered by the state of the n=10 finalist: budgeted
> SAT on quotients is now the bottleneck, and the crown-continuability
> correction (session 19, ERR-002, D-0026) showed that "larger circles" do
> not produce theorems.
>
> **Changelog.** v0.1 — initial draft (Claude). v0.2 (2026-07-17) —
> incorporates codex review R1, all six corrections accepted:
> periodic-point lemma (Lemma 1.1, §1.3) merging obligations O2/O4 into
> O1; T1.2 enumeration widened to all nonzero vectors (§3.2); W3
> global-consistency obligation C5 and certified-inball fix in the proof
> skeleton (§5.1–5.2); compactness admitted as a second existence route
> (§1.3, §2); "return scales" terminology (§1.5, §7); W4
> contact-connectivity lemma made an explicit obligation (§6.2).
> Session-22 correction — isolated nontrivial character blocks in W2.B cannot
> be infeasible because their transformed target is zero (T2.B0); Layer B is
> retained only as a decomposition tool and the obstruction path proceeds to
> the full integer SNF module.
>
> **Identity correction (2026-07-20, ERR-003/D-0048).** The n=10
> “finalist” that motivated this plan is exactly the published Turtle. All
> legacy `finalist` identifiers below mean the Turtle control. O1 and O3 are
> externally settled for this tile; internal W1--W3 work is independent
> certificate-method development, not a route to a new-einstein claim. The
> general family-level program remains intact.
>
> **Literature-scope correction (2026-07-20, ERR-004/D-0049).** The Hat
> paper already proves the periodic-alignment reduction for finite polykite
> sets (Appendix A, Lemmas A.1/A.3/A.5), and reports the complete `n≤24`
> aperiodic-polykite search horizon. W4 is therefore optional stronger
> rigidity/extension work, not a prerequisite for lifting a periodicity
> obstruction from the kite grid. See `docs/literature/POLYKITE_BASELINE.md`.

---

## 0. Goal and thesis

**Goal.** Produce publishable mathematics — theorems with machine-checkable
finite certificates — that (a) decides periodicity/aperiodicity questions for
restricted polykite tile families where the general problem is undecidable,
(b) converts the repository's budget-limited computational evidence into
proof components, and (c) stands as a community contribution independent of
whether any particular discovery candidate survives.

**Thesis.** For a *fixed tile* on a *fixed substrate*, the three obligations
of the einstein property split into problems with different logical
character, and each admits a distinct finite-certificate attack:

| Obligation | Logical form | Attack | Workstream |
|---|---|---|---|
| No tiling has any nontrivial period (⇔ no fully periodic tiling; Lemma 1.1) | ∀ over a countable family of vectors/quotients | piecewise: per-vector transfer automata + algebraic invariants; wholesale: substitution + recognizability certificate | W1, W2, W3 |
| Existence of at least one tiling | ∃ (not provable by any finite patch) | substitution fixed point + Extension Theorem (constructive); any all-radii tileability theorem + compactness (abstract) | W3 |
| Unconditional exclusion of periodic polykite tilings | published alignment reduction | Appendix A + an internal grid-aligned obstruction | external theorem; W4 optional |

A structural gift of the substrate (Lemma 1.1, §1.3): grid-aligned tilings
form a ℤ² subshift of finite type, where "some tiling has one period"
already implies "some tiling is fully periodic." The apparently harder
uncountable ∀ ("every tiling is nonperiodic") therefore collapses onto the
countable one ("no fully periodic tiling"); v0.1's separation of these two
obligations was illusory. What W3 adds over W1/W2 is not taming
uncountability but covering all infinitely many quotients in one theorem —
plus the existence certificate.

The general plane tiling problem is undecidable (Berger 1966), and
single-tile variants remain undecidable or open in closely related settings
(Ollinger 2009 for small polyomino sets; Greenfeld–Tao 2023–24 for
translational monotiles in high dimension). Restricting to a family —
bounded polykites on the Laves [3.4.6.4] substrate — is therefore not a
concession but the only honest route to decision procedures. Every theorem
below states its scope explicitly; Appendix A of the Hat paper supplies the
published bridge from arbitrary periodic polykite tilings to aligned ones.

---

## 1. Formal framework

### 1.1 Substrate and symmetry group

- Kite substrate: Laves [3.4.6.4] tiling; each hexagon (side 2, matching
  hatviz `hexPt`) is divided into **6 kites**. Kite boundary edges have
  lengths 1 and √3; all boundary angles are multiples of 30°.
- Exact coordinates: integer pairs over basis e₁=(1,0), e₂=(1/2,√3/2);
  norm form |v|² = x² + xy + y². All theory-path computation is exact
  integer/rational arithmetic (hard rule; floats only in A4-style
  prioritization signals).
- Translation lattice Λ (hexagon centers); full symmetry group
  **G = Λ ⋊ D₆**, giving 12 orientations per free shape (6 rotations ×
  optional reflection).
- K denotes the infinite kite complex (cells, edges, vertices) with its
  G-action.

### 1.2 Tiles, tilings, tiling space

- A **tile** T is a finite edge-connected set of kite cells (a polykite),
  identified up to G (free shape). n = |T| is its kite count.
- A **grid-aligned tiling** ω is a partition of the cells of K into
  G-images of T. Ω_T denotes the set of all such tilings, topologized as
  usual (local agreement on large balls); Ω_T is compact and G acts on it.
- The **stabilizer lattice** of ω is Stab(ω) = { t ∈ Λ : ω + t = ω }
  (translations only; rotational symmetry is tracked separately and is
  irrelevant to aperiodicity).

### 1.3 Periodicity taxonomy and the target property

- ω is **fully periodic** if rank Stab(ω) = 2 (equivalently ω descends to a
  torus quotient K/L for a finite-index L ≤ Λ).
- ω is **singly periodic** if rank Stab(ω) = 1.
- ω is **nonperiodic** if Stab(ω) = 0.
- T is **weakly aperiodic** if Ω_T ≠ ∅ and no ω ∈ Ω_T is fully periodic.
- T is **strongly aperiodic (einstein property, grid-aligned)** if
  Ω_T ≠ ∅ and every ω ∈ Ω_T is nonperiodic — no tiling admits *any*
  nontrivial translation symmetry.

> **Lemma 1.1 (periodic-point lemma; weak ⇔ strong on this substrate).**
> If some ω ∈ Ω_T has a nontrivial period v, then some ω′ ∈ Ω_T is fully
> periodic with v ∈ Stab(ω′). Consequently weak and strong aperiodicity
> coincide for grid-aligned finite tiles: "no fully periodic tiling"
> already forces every tiling to have trivial stabilizer.
>
> *Proof sketch.* Grid-aligned tilings by T form a ℤ² subshift of finite
> type. A tiling with period v descends to a tiling of the cylinder
> K/⟨v⟩, i.e. a bi-infinite path in the finite transfer graph of §3.1;
> pigeonhole yields a cycle, and periodic traversal of the cycle is a
> torus tiling — fully periodic, with v in its stabilizer. (Classical for
> ℤ² SFTs; §3.1 is the effective, certificate-producing version.)
> Contributed by codex in review R1.

The publication target is stated as strong aperiodicity; by Lemma 1.1 it
suffices to prove that no tiling is fully periodic. The practical corollary
cuts deeper than v0.1 noted: **a singly periodic tiling already implies a
fully periodic one**, so W1's per-vector decisions (§3) close refutation
channels for weak and strong aperiodicity simultaneously, and every
periodicity refutation anywhere in the program reduces to the fully
periodic case.

Classical fact used throughout (state and cite in any paper; proof is
standard compactness given finite local complexity, which grid alignment
gives for free):

> **Extension Theorem.** If T tiles disks of arbitrarily large radius, then
> Ω_T ≠ ∅.

Consequences we must respect (already learned the hard way in session 19):

1. No finite patch — nested or not — proves existence. A3 output is
   prioritization evidence only. Two theorem-level routes to existence
   remain open: W3's constructive substitution fixed point, or an abstract
   proof that disks of *every* radius are tileable (even by independently
   chosen patches), which the Extension Theorem converts to existence.
   Finite SAT runs reach single radii only, never "every radius" — either
   route needs a theorem, but W3 is the preferred, not the only, one.
2. No finite torus sweep proves weak aperiodicity: the quotient family is
   infinite. A1's `no-periodic-at-budget` becomes a theorem only after W2's
   quantifier reduction closes the tail.

### 1.4 Scope: grid-aligned vs unconditional

All funnel searches are currently grid-aligned (D-0006): positive tiling
certificates are sound, while a raw negative search result is grid-scoped.
For *periodicity*, however, the needed bridge is already published:
Appendix A, Lemmas A.1, A.3 and A.5 of *An aperiodic monotile* show that if a
finite polykite set admits a periodic tiling under arbitrary Euclidean
placements, it admits one aligned to a common Laves grid (with the stated
monokite presentation handled in the lemma). Thus a complete internal proof
excluding aligned periodic tilings excludes arbitrary periodic tilings too.

The stronger assertion that **every** tiling by a particular polykite is
aligned is different and is not needed for this implication. Lemma A.6 proves
it for the Hat; W4 may investigate it for other tiles or extend the alignment
reduction beyond polykites. Papers must cite the external reduction and still
label each internal computation's native scope.

### 1.5 What is already in hand (inputs to this program)

From the computational program, verified and relevant here:

- **A1**: exact torus solver over all HNF sublattices to an index budget,
  with machine-verified certificates; validated against Myers n≤8.
- **A2**: exact corona/Heesch machinery — importantly, this is already an
  *exhaustive local-configuration enumerator*, the primitive W3's
  completeness argument needs (§5.3).
- **A3**: SAT disk covers with required-placement (nested-core) support.
- **A6 v2**: blind hierarchy mining with a closed 17-state substitution on
  Spectre, SAT-proved unique composability over the recovered collar
  language, and a partially closed hat hierarchy (16/15-pattern shared
  libraries forcing 430→71/72 and 43/41→8).
- **The Turtle control** (legacy “n=10 finalist,” shape key
  `010001010104010502f002f1030b030c04fa04fb`, candidate 2): exact
  primary-source identity pinned by `tests/test_turtle.py`; no internal torus
  certificate through index 215; verified nested
  core chain r²=9,000 → 30,000 inside patches to r²=100,000 (18,386 tiles);
  robust diffraction rank ≥ 4 (D-0025); one exact period-47 stripe domain
  in one patch; ambiguous first-composition (8/7-type) decompositions in
  the blind hierarchy screen; period-(0,47) cylinder SAT escalation
  returns `unknown` at every width 30–150 under a 10⁵-conflict budget
  (`e1-finalist-period47.json`) — the concrete motivation for W1. A later
  overnight campaign completed 9,135 quotient executions (9,099 generic HNF
  instances and 36 targeted jobs), all reporting exact UNSAT before a power
  outage; this recovered finite evidence is checksummed in
  `e1-overnight-recovered.json`, includes deliberate reruns, and does not close
  the infinite quotient family. These facts independently exercise the
  machinery against a known aperiodic tile; they do not establish novelty.
- Observed strong return scales **18, 29, 47, 76** (lattice-coordinate
  separations, not Euclidean lengths — see §7) — consecutive Lucas numbers
  L₆..L₉.

---

## 2. Internal certificate ledger for the Turtle control

Maintained so every workstream knows exactly which internal certificate box it
fills. The Turtle's einstein status is already externally proved; “open” below
means not yet independently recovered by this repository's certificate class.

| # | Obligation | Current status | Closes via |
|---|---|---|---|
| O1 | No fully periodic tiling — by Lemma 1.1 this **is** "every tiling nonperiodic" | **externally proved for Turtle**; internal certificate partial through the recorded W1/W2 bounds | optional independent recovery: W1/W2 piecewise or W3 wholesale |
| O2 | ~~No singly periodic tiling~~ — merged into O1 (Lemma 1.1: singly periodic ⇒ fully periodic) | — | number retained so earlier notes stay readable |
| O3 | Existence of a tiling | **externally proved for Turtle** by substitution; internal nested-core evidence only | optional independent W3 certificate recovery |
| O4 | ~~Every tiling nonperiodic~~ — merged into O1 (Lemma 1.1) | — | — |
| O5 | Stronger claim that every Turtle tiling is grid-aligned | optional/open internally; not needed for periodicity | optional W4 contact theorem |

The v0.1 ledger treated O1/O2/O4 as independent; Lemma 1.1 collapses them
into one obligation with two attack granularities. W1/W2 close O1
*piecewise* (per vector, per index family) — unconditional partial theorems
that survive even if W3 never closes, and cheap refutation channels (a
transfer-graph cycle at any single vector would falsify that certificate
route). W3 can recover O1 *wholesale* and O3 constructively. For future unknown
candidates, internal grid-aligned O1 ∧ O3 plus the published Appendix-A
periodic-alignment reduction yields the ordinary polykite einstein property;
for the Turtle these are validation targets, not open status.

---

## 3. Workstream W1 — boundary-state transfer automata

**One-line goal:** replace budgeted SAT on strips/cylinders with *exact
decisions*, one candidate period vector at a time, and mechanize
collar-recognizability questions as automaton reachability.

### 3.1 Objects

Fix a nonzero vector v ∈ Λ (candidate period — any nonzero vector, **not**
only primitive ones; see T1.2). The quotient cylinder C_v = K/⟨v⟩ is an
infinite-strip complex of finite circumference. Key
observations, each elementary but worth stating precisely in the writeup:

1. A tiling of the plane with period v ↔ a tiling of C_v.
2. Tilings of C_v ↔ bi-infinite paths in a **transfer graph** whose nodes
   are boundary states (see below) and whose edges are legal one-step
   extensions.
3. The transfer graph is finite ⇒ a bi-infinite path exists iff a **cycle**
   exists (pigeonhole).
4. A cycle traversed repeatedly is itself periodic in the transfer
   direction ⇒ it yields a *fully* periodic tiling containing v in its
   stabilizer.

Together: **v ∈ Stab(ω) for some ω ∈ Ω_T ⟺ the transfer graph of C_v has a
cycle.** One finite computation simultaneously eliminates the width
quantifier *and* the second-period quantifier. Absence of a cycle is an
exact theorem: "no tiling of the plane by T (grid-aligned) is invariant
under translation by v." Presence of a cycle refutes aperiodicity outright
— weak and strong alike, this equivalence being exactly Lemma 1.1 — and
emits a fully periodic certificate checkable by the existing A1 verifier.

**Boundary state.** Sweep C_v cell by cell in a fixed canonical order
(lexicographic along the strip). A state is the canonical form of: the
set of already-placed tile germs crossing the frontier, i.e. the
partial-occupancy pattern of the window of cells within tile-diameter
distance of the frontier, with cells labeled by (pose, cell-within-tile) of
their covering germ or `empty`. Two states are identified when their
windows are exactly equal after canonical translation along v. Transition:
cover the first empty frontier cell by every legal pose; advance. This is
exact-cover reformulated as a finite automaton — the same move Myers'
strip methods and classical Heesch computations use.

### 3.2 Theorem targets

- **T1.1 (per-vector exclusion).** For explicit v: no grid-aligned tiling
  by T has period v. First targets: v with |v|² at the observed stripe
  scale (the period-47 direction), then the Lucas ladder directions.
- **T1.2 (norm-bounded exclusion).** No grid-aligned tiling by T has any
  period v with |v|² ≤ N, for the largest feasible concrete N. Enumerate
  **all nonzero** v with |v|² ≤ N up to the D₆ action (which contains −1)
  — not only primitive vectors: stabilizers are arbitrary sublattices, and
  a tiling can have period 2v without having period v, so imprimitive
  vectors are independent cases. Prune by W2 invariants where a per-vector
  argument applies, run T1.1 per survivor. This is the headline piecewise
  theorem toward O1, and it is *cumulative*: N only grows.
- **T1.3 (eventually-periodic width classification).** For fixed
  circumference, the set of tileable torus widths is semilinear and
  effectively computable from the transfer graph (cycle structure). This
  retires per-width SAT sweeps like `run_e1_finalist_period47.py`
  wholesale and turns their `unknown`s into decided rows.
- **T1.4 (recognizability radius).** For the finalist's ambiguous
  first-composition decompositions: build the collar automaton whose states
  are (decomposition interpretation, boundary germ) pairs and whose
  transitions are legal radius-increments. Outcomes: (a) one interpretation
  dies at finite radius R ⇒ R is a recognizability radius, feeding W3's C4
  obligation directly; (b) both interpretations persist and the ambiguity
  automaton contains a cycle ⇒ extract and analyze the resulting
  invariant structure (possible periodic object or genuine non-unique
  hierarchy — either is decisive information).

### 3.3 Algorithms, feasibility, mitigation ladder

The honest risk is state-space explosion. At circumference parameter 47
one strip ring holds ~6·47 kite cells and the frontier window spans a few
tile diameters — the *reachable* state count is the unknown. Mitigations,
in order:

1. **Frontier minimization:** store only the staircase frontier profile
   (occupied/germ labels within tile diameter), not the full window; hash
   canonically; lazy BFS.
2. **Ladder of circumferences:** validate and profile on small |v| first
   (the Lucas values 18 and 29 before 47 and 76). Feasibility data at small
   norms calibrates whether 47 is reachable.
3. **Symmetry:** quotient states by the stabilizer of v in D₆ where
   applicable.
4. **Automata minimization / bisimulation collapsing** on the fly.
5. **Fallback if a target circumference is infeasible:** keep SAT but make
   it complete per-vector via the closure insight — incremental
   assumption-based solving ring by ring, declaring closure when the set of
   distinct boundary states repeats. (This is the transfer computation in
   SAT clothing; correctness argument identical.)

All cycle certificates are re-verified by constructing the explicit torus
tiling and passing it to the existing A1 verifier. All "no-cycle" runs
record the full reachable state census as the artifact.

### 3.4 Validation anchors (D-0005)

Before any finalist verdict is trusted:

- **Positive control:** run W1 on known periodic tilers from the n≤8 census
  (Myers-validated); the transfer graph must find cycles exactly for the
  vectors their known tori contain.
- **Negative control:** a shape with a pose-free A3 disk refutation must
  yield an empty/cycle-free graph trivially.
- **Hat control:** the hat must show no cycle for a sample of small vectors
  (it is proven aperiodic; any cycle would be a bug with a loud alarm).

### 3.5 Deliverables

- `src/einstein/periodicity/transfer.py` (exact frontier automaton; pure Python
  reference) + compiled port if profiling demands.
- Decided replacement for `e1-finalist-period47.json`: circumference-47
  cycle verdict, plus the T1.2 norm ladder table.
- T1.4 recognizability-radius artifact for the 8/7-type ambiguity.
- Notebook entries + EXPERIMENTS.md rows per run; theorem statements with
  certificate hashes.

**Definition of done:** T1.1 decided for the stripe direction; T1.2 table
non-empty with all controls passing; T1.4 resolved either way.

**Phase-0 status (2026-07-17).** The exact Python reference is implemented.
Its archived validation matrix covers all 28 combinations of free n≤3
polykites with four primitive/nonprimitive vectors, 102 independent bounded
torus comparisons, a torsion trap with period `(2,0)` but not `(1,0)`, and four
cycle-free hat vectors. It records 25 A1-verified cycles, zero disagreements
and zero resource exhaustions (`theory-w1-phase0-controls.json`). T1.1 remains
proof-draft at this checkpoint because graph hashes were not standalone proof
objects. Session 21 subsequently closed that gap with complete
pattern/state/edge/topological manifests and a separate verifier. The finalist
now has independently verified cycle-free certificates for all 11 D6 vector
orbits through Q(v)=25 (90 vectors, including nonprimitive ones), establishing
the scoped bounded-norm theorem T1.2-25. Universal O1 remains open.

---

## 4. Workstream W2 — algebraic and number-theoretic periodicity obstructions

**One-line goal:** convert A1's "UNSAT up to index budget" into scoped
theorems by killing infinite families of quotients with invariants, leaving
a finite residue that exact computation already covers (quantifier
reduction), with cheap necessary tests doubling as A1 pre-filters.

### 4.1 The covering equation on quotients

For a finite-index sublattice L ≤ Λ (index k, Hermite normal form as in
A1), the quotient torus has 6k kite cells. Let P(L) be the finite set of
tile placements (pose × position) on the quotient, and let M(L) be the
{0,1} incidence matrix placements × cells. Fully periodic tilings with
period lattice ⊇ L are exactly the 0/1 solutions x of

  M(L)ᵀ x = 1  (every cell covered exactly once).

All invariants below are *necessary* conditions derived from relaxations of
this equation. They can prove UNSAT (kill L) but never SAT — exactly the
polarity we want.

### 4.2 Layer A — counting congruences (immediate, worked example in hand)

Area: 6k cells, n cells per tile ⇒ n | 6k. **For the n=10 finalist this
gives k ≡ 0 (mod 5)** — four fifths of all HNF indices die instantly, and
the sweep "no certificate through index 215" tightens to "all admissible
indices ≤ 215," i.e. 43 admissible index classes. (Consistency check
already visible in the data: 215 = 5·43, and every cylinder width tested in
`e1-finalist-period47.json` is a multiple of 5.) Extensions: per-orientation
counts under the D₆-action on the quotient, boundary-edge parity counts.
Cheap, exact, and every one of them prunes A1's enumeration immediately.

### 4.3 Layer B — character (coloring) invariants

> **Corrected by T2.B0 / D-0030.** The isolated nontrivial-character
> infeasibility proposal below is retired: the Fourier transform of the
> constant torus target is zero, so each such projected linear system is
> homogeneous and has the zero solution. The trivial character reduces to
> Layer A. Character decomposition may still accelerate Layer C, but is not an
> obstruction by itself. See `docs/theory/controls/turtle/invariants.md`.

**Original v0.2 proposal, retained for audit provenance (not active):** Cells
of the quotient form a free Λ/L-set of rank 6. For each character
ψ: Λ/L → ℂ×, the covering equation projects to a 6-dimensional linear
system over ℤ[ζ_m] (m = order of ψ). Rational or algebraic-integer
infeasibility of the projected system for any ψ ⇒ UNSAT for L. This is a
polynomial-time necessary test per quotient (exact arithmetic over
cyclotomic integers — no floats).

The research lever: infeasibility at ψ often depends only on m and the
tile's projected coefficients, not on the full structure of L. Each such
certificate then kills **every** L whose quotient admits a character of
order m — an infinite family — in one stroke. Cataloguing which m die for
the finalist is a concrete, bounded first experiment.

### 4.4 Layer C — Smith normal form of the incidence module

> **Phase-1 result (session 23, D-0031).** With no exact SNF library installed,
> the implemented first slice uses full-quotient GF(2) left-cokernel witnesses.
> It has zero false exclusions on 60,477 periodic certificates and kills 36/742
> area-admissible finalist HNFs through index 60. A uniform witness proves the
> thin family HNF (1,0,k) impossible for all k≥4 (proof draft T2.C1). This is
> genuine Layer C information but not full SNF; odd/prime-power torsion and
> integer lattice membership remain open. See
> `docs/theory/controls/turtle/cokernel.md`.

> **Phase-2 result (session 24, D-0032).** Pinned FLINT/SymPy exact backends
> now implement the full integer membership test. Canonical row HNF classifies
> all 742 finalist quotients through index 60: 36 rank obstructions, exactly
> the GF(2) set; 706 unrestricted integer solutions; zero same-rank torsion
> obstructions. Bare integer cokernels therefore add no finite kill at this
> horizon. Continue with positivity/0–1 family certificates or Layer D.

> **Phase-3 result (session 25, D-0033).** Translation averaging reduces the
> full nonnegative rational incidence system exactly to the cone generated by
> six-sector placement profiles. Exact witnesses show that all 706 integral
> survivors through index 60 are fractionally compatible; the same 36 rank
> cases fail. Ordinary positivity adds no kill. The remaining Layer C target
> is binary exact-cover family structure, not another linear relaxation.

> **Phase-4 result (session 26, D-0034).** W1's 126 certified-impossible
> vectors through Q=36 compose with exact HNF membership into 126 infinite
> binary quotient families. They cover every HNF through index 36 and
> 2,941/8,864 admissible HNFs through 215. Exact D6 maps extend the thin proof
> to `(1,0,k)`, `(k,0,1)`, and `(k,k-1,1)` for every k≥4.

Drop the 0/1 constraint: does M(L) x = 1 have *any integer* solution?
Decide by Smith normal form of M(L) (exact integer linear algebra; sympy or
flint). If not, the cokernel witness is a compact, independently checkable
UNSAT certificate for L, strictly stronger than Layer B (which is its
rationalization character by character). Run on every admissible L in the
A1 sweep; record which indices are SNF-killed vs need SAT.

### 4.5 Layer D — nonabelian boundary invariants (research-grade)

> **Phase-0 result (session 27, D-0035).** The exact p3 Cayley implementation
> reproduces Conway--Lagarias' published three-in-line winding obstruction.
> The finalist presentation has 2,556 S3 surjections, but their
> zero-displacement kernels have order 6 or 3 and every displacement-coset pair
> admits commuting representatives. Displacement-only holonomy is therefore
> retired. The next implementation must couple finite-group potentials to the
> selected binary tile-boundary network; no finalist torus kill is claimed.

> **Phase-1/2 result (session 28, D-0036).** The coupled CSP is implemented
> with an at-least-cover relaxation, S3 vertex potentials and all 18 commuting
> torus twists. Periodic one-kite and shape-392 controls pass. A fixed phase-0
> quotient adds no kills on the 96 W1-family survivors at admissible indices
> 40--60, but the 234 strong S3 surjections reduce to 39 inner-conjugacy
> classes, and exhaustive class search kills all three index-40 survivors.
> Fifty-four Glucose DRAT cores independently verify with `drat-trim` and a
> canonical-CNF subset checker. With area and T2.C4-36, every finalist HNF
> through index 40 is now excluded. This finite prefix is not O1.

> **Phase-3 result (session 29, D-0037).** All 39 strong S3 classes were
> exhausted on the nine W1-surviving index-45 HNFs. Nine maps, partitioned
> into three identical-signature triples, collectively kill every HNF. One
> deterministic killing map per HNF yields 162/162 independently replayed
> DRAT cores. The complete grid-aligned quotient prefix is now closed through
> index 45. The triple signature is finite data pending a symbolic congruence
> theorem; index 50 brute-force scaling is secondary to explaining it.

> **Phase-4 result (session 31, D-0041).** An exact small-group census selected
> A4 as the first complementary target: its strong maps have normal
> displacement kernel V4 and residual quotient C3, compared with the C2
> information retained by strong S3. Exact D6 reduction turns the 12×48
> index-50 survivor matrix into 48 pair orbits. Sixteen are UNSAT over all 48
> twists and cover every HNF; 32 explicit relaxed models verify clausewise.
> Fixing the lowest killer gives 576/576 independently cold-replayed DRAT
> cores. The full shell splits 75 W1 + 6 S3 + 12 A4, so the certified quotient
> prefix is closed through 50. The 16 killers are exactly the maps with three
> distinct V4 values on the final three generators, a finite pattern now
> targeted for a symbolic HNF-family theorem. O1 remains open.

> **Phase-5 result (session 33, D-0043).** Exact semidirect reduction turns
> the distinct-tail A4 maps into four-colour local coverability SFTs and closes
> the certified finite prefix through index 55. The proposed infinite-family
> obstruction is falsified sharply at index 60: one three-HNF D6 orbit survives
> every signature map. All escapes pull back from explicit HNF `(2,0,2)`
> models, giving an infinite blind family `L <= 2 Lambda`. Even the product of
> all 16 maps with shared placements has a multiplicity-at-most-two model.
> Therefore more products of the same at-least boundary invariant are retired;
> further Layer D must encode packing/density, or effort returns to W1/W3.

> **Phase-6 result (session 34, D-0044).** The required packing refinement is
> local and sparse. The full exact-cover relation has 22,680 colliding pairs
> in 40 geometric D6 orbits on each index-60 escape. Forbidding only the orbit
> of a representative pair sharing six kites (720 clauses) makes the common
> 16-signature product UNSAT on all three residual HNFs. Three independently
> checked and cold-replayed DRAT cores establish T2.D6. The certified prefix
> remains 55 only because the other 42 solver-verified map-7 exclusions have
> not yet received proof bundles; producing those is now a finite packaging
> task rather than an invariant-design problem.

> **Phase-7 result (session 35, D-0045).** The finite packaging task is
> complete. One selector-union CNF per HNF represents all 16 map-7 V4 twists;
> 42/42 Glucose proofs were checked during production and cold-replayed,
> covering 672 direct logical cases. Together with 123 W1 exclusions and the
> three Phase-6 packing proofs, this exhausts all 168 index-60 HNFs. Area
> excludes indices 56--59, so T2.D2-60 is promoted. Further finite shells are
> controls, not the main theorem path; the next target is an infinite
> packing/holonomy family or W1/W3 recognizability.

> **Phase-8 result (session 36).** The packing mechanism survives its first
> family-scale falsification gate: all 193 area-admissible HNF sublattices of
> `2 Lambda` through index 120 are UNSAT, and every one of the 16 distinct-tail
> maps suffices separately (3,088/3,088 searches). A sharper candidate theorem
> removes coverage: exact controls at `k=4,8,20` attain at most `k/2` selected
> placements, below the `3k/5` required by area. Fixed 2x2 blocks and pairwise
> conflict graphs both have explicit counterexamples; the missing constraints
> are higher affine V4 gluing circuits of sizes at least 3--5. The theorem path
> is now a translation-periodic circuit-hypergraph density certificate
> (discharging or rational dual), not a larger raw quotient sweep. T2.D7
> remains a conjecture.

> **Phase-9 result (sessions 37--38).** The planar two-center/Hall route is
> retired by a literal countermodel. A deletion-minimal set of 63 fully
> nonoverlapping placements is compatible with one complete V4 signature but
> touches only 125 centers, so the required 126-capacity matching is
> impossible. Exact matching, geometric nonoverlap, seam-free XOR integration
> and an independent CNF replay all verify. The general minimal-core curvature
> lemma survives, but T2.D7-H is false even with full packing. Radius tapers
> remain diagnostics; primary effort returns to W3 as prescribed by the
> Phase-7 branch point.

The abelian layers are known to be blunt in general: many non-tilers pass
all of them. The tools with historical teeth are nonabelian: the
Conway–Lagarias tiling group (1990) and Kenyon's boundary-word invariants,
both formulated for simply-connected regions. The research question this
workstream owns:

> Extend boundary-word invariants from disk regions to torus quotients. A
> fully periodic tiling lifts to an L-invariant tiling of the plane;
> its two period holonomies a, b satisfy [a,b] = 1, and the expected
> obstruction is a class (morally in H₂ of the tiling group G_T = F/⟨tile
> boundary words⟩) that must vanish for a tiling with period lattice L to
> exist.

Milestone ladder: (i) reproduce Conway–Lagarias on their triangle regions
with our exact machinery (external anchor); (ii) formulate the torus
holonomy obstruction precisely and prove it necessary; (iii) compute it for
the finalist across admissible L. Honest assessment: (ii) is the actual
mathematical contribution of W2 if it works; it may also fail to be
computable at useful sizes — that outcome is recorded, not hidden
(program §2 discipline).

### 4.6 Combined W1×W2 theorem shapes

- **T2.1 (index quantifier reduction):** "T admits no fully periodic tiling
  with index k ∈ S," where S is an infinite congruence-described family,
  by Layers A–C; plus "for all remaining k ≤ K₀, exact UNSAT by A1/SNF."
  Jointly: no fully periodic tiling of index ≤ K₀ *and* none in S — with
  K₀ pushed as far as SNF (cheap) rather than SAT (expensive) allows.
- **T2.2 (with W1):** "no tiling has any period of norm ≤ N" (T1.2)
  strengthened by pruning the vector enumeration with Layer A/B data.
- **Aspirational T2.3:** a single invariant killing *all* sufficiently
  large k (would settle O1 outright). Do not promise; do check whether the
  Layer B/D certificates exhibit the required uniformity.

### 4.7 Validation anchors and deliverables

Anchors: (a) Layers A–C must *not* exclude any torus certified periodic in
the n≤8 Myers-validated census — zero false exclusions across all 60,477+
verified certificates is the gate; (b) Layer D reproduces Conway–Lagarias'
published triangle-region results.

Deliverables: `src/einstein/periodicity/invariants.py`; per-layer kill tables
for the finalist; A1 integration (invariant pre-filter before SAT);
EXPERIMENTS.md gate rows; for Layer D, a standalone note (potentially its
own short paper if (ii) succeeds).

**Definition of done:** Layers A–C running as A1 pre-filters with the
zero-false-exclusion gate passed; T2.1 stated with concrete S and K₀;
Layer D outcome recorded (theorem, partial, or documented dead end).

---

## 5. Workstream W3 — substitution certificates and the aperiodicity meta-theorem

**One-line goal:** define a finite certificate format such that a
once-proved meta-theorem converts any valid certificate into "T tiles the
plane and every grid-aligned tiling is nonperiodic" — then make A6 emit
such certificates, validate on hat/Spectre, and hunt one for the finalist.

This is the endgame — the wholesale closure of O1 plus the constructive
route to O3 — and the paper the community most needs: the
hat proof was bespoke; a reusable certificate format plus verifier is the
generalization.

### 5.1 Certificate schema (combinatorial, collared)

A certificate is a finite object:

- **Alphabet** A of collared metatiles: each a ∈ A is an exact polykite
  patch (the support) together with a collar specification (the legal
  radius-r surrounding language it may occur in), all in exact coordinates.
- **Substitution** σ: A → finite patches over A (each metatile decomposes
  into child metatiles), with exact geometric realization: the realized
  children partition the realized parent's support exactly, and
  macro-boundaries match across adjacent parents.
- **Legality data:** the exhaustively enumerated legal radius-r
  configuration set 𝓛_r (see §5.3), and for each element its unique parent
  assignment.
- **Growth data:** primitivity of σ's incidence matrix and an inball
  growth witness: a certified center and radius ρ_ℓ of a ball contained in
  each level-ℓ supertile, with ρ_ℓ → ∞. (The certified centers are
  load-bearing in the nonperiodicity argument — §5.2 step 3.)

Format: versioned JSON with content hashes, following the repo's artifact
conventions; a standalone verifier re-checks every clause with exact
arithmetic and CaDiCaL for the uniqueness clauses (all SAT results
re-verified by our own exact code, as A6 v2 already does).

### 5.2 Meta-theorem and proof skeleton

> **Meta-theorem (target).** If a certificate satisfies C1–C5 below, then
> Ω_T ≠ ∅ and every ω ∈ Ω_T has trivial translation stabilizer.

Finite obligations:

- **C1 (legality):** every realized supertile σ(a) is a legal patch;
  exact check.
- **C2 (closure):** every child occurrence inside every σ(a), with its
  induced collar, lies in A; exact check.
- **C3 (existence):** σ is primitive and some seed grows: then σⁿ(a) are
  legal patches with inradius → ∞, and the Extension Theorem gives
  Ω_T ≠ ∅. Finite check + one classical theorem.
- **C4 (recognizability/forcing):** for every configuration in 𝓛_r, the
  parent assignment of the central tile is uniquely determined (SAT-forced,
  as in A6 v2's 17-state/19-pattern uniqueness proof for Spectre).
- **C5 (global consistency):** local parent assignments glue. Whenever the
  assigned parent supertiles of two tiles overlap, the assignments agree,
  so parent supertiles in any tiling pairwise coincide or are disjoint and
  their union partitions the plane; and the induced parent tiling's
  radius-r configurations lie again in 𝓛_r, so composition can iterate.
  Finite check over exhaustively enumerated overlap configurations — this
  is precisely the "closes recursively" condition A6 v2 verifies on
  Spectre. C4 alone gives per-tile uniqueness; without C5 the contracted
  object need not be a legal tiling and step 1 below fails. (Added in R1.)

Proof skeleton for the nonperiodicity direction (standard, to be written
carefully once; cf. Mossé's 1D recognizability theorem and Solomyak 1998
for self-similar tilings — our combinatorial-collar setting needs its own
statement but the same architecture):

1. C4 + C5 ⇒ the composition map σ⁻¹ is a well-defined map Ω_T → Ω_T (on
   *every* tiling, not just substitution-generated ones — this is exactly
   why 𝓛_r must be complete, §5.3), and commutes with translations.
2. If ω + t = ω, then σ⁻ⁿ(ω) + t = σ⁻ⁿ(ω) for all n: t is a period at
   every level of the hierarchy.
3. By C3, choose n with certified level-n inball radius ρ_n > |t|. Let S
   be a level-n supertile of σ⁻ⁿ(ω) and c the *center of its certified
   inball* — an arbitrary point of S would not do, since c + t must land
   inside S. Then c + t ∈ S, and also c + t ∈ S + t, which is a level-n
   supertile of σ⁻ⁿ(ω) because t is a period at every level (step 2). Two
   supertiles of a partition sharing a point are equal, so S + t = S; a
   bounded set equal to its own nontrivial translate is impossible
   ⇒ t = 0. ∎

The once-proved meta-theorem plus per-tile machine-checked certificates is
the publishable framework; the hat certificate is its validation instance.

### 5.3 The completeness gap (critical precision)

The single most dangerous soundness hole: if 𝓛_r is enumerated from
*sampled patches* (A3/A6 output), C4 and C5 prove uniqueness and gluing
only over configurations we happened to see — the meta-theorem's step 1
would be false as stated. **𝓛_r must be enumerated exhaustively by constraint
search over all legal radius-r configurations**, the same exhaustive-
exhaustion discipline the A2 Heesch engine already implements. Concretely:
enumerate all ways to legally surround a tile to radius r (A2 machinery),
not all ways observed in patches. Configurations legal at radius r but not
extendable to tilings may appear; that is sound (uniqueness over a superset
is stronger), only expensive. This requirement is why A2, not A3, is the
substrate for legality data, and it must be stated prominently in the paper
— it is exactly the kind of gap a referee (or ERR-003) would find.

### 5.4 Validation gates (order of battle)

> **2026-07-19 implementation status.** The Spectre gate now has a versioned
> partial certificate: 17 closed deterministic states, primitivity exponent 3,
> and a unimodular 16-coordinate exact geometry recurrence matching all 32
> vendored levels. Exact physical legality passes for all labels at levels
> zero/one. The nine labels reduce inductively to two geometric support types;
> their abstract boundaries are disks through level four, and a five-piece
> boundary-word recurrence survives through level five. A four-side macro
> endpoint grammar is proved on every recurrence level using the degree-eight
> matrix annihilator. C1 now awaits a simplicity/noncrossing induction; C3
> awaits inball growth; sampled A6
> forcing still does not satisfy exhaustive C4, and C5 remains open.

1. **Spectre gate:** wrap A6 v2's existing closed 17-state hierarchy +
   forcing results into certificate format; verifier passes; meta-theorem
   hypotheses checked (the known-aperiodic control).
2. **Hat gate (blind, = Gate G1 alignment):** complete the hat's
   certificate — currently the next scale is only partially closed
   (430→71/72, 43/41→8; eight terminal nodes, non-unique physical
   ownership). The certificate discipline (esp. §5.3 exhaustive legality)
   is expected to either close it or expose precisely what is missing.
   *No finalist certificate is trusted before this gate passes* —
   the theory-side extension of the program's G1 rule.
3. **Finalist:** run the certified pipeline blind.

### 5.5 Finalist-specific search guidance

The Lucas return structure (§7) suggests hunting substitutions whose
incidence matrix has dominant eigenvalue in ℤ[φ] (golden-mean Pisot class),
and whose abstract return-vector bases map to each other under the
inflation — codex's proposal, adopted: derive candidate inflation matrices
from consecutive exact return-vector bases (script lineage:
`run_e1_finalist_translation_lattices.py`) and test each against exact
macrotile dissections rather than free-form mining. Important honesty
clause: like the hat's H/T/P/F system, the substitution is combinatorial —
no exact geometric similarity of the kite lattice realizes φ, so all
"inflation" claims live at the metatile level; only the incidence-matrix
eigenvalue is number-theoretic.

### 5.6 Machine-checked formalization (stretch, = E10)

Phase-ordered: (1) paper proof of the meta-theorem + independent
Python verifier for certificates (mandatory); (2) Lean formalization of the
meta-theorem with certificates imported as data (stretch; high referee
value, not a publication blocker). The certificate format should be
designed now so that (2) needs no reformatting: explicit finite sets,
no implicit geometry.

**Definition of done:** meta-theorem written with complete proof; verifier
implemented; Spectre and hat gates passed (or hat's failure mode precisely
characterized); finalist run recorded either way.

---

## 6. Workstream W4 — optional stronger grid rigidity and extensions

> **Status after ERR-004:** no longer a core proof obligation for polykites.
> Appendix A of the primary Hat paper already proves the weaker statement the
> periodicity program needs: existence of any periodic polykite tiling implies
> existence of an aligned periodic one. The plan below is retained only for
> the stronger all-tilings claim and for substrate families not covered by
> that theorem.

**One-line goal:** characterize when every tiling is aligned, or extend the
published periodic-alignment theorem beyond polykites.

### 6.1 The question

Does every tiling of the plane by the geometric tile T (congruent copies,
reflections allowed) align all copies to a single kite grid? If yes,
Ω_T as defined in §1.2 captures all tilings and every theorem upgrades to
the stronger all-tilings statement. If no, this does **not** reopen the
periodicity bridge already supplied by Appendix A; it only shows that some
nonperiodic or otherwise unclassified tilings lie outside the internal SFT.

### 6.2 Approach: finite contact analysis (feasibility spike first)

Polykite boundaries are polygonal curves with edge lengths in {1, √3} and
vertex angles in 30°·ℤ. Conjecture to test: the possible edge-to-edge
contact configurations between two copies of T are finitely classifiable,
and chains of contacts propagate a rigid common frame.

Spike plan (bounded; timebox before committing):

1. Enumerate T's boundary as an exact edge-word (lengths and turning
   angles).
2. Classify all relative poses of a second copy sharing a boundary segment
   of positive length: relative rotation must lie in 30°·ℤ (angle
   arithmetic); relative offset along a shared straight maximal segment is
   the continuous degree of freedom to kill.
3. For each maximal straight boundary segment, determine whether an
   off-lattice slide is locally blocked by adjacent boundary features
   (reflex corners, incommensurate 1/√3 alternation). ℤ-linear-independence
   of 1 and √3 over ℚ is the number-theoretic lever: sub-segment matchings
   force integer equations in the two lengths.
4. **Contact-connectivity lemma (an obligation, not an assumption; R1):**
   frame propagation travels only along positive-length contacts, and the
   graph on tiles with positive-length-contact edges need not be connected
   a priori — tilings can cohere across point contacts or along fault
   lines. Prove connectivity for T, or classify the possible disconnection
   interfaces (fault lines, vertex-only meeting stars) and handle each
   with its own finite analysis.
5. If every contact locks the frame *and* the connectivity lemma holds:
   global frame ⇒ single grid, then a finite translation-offset check pins
   the lattice phase.

Outcomes: (a) rigidity theorem, likely automatable per-shape — high value,
reusable across the whole census; (b) an explicit sliding contact — then
characterize the resulting non-grid configurations (fault lines etc.) and
either handle them by a secondary argument or scope the paper; (c) spike
inconclusive — scope the paper grid-aligned (Myers precedent), record the
conjecture in §13, move on. All three outcomes are acceptable; only
untracked ambiguity is not.

**Definition of done:** spike executed and written up with one of outcomes
(a)/(b)/(c) explicitly claimed.

### 6.3 Deferred: sheaf-theoretic packaging

Discrete sheaf language is deliberately *not* a workstream. Once the
pieces exist it is the natural common formalism — W1 boundary states are
sections over cut neighbourhoods, W3's C5 is literally a gluing/cocycle
condition on parent assignments, W4 frame propagation is a locally
constant sheaf on the contact graph — and Paper A may adopt it as
presentation language if it genuinely shortens proofs. It decides nothing
by itself; it is packaging, introduced last (agreed in R1).

---

## 7. Cross-cutting: inflation numerics and falsifiable predictions

The observed return scales 18, 29, 47, 76 are consecutive **Lucas
numbers** (L₆–L₉; each the sum of the previous two; growth rate φ).
Terminology (corrected in R1): these are lattice-coordinate separations —
coefficients over the Λ basis, as in the (0,47) translation — not
Euclidean lengths; the Euclidean norms of the observed return vectors
differ by direction, and no collinear geometric scaling is claimed. The
same φ governs the hat family (our A3 independently recovered the
reflected-hat density 1/(1+φ⁴)). Working hypotheses, each with a cheap
falsifiable test:

- **P7.1:** the next strong return scale is **L₁₀ = 123**. Test on the
  existing 18,386-tile nested patch and any larger nested successors
  (extend `run_e1_finalist_translation_lattices.py`).
- **P7.2:** the period-47 stripe domain (D-0025) is a **periodic
  approximant** of a golden-mean hierarchy — expected behavior for Pisot
  inflation tilings (Baake–Grimm), i.e. *evidence for* hierarchy, not
  against aperiodicity — **iff** W1 finds no cycle at circumference 47.
  If W1 finds a cycle, P7.2 is dead along with the candidate's strong
  aperiodicity. This is the single most information-dense pending
  computation in the program.
- **P7.3:** candidate W3 incidence matrices have dominant eigenvalue in
  ℤ[φ] with the return-basis mapping property (§5.5). Enumerable and
  testable exactly.

These predictions are cheap relative to their evidential weight; run them
early and record outcomes in EXPERIMENTS.md regardless of result.

---

## 8. Verification and rigor standards

Inherited from the search program, restated as binding for theory work:

1. **Exact arithmetic only** in every certificate path (integer, rational,
   cyclotomic/ℤ[φ] as needed). No floats in anything called a proof.
2. **External anchors before trust** (D-0005): every new component
   validates against independent data before its output feeds anything —
   W1 vs Myers census cycles; W2 vs the verified periodic-certificate
   corpus (zero false exclusions) and Conway–Lagarias' published results;
   W3 vs Spectre and the blind hat gate; any optional W4 extension against
   the Hat paper's Appendix-A theorem.
3. **Independent re-verification:** every SAT/automaton result re-checked
   by a second implementation path (existing repo discipline).
4. **Negative results are results:** dead invariants, infeasible state
   spaces, failed spikes — all recorded in notebook/EXPERIMENTS.md with
   parameters, per program §2/§7.4.
5. **Scope honesty:** every theorem statement carries its scope
   (grid-aligned or unconditional; per-vector or norm-bounded; which
   quotient family). The Turtle is cited as externally aperiodic; an
   *internal-certificate* Turtle claim may say only which O1/O3 components its
   own artifacts close. Future unknown candidates still require internal O1
   and O3 plus the W3 control gates before any aperiodicity claim.

---

## 9. Publication plan

### 9.1 Papers

- **Paper A (core, the framework):** *"Exact finite certificates for
  periodicity exclusion and substitution hierarchies of polykite
  monotiles."* Contents: framework (§1), W1 transfer theorems T1.1–T1.3,
  W2 Layers A–C with the quantifier-reduction theorem T2.1, the W3
  certificate format + meta-theorem + Spectre/hat validation instances,
  and the verifier as released artifact. This paper does not depend on the
  Turtle-control computation — its validation instances are known aperiodic
  tiles, and its data instances are the census. Target venues:
  Combinatorial Theory (hat-paper venue), Discrete & Computational
  Geometry, or SoCG→journal track; arXiv (math.CO, cross math.MG) first.
- **Paper B (data/census, possibly merged into A or separate short
  paper):** the polykite Heesch census n≤8 (no published equivalent
  exists), the A1 periodicity census n≤16 with certificates, and the
  Layer A–C kill tables. Target: Experimental Mathematics or the
  electronic Journal of Combinatorics.
- **Former Paper C (the finalist): retired.** The subject is the known Turtle,
  so there is no new-einstein paper. The finite Turtle results move into Paper
  A as a demanding blind validation instance for the certificate framework.
- **Possible Paper D (only if W2 Layer D succeeds):** torus/holonomy
  extension of Conway–Lagarias–Kenyon invariants — standalone
  combinatorial-group-theory interest.

### 9.2 Coordination and credit

Joint work with codex (design contributions already substantive: the
program skeleton, the rigidity correction, the collar-automaton and
return-basis proposals). Agree early on: authorship model, a shared
statement of the meta-theorem before implementation races ahead of proof,
and division W1/W2 vs W3 to parallelize. All artifacts (code, certificates,
JSON) released with the papers; reproducibility is a stated selling point.

### 9.3 Claim discipline for anything public

Pre-registration style: the proof-obligation ledger (§2) is the public
scoreboard. Nothing stronger than the ledger's green rows is claimed in
any abstract, talk, or preprint. For Turtle, distinguish the cited external
theorem from the repository's partial independent certificates. For future
unknown shapes, finite evidence remains “prioritization, not proof” until O1
and O3 close.

---

## 10. Milestones and dependency structure

```
Phase 0  (infrastructure, ~2–4 sessions)
  W1.a  frontier automaton core + controls (anchors §3.4)
  W2.a  Layers A–C implemented + zero-false-exclusion gate
  P7.1  Lucas prediction test on existing patches
        [W1.a ⊥ W2.a ⊥ P7.1 — fully parallel]

Phase 1  (first theorems, ~4–8 sessions)
  W1.b  circumference ladder 18 → 29 → 47 (P7.2 decision) → 76
        [needs W1.a; W2.a congruences prune its vector list]
  W1.c  T1.4 recognizability radius for the 8/7 ambiguity   [needs W1.a]
  W2.b  T2.1 quantifier-reduction theorem, kill tables      [needs W2.a]
  W3.a  certificate schema + verifier + Spectre gate        [needs A6 v2 only]

Phase 2  (the hard middles)
  W3.b  exhaustive 𝓛_r via A2 machinery; hat gate           [needs W3.a, W1.c]
  W2.c  Layer D research (torus holonomy invariants)        [independent]
  W3.c  optional Turtle certificate recovery (legacy finalist) [needs W3.b]

Phase 3  (writing)
  Paper A draft   [needs W1.b, W2.b, W3.b]
  Paper B draft   [needs W2.b; census already in hand]
  Paper D         [conditional per §9.1; former finalist Paper C retired]
```

Kill-switches / reprioritization triggers:

- W1 finds a Turtle cycle → treat it as a bug in the internal model or scope,
  because it contradicts the published Turtle theorem; preserve and diagnose
  the counterexample before trusting further certificate output.
- W3 hat gate fails irreparably → the meta-theorem stands but the
  "blind pipeline" claim is weakened; Paper A rescopes to
  Spectre-validated; the failure analysis itself goes in the paper.
- W1 state explosion at circumference 29 already → escalate mitigation
  ladder §3.3; if the fallback also fails, T1.2's N shrinks — record and
  proceed (partial N is still a theorem).

---

## 11. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| W1 state-space explosion at useful norms | medium–high | T1.2's N smaller than hoped | mitigation ladder §3.3; small-norm results still publishable |
| W2 abelian layers too blunt (kill few L) | medium | quantifier reduction weak; O1 stays budget-bounded | SNF layer is strictly stronger; Layer D is the real bet; bluntness data itself is reportable |
| W2 Layer D not effectively computable | medium–high | no torus holonomy theorem | milestone ladder isolates it; Paper A doesn't depend on it |
| W3 completeness gap (𝓛_r) prohibitively large at needed r | medium | Hat/Turtle independent certificates out of reach | A2 machinery is the best-in-repo tool; r grows one step at a time; partial-r results bound the recognizability radius from below |
| Hat gate reveals hat has no certificate in our format | low–medium | framework claim weakens | format designed after A6-v2's Spectre success; failure analysis publishable |
| Turtle control appears periodic internally | low but severe | model/certificate unsoundness | stop promotion, preserve witness, reconcile scope and geometry against published proofs |
| Rigidity spike inconclusive | medium | grid-aligned caveat permanent | acceptable published scope (Myers precedent); conjecture logged |
| Parallel-with-codex divergence (formats, definitions) | medium | wasted work, merge pain | freeze §1 definitions + §5.1 schema in this document before splitting work |
| Literature collision (someone publishes the framework first) | low | novelty loss | arXiv early once meta-theorem + Spectre gate done; census data is collision-proof |

---

## 12. Literature map (to engage before writing; verify all claims against sources at citation time)

The live, source-ID-based map is now `docs/literature/SOURCES.json`; its
synthesis and implementation gaps are `STATE_OF_THE_ART.md` and
`METHODS_MATRIX.md` in the same directory. Those files supersede this compact
orientation list for current publication status. D-0050 requires every new
theory branch to name its prior-art controls before implementation.

Immediate W3 dependencies are the SMKGS hierarchy proofs, Chéritat's Spectre
cluster analysis, Walton's general recognisability hypotheses,
Labbé--Selinger's SFT/Markov construction, and Tatham's finite-state
transducers. Optional Turtle recovery must additionally compare its output to
Akiyama--Araki's Golden Hex/Sturmian/Ammann-bar proof and James Smith's
rhombille representation. W1/W2 group work must distinguish itself explicitly
from the poly-`K` correspondence of Coulbois et al. None of these comparisons
is discharged by bibliographic presence alone; review depth remains recorded
per source.

- **Undecidability / decidability frontier:** Berger 1966 (domino problem);
  Ollinger 2009 (five polyominoes); Greenfeld–Tao 2023–24 (translational
  monotile aperiodicity in high dimension; undecidability program);
  Wijshoff–van Leeuwen 1984 and Beauquier–Nivat 1991 (exact polyomino
  translation tiling — the decidable base case).
- **The hat family:** Smith–Myers–Kaplan–Goodman-Strauss, *An aperiodic
  monotile* and *A chiral aperiodic monotile* (Combinatorial Theory, 2024)
  — both the results and the two proof architectures (computer-assisted
  case analysis; Tile(1,1) continuum argument); Myers' polyform census
  (our A1/A2 anchor).
- **Substitution/recognizability:** Mossé 1992 (1D recognizability);
  Solomyak 1998 (nonperiodicity of self-similar tilings; unique
  composition); Goodman-Strauss 1998 (matching rules for substitution
  tilings — the converse direction, relevant context for W3);
  Anderson–Putnam 1998, Sadun's book (tiling spaces, for framing only).
- **Boundary invariants:** Conway–Lagarias 1990 (tiling groups);
  Kenyon (boundary words); Thurston 1990 (height functions).
- **Aperiodic order / approximants:** Baake–Grimm, *Aperiodic Order* vol. 1
  (Pisot inflations, periodic approximants — underpins §7).
- **Transfer-matrix tiling enumeration:** standard strip-method literature
  (e.g., Klarner–Ries; Myers' methods) for W1 precedent.

---

## 13. Open problems (append-only)

1. Optional stronger rigidity: are all Turtle tilings grid-aligned? This is
   not needed for unconditional periodicity exclusion because the published
   Appendix-A reduction already supplies that bridge.
2. Does any single computable invariant independently recover O1 for the
   Turtle control (aspirational T2.3)?
3. Extend the binary-coupled Conway–Lagarias torus obstruction beyond the
   certified index-45 shell. Exact diagonal D6 covariance now reduces each
   finite HNF/map matrix to pair-orbit representatives; seek finite-group or
   HNF families rather than treating a larger finite prefix as O1.
4. Is the tiling problem decidable for the grid-aligned polykite family
   with bounded n? (Our W1+W2+W3 machinery is a partial decision
   procedure; characterizing where it must fail is itself interesting.)
5. Non-unique physical ownership in the hat A6 hierarchy: obstacle or
   feature of the certificate format?
6. Lean formalization of the W3 meta-theorem (E10).

---

## Appendix A — notation

| Symbol | Meaning |
|---|---|
| K | infinite kite complex (Laves [3.4.6.4]) |
| Λ | hexagon-center translation lattice |
| G = Λ ⋊ D₆ | full symmetry group; 12 orientations |
| T, n | tile (polykite), its kite count |
| Ω_T | space of grid-aligned tilings by T |
| Stab(ω) | translation stabilizer lattice of ω |
| L, k | finite-index sublattice of Λ, its index (HNF as in A1) |
| C_v | cylinder quotient K/⟨v⟩ for nonzero v ∈ Λ |
| M(L) | placement × cell incidence matrix on the L-torus |
| A, σ, 𝓛_r | metatile alphabet, substitution, exhaustive legal radius-r configuration language |
| φ, L_i | golden ratio, Lucas numbers (18, 29, 47, 76, 123 = L₆..L₁₀) |

## Appendix B — adopted decision

> **D-0027 — Adopt the theory research program (docs/program/
> theory_research_plan.md v0.2).** A theorem-producing track (W1 transfer
> automata, W2 algebraic obstructions, W3 substitution certificates, W4
> rigidity) runs in parallel with the computational funnel. Finite-patch
> and budget-limited results are henceforth treated as prioritization
> evidence only; claims stronger than the §2 proof-obligation ledger are
> prohibited. The W3 hat gate extends Gate G1 to the theory track: no
> unknown-candidate certificate is trusted before the known control
> certificates close blind. Budgeted per-width cylinder SAT sweeps are deprecated in favor of
> W1 exact per-vector decisions once W1.a passes its anchors.

The authoritative decision text is in `docs/DECISIONS.md`; this appendix is a
compact roadmap copy and must not be edited independently to change policy.
