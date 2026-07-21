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
  kernel, its conditional unique-pairing argument, and the open B0/contact-
  guard obligations that stop geometry after HC-11.
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
