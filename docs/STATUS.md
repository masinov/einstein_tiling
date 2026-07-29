# Program status

> Living dashboard. Update at the end of every working session.
> The specification is [docs/program/einstein_search_program.md](program/einstein_search_program.md)
> (with corrections in [docs/program/ERRATA.md](program/ERRATA.md)).
> Session-by-session detail lives in [docs/notebook/](notebook/); decisions in
> [DECISIONS.md](DECISIONS.md); experiment gates in [EXPERIMENTS.md](EXPERIMENTS.md).

**Last updated:** 2026-07-29 (session 195 ordinary-vertex parity no-go)

> **Identity correction (ERR-003/D-0048):** every current use of “the
> finalist” and every legacy `e1-finalist-*` artifact refers to the published
> ten-kite **Turtle**, not a new candidate. Its tilability and nonperiodicity
> are known. The preserved computations are Turtle-control and method results.
>
> **Horizon correction (ERR-004/D-0049):** the peer-reviewed Hat paper reports
> the exhaustive aperiodic-polykite horizon `n≤24`, not 21. E1 is entirely
> validation; frozen E2 (`n≈22–24`) is invalid as discovery. Promotion is
> fail-closed against both that horizon and the infinite polykite portion of
> `Tile(a,b)`. See the [literature baseline](literature/POLYKITE_BASELINE.md).

## Where we are

| Milestone | Scope (program §) | Status |
|---|---|---|
| M0 — kite substrate + A0 enumeration | §7.1 (kernel v0), §4 A0 | ✅ done through E1 n≤16 horizon, validated vs OEIS (sessions 01, 12) |
| M1 — A1 periodicity rejection + shape DB | §4 A1, §7.4 | ✅ done v0, validated vs Myers (session 02) |
| M2 — A2 corona/Heesch engine | §4 A2 | ✅ done v0, hat = unique n≤8 anomaly (session 03) |
| M3 — A3 large-patch growth | §4 A3 | ✅ done v1; exact disk SAT plus required-placement nested-core extension (sessions 04, 11, 19) |
| M4 — A4 diffraction fingerprint | §4 A4 | ✅ done v0; 12-fold core calibration passed (session 05) |
| E4 — full fingerprint calibration gate | §8 E4 | ✅ passed (sessions 05–06) |
| M5 — A6 hierarchy mining | §4 A6 | ✅ done v0; recursive, stationary-collar and SAT forcing gate passed |
| T0/W1/W2 — exact theory foundations | theory program v0.2 | ⏸ frozen control branch; Turtle-control T1.2-36 and the finite S3/A4 holonomy prefix remain exact, but abelian methods are classical and all Turtle conclusions are subordinate to published aperiodicity (D-0067) |
| W3 — substitution certificates | theory program v0.2 | ✅ closed as a novelty branch; exact Spectre results retained as a machine-readable reconstruction/control, with no further radius or D4-context work authorized (D-0070) |
| **Gate G1 — E1 Hat/Turtle validation** | §8 E1 | ✅ closed as validation/postmortem; historical runs are not an unbiased global benchmark (D-0068) |
| ST-M1 — Sturmian monotile encoding | outside-horizon theorem branch | ▶ active at one non-ordinary contact-hyperedge/visible-star problem plus the cross-carrier boundary. Minimality eliminates proper lattice-factor pruning; rail-separable schemes are periodic. K68V proves the local vertex algebra has no charge beyond parity, N68H closes boundary-neutral carriers at every area, and K69A/N69O close ordinary multi-tile sector vertices as the joint coupler. Any survivor must export joint rail state through a visible auxiliary completion, T-junction/fusion hyperedge, or proved larger-radius exclusion. The marked family is undecidable and contact-complete separable Stade erasures are periodic (ERR-017/D-0208--D-0222). |
| Pipelines B, C; substrates n=5,8; scaling | §5, §6, §3.3 | ⬜ not started |

**No verdicts on new shapes are trusted before Gate G1 passes** (program §8).

## What exists and is verified

- **Versioned literature subsystem:** 38 source records distinguish
  peer-reviewed theorems, computational methods, preprints, reviews and
  secondary evidence; 35 open PDFs plus text extracts are reproducibly cached
  outside Git. The state-of-the-art map, methods-to-code matrix, reading queue,
  and novelty protocol make exact shape novelty, tiling-system novelty,
  aperiodicity, and method novelty separate claims. Turtle is now a blinded
  positive control. See [`docs/literature/`](literature/README.md) and D-0050.
- **Golden-Sturmian Turtle control:** the Akiyama--Araki proof is now audited
  theorem by theorem. Exact code verifies its standard/central words through
  level 24 and both irrational density polynomials. The independently grown
  9,239-tile Turtle disk has minority handedness `1181/9239=0.127827687`, close
  to the published exact `(3-sqrt(5))/6=0.127322004`. Forced Ammann-bar and
  Golden Hex geometry remain external, so this is validation rather than a
  new aperiodicity proof (D-0051).
- **Isohedral-surround SAT control:** Kaplan's finite extendable-surround
  criterion is implemented with the full vertex halo. The complete `n<=8`
  counts `1,1,4,4,0,70,52,37` match Myers exactly; all 169 positive surrounds
  cold-verify. It separates periodic anisohedral shapes for A1 and rejects Hat
  and Turtle. This is a portable early filter, not an aperiodicity test
  (D-0052).
- **Recognisability theorem crosswalk:** Walton's compact-Hausdorff expansive
  `L`-sub theorem and Chéritat's all-whole-plane Spectre hierarchy are now
  mapped to separate W1--W5 and D1--D7 machine obligations. The distinction
  prevents a circular proof: in return-discrete tiling spaces Walton's strict
  injectivity is equivalent to already excluding periodic hull elements,
  whereas Chéritat directly proves total unique grouping for every tiling.
  Certificate v2 cold-verifies and honestly remains partial (D-0053).
- **W3 method-novelty audit:** the reduced-patch/overlap-deletion/forced-parent
  architecture is already explicit in the original Spectre proof, Chéritat
  supplies the all-whole-plane equivalence, and the matching-rule and
  finite-state literature covers the general encoding ideas. A new July 2026
  Hat paper also publishes exact JSON retiling certificates and a verifier.
  W3 is therefore an exact reproducibility/control implementation, not a new
  aperiodicity theorem or established general method. The 80 abstract D4
  contexts will not be extended (D-0070).
- **ST-M1 theorem design:** minimal aperiodicity is separated from the
  surjective positive-entropy strengthening. A coupled contact-star carrier
  is the only retained mechanism; independent finite-state rails admit a
  periodic product. The full-isometry theorem requires geometric
  homochirality and a reflected global decoder. The source's
  `kappa=infinity` remark was not itself a complete system theorem, motivating
  the explicit S0 derivation below; no unmarked contact kernel has yet been
  derived (D-0071).
- **ST-M1 equal-support compiler:** a finite connected macrotiling system over
  one congruent periodic cell is MLD with a finite colored one-support system
  by explicit internal-address ports. This closes only the conditional
  compiler S0C. The source's `kappa=infinity` remark does not provide the
  common-cell subdivision or preserve the complete Section 10.1 language
  (D-0072, ERR-006).
- **ST-M1 source correction:** primary Table 1 gives the optimized
  `sqrt(2)-1` large templates composition `12S+6M+6L`, not bare `2S+L`.
  The one-support `kappa=infinity` sentence belongs to the separate Turtle
  subsection. The session-65 `18,18,2` specialization, its all-`M` exclusion,
  and the resulting S0 closure are withdrawn. S0C remains a valid conditional
  compiler, but S0/E-infinity are blocked (ERR-006/D-0076).
- **ST-M1 corrected composition skeleton:** in the source convention the
  actual large templates are `[12:12:6]` and the small template is
  `M=[0:2:0]`. Their segment meets the Sturmian parabola exactly at
  `beta=sqrt(2)-1`, with positive mixture coefficients. This proves P0 and
  retains the irrational-slope arithmetic target. The source SAB language,
  not composition alone, excludes all-`M`; E-infinity remains blocked
  (D-0077).
- **ST-M1 corrected common-support geometry:** direct centroid coordinates
  show normalized `kappa→infinity` isometric cells converge to one
  `60/120` rhombus. Splitting each `M` along the marked short diagonal gives
  common equilateral triangles and actual raw template counts `30,30,2`.
  This proves G0 only. New limiting point contacts and bent SAB/vertex rules
  leave the all-tilings language equivalence L0 open; S0 and K1 remain blocked
  (D-0078).
- **ST-M1 overlap-semantics correction:** Section 10.1's overlapping tiny
  triangles belong to auxiliary `P1/P2/P3` BD patches, not the final physical
  patch-tile tiling. O0 proves that disjoint auxiliary overlap disks contract
  to finite decorated vertices retaining participant identities and cyclic
  order. L0 is now split into O0 (proved), physical incidence I0 and total
  decoder D0 (open). No atlas enumeration is authorized (D-0079).
- **ST-M1 limiting physical incidence:** exact centroid indices place vertices
  in three disjoint order cosets. The coset and lattice coordinate uniquely
  recover the source triangle; primitive limiting edges contain no interior
  vertex. With retained role/address/SAB colors, every physical vertex star
  has one prelimit lift. The physical-order restriction `s in {-1,0,1}` is
  essential and now explicit: unrestricted indices have a diagonal `(1,1,1)`
  ambiguity. I0 closes without an atlas (D-0080/D-0082); the following
  session supplies D0.
- **ST-M1 minimal colored source:** the global triangular frame integrates
  exact line-index increments with zero face holonomy. Local gap-equality
  ports recover three global narrow/wide sequences; source edge/SAB rules and
  P0 force slope `sqrt(2)-1`. D0 closes L0, E-infinity and S0 in proof draft
  without enumerating an atlas. This is a period-reflecting symbolic decoder,
  not finite-`kappa` MLD or a positive-entropy result. The possible source
  conjugate is `-1-sqrt(2)`, outside `[0,1]` (D-0081/D-0082).
- **ST-M1 symbolic quotient boundary:** Q0 correctly requires safety on the
  full finite local closure. Erasing ownership to unrestricted `S/M/L`
  restores rational periodic tilings, and independent corridor rails admit
  periodic products. The full addressed S0 presentation is now available,
  but no smaller future-equivalent K1 quotient or collar table is established.
- **ST-M1 lossless contact compiler:** directed half-contact records name both
  addressed endpoint states and sides; the three records incident to one
  triangle share a center state, and legal cyclic corner words retain the
  vertex rule. Encoding and decoding are inverse radius-one maps on the full
  contact-rule space. K1C is a standard symbolic recoding, not a nontrivial
  quotient or geometric carrier (D-0083).
- **ST-M1 quotient safety contract:** K1R separates injectivity on the
  intended compact image from K1T's stronger totality on the quotient SFT.
  K1T requires a bounded decoder that satisfies source rules and re-encodes
  every admitted quotient configuration. Erasing all modes fails because the
  remaining triangular frame is periodic. At session 74 no quotient or radius
  had yet been chosen (D-0084); K1D below supplies the quotient without a
  collar-radius search.
- **ST-M1 distributed contact quotient:** an injective three-coordinate code
  distributes each addressed source state over its incident contacts. The
  joint tile star decodes exactly and satisfies K1T on the whole local-rule
  space. At least 32 essential addresses force four modes per side for an
  immediate balanced decoder. The original N4 application omitted its
  non-Cartesian premise: `32=4*4*2` permits a Cartesian image. K1P repairs this
  by selecting the even-parity half of `{0,1,2,3}^3` on the guaranteed
  32-state core and fresh diagonal triples thereafter. This selected safe
  code requires joint star coupling; no 62-state essentiality or universal
  coding no-go is claimed (D-0085/D-0086).
- **ST-M1 exact geometric contract:** K2E separates the stronger exact K1P
  realization from minimal ST-M1 and states six sufficient obligations. N5
  proves that the parity core has full binary projections, so independent
  sides and ordinary two-side corner checks cannot enforce it. K2G needs a
  ternary junction, a locally recoverable auxiliary phase, or a proved
  larger-radius exclusion; no polygon or atlas exists yet (D-0087).
- **ST-M1 auxiliary-phase bound:** K2H factors the parity core through four
  hidden states and pairwise phase/interface relations; N6 proves four is
  minimal by a product-box cover argument. The phase must be a locally
  distinguishable geometric pose/star class, not an absolute lattice residue
  ambiguous under global gauge shift. This closes only the symbolic auxiliary
  calculation; K2G remains open (D-0088).
- **ST-M1 pure-pose no-go:** four pose labels need not form a subgroup, but a
  fixed intrinsic three-side pattern moves only by coordinate permutation.
  Such an orbit preserves Hamming weight and cannot contain both `000` and
  the three weight-two K2H phases. N7 closes pure pose, not contextual
  docking. G6's parity core is now tied to one fixed occurring large type and
  witness tiling (D-0089).
- **ST-M1 lattice-phase no-go:** `L/2L` has the right four-element algebra but
  the bare triangular frame cannot select an absolute coset by a local
  translation-equivariant rule. Primitive `L` translations fix the frame and
  permute the cosets; integrated phases retain a global gauge. Only additional
  bounded contact geometry could anchor the phase (D-0090).
- **ST-M1 frame-pose closure:** translation equivariance removes dependence on
  an unanchored `L/2L` residue, leaving the pure orientation case already
  excluded by N7. K2H helps geometry only if one independently visible
  four-class central feature is shared by all interfaces. No such feature or
  ternary junction is known; K2G is frozen at that exact boundary (D-0091).
- **ST-M1 boundary-cocycle candidate:** K2C factors the complete K1P codebook
  on a carrier's three-corner cycle. Contextual `Z/2` corner potentials make
  base side parities exact differences, so boundary holonomy enforces even
  parity; cyclic equality enforces every remaining fresh diagonal tag. The
  two potential lifts differ by gauge flip. This survives N7--N9 symbolically
  but has no geometric vertex gadget yet (D-0092).
- **ST-M1 sector vertex lift:** one bit shared by all six incident carriers
  would wrongly force adjacent half-mode parities to match. K2V instead keeps
  six participant sectors in cyclic order; independent face integration lifts
  every K1P configuration, with at most 64 raw base sector words. This proves
  symbolic consistency, not geometric realizability (D-0093).
- **ST-M1 K2G kill decision:** K2J requires an actual bounded unmarked sector
  invariant, exact side transducer, complete six-sector contact atlas,
  frame/chirality forcing and a witness lift. Zipper/forked-corner metaphors
  supply none of these proofs and merely rename colors. K2C/K2V are retained,
  but active exact-compiler geometry is frozen until an exact gadget lemma
  meets J1--J6 (D-0094).
- **ST-M1 serialization audit:** SER0 defines the extensional `30,30,2`
  templates, rules, decoder and K1P certificate a cold checker would need.
  The primary arXiv source contains exact prose/formulas but only Illustrator
  PDFs for the construction figures, not address/SAB/vertex tables. SER1 now
  supplies the separately validated reconstruction (D-0095/D-0199).
- **ST-M1 exact source atlas:** the pinned Section 10.1 vector figure
  cold-verifies as exact `30,30,2` primitive supports with `15,15,1` SAB
  components. Each component pairs two adjacent triangles; the role census is
  `6S+6M+3L` per large template, all embeddings form one support-isometry
  orbit, and the connected common-rhombus compiler has 31 addresses. This
  closes finite SER0 transcription, not unmarked color erasure or ST-M1
  (D-0199).
- **ST-M1 exact contact kernel and compiler boundary:** the 31 addresses have
  44 internal contacts and an exact three-cycle obstruction to every binary
  domain wall. All internal contacts change diagonal axis, but no affine
  mod-three axis law contains either large template. More generally, any
  root-deterministic finite carrier is periodic, while unrestricted symbolic
  factor synthesis is domino-problem hard. The latter does not establish
  undecidability for one connected unmarked polygon (D-0201).
- **ST-M1 twelve-state source quotient:** exact signed bends of the published
  SABs lift the 31 addresses to `axis x two ordered corridor bits`; both large
  macro lifts are unique, the singleton has its reflected pair, and all
  twelve states occur. The source action has orbits `3+6+3`, proving pure pose
  insufficient and fixing the K52E endpoint-contact architecture (D-0202).
- **ST-M1 binary macro normal form:** the role-induced exact contact graph
  partitions each large macro into one regular `L` hexagon, two regular `S`
  hexagons and six `M` connectors.  Relative to its unique `L` anchor, the two
  published macros are exactly two full-isometry classes.  The addressed
  source is therefore equivalent to the twelve-state field plus one binary
  rooted exact cover, but geometric totality of that cover remains open
  (D-0203).
- **Direct Turtle-mechanism no-go:** the singleton `M` collapses under the
  published rhomb-center edge substitution, but an exhaustive exact census of
  both sixteen-edge polarity spaces finds no congruent simple support shared
  by the two large source macros. Direct one-notch hole elimination is closed;
  the active constructive burden remains the cell-level K52E/K53E compiler
  (D-0204).
- **Exact common-support kernel:** the two large macros overlap in at most
  `13/15` rhombi.  There is no one-rhombus equalizer, but four
  symmetry-equivalent two-rhombus alignments form a 17-rhombus disk.  Its role
  difference is `M+S` versus `L+S`, so the published singleton `M` tile cannot
  directly complete both decompositions.  The constructive route now targets
  the paper's own same-support interchangeable patches (D-0205).
- **Source-native contextual flips:** exact Figure 45 transcription gives
  51-rhombus `3A+6M` and 49-rhombus `2A+B+4M` same-support pairs.  Each pair is
  exchanged by a symmetry of its common support, so it carries no intrinsic
  radius-zero unmarked bit; a surrounding contact frame must root it.  Neither
  support is a translation fundamental domain (complete index-51/index-49 HNF
  tests), but other periodic tilings and global tilability remain open
  (D-0206--D-0207).
- **Explicit P17 carrier and carrier-local impossibility theorem:** ERR-017 corrects the
  role/support conflation in K54S.  The exact 17-rhombus 16-gon is a genuine
  local `large_A+2M <-> large_B+2M` compiler under the source's endpoint-
  continuation rule.  Its one-/two-copy translation gates and the induced
  51-rhombus one-/two-macro gates are negative only in those exact classes.
  The new composition-cone theorem proves that the large state alone cannot
  realize the source ratio `6(sqrt(2)-1)`: a carrier-local decoder must use
  the local all-singleton state `Z=(0,17)` with exact relative frequency
  `(6sqrt(2)-8)/17`.  The apparent all-singleton state is locally impossible:
  one three-axis hexagon would require three binary corridor bits to be
  pairwise unequal.  Area leaves no third state, so the complete
  carrier-local P17 family is refuted.  Cross-boundary decoding and different
  carriers remain outside this theorem.  The all-M quantifier is exhaustive:
  all 60 lozenge subdivisions contain the three-axis obstruction and cold-
  verify from the fixed support (D-0208--D-0211).
- **Marked geometric undecidability boundary:** for arbitrary Wang `W`, the
  product of `W` with the fixed AHI source followed by Stade's local
  Wang-to-AB-to-weave construction yields one connected polygon with finite
  edge rules.  Every valid tiling locally decodes to the AHI source, and a
  tiling exists exactly when `W` does.  This proves undecidability for the
  marked one-polygon family and gives decidable directed-graph and
  fixed-cylinder subfamilies.  It does not remove the edge rules: the audited
  geometric conversion uses a second staple polygon (D-0212).
- **Separable color-erasure classification:** independent complete-port
  profiles with exactly two participants realize precisely the finite
  compatibility relations whose bipartite graphs are disjoint unions of
  bicliques.  Stade's fixed weave rules contain a permanent forbidden
  `3-of-4` rectangle, so no polygonal profile choice in this entire family can
  erase the U2 relation.  The staple's third-party role is structurally
  necessary within this class (D-0213).
- **Physical-contact periodicity obstruction:** the old N61S forbidden
  rectangle is partly nonphysical, but the exact replacement is stronger.
  Biclique completion is the minimum two-body compatibility relation after
  physical filtering.  Five explicit all-`n` contact families still connect
  every directed Stade port after every possible input-dependent deletion,
  forcing universal profile compatibility.  The ordinary axial row partition
  then lifts to a periodic tiling with periods `(n,0)` and `(0,1)`.  Hence
  contact-complete separable erasure is impossible as an aperiodic monotile
  even when extra marked-forbidden matches are allowed (K62P/K62C/N62S,
  D-0214--D-0215).
- **Minimal source and sub-30 carrier theorem:** the irrational three-rail
  lattice hull is minimal, so a nonempty total decoder cannot select a proper
  lattice subsystem; rail-local biclique schemes necessarily add a periodic
  constant rail.  Independently, exact source frequencies restrict every
  carrier-local compiler below area 30 to areas 15--17.  A complete geometric
  superset contains 997 supports and 29,443 all-singleton subdivisions, all
  with an odd continuation cycle.  Thus the minimum carrier-local area is at
  least 30; cross-carrier and nonseparable decoders remain open
  (K63M/K63D/N63R/K64A--K64C/N64S, D-0216--D-0217).
- **Area-30 closure and all-area trade reduction:** the 65 possible
  two-large supports have 52,042 exact `G/Z` alternative subdivisions and
  zero parity survivors, closing area 30.  For arbitrary `A=15q+s`, the
  composition cone is feasible exactly when
  `s/q<6*(sqrt(2)-1)` and every viable library straddles one explicit
  large-count threshold.  Hence every carrier-local solution at any area
  contains a count-changing same-support AHI trade.  The infinite carrier
  problem is now one cut-admissible exact-cover/height-charge question, not an
  area census (K65A/K65C/N65S/K66A/K66T/K66C, D-0218--D-0219).
- **Coupled-vertex and boundary-neutral closure:** an indexed source vertex
  carries the exact pairwise-XOR code `{000,110,101,011}`.  Its incidence
  lattice admits the synchronized even defect, so no stronger additive local
  charge exists.  Globally, a changed corridor bit propagates along an
  unbounded strip; two same-support states with identical complete marked
  boundary therefore have the same corridor field and, by K67D, the same
  large-macro count.  All boundary-neutral carrier trades are closed at every
  area.  The sole carrier-local residue is boundary-active, joint multi-rail
  phase transport (K68V/N68H/K68R, D-0221).
- **Ordinary-vertex parity no-go:** the even AHI relation has full unary and
  binary projections.  At an ordinary multi-tile vertex, accepting its four
  even states makes the four sector-angle equations force every active angle
  difference to zero, so all four odd states survive too.  Fixed guards and
  nonconvexity away from the vertex do not help.  Any boundary-active compiler
  therefore needs a visible auxiliary star state, a genuine T-junction or
  fusion hyperedge, or a proved larger-radius exclusion (K69A/N69O/K69F,
  D-0222).
- **ST-M1 consolidated dossier:** theory note 14 now gives the complete
  P0/S0/Q0/K1T/K1P/N5--N9/K2C/K2V chain and conditional K2J-to-monotile
  argument in one self-contained proof draft. It makes no novelty or monotile
  claim and keeps SER0/K2J as independent blockers (D-0096).
- **ST-M1 flag-carrier reduction:** partitioning each source triangle into
  three congruent corner kites gives a colored system MLD with K2V. The K2C
  potentials and the six source-vertex sectors now belong to distinct
  physical occurrences; parity is a three-carrier cycle. This removes the
  one-rigid-carrier sector bottleneck but leaves K3G, exact unmarked
  contextual color erasure and contact completeness, open (D-0098).
- **ST-M1 inverse retiling route:** the convex flag kite's three-copy
  equilateral dissection is unique, and uniquely aligned full-side contacts
  carry no contextual state. K3R instead treats multiple exact retilings of a
  forced macrocell as symbols and states the complete R1--R5 conditional
  monotile contract. No macrocell/retiling family or polygon exists yet
  (D-0099).
- **ST-M1 binary retiling kernel:** two congruent right-isosceles carriers
  retile one square along either diagonal. Exclusive hypotenuse pairing would
  force binary macro grouping, with edge ownership and corner stars carrying
  two-dimensional constraints. No unrestricted polygonal guard or total
  binary-to-K3F decoder B0 is proved, so this is a mechanism kernel rather
  than a candidate and HC-11 admits no run (D-0100).
- **ST-M1 binary-radius boundary:** Hu--Lin prove every nonempty binary
  `2x2` corner-plaquette SFT has a periodic point, refuting the immediate
  bit-only B0. Kari--Moutot prove exact full-closure binary rectangular
  recodings of arbitrary Wang SFTs, including strongly aperiodic fixed-height
  two systems at sufficiently large width. Larger support survives
  symbolically; no geometric reader or smallest width is established
  (D-0102).
- **ST-M1/Wang retiling compiler:** the diagonal bit is only a sofic
  projection when bounded hidden docking states remain physically visible.
  In an ordinary edge-Wang realization, Jeandel--Rao force at least 11
  macrostates and four interface colors (`h>=6` modes per diagonal in the
  balanced two-retiling model). K4W proves that unique macro grouping, exact
  realization of any fixed aperiodic Wang set, full-isometry contact
  completeness and one lift suffice for one polygon to be an aperiodic
  monotile. This is a contract, not a construction (D-0103).
- **ST-M1 single-tile simulation audit:** K5C's codeword selector, four
  interface wires and all-tilings decoder architecture are already represented
  by Ollinger's five-role polyomino compiler. Demaine et al. reduce arbitrary
  square/hexagonal systems to one rotatable puzzle piece only in a prescribed
  lattice near-plane model with gaps; Greenfeld--Tao use an auxiliary finite
  group fibre. Marked, atlas and corner recodings are also established. The
  only retained research target is one connected unmarked planar polygon with
  exact gapless coverage and a total decoder on every unrestricted tiling
  (D-0108).
- **ST-M1 fixed-successor no-go:** one intrinsic head/tail fit iterates a
  fixed Euclidean isometry. Any finite component longer than two is a
  transitive rotational orbit, so it cannot equivariantly select one delimiter
  or carry a nonconstant K5C word. An order-42 keyed rosette therefore closes
  geometrically only by erasing the state asymmetry it needs (N17/D-0109).
- **ST-M1 gapless-port boundary:** every nondegenerate boundary port is
  contacted in a locally finite gapless disk tiling, so disjoint option keys
  cannot be selected by leaving the others unused (N18). One specified full
  polygonal arc pair has at most four Euclidean docking alignments (N19). A
  two-mode holonomy analogy lacks an explicit boundary, bounded-cycle theorem,
  exact eleven-word acceptance and visible state. HC-14's kill fires and K5C
  is frozen with reopening obligations R1--R5 (D-0110).
- **ST-M1 T-junction audit:** complete edge-patch/T-junction atlases and FLC
  symbolic recodings are prior art. The audited sources do not erase a
  finite state into one unrestricted congruence class. HC-15 admits only one
  fully occupied subdivision-word contact class and requires an exact local
  realization or scoped no-go by session 102, without enumeration (D-0111).
- **ST-M1 subdivision-word capacity:** `k` unequal complete neighbor sides
  partitioning one host side have exactly `k!/2` abstract order states under
  full isometry. The smallest three-occurrence split is not binary; three
  neighbors give three states and four give twelve. Every ordinary internal
  junction obeys the exact complementary-angle equation. No congruent
  polygonal realization is yet supplied (K6O/N20/J0, D-0112).
- **ST-M1 convex subdivision no-go:** complementary endpoint ports each
  consume `pi` of exterior turning, so no convex polygon with a separate host
  realizes the three- or four-neighbor universal order channel. Right-angle
  ports are closed. Nonconvex/contextual carriers remain logically open, but
  no exact witness was derived; HC-15's stop fires (N21/D-0113).
- **ST-M1 selected-word angle selector:** any two three-neighbor reversal
  classes normalize to `ABC,ACB`. J0 then forces a shared complementary
  vocabulary on every internal junction while leaving the exterior endpoint
  of `A` free. The exact orthogonal choice
  `A=(3pi/2,pi/2)`, `B=C=(pi/2,pi/2)` admits precisely those two classes and
  excludes the class with `A` in the middle. This is local feasibility only;
  no polygonal witness exists yet (K7A/D-0114).
- **ST-M1 common-collar reduction:** requiring complete neighbor stems with
  no extra participant forces the five used stem lengths in `ABC,ACB` to one
  depth `d`. Both words are automatically disjoint through that orthogonal
  collar; the entire unresolved geometry is the exact intersection of three
  rooted tails at two listed offset triples. No tail or polygon is claimed
  (K7C/D-0115).
- **ST-M1 HC-16 stop:** no exact orthogonal polygon closes both K7C rooted-tail
  packings and the host intersections. K7A/K7C are retained as an exact local
  binary contact primitive and reduction, not as a candidate. The route is
  frozen without computation; arbitrary nonconvex carriers are not refuted
  (K7W/D-0116).
- **ST-M1 unequal-stem boundary:** ERR-007 restricts K7C to the host
  footprint and puts `A`'s reflex spillover back into the tail checks; without
  a third endpoint participant the host corner is `pi/2`. N22 proves that an
  unequal first stem necessarily creates a secondary participant. HC-17
  admits exactly one cap occurrence there; no cap geometry exists yet
  (D-0117).
- **ST-M1 uniform mismatch algebra:** up to reflection, all four legal
  adjacencies expose one cap socket exactly when every used right stem is `s`
  and both used left stems are `s+Delta`. Each selected word then has two
  identical right-angle sockets with a complete cap side of length `Delta`.
  The lower finite contact cycle remains unproved (K8U/D-0118).
- **ST-M1 one-edge cap no-go:** a `pi/2+3*pi/2` lower endpoint fills the
  angle but cannot terminate a two-tile interface. With no third occurrence,
  the common boundary must continue through the vertex. Unequal next sides
  recreate N22 and equal sides transport the obligation. No finite cyclic
  cap word was derived, so HC-17 freezes without a polygon; multi-edge cycles
  are not refuted (N23/D-0119).
- **ST-M1 four-participant selector:** inserting one fixed positive guard
  sector `gamma` at each primary subdivision replaces J0 by
  `rho_X+gamma+ell_Y=pi`. The four adjacencies in `ABC,ACB` force one common
  left angle and one common right angle, while the unused `ell_A` excludes
  exactly the third reversal class. Complete guard spokes require two length
  classes rather than K7C's one. This is angle/contact algebra only; the guard
  occurrence and its remote interfaces remain unrealized (K9A/D-0120).
- **ST-M1 four-participant curvature/topology filters:** convexity forces
  `B,C` to be adjacent and leaves only `pi-alpha-2gamma` turn; a distinct
  guard corner cannot fit, so the guard vertex must be reused or the carrier
  is nonconvex. The positive guard also sends two real interfaces to
  secondary junctions and cannot be a point plug. A finite bounded guard
  topology remains the final HC-18 obligation (K9V/N24/D-0121).
- **ST-M1 bounded shield topology:** one shield occurrence can terminate both
  guard interfaces and partition the guard's complete boundary into three
  named contact arcs. Fixed poses force common terminal-angle classes, and
  the two non-reversal host words remain distinct. This closes HC-18 only as
  a finite abstract contact complex; no polygon, patch or forcing result is
  established (K9T/D-0122).
- **ST-M1 convex guard-reuse no-go:** once host, `A,B,C`, guard and shield
  roles are enumerated, the K9V escape disappears for fixed complete spokes.
  A shared guard tip swaps outgoing `b,c` lengths and forces them equal; an
  outer guard tip saturates the entire convex turn budget. Any surviving K9T
  carrier is therefore nonconvex under the retained recognition assumptions
  (N25/D-0123).
- **ST-M1 fixed nonconvex shield skeleton:** the sole retained HC-19 word is
  `d,A,d,B,d,C,d,H,d,C,d,B,d,A,d` with lengths `1,2,4,7`, a right-angle
  guard and a centrally paired shield spine. Half-turn gives exact conditional
  guard/shield docking. No coordinates or full host-word patch yet satisfy
  the simplicity, lens, recognition and disjointness obligations
  (K10B/D-0124).
- **ST-M1 half-turn role correction and HC-19 stop:** paired nonterminal
  spine vertices have angles summing to `2pi`, so the internal mirror-side
  endpoints are auxiliary contexts, not duplicate code roles. The terminal
  scope is corrected by ERR-009 below. No exact simple lens-contained spine
  or complete `ABC/ACB` placement pair was derived. K10B stays conditional
  and K10W freezes without a candidate (ERR-008/N26/D-0125).
- **ST-M1 auxiliary polarity filter:** N26 duplication is unavoidable but not
  automatically uncontrollable. At an internal straight-host subdivision,
  the host's `pi` sector and any reflex auxiliary endpoint exceed `2pi`, so
  length plus convex endpoint context recovers the intended code side. N27
  is local only; a finite full-arc synchronization criterion is the remaining
  HC-20 question (D-0126).
- **ST-M1 atomic-root synchronization:** under proved vertex alignment, a
  complete finite root cover table with one full-side mate fixes that
  neighbor's Euclidean pose. If the exact pose shares the selected full arc,
  every auxiliary side on it is controlled by the same bounded decision.
  K11S shows duplication is not intrinsically uncontrollable, but K10B's
  unique `H` still has to exclude subdivided root covers (D-0127).
- **ST-M1 terminal-scope correction and K10B root obstruction:** only
  nonterminal spine vertices have complementary `2pi` carrier angles. The
  paired terminal `A` angles fill the `pi/2` guard-lens corner, so the
  shortest-two-reflex-root shortcut is invalid. K10B's `H` is provably
  non-atomic because its language requires `[H]`, `[A,B,C]` and `[A,C,B]`.
  No other side has a complete root table; HC-20 ends without reopening
  coordinates or producing a candidate (ERR-009/N28/D-0128).
- **ST-M1 fixed-radius contextual contract:** `Star_1(H)` contains exactly
  the root and every occurrence meeting its `H` side, including point-only
  participants there. K12C requires a complete three-class local language
  for `[H]`, `[A,B,C]`, `[A,C,B]`, disjoint decoding, exact shield/host
  soundness, exclusion of every fourth class, and one lift per class. This is
  a bounded contract, not a K10B decoder (D-0129).
- **ST-M1 radius-one fourth-word obstruction:** K9A's common endpoint angles
  force `B|B` to satisfy the same primary equation as the desired
  transitions. Thus `1+2+2+2=7` gives `[A,B,B,B]`, also accepted by the
  clean-spoke and K9T terminal algebra. N29 closes every factorized
  length/sector proof; only a full-occurrence collision or joint part-count
  feature inside the fixed `H`-star could still prove K12C (D-0130).
- **ST-M1 radius-one collar survival and stop:** the `ABBB` word has an exact
  disjoint collar along `H`: all three upper-half-plane primary sectors close,
  and its independent endpoint roles are already accepted. Only overlap or
  coupling among complete occurrences away from `H` can exclude it. No such
  theorem or exact K10B polygon exists, so HC-21 closes at its fixed radius
  without escalation or a candidate (N30/D-0131).
- **ST-M1 weighted-language criterion:** a finite transition graph with exact
  positive role lengths has no accepted host word longer than
  `floor(h/min w)`. K13W makes equality with a desired language a finite exact
  path-weight test and requires the transition closure forced by the selected
  words. It is an arithmetic design filter, not geometry or a novelty claim
  (D-0132).
- **ST-M1 exact K9A arithmetic characterization:** the forced transition
  closure is `{A,B,C} x {B,C}`. Exactly `ABC,ACB` have host weight iff
  `b+c` has only its mixed representation and `a+b+c` lies outside
  `<b,c>`. K13A is necessary and sufficient. It explains `ABBB` for
  `(1,2,4)` and the separate `BBB/CC` failure for `(1,2,3)` (D-0133).
- **ST-M1 infinite arithmetic repair family:** for every `n>=4`, weights
  `(a,b,c,h)=(1,n,n+2,2n+3)` satisfy K13A and accept exactly `ABC,ACB` among
  code-only covers. With cover-side alignment and `d=3n>h`, the full-side
  arithmetic language adds only `[H]`. K13F is a symbolic design theorem;
  it supplies no polygon, local-completeness result or candidate (D-0134).
- **ST-M1 fixed K13F geometry admission:** for `(1,4,6,11;d=12)`, every
  `A,B,C,d` full-side coefficient table is now explicit and the corrected
  intended/auxiliary endpoint contexts are re-audited. The half-turn guard
  lens is an exact square of side `d`; its first `A,d` spine edges turn by
  `3pi/4`. K14R is an admission reduction, not a polygon (D-0135).
- **Primary-source polykite baseline and enforced novelty gate:** the positive
  unequal `Tile(a,b)` continuum is completely classified; it contains
  infinitely many polykites; the three degenerate similarity classes are
  periodic; `Tile(1,1)` is only weakly chiral aperiodic; and suitable edge
  modifications give families of strict Spectres. The finite search report is
  `n≤24`. Code now distinguishes an unregistered key from a discovery-eligible
  shape and blocks all promotions until the full family audit passes.
- Exact integer-arithmetic kite substrate (Laves [3.4.6.4]); A0 enumeration
  matches OEIS A057786 exactly n=1..16. The Rust production enumerator reaches
  19,035,075 free n=16 polykites in 364.48 s / 1.35 GiB and emits a compact
  fixed-width stream; Python remains the reference implementation.
- **A1 torus periodicity test** with machine-verified certificates
  (`src/einstein/funnel/a1_torus.py`): exact cover of quotient tori over all
  center-sublattices (HNF) up to index budget. Verdicts are three-valued:
  `periodic` (certificate), `no-periodic-at-budget`, `unknown-budget-exhausted`.
  The compiled streaming port reproduces the n=8 Myers split and screens
  n=9..16 with 60,477 independently re-verified positive certificates.
  At n=16, 29 are periodic at k≤12 and 19,035,046 survive; zero searches
  exhaust the node budget.
- **Shape database** (`src/einstein/db.py`, `data/shapes.sqlite`): 1,264
  shapes (all free polykites n≤8), one A1 verdict each, with budget + code
  version stamps. Batch runner `scripts/run_a1.py` is resumable.
- **A1 validated against Myers' independent census** (same grid-aligned
  scope): periodic-capable counts n=1..8 = 1, 1, 4, 5, 1, 71, 55, 39 —
  exact match at every n; the hat correctly survives as
  `no-periodic-at-budget`. Regression: `tests/test_a1_vs_myers.py`.
- **A2 corona/Heesch engine** (`src/einstein/funnel/a2_heesch.py`): full
  exact H_c census n≤8; the hat is the unique unbounded-corona anomaly
  (session 03).
- **A3 large-patch construction** (`src/einstein/funnel/a3_patch.py`):
  disk exact-cover; SAT (CaDiCaL) workhorse + pure-Python greedy for the
  growth-profile feature (D-0009). All certificates re-verified by our own
  exact code. Hat patches to 22,940 tiles (r2=100000, 551 s); reflected-hat
  density converges to the literature value 1/(1+φ⁴) — an external anchor
  A3 was never told about. Six H_c=2 shapes get pose-free disk-cover
  refutations at r2≤200. Periodic control patch (shape 392) stored for A4.
- **Compiled A2 first-corona filter:** exact vertex-ring cover plus hole-free
  exhaustion reproduces n=8 (720 H_c=0, 114 witnessed) and screens the actual
  n=9..16 corpus. At n=16 it proves 19,012,171 shapes H_c=0 and retains 22,875
  witnessed shapes. Across n=9..16 only 40,216 survive, every one with an
  independently verified corona; five initial budget cases all resolve under
  targeted escalation.
- **Compiled A2 recursive depth:** exact search enumerates all corona choices,
  not only one stored witness. The 40,216 first-corona survivors reduce to
  9,841 witnessed depth-2 shapes with no unknowns after escalation. On the
  complete n=8 universe, depth 3 leaves exactly one independently verified
  survivor—and its canonical form is the hat. This is the first direct blind
  rediscovery result.
- **Blind local-growth survivors:** depth 3 over n=9..16 yields 9,728
  independently verified chains, 105 exact H_c=2 shapes and eight conservative
  unknowns. The smallest complete witnessed sets—two n=10 and eight n=12
  shapes—are rendered in `a2-depth3-small-candidates.svg`. These are local
  growth candidates only; known-shape classification is mandatory before
  novelty promotion. In the smallest gallery, n=10 candidate 2 is the Turtle.
- **Blind Turtle rediscovery (formerly “new-shape finalist”):** the complete
  smallest-survivor batch passed A3/A4 and an extended exact A1 audit. One n=10 shape
  is disk-refuted; all eight n=12 shapes are exact periodic tilers at torus
  index 16. The remaining n=10 candidate 2 has no torus certificate through
  index 215 (plus several larger spot refutations), covers an independently
  verified r²=50,000 disk with 9,239
  tiles, and retains a rank-4, sixfold diffraction signature after patch
  enlargement. These independently reproduce expected Turtle behavior; the
  published Turtle proofs, not these finite tests, establish aperiodicity.
- **Turtle robustness audit (legacy finalist assets):** the apparent crown gaps are outside A3's
  certified disk (zero missing cells inside). Four independently phase-biased
  r²=12,800 patches share at most 6.7% exact placements but all retain
  estimated rank≥4 at 1024² and 2048². The first large patch contains one
  exact period-47 stripe domain; it does not recur as an exact period across
  the independent patches. Symmetry votes vary at small size/resolution, so
  the robust signal is rank≥4, not universally sixfold symmetry (D-0025).
- **A3 crown correction:** the preceding gap audit addressed coverage, not
  continuability. All five complete r²=12,800 crowns are exact dead ends.
  After measured collar rewrites, however, a literal nested chain preserves
  growing cores r²=9,000 then r²=30,000 inside outer patches r²=50,000 and
  r²=100,000 (18,386 tiles). Candidate status now rests on nested core growth,
  with collar depth reported explicitly; independent disk covers alone no
  longer count as growth evidence (ERR-002, D-0026).
- **A4 diffraction fingerprint v0**
  (`src/einstein/funnel/a4_diffraction.py`): per-orientation Hann-windowed
  FFT powers on a shared grid, null-calibrated peak detection, sidelobe
  exclusion, bounded-integer module indexing, rotational-symmetry vote and
  crystal/quasicrystal-candidate/diffuse prioritization verdicts. Both stored
  hat patch sizes (11,514 and 22,940 anchors) recover rank 4 and symmetry 6;
  patch doubling calibrates the free coefficient bound at 8 (D-0018).
- **Vendored spectre reference generator** (`vendor/spectre/`) with an exact
  rank-4 anchor dump and independent Python module projection
  (`substrate/module12.py`). Its N=3 Delta output agrees three ways: upstream
  float leaves, Rust exact traversal and our projection; recurrence and
  chirality pins are tested.
- **E4 full calibration gate passed:** the phase-1 random/periodic/hat/spectre
  core is joined by canonical Penrose and Ammann–Beenker cut-and-project
  patches, Taylor–Socolar dyadic hierarchy, and genuine boundary-grown random
  square–triangle tilings. Known ranks/symmetries are recovered; ranks survive
  patch doubling and invertible rotations/shears; 10,000 randomized periodic
  tilers produce zero confirmed quasicrystal false positives. The
  square–triangle ensemble retains broad twelvefold order but is separated
  from pure-point references by background-subtracted narrow-peak mass.
- Wider artifacts: `scripts/run_e4_wide.py`,
  `docs/notebook/assets/e4-wide-results.json`, and
  `e4-spectrum-{penrose,ammann-beenker,taylor-socolar,square-triangle-random}.png`.
- **A6 hierarchy miner v0** (`src/einstein/funnel/a6_hierarchy.py`) uses
  exact rank-4 pose arithmetic and exact tile-edge adjacency. On pose-only
  Spectre patches it discovers a repeated 9-tile scaffold plus an 8-tile
  one-child exception. The selected rule uniquely covers all nine level-3
  root patches and recovers every withheld immediate parent in Delta levels
  1–4: 1/1, 8/8, 63/63 and 496/496. Physical counts
  9, 71, 559, 4,401 yield `T[n+1] = 8T[n] - T[n-1]` and dominant root
  `4 + sqrt(15)`. Artifact: `a6-spectre-results.json`; runner:
  `scripts/run_a6_spectre.py`.
- **A6 v1 recursive closure:** consecutive level-4/5 pose-only patches are
  contracted by exact scale-specific 8/7 rules. Colored physical-boundary
  adjacency graphs at equal abstract size become discrete after exact joint
  refinement, allowing partitions to transfer across scales. The level-4
  hierarchy closes `496 → 63 → 8 → 1`; every recovered cluster matches
  withheld ancestry at every depth. One exact oriented adjacency collar gives
  17 interior states that are 100% pure against all nine withheld labels
  (3,109 nodes), and all 17 states have one deterministic ordered child rule
  across 310 fully collared parents.
- **A6 v2 forcing gate:** the v1 parent and child collar numbers were found to
  be independently named rather than one stationary alphabet. Exact graph
  alignment now produces a closed, strongly connected 17-state substitution
  on normalized states `0..16`. Both locally exact physical phases enter the
  wider gate; only one closes recursively (`496→63→8→1`). Radius-1 physical
  collars stabilize at 32 states and 19 legal parent patterns: among 11,715
  occurrences from both phases, exactly the selected 3,905 groups remain
  legal. CaDiCaL proves all 19 physical patterns and all 17 metatile-state
  cases uniquely composable. Hidden ancestry and labels are still opened only
  after discovery and agree exactly.
- **W3 ancestry-blind physical language:** exact straight-`Tile(1,1)`
  geometry produces all 166 fixed-chirality edge-to-edge first coronas.
  Exact SAT ring completion contracts the existential central-corona prefix
  `166→30→21`; the generated level-3/4 controls contain 18 stable types.
  The three extras `[33,44,155]` all have radius-four witnesses. None of the
  21 radius-three survivors has unique isolated parent ownership
  (`2:17,3:3,5:1`), while all eight superficially unique radius-one types die
  at radius two. C5 became partial rather than proved; this result supplies
  the input language for the coordinated experiment below.
- **W3 coordinated parent-overlap language:** physical ring variables and
  recovered 9/8-parent variables now share one exact SAT problem on a
  universally buffered core. All 18 generated corona controls group. The
  extras exhaust as `33: 2→200→0`, `44: 27→0`, and `155: 60→24→0`, so the
  conditional finite language equals those 18 controls. Empty-buffer branches
  are expanded physically, never called UNSAT. The result assumes the parent
  language; it does not prove all physical tilings have a parent partition or
  that the partition is unique and iterable.
- **W3 L18 physical-to-parent transducer:** the 18-type language has 87
  radius-two and 418 radius-three rooted cases. Exhaustive grouping gives one
  parent-anchor map in every case; 48 raw 8/9 ambiguities retain the same
  anchor. Among all 15,216 radius-six survivors, the complete canonical eight
  children map to that anchor, proving the unique full/missing partition for
  every whole-plane L18 tiling. Contraction is not closed: non-generated
  complete parent coronas have frontiers `6280→1796→4482` at radii 7–9.
  Further blind rings are replaced by a contracted parent/interface graph.
- **W3 contracted-interface no-go:** the frontier compresses to nine extra
  uncolored parent coronas beside the 17 generated states. Exact reciprocal
  edge and triangle-overlap CSPs leave all 26 states alive; fixed-point support
  pruning removes none. Parent type and physical interface color are therefore
  necessary state, not optional detail.
- **W3 one-sided colored-interface no-go:** all 57,589 resolved radius-seven
  extensions collapse to 17 generated and five extra states after retaining
  the center full/missing type and exact oriented child-edge contacts. The
  generated set exactly matches the independent substitution control, but all
  22 states survive colored star pruning and form one closed SCC. The next
  finite alphabet must buffer the neighbor component types as well.
- **W3 two-sided defect frontier:** exhaustive continuation gives
  `6280→1796→4482`; every radius-nine interface has all six endpoint types
  physically buffered. The branches collapse to three new full-component
  states, and all three survive beside the 17 controls in one SCC. Their exact
  minimum extra-neighbor costs are `[1,0,1]`: one state is locally absorbable,
  while the other two require an extra neighbor and minimally point to each
  other. The next proof object is a pinned radius-two defect CSP.
- **W3 pinned radius-two defect propagation:** only one of each defect's
  `28,100,3` colored root stars survives exact pair agreement and physical
  8/9-child support nonoverlap. The three surviving problems have
  `960,432,840` complete assignments, but all 131 are UNSAT with a
  generated-only second ring. The forced type map is `A→C, B→C, C→A`, so the
  apparently absorbable defect enters the alternating `A/C` pair. This is a
  finite propagation theorem, not yet contraction closure or a plane-tiling
  counterexample.
- **W3 radius-three conditional closure:** all `960+432+840=2,232`
  radius-two assignments were extended with exact colored pair and physical
  support constraints. The three roots have `0,2,1` survivors. The dead root
  `288…` cannot occur in a whole-plane 20-state configuration, and every
  survivor of either other root contains `288…` in its fixed inner patch.
  Hence all extras are eliminated and contraction closes to the 17 generated
  states inside L18. Entry of every geometric Spectre tiling into L18 remains
  the recognisability blocker.
- **E1 hat A6 screen:** A3 kite-grid placements now map exactly into module12,
  with candidate boundaries derived from their polykite cells. Disk cuts use
  an exact core-plus-halo SAT cover. On the 11,514-hat patch, 160 blind 8/7
  rules yield one full scaffold with two allowed exception positions. The
  ownership cover is non-unique (at least 20 solutions), but every sampled
  cover gives the same parent-anchor lattice and SAT forces all 141 safe-core
  anchors across every cover. Separate r2=50,000 and r2=100,000 SAT patches
  initially produced different patch-specific minimum libraries. A shared
  MaxSAT fit now requires 16 arity-7 patterns and forces both 430-parent cores
  to 71 and 72 groups respectively, with zero optional groups. The normalized
  16-state contractions admit one shared 15-pattern next-scale library
  (six arity 7, nine arity 8), forcing 43→8 and 41→8 with zero alternatives.
  Artifact:
  `a6-hat-screen-results.json`; inspection drawings:
  `a6-hat-candidate-{1,2}.svg`; runner: `scripts/run_a6_hat.py`.
- **Theory dossier v0.2 adopted:** `docs/theory/` now separates roadmap,
  theorem text, stable-ID proof status, experiment evidence and monograph
  structure. The dossier's historical “finalist” identifier now means the
  Turtle control (D-0048). T0.1 gives a proof draft that singly periodic grid-aligned
  tilability implies doubly periodic tilability; W1's auditable transfer
  certificate contract is specified. No new-tile verdict is claimed.
- **W1.a exact reference implementation:** the new cylinder engine enumerates
  all whole-tile crossing-state unions, searches the entire graph, and converts
  cycles to independently verified A1 certificates. Eight unit controls pass,
  including a four-kite example that has period (2,0) but not (1,0), preventing
  primitive-only vector collapse. The archived phase-0 matrix adds 28 n≤3
  census/vector cases and 102 independent bounded-torus checks: 25 verified
  cycles, four cycle-free hat vectors, zero disagreements/exhaustions. Those
  phase-0 graph hashes motivated the complete certificate gate below.
- **W1 negative gate and first Turtle-control theorem:** cycle-free results now carry
  complete graph manifests checked by a separate geometry/state/transition
  verifier. Five negative controls pass tamper-resistant verification. For the
  Turtle, 11 D6 representatives cover every one of the 90 nonzero vectors
  with Q(v)≤25, including nonprimitive vectors; all are independently verified
  cycle-free with zero exhaustions. Thus T1.2-25 exactly excludes every such
  grid-aligned period. Larger vectors and unconditional geometry remain open.
- **W1 exact extension through Q=36:** four incremental shell certificates
  cover 36 more vectors, with complete graphs up to 159,860 states. Combined
  with T1.2-25, all 126 nonzero vectors in 15 D6 orbits through Q=36 are
  independently verified cycle-free. The 51 MB shell artifact makes proof-size
  scaling explicit; it contains zero resource exhaustions.
- **W2 Layer A and B audit:** exact area and prime-sector coloring witnesses
  have zero false exclusions on all 60,477 materialized periodic certificates.
  For the Turtle, sector coloring adds nothing beyond k≡0 mod 5. The proposed
  isolated nontrivial-character Layer B is mathematically vacuous because its
  projected target is zero; T2.B0 retires it and redirects W2 to integer SNF.
- **W2.C modular cokernel:** quotient-wide GF(2) witnesses pass all 60,477
  periodic controls with zero false exclusions and kill 36/742 area-admissible
  Turtle HNFs through index 60. A closed odd-weight support annihilates both
  thin placement profiles for HNF (1,0,k), producing proof draft T2.C1 for all
  k≥4—W2's first infinite quotient-family exclusion.
- **W2.C exact integer normal forms:** pinned FLINT 0.9.0 and SymPy 1.14.0
  independently agree on Smith controls; canonical FLINT row-HNF completes all
  742 Turtle quotients through index 60. It finds exactly the same 36 rank
  obstructions as GF(2), 706 unrestricted integer solutions, and zero
  torsion-index obstructions. Thus the bare integer relaxation is exhausted at
  this horizon; integer compatibility is not a 0/1 cover.
- **W2.C nonnegative rational no-go:** translation averaging reduces the full
  incidence LP exactly to a six-sector cone. Exact compact witnesses verify
  that all 706 integer-compatible Turtle quotients through index 60 are also
  nonnegative-rational compatible; the same 36 rank cases are obstructed.
  Ordinary positivity therefore adds zero kills. Binary exact-cover structure
  or nonabelian holonomy is the remaining algebraic target.
- **W2.C binary quotient families:** T1.2-36 composes with exact HNF vector
  membership into 126 infinite congruence families. They exclude every HNF
  through index 36 and 2,941/8,864 Turtle area-admissible HNFs through index
  215. Exact D6 maps promote the thin proof to all three families `(1,0,k)`,
  `(k,0,1)`, `(k,k-1,1)` for every k≥4. Missing family membership is unknown.
- **W2 prior-art disposition:** additive incidence/cokernel witnesses are
  classical generalized coloring/tile homology, including on finite tori.
  The explicit Turtle thin support was not found in the audited Turtle papers,
  but is only a small corollary of published aperiodicity. W2 is frozen as a
  control branch (D-0067), not a method- or Turtle-novelty claim.
- **W2.D phase 0:** an exact p3 Cayley model reproduces Conway--Lagarias'
  three-in-line boundary invariant. The Turtle has 2,556 S3 boundary-group
  surjections, but exhaustive zero-displacement analysis yields no commuting-
  coset obstruction: 2,322 kernels have order 6 and 234 have order 3. A sound
  torus certificate must couple group potentials to the selected binary tile-
  boundary network; no Layer-D Turtle quotient is yet excluded at this phase.
- **W2.D binary-coupled result:** the at-least-cover/S3-potential CSP passes
  one-kite and nontrivial shape-392 periodic controls. The 234 strong Turtle
  surjections reduce to 39 inner-conjugacy classes. Exhaustive class search
  kills all three W1-family survivors at index 40—`(10,3,4)`, `(40,11,1)`,
  `(40,28,1)`—with six killing classes each, while their placement-only
  relaxations are SAT. All 54 selected map/twist core CNFs and DRAT proofs
  replay under independent `drat-trim`; together with area and T2.C4-36 this
  excludes every HNF through index 40. The later bullets extend this finite
  prefix; O1 remains open.
- **W2.D index-45 extension:** all 39 strong S3 quotient classes are classified
  on the nine W1-surviving HNFs. Nine effective maps form three exact
  same-signature triples; every HNF is killed by at least six maps. One
  deterministic map per HNF supplies 162/162 independently replayed DRAT
  cores (377,474,096 compressed bytes). The shell splits 69 W1-family plus 9
  Layer-D exclusions, closing every grid-aligned quotient through index 45.
  Exact diagonal D6 covariance explains the triple pattern: 4,212/4,212
  transformed matrix entries agree. It is not an infinite-family theorem and
  O1 stays open.
- **W2.D index-50 complementary closure:** S3 excludes one six-HNF orbit, then
  an exact small-group census selects A4 with V4 displacement kernel and
  residual C3 information. On the 12 S3 survivors, 48 strong A4 classes reduce
  to 48 diagonal pair orbits: 16 are obstructed and cover every HNF, while
  32/32 relaxed SAT witnesses verify clausewise. Fixing map 7 yields 576/576
  cold-replayed DRAT cores (2,166,298,658 compressed bytes). The complete shell
  splits 75 W1 + 6 S3 + 12 A4, closing the certified quotient prefix through
  50. The shared killer signature is three distinct V4 values on the final
  three generators; this is finite evidence for a symbolic family theorem,
  not O1.
- **Interrupted overnight Turtle campaign recovered (legacy finalist logs):** checksummed parsing of
  the append-only logs records 9,099 completed generic HNF quotient executions
  plus 36 targeted executions, all reporting exact UNSAT, with zero periodic
  certificates. The count includes deliberate reruns; jobs lacking completion
  lines remain unknown. The completed blind hierarchy
  screen retained two non-unique first-composition rules out of 22,094 but no
  stationary recognizable recursion. Artifact: `e1-overnight-recovered.json`.
- Test suite: **222 fast passed** (17 deselected, 145.53 s, session 108);
  **17 slow passed** previously (192 deselected, 389.36 s).
  Vendored Rust: **5 passed**.

## Funnel state (polykites, grid-aligned scope — D-0006)

| n | shapes | A1: periodic | A2: H=0 | H=1 | H=2 | grows (anomaly) |
|---|---|---|---|---|---|---|
| 1–3 | 7 | 6 | 1 | — | — | — |
| 4 | 10 | 5 | 4 | 1 | — | — |
| 5 | 27 | 1 | 12 | 14 | — | — |
| 6 | 85 | 71 | 13 | 1 | — | — |
| 7 | 262 | 55 | 165 | 41 | 1 | — |
| 8 | 873 | 39 | 720 | 108 | 5 | **1 — the hat** |

All H values exact by exhaustion (D-0008). **The hat is the unique
unbounded-corona anomaly among all 1,264 free polykites n ≤ 8** — a
mini-E1 positive-control result: Heesch depth alone ranks it #1 in its size
class. This is not a new census. Kaplan's public 2023 eight-kite artifact has
exactly the same 108 `H_c=1` and five `H_c=2` counts; its three inconclusive
cases are the two periodic anisohedral shapes removed by A1 and the Hat.
Our structurally independent A2 engine therefore supplies an exact 116/116
per-shape reproduction and cold-verifiable benchmark; session 58 maps the two
periodic-anisohedral controls to IDs 506/793 and the Hat to ID 635. See ERR-005 and
`docs/literature/reviews/KAPLAN_HEESCH_POLYKITES.md`. A3 sharpens the
internal ranking: all six `H_c=2` shapes are pose-free refuted on disks of
`r2<=200` (19–35 tiles max), while the Hat covers `r2=100000` (22,940 tiles);
that separation is finite benchmark evidence, not a novelty claim.

## Known capacity limits (honest)

- Compiled A0 reaches E1 n=16, but its 19,035,075 records still require
  A3/A4 ranking. Depth 3 still leaves 9,728 witnessed n=9..16 shapes because
  raw depth is strongly size-dependent, especially at n=13 and n=16. The
  first complete ten-shape promotion blindly rediscovered the Turtle, but
  9,718 witnessed shapes plus eight unknowns remain outside A3. Within-size
  ranking and batched large-patch/diffraction evidence are now mandatory.
  The next complete *validation/corpus* batch would be all 29 n=14/n=15
  depth-3 witnesses; the much larger n=13 and n=16 sets follow after its
  measured yield. None can be a new aperiodic polykite under the published
  `n≤24` classification. Frozen E2 is invalidated rather than awaiting a
  wider key.
- A1 torus budget k ≤ 12 proven sufficient for n ≤ 8 only (by Myers
  agreement); larger n may need larger tori — revalidate per horizon.
- A3 single-shot SAT: demonstrated at 22,940 tiles in 551 s, but an
  independently covered disk is not continuation evidence. Required-placement
  nested cores now provide the sound growth feature; optimizing retained-core
  radius across many scales still needs an incremental encoder
  (assumption-based collar growth) or compiled encoding.
- A3 greedy engine (growth profile): useful to ~10² tiles on hard shapes.
- Funnel v0 sees grid-aligned tilings only (D-0006) — sound positives,
  incomplete negatives; matches the external census scope.
- A4's module indexer remains a bounded greedy numerical estimator rather
  than a general LLL/PSLQ solver (D-0011). E4 supports it for the current
  prioritization role: every known finite-rank reference is correct under
  patch doubling and affine transforms, and the two-resolution periodic
  control gives 0/10,000 confirmed false positives. It is not a proof tool.
- The narrow-peak mass used to distinguish random square–triangle order is
  grid/extent dependent and may only be compared at the shared E4 calibration
  settings. A4 verdicts remain prioritization signals, never spectral-type
  certificates.
- The Spectre source is user-owned and was explicitly supplied for integration
  here. It has no separate license declaration; that matters only if explicit
  third-party reuse terms are wanted later, not for work in this repository.
- A6's current forcing certificate is verified finite computation over the
  recovered physical/collared languages, not a Lean theorem about arbitrary
  infinite tilings. The artifact contains the complete case counts and SAT
  results; a Lean wrapper is deferred to E10.
- Exact graph refinement becomes discrete on the calibrated Spectre patches;
  a general graph-isomorphism backtracker is not implemented. A future
  candidate whose refinement remains ambiguous must fail honestly or trigger
  that escalation.
- The traditional two-tile Gamma/Mystic fusion is not recovered uniquely, but
  the closed 9/8 hierarchy and its local forcing certificate do not require
  it. Recovering that named reference motif is optional validation archaeology.
- Hat A6 has a forced first parent-anchor lattice, but the next level is not a
  single Spectre-style full/deletion rule. Nearest 7/8 grouping cannot be made
  a deterministic function of geometry-only collars through radius 4; the
  recursive solver instead uses cover-invariant option states. Patch-specific
  minimum rulebooks do not transfer: the old 15-pattern library is globally
  UNSAT on the doubled patch, while its naive 17-pattern union introduces
  optional compositions. Joint fitting across both patches repairs this with
  forced shared libraries closing `430→71/72` and `43/41→8`. Eight terminal
  nodes are still too few to claim another independently replicated scale,
  and physical-hat ownership remains non-unique.

## Next actions (in order)

Research is under the 2026-07-21 reset recorded in
`docs/literature/RESEARCH_RETURN_AUDIT.md`.

The controlling 2026-07-28 target supersedes the chronological archive below:

1. Treat N64S/N65S/N68H as completed carrier-local base cases: no synthesis
   through area 30, no boundary-neutral count-changing state at any area, and
   no return to P17 or an integer-by-integer carrier census.
2. Classify the minimal non-ordinary joint interface: a host boundary arc
   partitioned by congruent neighbors or an equivalent carrier--verifier
   fusion.  Decide its full local-closure relation and whether it realizes
   the AHI even-parity hyperedge without odd words or periodic faults.
   Ordinary sector vertices are closed by N69O; local additive charges are
   exhausted by K68V.
3. In parallel, formalize the cross-carrier alternative: bound how a fixed
   source macro can intersect neighboring carriers and state the finite local
   data required for a total decoder.  This is the only way to escape the
   carrier-trade frontier without inventing an unrelated gadget.
4. Use K63D/K63E to reject source-pruning proposals unless they identify an
   explicit joint multi-rail fiber component and prove it covers the whole
   minimal lattice hull.  Rail-local or boundary-neutral entropy choices are
   closed.
5. U2 licenses no unmarked claim.  Any nonseparable self-stapling route must
   give a total all-tilings decoder and hit the periodicity gate immediately.

The remaining numbered material is retained as the historical decision log.

1. The T2.C1/T2.C5 audit is **closed**: the method class is classical tile
   homology and the explicit Turtle formula is retained only as a worked
   control. W2 escalation is frozen.
2. The E1 benchmark assessment is **closed no-go** for new ablations. Package
   the exact reproduction fixtures and postmortem during release work only.
3. Human checkpoint `HC-2026-07-21-06` is closed after sessions 73--75. The
   user explicitly authorized `HC-2026-07-21-07` after independent review.
   Sessions 76--78 exhaust HC-07. The user authorized HC-08 for the bounded
   pose-action question; session 79 proves N7 and closes pure intrinsic pose.
   Sessions 79--81 exhaust HC-08. The user authorized HC-09 with a three-
   session kill condition; session 82 derives the surviving K2C boundary-
   cocycle candidate and its sector-separated vertex lift; session 84 applies
   the kill condition because no unmarked gadget meets K2J. HC-09 is exhausted
   with no experiment or large artifact. HC-10 is authorized for
   consolidation; session 85 defines SER0 and records the primary-source data
   blocker; session 86 consolidates the full symbolic chain; session 87 audits
   and integrates it. HC-10 is exhausted at 3 of 3 sessions with no experiment
   or generated artifact.
4. Keep all polykite discovery work through `n=24`, all Turtle quotient-shell
   escalation, and all Spectre radius escalation frozen.
5. HC-11 is exhausted after sessions 88--90. K3G is frozen. Before geometry,
   audit B0 against primary work on binary square-plaquette SFTs and binary
   higher-block simulation. Only if B0 survives may a new checkpoint consider
   a fixed-`N` boundary-word synthesis with an explicit contact-completeness
   certificate.
6. The user authorized HC-12 for that audit. Session 91 establishes that K3F
   is the exact primitive repository kite up to scale and fixes the controlling
   distinction between rule support, decoder radius and geometric visibility.
   No enumeration or shape run is admitted. Session 92 refutes bit-only
   `2x2` B0 by Hu--Lin and retains only a larger-support/hidden-state route by
   Kari--Moutot. Session 93 translates the boundary into K4W and stops. HC-12
   is exhausted. The bit-only guard route is closed; K4W remains frozen until
   a new checkpoint authorizes an on-paper 11-retiling topology attempt with
   the recorded kill condition.
7. The user authorized HC-13 after independent review. Session 94 repairs the
   Hu--Lin cache and Kari--Moutot exponent transcription, then constructs the
   exact 12-state `2 x 16` synchronizing-domino topology K5S. Its six-bar
   marker gives conditional unique finite-radius grouping. Session 95 proves
   that its one raw ownership channel is periodic (N14), while four
   independent binary quadrant flips merely reproduce Hu--Lin's refuted
   corner SFT (N15). K5Q retains a six-mode corner-socket topology, but no
   central exact-cover selector or unmarked guard exists. Session 96 proves
   independent sockets periodic (N16) and replaces them with K5C: one rooted
   closed corridor whose 11 exact length-42 words couple all four source
   interfaces through a finite selector automaton. HC-13 is exhausted. K5C is
   a compiler topology, not a polygon; a future checkpoint requires prior-art
   review and one concrete geometric mechanism for bounded cycles, visible
   automaton modes and contact completeness before any run.
8. The user authorized HC-14 with Greenfeld--Tao, Ollinger, Ammann A2,
   Socolar--Taylor and the exact `44/6` corner source as mandatory prior-art
   targets. Session 97 completes that audit and adds the closer Demaine
   one-puzzle-piece, Fletcher atlas and Mampusti--Whittaker dendrite controls.
   The symbolic compiler is prior art. Session 98 tests and refutes the
   fixed-successor order-42 rosette: transitive rotational symmetry forbids a
   unique delimiter or nonconstant word. Session 99 proves the gapless
   boundary-coverage and full-arc alignment bounds N18--N19. No multiplexed
   boundary meets K5C.1--K5C.3, so the predeclared kill fires. HC-14 is
   exhausted at 3 of 3 sessions with no experiment or generated research
   artifact; K5C is frozen until an explicit boundary satisfies R1--R5 before
   computation.
9. The `Tile(a,b)` recognizer remains required infrastructure before any
   future polykite novelty promotion, but is not itself the next research
   result.
10. The user authorized HC-15. Session 100 completed the mandatory
    T-junction/non-edge-to-edge prior-art audit. Session 101 proved the exact
    `k!/2` order capacity, the two-neighbor reflection no-go and the endpoint
    angle equation. Session 102 proves the convex complementary-port no-go
    N21. HC-15 is exhausted at 3 of 3 sessions; no exact nonconvex witness,
    run, SVG or shape promotion exists. A new checkpoint is required.
11. The user authorized HC-16. Session 103 fixed the escape route before
    geometry and proved K7A, an exact two-of-three orthogonal angle selector.
    Session 104 proves the common clean-collar reduction K7C. Session 105 may
    only close the two exact rooted-tail packings with hand-verifiable
    coordinates. No coordinate set closes them, so session 105 fires the
    predeclared stop. HC-16 is exhausted at 3 of 3 sessions; the route is
    frozen without computation and a new checkpoint is required.
12. The user authorized HC-17 after review. Session 106 applies ERR-007,
    removes the zero-byte Conway--Lagarias fetch remnant and proves N22.
    Session 107 proves the uniform mismatch classification K8U. Session 108
    may only close the cap's lower endpoint by a finite exact contact cycle.
    N23 proves the one-edge cap merely transports the mismatch; no finite
    cycle is derived. HC-17 is exhausted at 3 of 3 sessions and freezes
    without coordinates or computation.
13. The user authorized HC-18 after review. Session 109 removes all verified
    zero-byte PDF remnants, classifies three legitimate empty compiled
    streams, and proves the K9A four-sector selector. Session 110 proves the
    K9V convex curvature dichotomy and N24 point-plug no-go. Session 111 gives
    the bounded K9T guard-and-shield topology. HC-18 is exhausted at 3 of 3
    sessions with no experiment or generated artifact. Exact geometry needs
    a new checkpoint and predeclared intrinsic role identifications.
14. The user authorized HC-19 after review. Session 112 enumerates all six
    occurrence roles and proves N25, closing the complete convex fixed-spoke
    branch. Session 113 fixes the sole nonconvex 15-edge K10B word and
    half-turn shield isometry. Session 114 corrects its paired-role claim by
    ERR-008/N26 and fails to derive a coordinate list satisfying the lens and
    both full host patches. HC-19 is exhausted at 3 of 3 sessions and freezes
    without computation or a candidate.
15. The user authorized HC-20 after review. Before research, session 115
    corrects theory note 25's stale same-role sentence and proves N27: angle
    polarity excludes every reflex auxiliary side from an internal straight-
    host subdivision. This repairs local decoding only. Sessions 116--117
    must derive a finite auxiliary-arc synchronization criterion, test K10B,
    and either meet K10W's existing exact reopening rule or retain the freeze.
    Session 116 proves K11S: a complete finite one-word root cover fixes the
    congruent mate pose and synchronizes the whole selected arc. Session 117
    applies this criterion to K10B. ERR-009 first corrects N26 at the terminal
    `A` endpoints. N28 then proves the unique `H` is non-atomic because the
    same language requires full shield and two subdivided host covers. No
    other atomic root is proved, so HC-20 is exhausted and K10W stays frozen.
16. The user authorized HC-21 after review with radius fixed in advance.
    Session 118 defines radius one as the closed `H`-star and K12C as a total
    three-class certificate on its full local closure. Sessions 119--120 may
    only derive the cover language from existing exact length/sector algebra.
    A surviving fourth word closes radius one; context escalation is forbidden.
    Session 119 derives N29: the fixed K9A equations force `B|B`, so
    `[A,B,B,B]` satisfies every factorized length, primary, spoke and terminal
    constraint. Session 120 may only seek an already-available non-factorized
    geometric exclusion inside `Star_1(H)` before applying the stop. Session
    120 proves N30, an exact disjoint boundary collar for `ABBB`; no theorem
    controls the complete occurrences away from `H`. HC-21 is exhausted,
    K12C freezes at radius one, and no larger context is opened.
17. The user authorized HC-22 after review. Session 121 treats side lengths
    and the forced transition language jointly and proves K13W, the finite
    exact weighted-path criterion. Sessions 122--123 must solve the K9A
    `ABC/ACB` specialization symbolically and either exhibit a proved family
    or close the arithmetic design class; no triple search is admitted.
    Session 122 proves K13A: unique mixed representation of `b+c` plus
    exclusion of `a+b+c` from `<b,c>` is exactly necessary and sufficient.
    Session 123 proves K13F, the infinite passing family
    `(1,n,n+2,2n+3)` for every `n>=4`, and closes HC-22 positively at the
    arithmetic level. Geometry and prior-art gates remain wholly open.
18. The user authorized HC-23 after review for the fixed smallest K13F member
    with `d=12`. Session 124 redoes role recognition, enumerates the full-side
    arithmetic tables of `A,B,C,H,d`, and expresses the guard lens as a square
    of side `d`. Session 125 must test the exact first-turn and central-edge
    containment inequalities before any coordinate list. N31 proves
    `d<=sqrt(2)a` and `h<=sqrt(2)d`, hence `b+c<=a`. The fixed tuple violates
    both the prefix and combined bounds, and every K13F member violates the
    combined bound for this unchanged K10B topology. HC-23 therefore closes
    one session early with no coordinates, experiment or candidate. A new
    checkpoint is required before changing a named N31 hypothesis.
19. The user authorized HC-24 after review. It retains the K10B word and
    square lens but varies the weights only after the complete spine and all
    containment inequalities are derived over `Q(sqrt(2))`. Those inequalities
    must be solved jointly with U1/U2 and semigroup exclusion of unintended
    `d` host covers. Any survivor gets a fresh role/cover audit. The checkpoint
    permits no numerical search, coordinate fitting, experiment, SVG or
    candidate promotion and stops within three sessions with a proved family
    or scoped no-go. Session 126 derives K15S: six exact relative partial
    sums, 12 two-sided open-square coordinate bounds (24 scalar inequalities)
    and the central closure line on the
    unit circle. The free terminal angle makes the system semialgebraic, not
    linear in weights alone. N32 adds the necessary wedge
    `b+c<a<(1+sqrt(2))b-c`, hence `b>sqrt(2)c`, refuting the illustrative
    `(11,4,6,21)` tuple. K15D reduces unintended arithmetic `d` host covers
    to `h-d in <a,b,c>`. Session 127 proves N33: after exact normalization,
    the `w_4` and `w_6` containment inequalities require one margin to be
    simultaneously above `L(t)` and below `U(t)`, while a positive polynomial
    factorization gives `L(t)>U(t)` for every allowed orientation. Hence the
    unchanged K10B square-lens system is empty for all positive weights.
    HC-24 closes one session early without a tuple, coordinates, experiment
    or candidate; changing weights alone is no longer an admissible repair.
20. The user authorized HC-25 to relax only N33's equal-leg guard assumption
    while retaining the right-angle K9A/K9T mechanism. The old one-edge
    connectors must first be checked against unequal outgoing/incoming spoke
    lengths. Only the minimal split-spoke topology may then be introduced,
    and its exact rectangular-lens equations precede any coordinates. The
    checkpoint admits no numerical search, experiment, SVG, larger atlas or
    candidate promotion and stops within three sessions with an exact
    mechanism or scoped no-go. Session 128 proves N34: each old one-side
    connector is both an outgoing `u` and incoming `v`, so it forces `u=v`.
    K16B replaces exactly the four centrally paired dual-role connectors by
    `u,v` paths, giving one fixed 19-side word and a `v`-by-`u` rectangular
    lens. Session 129 derives K17S, the complete partial-sum, rectangle and
    central-closure system. K17G proves the two bridge angles are locally
    measurable shape geometry because their incident lengths are the ordered
    unequal pair `(u,v)`. Session 130 tests the straight and all-sharp bridge
    specializations and the opposed-width-chord decomposition. None supplies
    an exact simple spine or a general no-go. HC-25's predeclared stop fires
    at 3 of 3 sessions. K16W freezes the exact missing witness; no numerical
    fit, extra edge, SVG, placement patch or candidate is admitted.
21. After independent audit, the user authorized HC-26 as one theorem-only
    bridge-elimination checkpoint with a strict witness/no-go/freeze
    trichotomy. Session 131 derives K18H, the exact twelve-bound cone for each
    rigid `v,w,u` hook. An exact unequal-rectangle control proves the cone is
    nonempty, so it gives no cheap incompatibility theorem. N35 excludes the
    identically-satisfied closure line and K18R treats the reflected global
    turn orientation isometrically. Two sessions remain to couple the hooks
    through the bridges and closure; partial analysis is not success.
22. Session 132 derives K19P, the complete first-corner prefix cone and
    `a>u/sqrt(2)`, and K19E, the exact three-rotor annulus criterion for host
    closure after containment is relaxed. Exact unequal-leg controls pass
    both separate tests. They are not K16W witnesses and do not satisfy the
    checkpoint trichotomy. One session remains to settle the simultaneous
    system or fire the predeclared freeze.
23. Session 133 proves K20L: one exact positive unequal-leg tuple passes the
    prefix, each isolated hook cone and relaxed closure separately. The
    cumulative placement phases cannot be discarded, and no exact simple
    simultaneous spine or all-phase incompatibility theorem is obtained.
    HC-26's third terminal outcome fires. K16W remains open but frozen; a new
    checkpoint is required for the pre-agreed `gamma!=pi/2` pivot.
24. Independent audit found K20L's printed direction was not unit. ERR-010
    replaces it with `(544/545,33/545)` and withdraws the false session-133
    check without changing the freeze. The user authorizes HC-27. Session 134
    passes the experiment gate and builds K21Q, one complete normalized
    QF_NRA sentence with every K17S bound and all 120 nonadjacent spine-pair
    predicates. The fixed run consumed 9h26m33s of CPU without returning a
    verdict; Z3's internal timeout did not return, so the wall stop was
    externally enforced at 9h27m27s. K16W remains frozen. No rerun, alternate
    ordering or weakened formula is authorized; the symbolic non-right guard
    family is the next proposed checkpoint.
25. The user authorized HC-28 as a theorem-first change to N33's guard-angle
    hypothesis. Session 135 derives K22R/K22S, the complete equal-spoke
    rhombic family, and recovers K15S exactly at `gamma=pi/2`. Session 136
    originally stated K23I too narrowly. ERR-012 corrects the necessary
    interval to `pi/3<gamma<2*pi/3`; exact K23C shows containment alone is
    nonempty on the lower branch.
    Session 137 proves K24C, an exact quadratic-algebraic point satisfying
    every containment and host-closure equation, so the non-right family
    genuinely escapes N33 at that level. N36 then rejects this point because
    two nonadjacent segments cross transversely at `(5/12,7/12)`. HC-28 is
    exhausted and K24W freezes the remaining existence of a simple point
    satisfying all 66 segment predicates across both non-right subintervals.
    ERR-011 records and discards one
    transient floating-angle diagnostic outside the authorized method; no
    theorem or exact control depends on it. No polygon, patch, decoder,
    aperiodicity result or candidate is claimed.
26. The user authorized HC-29 after ERR-012. Session 138 derives K25X: the
    N36 spoke pair has exact intersection parameters
    `u=b/(2*d*sin(gamma/2))` and `1-u`. On the upper corrected branch, strict
    containment bounds `b` by the long rhombus diagonal; on the lower branch,
    the corrected K23I orientation window and an oblique-coordinate chord
    bound give the same strict inequality `b<2*d*sin(gamma/2)`. N37 therefore
    forces a transverse crossing everywhere in K24W's domain. K23I excludes
    both endpoints, and the diameter proof also covers the right angle. K24W
    is closed by theorem, so D-0155's decomposed solver branch is not
    activated. No research command, artifact, polygon, patch, decoder,
    aperiodicity result or candidate was produced.
27. The user authorized HC-30 to aim K25X's exact intersection method at the
    frozen K16W rectangle before opening another family. Session 139 derives
    K26X for both rigid `v,w,u` hooks and sharpens K19P to K26P. N38 combines
    those crossings with host-chord containment to force the extreme aspect
    cone `v/u>sqrt(23/2)`, `b,c>sqrt(2)u`; both long-spoke directions lie in
    four narrow horizontal polarity cells. Session 140 derives K27X for the
    two bridge-dependent length-`v` spokes. Its closed intersection region is
    three linear sign conditions in the relative phase, and its complement
    is the exact disjoint union C0--C2. Thus the three critical spoke pairs
    reduce to at most twelve named semialgebraic cells. This is a strict
    decomposition, not a K16W decision; the other 117 pairs remain exact
    conjuncts. Session 141 assesses unequal guard sides `e,f`: K28G gives the
    conditional parallelogram system and K28T proves N37's squeeze no longer
    transfers because lens and spoke scales decouple. K28W freezes that
    family at the missing full-local-closure guard-role theorem. HC-30 is
    exhausted with no run, artifact, polygon, patch, decoder, aperiodicity
    result or candidate.
28. HC-31 first proves N39/K29O, reducing the twelve K16W critical cells to
    exactly two opposite-polarity cells while retaining all 120 pair
    predicates.  The gated sequential decision then runs each 174-assertion
    formula under an external four-hour wall stop.  Both return only
    `resource_stop` (return code 124), with no SAT, UNSAT, `unknown`, model or
    certificate.  The formulas and manifest are checksummed and tied to
    `d30342f`; K16W remains open/frozen and no timeout/order rerun is allowed.
29. The user authorizes theorem-only HC-32.  Every reduction must be recorded
    as an implication from complete K16W or an exact equivalence.  The work
    targets the exact `b,c` window and host budgets, orientation elimination
    with degree accounting, the proposed cell mirror, `lambda=1/v`
    compactification including limiting self-contact, and an exhaustive
    strand-order theorem if the preceding analysis supports one.  No solver
    run, angle sample, coordinate fit, polygon or candidate is authorized.
30. Session 145 proves K30W's exact shrinking window for both code-edge
    weights and K30B's equivalent host component budgets.  N40 rules out the
    proposed mirror quotient because the intrinsic cyclic word has no
    nonidentity dihedral automorphism.  K30E derives the exact line--circle
    substitution but rejects it: relative to the live tangent chart it saves
    no variable and raises the cleared degree ceiling from 28 to 84.  These
    are implication/equivalence audits only; no formula or solver is run.
31. Session 146 proves N41: the `P_-+` K16W cell is empty.  K31C then uses
    exact long-spoke endpoint margins and host closure to bound every point
    in the remaining `P_+-` cell by `v<V_*<13`, `a<3/2`, and
    `b,c<98/43`.  This replaces the planned asymptotic blow-up with a strict
    finite theorem, so self-contact at infinity cannot escape.  The bounded
    feasible set remains open at straight-bridge, containment, tangency and
    singular-closure boundaries; no complete interval decision is inferred.
32. Session 147 proves K32S: all four long spokes and the host cross the
    symmetry line, their C/B order is forced, and exactly four strict
    central-symmetric strand orders remain.  K32A covers both bridge circles
    with four bounded chart pairs, while K32R separates impossible, tangent
    and transverse closure strata.  The remaining obligation is an exact
    16-cell bounded cover retaining all 120 pair predicates.  HC-32 closes
    without a run; a certified all-cell decision requires a new checkpoint.
33. The user authorizes theorem-first HC-33 after independent verification.
    Session 148 originally claimed N42 closed K16W.  ERR-013/session 149
    retract that conclusion: central pairing preserves traversed edge vectors,
    so C' is westward like C.  The H-west reset contradiction and its exact
    budgets survive, proving only `v-2*p_(8,x)>0`; H points east and the long
    strands traverse `E,W,E,W,E`.  All sixteen K32S/K32A cells remain open
    with that sign added.  A symbolic regression now pins the paired-edge
    identities.  No formula or solver was launched; HC-33 has one session
    remaining under D-0168.
34. Session 150 uses the corrected `E,W,E,W,E` traversal.  K33M proves that
    no short connector touches the symmetry line, so the five long strands
    are its complete crossing list.  N43 eliminates S4 by alternating
    right-half-plane chord endpoints.  K33C proves `Re(z_1)<0`, eliminating
    both positive-first bridge charts.  Exactly six bounded complete cells
    remain (`S1--S3` times second-bridge sign), with all 120 pair predicates
    and all boundary strata retained.  HC-33 is exhausted without a run;
    serialization and any exact decision require a new checkpoint.
