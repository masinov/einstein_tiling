# Theory dossier

This directory is the reviewable mathematical layer of the project. It turns
the living roadmap in `docs/program/theory_research_plan.md` into stable
theorem statements, proof drafts, certificate specifications, and a ledger of
what has actually been established.

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
  machine-verified T1.2-25 finalist bounded-norm theorem.
- `03_w2_invariants.md` — Layer A exact result, zero-false-exclusion gate,
  and T2.B0 showing why isolated nontrivial character blocks are vacuous.
- `04_w2_cokernel.md` — quotient-wide modular cokernel certificates, the
  finite Layer C kill table, T2.C1's infinite thin-family proof draft, and the
  exact HNF/Smith integer-membership classification T2.C2 plus T2.C3's
  translation-averaged nonnegative cone reduction.
- `05_w2_binary_holonomy.md` — binary period-vector quotient families,
  the three-family thin D6 theorem, the Conway--Lagarias primary-source
  control, the binary-coupled torus-holonomy theorem, and the independently
  certified complete finalist quotient prefix through index 40.
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

Changes to definitions or logical dependencies require a DECISIONS entry.
Changes to proof wording alone are tracked by ordinary version control.
