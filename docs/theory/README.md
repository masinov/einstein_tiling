# Theory dossier

This directory is the reviewable mathematical layer of the project. It turns
the living roadmap in `docs/program/theory_research_plan.md` into stable
theorem statements, proof drafts, certificate specifications, and a ledger of
what has actually been established.

> **Terminology correction (ERR-003/D-0048):** “finalist” in legacy theorem
> IDs, prose, symbols, scripts, and artifact filenames means the published
> ten-kite **Turtle**. These results are known-control and independent
> certificate results, not evidence for a new monotile.
>
> **Literature-scope correction (ERR-004/D-0049):** the primary Hat paper's
> Appendix A already reduces arbitrary periodic polykite tilings to aligned
> periodic tilings. W4 is optional stronger rigidity/extension work, not a
> missing bridge. The same audit places all `n≤24` polykites inside the
> published classified horizon; see `docs/literature/POLYKITE_BASELINE.md`.

## Source-of-truth hierarchy

1. `docs/program/theory_research_plan.md` is the living research roadmap.
2. Files in this directory contain stable theorem and certificate texts.
3. `PROOF_LEDGER.md` is the claim-status authority.
4. `docs/DECISIONS.md` records adopted methodological changes.
5. `docs/EXPERIMENTS.md` and `docs/notebook/` record executed evidence.
6. `docs/notebook/assets/` contains machine-readable certificates and raw
   artifacts; an interrupted log is evidence only after recovery into a
   versioned artifact.

No narrative status page, notebook sentence, or promising finite patch may
upgrade a theorem's status without a corresponding ledger change and a
reviewable proof or certificate.

## Current documents

- `01_periodic_completion.md` — T0.1, the reduction from arbitrary
  translational periodicity to a rank-2 torus tiling.
- `02_transfer_certificates.md` — T1.1 correctness proof and the
  machine-verified T1.2-25 Turtle-control bounded-norm theorem.
- `03_w2_invariants.md` — Layer A exact result, zero-false-exclusion gate,
  and T2.B0 showing why isolated nontrivial character blocks are vacuous.
- `04_w2_cokernel.md` — quotient-wide modular cokernel certificates, the
  finite Layer C kill table, T2.C1's infinite thin-family proof draft, and the
  exact HNF/Smith integer-membership classification T2.C2 plus T2.C3's
  translation-averaged nonnegative cone reduction.
- `05_w2_binary_holonomy.md` — binary period-vector quotient families,
  the three-family thin D6 theorem, the Conway--Lagarias primary-source
  control, the binary-coupled torus-holonomy theorem, and the independently
  certified complete Turtle-control quotient prefix through index 60.
- `06_w3_substitution_certificates.md` — the C1--C5 certificate contract,
  Spectre's exact 17-state finite kernel, its recurrent rank-four geometry,
  the ancestry-blind `166→30→21` physical-language prefix, its conditional
  coordinated contraction to 18 types, and the remaining
  legality/growth/recognizability/gluing obligations.
- `07_stm1_sturmian_monotile_design.md` — the minimal versus
  positive-entropy ST-M1 targets, the independent-rail no-go, a
  reflection-safe conditional carrier theorem, and the pre-geometric kill
  conditions for a coupled contact-star encoder.
- `08_stm1_equal_support_compiler.md` — the proof-draft compiler from
  connected common-cell macrotiles to one colored support, P0's corrected
  slope intersection, G0's `30,30,2` common-support geometry, and the later
  corrected E-infinity closure through L0.
- `09_stm1_symbolic_quotient.md` — the full-local-closure safety criterion and
  the source-backed failure of the natural `S/M/L` quotient; it now governs
  reductions of the valid addressed equal-support source.
- `10_stm1_limit_language.md` — the distinction between auxiliary overlapping
  Sturmian-triangle patches and the physical cell tiling, O0's decorated-
  vertex contraction, the three-coset proof of unique physical provenance
  I0, and the face-cocycle/global-gap decoder D0 closing minimal colored L0.
- `11_stm1_contact_kernel.md` — the lossless contact-incidence compiler K1C
  and the exact local-closure boundary, distributed quotient K1D, and selected
  parity-check compiler K1P.
- `12_stm1_geometric_carrier.md` — K2E's exact carrier contract, N5's
  unary/binary arity obstruction, and the sharp four-state hidden-phase
  factorization and lower bound K2H/N6; N7--N9 close unanchored pose routes,
  while K2C/K2V retain the gauge-invariant boundary mechanism and K2J states
  the unresolved geometric admission contract.
- `13_stm1_serialization_contract.md` — SER0's extensional source/quotient
  schema, cold-verifier obligations, and the primary-archive finding that
  direct serialization is blocked by figure-only construction data.
- `14_stm1_symbolic_chain.md` — the self-contained P0/S0/Q0/K1T/K1P/
  N5--N9/K2C/K2V dependency chain and the conditional K2J-to-monotile
  theorem. This is the canonical review entry point for ST-M1; it is a proof
  draft, not a construction or novelty claim.
- `15_stm1_flag_carrier.md` — K3F relocates the three K2C potentials to three
  congruent corner-kite occurrences and states the remaining K3G color-erasure
  problem.
- `16_stm1_retiling_compiler.md` — N10's corner-kite rigidity and K3R's
  conditional inverse-retiling theorem/search architecture.
- `17_stm1_binary_retiling_kernel.md` — the concrete two-diagonal square
  kernel, its conditional unique-pairing argument, and the HC-12 refutation of
  bit-complete B0.
- `18_retiling_wang_compiler.md` — the HC-12 correction from binary SFT to
  hidden-state sofic projection, the 11-state/four-interface design floor,
  and the direct K4W sufficient monotile contract.
- `19_synchronizing_retiling_topology.md` — the exact twelve-state domino
  inverse-dissection kernel and its conditional six-bar unique-grouping
  invariant, the cheap-channel no-gos, and the surviving K5C closed-corridor
  compiler contract; no unmarked carrier or Wang interface realization.
- `20_k5c_boundary_forcing.md` — the HC-14 geometric mechanism test. N17
  refutes a fixed-successor order-42 rosette as a rooted state carrier; N18
  closes disjoint optional ports under gapless coverage; N19 bounds one full
  arc pair's alignments. No boundary meets K5C.1--K5C.3, so the route is
  frozen after HC-14.
- `21_subdivision_word_contacts.md` — the HC-15 fully occupied partial-contact
  alternative. K6O counts `k!/2` order states, N20 closes the apparent
  two-neighbor bit under full isometry, and J0 gives the exact endpoint-angle
  equations. No congruent polygonal witness or whole-plane forcing theorem is
  claimed.
- `34_nonright_spoke_crossing.md` — K25X gives the exact intersection
  parameters for the N36 spoke pair, and N37 combines them with the corrected
  K23I branches to close the entire equal-spoke non-right rhombic family by a
  forced transverse crossing.
- `35_k16w_crossing_cells.md` — K26X/N38 reduce the frozen unequal-spoke
  rectangle to one extreme aspect cone and four phase-polarity cells; K27X
  partitions the remaining long-spoke pair into three exact safe cells.
- `36_unequal_guard_parallelogram.md` — the unequal-guard transfer: K28G is
  the complete conditional parallelogram-lens system, K28T proves N37's
  squeeze no longer transfers, and K28W freezes geometry at contact roles.
- `49_k28w_guard_role_collapse.md` — the K28W role audit: distinct `e,f`
  are boundary-intrinsic, but selected complete clean-spoke contacts force
  `e=f=d`; the collapse is K22S and N37 closes it. Partial/contextual guard
  interfaces and different side words remain outside the no-go.
- `50_clean_spoke_topology_classification.md` — K42P/K42M classify the
  edge-minimal full-side/half-turn incidence words: K10B is the equal-port
  branch and K16B the unique unequal-port branch. N46 forces any fresh
  carrier to change contact type, role order, docking involution or guard
  topology rather than another numerical lens parameter.
- `51_reflection_docking_normal_form.md` — K43I reduces copy-exchanging
  docking to half-turn or reflection; K43R derives the conditional non-axis
  normal form and N48 closes it by the fixed-side half-plane overlap missed
  in session 165 (ERR-016).
- `52_reflection_clean_interface_no_go.md` — concise disposition of N48 and
  the exact scope boundary: reflection can reopen only through partial,
  disconnected or third-participant contact topology.
- `53_reflection_hinge_orbits.md` — K45O/N49 prove that a symmetry-free
  reflection hinge has an even number of participants; K45H classifies the
  minimum four-sector star and its exact nonempty angle equation.
- `54_rooted_binary_reflection_hinge.md` — N50 shows the unrooted four-star
  is state-neutral; K46S proves distinct opposite roots create exactly two
  reflection-stable states, and K46J states the finite geometric contract.
- `55_full_side_hinge_compiler.md` — K47P gives the exact two-state port
  cross-match, K47T proves sector-level totality, and K47B reduces carrier
  generation to one rooted word with two residual arcs.
- `37_k16w_polarity_elimination.md` — N39 rules out equal-polarity long
  spokes by a width-reset inequality, and K29O collapses the surviving K16W
  critical-pair domain to two exact opposite-polarity cells.
- `38_k16w_budget_and_encoding_audit.md` — K30W gives the exact shrinking
  `b,c` window, K30B exposes host component budgets, N40 rejects a mirror
  quotient, and K30E audits then rejects high-degree terminal elimination.
- `39_k16w_exact_compactification.md` — N41 refutes the west--east polarity
  cell and K31C bounds the surviving east--west cell by `v<V_*<13`, while
  retaining the finite strict-boundary obligations for any later decision.
- `40_k16w_finite_strand_atlas.md` — K32S gives four exhaustive midline
  strand orders, K32A gives four bounded bridge-chart pairs, and K32R isolates
  tangent versus transverse closure strata for a later exact decision.
- `41_k16w_thin_lens_reset_no_go.md` — corrected N42 proves that H cannot
  point west with C, hence the central host points east.  ERR-013 withdraws
  the original C'-direction claim and all-cell refutation; all sixteen
  K32S/K32A cells remain open with traversal pattern `E,W,E,W,E`.
- `42_k16w_corrected_six_cell_atlas.md` — K33M proves that only the five long
  strands cross the symmetry line; N43 eliminates the alternating S4 order;
  K33C fixes the first bridge to the left semicircle.  Six bounded complete
  K16W cells remain, with every original predicate retained.
- `W1_TRANSFER_SPEC.md` — the soundness/completeness contract for the exact
  cylinder transfer engine and its certificates.
- `PROOF_LEDGER.md` — stable IDs, scope, status, dependencies, and artifacts.
- `MONOGRAPH_OUTLINE.md` — integration map for papers or a monograph.

## Status vocabulary

- **proposed** — precise statement exists; proof work has not closed.
- **proof-draft** — a complete internal argument exists; external literature
  and adversarial review remain.
- **machine-verified** — finite claim checked by the stated verifier and
  preserved certificate.
- **theorem-ready** — proof, scope, dependencies, and independent controls are
  complete enough for a paper draft.
- **refuted** — a counterexample or failed statement is preserved.
- **blocked** — a named missing lemma or infeasible computation prevents
  progress; this is not a negative mathematical result.

## Review protocol

Every theorem or computational proposition must state:

1. a stable identifier;
2. exact scope (grid-aligned or geometric; fixed vector, bounded norm, or
   universal);
3. hypotheses and dependencies;
4. proof/certificate location;
5. independent validation controls;
6. failure polarity — what a positive or negative computation proves;
7. whether the result concerns existence, periodicity, or both.

A conditional reduction is not a construction: every unproved hypothesis
remains a separate ledger row, especially contact completeness,
mixed-handedness exclusion, and totality of a local decoder.

Changes to definitions or logical dependencies require a DECISIONS entry.
Changes to proof wording alone are tracked by ordinary version control.
