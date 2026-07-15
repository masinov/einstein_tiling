# Finding the Next Einstein: A Research Program for the Systematic Discovery of Aperiodic Monotiles

*A methods cookbook: theory, algorithms, experiments, and infrastructure for a serious search
beyond the hat/spectre family.*

---

## 0. Executive summary

The hat (Smith–Myers–Kaplan–Goodman-Strauss, March 2023) and the spectre (May 2023) ended a
60-year search for an aperiodic monotile, but they were found by tactile exploration plus
bespoke software, not by a method. The theory that *analyzes* aperiodic order — substitution
dynamics, cut-and-project schemes, Pisot arithmetic, tiling-space cohomology — is mature; the
theory that *generates* it barely exists. This document specifies a research program that
mechanizes discovery along three coordinated pipelines:

- **Pipeline A (forward funnel):** industrialized enumeration of candidate shapes over
  arithmetically rich substrates, with fast periodicity rejection, SAT-driven patch growth,
  and a new *diffraction fingerprint* filter that detects quasicrystalline order in grown
  patches long before any proof exists.
- **Pipeline B (inverse design):** enumerate the *algebra first* — Pisot inflation data and
  combinatorial substitution systems over chosen rotation modules — then solve the geometric
  realization problem for a single shape.
- **Pipeline C (moduli prospecting):** systematize the hat's second aperiodicity proof
  (the Tile(a,b) interpolation between incommensurate periodic degenerations) as a *generator*
  of einstein continua with the proof pre-installed.

Each pipeline is specified to the level of data structures, constraint encodings, and numbered
experiments with success criteria. Throughout, "the engine" refers to an exact-arithmetic
substitution/tiling kernel of the kind already built for the spectre (integer-module
coordinates, implicit hierarchy traversal, tens of millions of tiles per second): every
pipeline consumes it.

---

## 1. Problem statement, made precise

### 1.1 Objects

A **tiling** of the plane is a countable collection of closed topological disks (tiles) with
pairwise disjoint interiors whose union is ℝ². A **monotile** setting fixes one prototile *T*
and allows placements by a specified symmetry group *G* — usually all isometries (rotations,
translations, reflections), sometimes orientation-preserving isometries only, sometimes
translations only. A tiling is **periodic** if its symmetry group contains a rank-2 lattice of
translations, **nonperiodic** if it has no nontrivial translation, and *T* is **aperiodic**
(an *einstein*, from German "ein Stein") if *T* admits at least one tiling and admits **no**
periodic tiling.

Three refinements matter operationally:

1. **Chirality of the allowed group.** The hat is aperiodic when reflections are allowed but
   requires reflected copies in every tiling. Tile(1,1) is aperiodic *only if* reflections are
   forbidden ("weakly chiral"); the spectre (curved-edge Tile(1,1)) is aperiodic outright and
   uses one chirality ("strictly chiral", the "vampire einstein"). Any search must fix, per
   run, which group *G* it is searching under, because the answer changes.
2. **Decorations vs. shape.** Matching rules painted on a tile (Socolar–Taylor 2010) can force
   aperiodicity where pure shape cannot; shape-only is the strong form. Boundary modifications
   (like the spectre's edge curves) convert some rule content into shape. A search should
   track the *pair* (shape, rule budget) with rule budget zero as the prize.
3. **Combinatorial vs. geometric aperiodicity.** In hyperbolic space and on other complexes
   the phenomenon changes character (binary tilings are weakly aperiodic monotiles in ℍ²);
   this program targets Euclidean ℝ² primarily and ℝ³ as a stretch goal (§9, E9).

### 1.2 When are two einsteins "the same"? The hull, MLD, and the enumeration target

The hat is not one tile: Tile(a,b) is a two-parameter continuum of einsteins (hat = Tile(1,√3),
turtle = Tile(√3,1)), and every einstein admits infinitely many boundary decorations. Naïve
enumeration of shapes is therefore the wrong target. The field's working equivalences:

- The **tiling space (hull)** Ω_T of a prototile *T* is the set of all tilings by *T*, with
  the local topology (two tilings are close if they agree on a large ball up to a small
  wiggle); ℝ² acts on Ω_T by translation. Ω_T is compact for finite-local-complexity (FLC)
  tilings and is the fundamental invariant-bearing object.
- Two tilings are **MLD** (mutually locally derivable) if each can be reconstructed from the
  other by a local rule. Two prototiles are "the same einstein" if their hulls are MLD (or,
  coarser, topologically conjugate / orbit equivalent). All Tile(a,b) hulls for generic (a,b)
  are related by shape deformation; the meaningful question is: **how many einstein hulls
  exist, up to MLD and deformation?** Known so far: essentially *one* (the hat/spectre
  family). The program's goal is a second, provably non-MLD hull — certified by the invariants
  of §3.6 — or structural evidence toward scarcity.

### 1.3 What a discovery deliverable looks like

A claimed new einstein must ship with: (i) the prototile with exact coordinates in an explicit
ℤ-module; (ii) an existence certificate — in practice a substitution system whose closure is
machine-verified (the spectre repo's `gen_tables.py` validation loop is a working prototype of
exactly this check); (iii) an aperiodicity certificate — one of the three proof schemata of
§3.7, formalized or at minimum computer-verified case analysis; (iv) invariant computations
(inflation field, diffraction module, cohomology) demonstrating non-MLD-ness from the hat
family; (v) the interactive/visual artifact (the engine renders it, which is not decoration:
human inspection of large patches has historically caught errors that proofs missed).

---

## 2. Hard limits: what computability theory forbids

Any honest program states its ceiling first.

- **Berger 1966:** the domino problem (does a given finite Wang-tile set tile the plane?) is
  undecidable; tilings simulate Turing machines. Modern self-referential constructions
  (Durand–Romashchenko–Shen fixed-point tilings) derive aperiodicity from Kleene's recursion
  theorem — evidence that tiling behavior can encode arbitrary logic.
- **Small-set undecidability:** undecidability has been pushed to single-digit numbers of
  polyominoes (Ollinger's 11, later reduced; most recently to around five, with active work
  below). Whether *one* tile's tileability is decidable is **open**. A complete algorithmic
  enumeration of all einsteins is therefore plausibly impossible.
- **Greenfeld–Tao (2022–):** the periodic tiling conjecture fails in ℤ^d for large d — a
  single *translational* tile whose tilings encode Sudoku-like constraint systems. Conversely,
  **Bhattacharya** proved the conjecture in ℤ²: a single tile tiling ℤ² by translations alone
  always tiles periodically. Consequence for us: **planar einsteins must exploit rotations
  and/or reflections**; the search space design (§4) bakes this in by enumerating over point
  groups, not just shapes.

The program's response to undecidability is restriction to structured classes where the
questions become hard-but-legitimate mathematics: FLC tilings over finitely generated
ℤ-modules, with substitutive or model-set structure as the certificate class. Every algorithm
below is a *semi-decision* procedure with explicit resource bounds, and "no result at budget"
is recorded data, not failure (§8, database schema).

---

## 3. Theoretical apparatus (what a researcher must have loaded)

This section is the required-reading map, organized by what each theory *does* for the search.

### 3.1 Substitution tilings: the certificate class

A substitution (inflation) rule replaces each prototile (or metatile) by a patch of tiles,
scaled by an inflation factor λ > 1. Key theorems the pipelines rely on:

- **Primitivity + FLC ⇒ minimality and unique ergodicity** of the hull: every patch appears
  in every tiling with well-defined frequency. This is why the app's choice of patch "doesn't
  matter" and why patch statistics (used by the ML filter, §4.6) are well-defined objects.
- **Recognizability / unique composition** (Mossé in 1D; Solomyak for nonperiodic
  self-affine tilings): in a nonperiodic substitution tiling, the supertile decomposition is
  locally determined and unique. This is the engine of most aperiodicity proofs: a lattice of
  periods would have to survive infinitely many compositions, contradicting growth. Pipeline
  A's certification stage (§4.5) is precisely an automated search for a recognizable
  substitution in grown patches.
- **Perron–Frobenius:** the substitution matrix M (entry M_ij = count of tile-type j in the
  inflation of type i) has a dominant eigenvalue λ² (area inflation); its left/right
  eigenvectors give tile frequencies and relative areas. For the spectre system, the counts
  satisfy T(n+1) = 8T(n) − T(n−1), so λ² = 4 + √15 — this recurrence check is a one-line
  validation every candidate system must pass.

### 3.2 Pisot arithmetic and why the number theory is load-bearing

λ² = 4 + √15 is a **Pisot number** (algebraic integer > 1, all conjugates inside the unit
circle; here the conjugate is 4 − √15 ≈ 0.127). Pisot inflation is what makes coordinates
*controlled*: deviations of tile positions from an ideal lattice projection stay bounded
because conjugate contributions contract. Consequences used constructively in Pipeline B:

- Vertex coordinates land in a finite-rank ℤ-module. For 12-fold geometry this is
  ℤ[ζ₁₂] ≅ ℤ⁴, which — not coincidentally — is exactly the rank-4 module (unit vectors at
  0°, 30°, 60°, 90°) the spectre engine computes in. The field tower is ℚ(√3, √5): √3 from
  the hexagonal substrate, √5 smuggling in the golden ratio (measured supertile boundary
  growth → 2 + √5 = φ³).
- The **Pisot substitution conjecture** (irreducible Pisot substitutions have pure point
  dynamical spectrum) is the deepest open problem adjacent to the program; any new einstein
  is automatically a new test case, and conversely the conjecture's verified instances guide
  which inflation data are worth realizing geometrically.
- **Meyer sets and cut-and-project (CPS) schemes** (Meyer, Lagarias; Hof; Schlottmann): a
  regular model set — projection of a slab of a higher-dimensional lattice — has pure-point
  diffraction. Baake–Gähler–Sadun showed the hat tiling is, up to local derivability and a
  linear shear, a cut-and-project set. Working hypothesis of this program: *every* planar
  einstein hull is MLD-or-close to a model set over a Pisot module. This hypothesis is
  falsifiable by the program itself and productive either way: it tells Pipeline B which
  internal spaces to enumerate and gives Pipeline A its fingerprint (§3.4).

### 3.3 The module substrate: where candidate shapes live

Aperiodic order with n-fold symmetry requires coordinates in ℤ[ζₙ], of rank φ(n) over ℤ
(Euler φ). Rank 2 (n = 3, 4, 6) is the crystallographic/lattice world — no einsteins there by
Bhattacharya-type rigidity for translations, and empirically none found for isometries on
plain lattices. The first non-lattice ranks are the program's hunting grounds:

| n-fold | ring | rank | field | status |
|---|---|---|---|---|
| 12 | ℤ[ζ₁₂] | 4 | ℚ(√3, i) / real: ℚ(√3) ⊂ ℚ(√3,√5) | hat/spectre live here |
| 5, 10 | ℤ[ζ₅] | 4 | ℚ(√5) | Penrose module; **no einstein known** |
| 8 | ℤ[ζ₈] | 4 | ℚ(√2) | Ammann–Beenker module; **no einstein known** |
| 7, 9, higher | ℤ[ζ₇], … | 6+ | cubic+ fields | terra incognita |

The concrete search substrates (Pipeline A) are polyforms whose edges are short vectors in
these modules: polyiamonds/polykites/polydrafters and half-kite refinements for n = 12;
Penrose-rhomb and kite–dart sub-polyforms plus Robinson-triangle polyforms for n = 5;
Ammann-bar-compatible square/rhomb polyforms for n = 8. The hat being a 13-polykite says the
winning granularity for n = 12 was "kites"; the analogous granularity for n = 5, 8 is an open
design choice that Experiment E3 sweeps.

### 3.4 Diffraction theory: the detector

For a point set Λ (e.g., tile anchor points of a grown patch), the autocorrelation γ and its
Fourier transform γ̂ (the diffraction measure) split into pure-point (Bragg peaks), absolutely
continuous, and singular-continuous parts. Facts the fingerprint filter (§4.4) is built on:

- Crystals: Bragg peaks supported on the dual lattice (rank 2). Regular model sets: Bragg
  peaks supported on a **dense, finitely generated module of rank > 2** (rank 4 for the
  families above) — sharp peaks that do *not* index to any lattice. Random/turbulent tilings:
  diffuse spectrum.
- **Dworkin's argument** connects diffraction spectrum to the dynamical spectrum of the hull:
  the fingerprint is not a heuristic but a shadow of the conjugacy invariant we ultimately
  care about.
- Numerically, γ̂ of a 10⁶–10⁷-point patch is a weighted FFT away, and *module-rank
  estimation* from detected peak positions is an integer-relation problem (LLL/PSLQ on peak
  coordinate vectors, §4.4). This converts "does this shape smell aperiodic?" — the judgment
  that took Smith's trained eye — into an overnight batch statistic.

### 3.5 Topological and operator-algebraic invariants: the deduplicator

To certify that a find is *new* (non-MLD to the hat family):

- **Čech cohomology of the hull** via Anderson–Putnam complexes (build the AP CW-complex from
  collared prototiles; the hull is an inverse limit under the substitution-induced map; H¹, H²
  are computable from the induced matrices). MLD tilings have isomorphic cohomology with
  matching order structure.
- **K-theory of the crossed-product C\*-algebra** and Bellissard's **gap labeling**: the trace
  on K₀ takes values in the frequency module — an MLD invariant with a physical meaning
  (spectral gaps of Schrödinger operators on the tiling).
- Cheaper first-line invariants: the inflation eigenvalue's minimal polynomial and field, the
  diffraction module (rank + rotational symmetry of the peak set), tile frequency vector's
  field, complexity/repetitivity growth. The dedup protocol (§8, E-invariants) computes cheap
  invariants first and escalates to cohomology only for survivors.

### 3.6 Search-side combinatorics

- **Heesch numbers:** the maximum number of coronas (full surrounding layers) a non-tiler
  admits. Kaplan's computations and Bašić's record (H = 6) define the state of the art;
  einsteins are the shapes where corona growth never stops but no period appears —
  operationally, *anomalously deep Heesch behavior* is the funnel's primary anomaly signal.
- **Isohedral numbers and the Grünbaum–Shephard classification** of the 81/93 isohedral types:
  the periodicity-rejection stage tests candidates against transitivity classes; shapes that
  tile only with high isohedral number (many orbits) are "almost aperiodic" and get priority.
- **Conway criterion and boundary-word methods** (BLD factorization for translation tilings):
  linear/near-linear sufficient tests for periodic tiling used as cheap early rejection.
- **Coordination/adjacency graph theory:** grown patches are graphs; frequent-subgraph mining
  over them is how candidate metatiles are extracted (§4.5), and spectral graph statistics
  feed the ML ranker.

### 3.7 Anatomy of the three known aperiodicity proof schemata (the templates to mechanize)

1. **Substitution + recognizability** (hat proof #1, spectre proof): exhibit metatiles, prove
   the inflation is forced (every tiling admits a unique composition into supertiles), conclude
   nonperiodicity from unbounded hierarchy. Mechanizable: closure verification is exact table
   arithmetic (already implemented for the spectre); forcing is a finite case analysis over
   collared configurations — SAT-checkable, Lean-formalizable.
2. **Incommensurate interpolation** (hat proof #2): embed the tile in a continuum Tile(a,b)
   whose endpoints tile periodically on lattices with irrational shape ratio; a period for an
   interior member would deform to a common period of both endpoints — contradiction. This is
   Pipeline C's generator: the proof is a property of the *family*, installed by construction.
3. **Coupling/HBS-marking arguments** (Goodman-Strauss style combinatorial coupling to a known
   aperiodic structure, e.g., a hexagonal parity field): show every tiling locally derives a
   known aperiodic object. Mechanizable as a local-derivation search between the candidate's
   grown patches and a library of reference structures (Penrose, Ammann–Beenker, hat,
   Taylor–Socolar parity patterns).

---

## 4. Pipeline A — the forward funnel

Goal: reduce ~10⁹–10¹¹ raw shapes to ~10²–10³ certified-interesting candidates per substrate,
with machine-attached evidence at every stage. Stages are strictly ordered by cost; each stage
writes its verdict to the shape database (§7.4) so no computation is ever repeated.

### A0 — Substrate enumeration

Enumerate polyforms up to isometry on each substrate of §3.3. Canonical-form hashing
(lexicographically minimal boundary word over the dihedral orbit) deduplicates; counts grow
roughly exponentially (base ≈ 3–5 depending on substrate), so the practical horizons are
polykites to n ≈ 20–24 cells, polyiamonds to n ≈ 28–32, with the ML ranker (A5) prioritizing
beyond the exhaustive horizon. Two non-classical substrates are mandatory because they are
where the theory says einsteins live and where hobbyist software never looked:
(i) *module polygons*: simple polygons whose edges are drawn from a fixed finite set of short
ℤ[ζₙ] vectors (this generalizes polyforms and includes the hat family's deformations);
(ii) *marked variants*: shapes plus a rule budget of 1 bit (chirality constraint or one edge
decoration), tracked separately since the spectre shows one bit sometimes converts.

Output per shape: boundary word, area, perimeter, symmetry group, substrate coordinates.

### A1 — Fast periodicity rejection

Ordered battery, cheapest first, each with a certificate: (1) Conway criterion and
translation-only BLD boundary-word factorization — microseconds, catches the bulk;
(2) isohedral search: SAT/CP instance asking for a fundamental-domain tiling within each of
the Grünbaum–Shephard isohedral types — milliseconds to seconds; (3) small-torus search:
does the shape tile a k×k torus for k up to a budget (periodic tiling ⟺ torus tiling for some
period); encoded as exact cover, solved with dancing-links or SAT. Any success stores the
period certificate and *retires* the shape from einstein candidacy (but feeds the isohedral-
number statistics that train A5, and high-isohedral-number tilers are logged: they cluster
near einsteins in shape space — the hat's neighbors tile with high isohedral numbers).

### A2 — SAT-driven patch growth (Heesch engine)

For survivors, grow coronas. Encoding: ground the placement set P = {isometry g : g·T
overlaps the disk of radius R}, boolean variable x_p per placement; clauses: every cell/point
of the region already committed must be covered exactly once (exactly-one over the covering
placements — use sequential-counter or totalizer encodings), pairwise-overlap conflicts as
binary clauses precomputed by geometric hashing; solve incrementally (IPASIR: kissat/CaDiCaL)
corona by corona, pushing assumptions per layer so UNSAT cores identify the blocking
configuration. Symmetry breaking: fix the seed tile's pose; break the stabilizer of the seed.
Deliverables per shape: Heesch depth h (last completable corona), UNSAT core signature if
blocked, and — critically — *all* distinct corona-1 configurations (their count and diversity
are strong features; einstein-adjacent shapes have many inequivalent surroundings).
Budget policy: exponential budget ladder (1s → 10s → 100s → distributed) with the ML ranker
deciding promotion. Anomaly definition: h ≥ h* where h* is the 99.99th percentile of the
substrate's Heesch distribution, or solver time-out with nontrivial growth — these graduate
to A3.

### A3 — Large-patch construction

Anomalies get 10⁵–10⁷-tile patches. SAT alone won't scale; use the hybrid: SAT for a seed
patch of ~10³ tiles, then greedy frontier extension with conflict-directed backjumping
(maintain the frontier's feasible-placement lists; on dead-end, backtrack the minimal
conflicting region using the SAT solver locally), with restarts and portfolio randomization.
Record the *growth-rate profile* (feasible placements per frontier length): forced structures
(substitution tilings) show characteristic near-deterministic profiles; this is itself a
feature. Failure to grow past ~10⁴ despite deep Heesch is also signal (Heesch-record shapes,
a different prize, logged for the combinatorics literature).

### A4 — Diffraction fingerprinting (the new eye)

From a big patch: take anchor points (or per-tile-orientation sublattices — computing one
diffraction per orientation class sharpens peaks), window with a smooth taper, compute the
2D FFT power spectrum. Detect peaks (local maxima above a noise floor calibrated on
randomized-patch nulls). Then **index the peaks**: stack peak position vectors and run
LLL/PSLQ to find a minimal integer generating set; report (rank r, generator matrix,
rotational symmetry of the peak set, pure-point fraction of spectral mass). Decision rule:
r = 2 ⇒ crystal (should have been caught by A1 — flag as A1 escape and improve A1);
r ≥ 4 with sharp peaks and n-fold symmetry ⇒ **quasicrystal candidate**, highest priority;
diffuse ⇒ likely tiles only "turbulently" (still interesting, low priority). Calibration is
Experiment E4: the filter must give textbook signatures on Penrose/Ammann–Beenker reference
patches and on hat patches grown *by the funnel itself, blind*, before any verdict on new
shapes is trusted. This stage is the single biggest methodological upgrade over 2022-era
search: it detects aperiodic *order* (not just non-periodicity) with zero proof effort, and
its output (the module) is exactly the input Pipeline B needs.

### A5 — Learned guidance (PatternBoost-style outer loop)

Train a ranker on all funnel verdicts: features = boundary turning word (sequence model),
symmetry, substrate stats, corona-1 diversity, Heesch depth of neighbors in edit distance;
label = graduated funnel stage reached. Use it to (a) order the beyond-exhaustive-horizon
frontier, (b) drive local search: mutate high-scoring shapes (cell add/remove, edge swaps in
the module polygon representation) — the hat's own neighborhood (hat→turtle→Tile(1,1)) shows
einsteins come in connected shape-space families, so hill-climbing near anomalies is sound.
Discipline: the oracle is always the funnel; the model only allocates oracle budget (A/B
tested in E5 against uniform allocation — if it can't beat uniform by ≥5× discovery
efficiency on held-out known anomalies, it's dropped).

### A6 — Hierarchy mining and auto-certification

For quasicrystal-flagged shapes, attempt the substitution certificate automatically:
(1) frequent-subgraph mining on the patch adjacency graph at increasing radii → candidate
clusters; (2) cluster the clusters by congruence → candidate metatile set; (3) hypothesize
composition rules by matching cluster adjacencies; (4) verify closure with the exact engine —
this is literally `gen_tables.py`'s validation loop run in reverse discovery mode: solve for
integer-module child transforms that reproduce observed patches, then check the substitution
reproduces itself; (5) prove forcing: enumerate all collared configurations up to the
recognizability radius and SAT-check that each admits a unique composition; (6) emit a Lean
skeleton of proof schema §3.7(1) with the case analysis as verified computation. Where no
substitution emerges, attempt schema §3.7(3): search for a local derivation to each reference
structure in the library (formulated as: does there exist a radius-ρ local map sending grown
patches onto a reference tiling's patches consistently — a constraint problem over the joint
patch database).

---

## 5. Pipeline B — inverse design (algebra → combinatorics → shape)

Motivation: the spectre's fingerprints (λ² = 4+√15 Pisot, ℤ[ζ₁₂] module, 9-label
substitution with an 8-child rule and one skip) are *small data*. The set of such fingerprints
is enumerable. Design order: number theory → matrix → combinatorial substitution → geometry.

### B1 — Enumerate inflation data

Fix a module ℤ[ζₙ] (n ∈ {12, 5, 8, 7} in priority order) and its real field K. Enumerate
candidate area-inflation numbers λ²: Pisot algebraic integers in K (or small extensions) up to
a height bound — for quadratic K this is a two-parameter sweep of minimal polynomials
x² − px + q with p² − 4q > 0, |root₂| < 1, and λ compatible with the rotation group (λ·module
⊆ module after the substitution's rotational part — an explicit divisibility condition in
ℤ[ζₙ]). For each λ², enumerate small primitive non-negative integer matrices M with Perron
eigenvalue λ²: dimension d ≤ 12, entries bounded by λ² + slack; this is a lattice-point
enumeration on the variety det(λ²I − M) = 0 intersected with primitivity — prune by trace
= sum of eigenvalues and by Perron eigenvector positivity. Sanity anchor: the sweep at n = 12
must rediscover the spectre's (d = 9, T(n+1) = 8T(n) − T(n−1)) data.

### B2 — Combinatorial substitution systems over M

For each (M, rotation assignment): enumerate abstract substitution rules — for each metatile
type, a multiset of children with types (given by M's rows), each child carrying a rotation
in ℤ/n and optional mirror, plus adjacency structure (which child edges glue). Consistency
conditions prune hard: edge hierarchies must be self-consistent (each parent boundary edge
decomposes into a fixed word of child edges — the same machinery as 1D substitution on the
boundary), Euler/angle sums must close, and mirror parity must be globally coherent (the
spectre's everything-flips-per-level pattern is one of few consistent parity schemes —
enumerate them). This stage is finite graph/word combinatorics; expect 10²–10⁵ consistent
systems per (M, n) cell.

### B3 — Geometric realization

Unknowns: edge vectors of each metatile as elements of the module (integer vectors of rank
φ(n)), and child translation offsets. Constraints: (i) each metatile's boundary word closes
(linear over ℤ); (ii) inflation consistency — parent edges scale to the prescribed child-edge
words under λ and the rotational parts (linear over the module once λ's multiplication matrix
is fixed); (iii) simplicity and non-overlap of the children inside the parent (semialgebraic —
polynomial inequalities over K). Solution strategy: solve the linear system (i)–(ii) exactly
over the module first (Smith normal form; the solution space is usually low-dimensional —
these are the *shape deformation parameters*, and Tile(a,b) reappears here as a 2-parameter
solution family); then decide (iii) on the solution family with exact computational real
algebraic geometry — SMT with nonlinear real arithmetic (Z3/cvc5) for point solutions, CAD or
sampling+interval certification for families. Output: metatile geometries with exact module
coordinates, verified by the engine (render, compose, check).

### B4 — Collapse to a monotile

Most realizations are k-prototile systems (new Penrose-like families: publishable byproduct,
and each enriches the reference library of A6). The collapse toolbox, in increasing
aggression: (a) *fusion* — search for a way to merge the prototiles' MLD-classes so that a
single shape with different orientations plays all roles (this is what the hat metatiles do:
H, T, P, F are all built of hats/anti-hats); formulated as: does a single polygon Q exist
whose translated/rotated/reflected copies partition each metatile compatibly with the
substitution — an exact-cover problem over the module; (b) *boundary reshaping* — deform
shared edges (the linear solution family of B3 plus non-polygonal decorations à la spectre
curve) to break unwanted symmetries or forbid unwanted matings, with the sine-curve
construction (180°-rotation-symmetric, mirror-asymmetric) as the canonical chirality-forcing
move; (c) *rule shaving* — if a 1-bit matching rule remains, search systematically for a
shape modification encoding that bit (the Socolar–Taylor → spectre precedent), as a small SAT
problem over edge-modification vocabularies.

---

## 6. Pipeline C — moduli prospecting (proofs pre-installed)

Systematize hat proof #2 as a generator.

**C1 — Formal template.** A *polyform continuum* is a combinatorial polygon with fixed edge
directions (in ℤ[ζₙ]) and edge lengths linear in parameters (a, b, …) ≥ 0. Endpoints of the
parameter simplex collapse edge subsets, degenerating the shape to smaller polyforms P₀, P₁.
Suppose P₀ and P₁ tile periodically with period lattices L₀, L₁, and every tiling by the
interior shape induces (by the collapse maps) tilings by P₀ and P₁ simultaneously whose
combinatorics agree. If a translation preserved an interior tiling, it would map to
translations in both L₀ and L₁ under the two collapses with the *same* combinatorial data —
impossible when the lattices are incommensurate (no common finite-index structure; concretely,
when shape moduli like |det L₀|/|det L₁| or angle ratios are irrational in the right sense).
The hat family realizes this with L₀, L₁ related by √3.

**C2 — Search algorithm.** (1) Enumerate pairs (P₀, P₁) of small periodic polyform tilers on
the same substrate whose boundary words are related by *edge-collapse duality*: there exists a
combinatorial polygon W and two collapse maps W → ∂P₀, W → ∂P₁ killing complementary edge
sets (a word-alignment problem — solve with dynamic programming over boundary words, feasible
for all pairs up to size ~20). (2) For each aligned pair, write the interior family and check
tileability of a generic member: the periodic tilings of P₀, P₁ give candidate combinatorics;
verify a generic-parameter tiling exists with the same combinatorics (linear feasibility over
the parameters, exact). (3) Check incommensurability of (L₀, L₁) exactly in the module —
an ideal-arithmetic computation, not a numerical one. (4) Each survivor is an einstein-
continuum *candidate with proof schema attached*; remaining obligations (the "same
combinatorics" forcing step, the hat proof's hard part) go to the A6 certifier and the Lean
track. Expected yield: the hat family rediscovered (mandatory sanity), likely siblings in
12-fold, and the first serious test of whether 5- and 8-fold moduli contain any such pair —
a structured question no exhaustive search has ever asked.

---

## 7. Infrastructure

### 7.1 The exact kernel

Generalize the spectre engine into a substrate-parametric library: (module = ℤ^r with an
embedding matrix into ℝ² and exact rotation/mirror actions as integer matrices; shapes =
boundary words of module vectors; substitutions = the exact table format already in
production). Required operations, all exact: congruence hashing, polygon simplicity,
patch composition/decomposition, adjacency extraction, rendering. The existing code base
(rank-4 module, implicit traversal at 15 ns/tile, wasm/webgl viewer) is the seed; the viewer
matters operationally — every anomaly gets a URL a human can pan around in, because trained
eyes remain the best free anomaly detector after the automated ones.

### 7.2 Solver stack

SAT: CaDiCaL/kissat via IPASIR for incremental corona pushing; CryptoMiniSat where XOR
structure appears (parity constraints from mirror bookkeeping). CP: OR-Tools CP-SAT for
exact-cover-flavored stages (torus tiling, fusion search). SMT: Z3/cvc5 (nonlinear real
arithmetic) and dReal (δ-decidability) for realization; exact fallback via CAD in
SageMath/Mathematica for low-dimensional families. Algebra: PARI/Sage for number-field and
ideal arithmetic (B1, C2 incommensurability), FLINT for Smith normal forms, fpylll for the
LLL peak indexing. Formalization: Lean 4 + mathlib; target reusable libraries: module
geometry, substitution closure, recognizability case-checks.

### 7.3 Compute shape and budgets

The funnel is embarrassingly parallel across shapes: a fleet of preemptible CPU nodes with a
work queue. Order-of-magnitude budget for one substrate season (polykites n ≤ 22):
~10⁹ shapes × (A1 ≈ 5 ms avg) ≈ 60 CPU-days; ~10⁶ A1-survivors × (A2 ladder ≈ 30 s avg) ≈
350 CPU-days; ~10³ anomalies × (A3+A4 ≈ 1 h) ≈ 40 CPU-days: comfortably a few weeks on a few
hundred cores — the bottleneck is engineering quality, not FLOPs. GPUs: FFTs (A4), the ranker
(A5), and batched geometry hashing; patch-growth SAT is CPU-bound and branchy, leave it there.

### 7.4 The shape database (the real asset)

Content-addressed store keyed by canonical boundary word: substrate, symmetry, all funnel
verdicts with certificates (period lattice / UNSAT core / Heesch depth / corona census /
diffraction module / substitution tables), solver versions, budgets, and negative results.
Every claim in eventual papers resolves to a database row + rerunnable job spec. Publish it:
the field currently has no shared corpus, and the ML stage is only as good as this labeled
data — which is why even "boring" verdicts are stored.

---

## 8. Experiments

Each experiment states hypothesis, method, and pass/fail criteria. E1–E4 are validation
(no verdicts on new shapes are trusted before they pass); E5–E9 are discovery.

**E1 — Blind rediscovery of the hat (funnel validation).** Hypothesis: the funnel, run on
polykites n ≤ 16 with no hat-specific knowledge, surfaces the hat (and turtle) at the top of
its anomaly ranking. Method: full A0–A4 sweep; freeze all thresholds beforehand. Pass: hat
flagged quasicrystalline with a rank-4 ℤ[ζ₁₂] diffraction module and graduates to A6, which
finds a working substitution automatically. Fail-analysis clause: any stage that loses the hat
gets redesigned before any new-shape claims. (This is the program's unit test; it also
calibrates all cost models.)

**E2 — Exhaustive 12-fold sweep beyond the known horizon.** Polykites to n ≈ 22–24 and
module polygons with ≤ 16 edges from the short-vector vocabulary. Hypothesis (from the
hat→turtle→spectre connectivity): additional einstein continua exist in 12-fold geometry
adjacent to, but not MLD with, Tile(a,b). Deliverable either way: the complete anomaly census
of the substrate — the first of its kind.

**E3 — First serious hunts in 5-fold and 8-fold.** Robinson-triangle/rhomb polyforms (n = 5)
and Ammann-rhomb polyforms (n = 8) through the funnel, plus granularity sweep (which cell
shape plays the role kites played). Hypothesis: the working hypothesis of §3.2 predicts
einsteins *can* exist here; no search has ever been run. Even a strong negative (no anomaly
beyond depth h* at exhaustive horizons) is a publishable structural signal that 12-fold is
special.

**E4 — Fingerprint calibration.** Build the reference library: Penrose, Ammann–Beenker,
hat/spectre, Taylor–Socolar, a periodic control set, and a random-tiling control (square-
triangle random tilings). Verify the A4 detector: pure-point module ranks recovered exactly;
false-positive rate on 10⁴ random periodic tilers < 10⁻³; peak-indexing stable under patch
size doubling. Also validates the LLL indexer against deliberately sheared/rotated patches.

**E5 — ML allocation A/B.** Split an untouched shape stratum; allocate A2 budget by ranker vs.
uniformly; measure anomalies found per CPU-hour. Keep the ranker only if ≥ 5× efficiency at
equal budget, evaluated on strata disjoint from training. Secondary: mutation hill-climbing
seeded at known anomalies must rediscover the hat's family from the turtle in ≤ 10⁴ oracle
calls.

**E6 — Inverse-design season, 12-fold then 8-fold.** B1–B3 sweep: quadratic Pisot λ² with
trace ≤ 20 over ℚ(√3) and ℚ(√2), matrices d ≤ 10. Mandatory anchor: rediscover the spectre's
system (d = 9, λ² = 4+√15) and realize it geometrically ab initio. Then the discovery claim:
enumerate all realizable systems at this height — each realization is at minimum a new
substitution tiling family; run B4 collapse search on each. Success tiers: (i) new k-prototile
families (near-certain), (ii) a 2-prototile system admitting fusion (breakthrough-adjacent),
(iii) a monotile (the prize).

**E7 — Moduli prospecting season.** C2 over all periodic polyiamond/polykite tilers with
≤ 14 cells: full pairwise edge-collapse alignment, incommensurability filter, generic-member
tiling check. Mandatory anchor: the Tile(a,b) family emerges from its two degenerate endpoint
tilers. Deliverable: the complete list of interpolation-eligible pairs on the substrate — the
first systematic map of where the hat's proof technique can possibly apply.

**E8 — Convex exhaustion (negative program).** Rao-style: convex polygons tile only if
triangle/quadrilateral/one of 15 pentagon families/certain hexagons; all are periodic-capable.
Formalize "no convex einstein exists in ℝ²" by auditing and Lean-formalizing the Rao
computation plus the classical classifications. Value: closes a standing folklore gap and
builds the formalization muscle the certification track needs.

**E9 — 3D pilot (moonshot tier).** The SCD biprism is only weakly aperiodic (screw-periodic);
a strict 3D einstein is open. Method: restrict to structured families where 2D machinery
lifts — prism-like and layered shapes over the 2D anomaly census (a hat-cross-section prism
with height-encoded phase constraints is the natural first family), Danzer-tetrahedra
polyforms, and Voronoi cells of model sets in ℝ³. 3D SAT patch growth is brutal; budget it as
exploration, success criterion is a calibrated 3D funnel (E1-analog on SCD), not a find.

**E10 — Certification and formalization track (runs throughout).** Lean formalization of:
module geometry library; substitution closure checker (reflecting the exact tables);
recognizability case-analysis verifier; the interpolation proof template of C1. Milestone:
hat aperiodicity fully formalized via schema (1) or (2) — independently valuable, and it is
the referee for any discovery claim this program makes.

---

## 9. Deduplication protocol for a claimed find

Cheap → expensive: (1) inflation eigenvalue's minimal polynomial and field — differs from
x² − 8x + 1 / ℚ(√3,√5) ⇒ new hull immediately; (2) diffraction module rank and rotational
symmetry; (3) tile-frequency vector field; (4) complexity function growth; (5) Anderson–Putnam
cohomology H¹, H² with order structure; (6) if all coincide with the hat family, search
explicitly for an MLD map (bounded-radius local derivation, SAT over the joint patch
database) — failure to find one at generous radius is evidence, not proof, and gets flagged
honestly as such.

## 10. Risks and epistemic posture

(1) *Undecidability leakage:* some anomalies will be neither certifiable nor refutable at any
budget; the database records them as open with exact resource stamps — they are data about
the boundary of the decidable, not embarrassments. (2) *Scarcity:* it is entirely possible
that 12-fold-with-reflections is essentially the only planar einstein hull; the program is
designed so that strong negatives (E2, E3, E7 exhaustions) are themselves theorems-in-waiting
about rigidity. (3) *Fingerprint blind spots:* einsteins with singular-continuous spectrum
(no Bragg peaks) would evade A4; mitigation is that A2/A3 anomaly signals are spectrum-
agnostic, and the random-tiling control in E4 measures exactly this gap. (4) *The Smith
factor:* keep a human-in-the-loop channel — every anomaly ships as an interactive viewer
instance; budget explicitly for unstructured play. The last einstein was found by someone
cutting shapes out of card; the program's job is to make sure the next Smith is looking at a
pre-filtered gallery of the 200 strangest shapes in a billion, not at all billion.

## 11. Milestones (indicative 3-year shape)

Year 1: kernel generalization, funnel build, E1 pass, E4 calibration, database public, E2
launched. Year 2: E2/E3 complete censuses, E5 verdict, E6 12-fold inverse season, E7 map,
first new substitution families published, hat formalization (E10) landed. Year 3: E6 8-fold
and collapse campaigns, certification automation mature, E9 pilot; go/no-go on scarcity
thesis. Team shape: 1 substitution-dynamics theorist, 1 computational number theorist,
1 SAT/solver engineer, 1 systems engineer, 1 formalization specialist, plus the play channel.

## 12. Core reading list

Grünbaum & Shephard, *Tilings and Patterns* (the canon); Baake & Grimm, *Aperiodic Order*
I–II (diffraction, model sets, Meyer sets); Sadun, *Topology of Tiling Spaces* (hulls,
Anderson–Putnam, cohomology); Smith–Myers–Kaplan–Goodman-Strauss, "An aperiodic monotile" and
"A chiral aperiodic monotile" (2023) — read both proofs as templates; Baake–Gähler–Sadun on
the hat as a cut-and-project set; Socolar–Taylor (2010); Berger (1966), Ollinger and
successors on small-set undecidability; Bhattacharya (ℤ² periodic tiling conjecture);
Greenfeld–Tao (counterexample program); Solomyak (recognizability); the Pisot substitution
conjecture surveys (Akiyama et al.); Kaplan on Heesch numbers; Rao (pentagon exhaustion);
Myers' polyform tiling records; Charton–Ellenberg–Wagner et al., PatternBoost, and
Romera-Paredes et al., FunSearch (learned search methodology).

---

*Everything above assumes the exact-arithmetic engine as substrate. The spectre repo built
alongside this document — integer-module coordinates, machine-verified substitution tables,
implicit hierarchy traversal at tens of millions of tiles per second, diffraction-ready patch
generation, and an interactive viewer — is deliberately the v0 of that kernel.*
