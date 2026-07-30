# Documentation map and authority

This page is the entry point for repository documentation. The repository
separates current research direction, canonical mathematics, evidence,
knowledge, and historical provenance so that an old plan or a long session log
cannot silently become the research agenda.

## Current authority chain

Read these documents in order when deciding what research to pursue:

1. [`research/charter.md`](research/charter.md) defines the field-level mission,
   meaningful terminal outcomes, research modes, and promotion boundaries.
2. [`research/portfolio.json`](research/portfolio.json) lists the current
   programs and their relationship to the mission.
3. [`research/status.md`](research/status.md) is the concise present-tense view
   of what is established, open, paused, or awaiting a strategic decision.
4. [`theory/README.md`](theory/README.md) navigates the canonical mathematics.

The root [`CLAUDE.md`](../CLAUDE.md) is the executable repository contract for
agents. It must agree with this authority chain. If a historical document
describes itself as "living" or "current", this page and the files above
supersede that old description.

## Research layers

- [`research/ideas/`](research/ideas/README.md) is a permissive,
  non-authoritative space for conjectures, analogies, sketches, and questions.
- [`research/workspaces/`](research/workspaces/README.md) holds problem-centered
  working notes and proof drafts. A workspace is not a claim registry.
- [`research/proposals/`](research/proposals/README.md) contains ready or
  closed sustained commitments, experiment specifications, and promotion
  dossiers.
- [`research/admissions/`](research/admissions/README.md) records separate
  human authorization of exact proposal bytes; proposal authors cannot admit
  themselves.
- [`theory/`](theory/README.md) contains integrated mathematical statements and
  their dependency-oriented exposition.
- [`literature/`](literature/README.md) contains the source catalog, reviews,
  syntheses, anchors, and prior-art controls.
- [`consolidation/`](consolidation/README.md) is a temporary non-destructive
  migration control layer, not a research authority.
- [`harness/`](harness/README.md) documents the strict commitment and evidence
  boundary without regulating free mathematical exploration.

## Evaluation, evidence, and history

- [`evaluation/`](evaluation/README.md) contains method assessments and
  postmortems. It currently records no sealed general discovery benchmark.
- [`history/`](history/README.md) is the single navigation page for the
  chronological research record.
- [`notebook/`](notebook/README.md), [`STATUS.md`](STATUS.md),
  [`DECISIONS.md`](DECISIONS.md), [`EXPERIMENTS.md`](EXPERIMENTS.md), and
  [`HUMAN_CHECKPOINTS.json`](HUMAN_CHECKPOINTS.json) are chronological
  provenance. They are not current authorization.
- [`program/`](program/README.md) contains superseded research programs and
  append-only historical errata.
- [`archive/`](archive/README.md) contains preserved derivations and frozen
  material that no longer belongs in active navigation.

Historical provenance is retained even when its path or navigation role is
changed. A later migration will separate compact evidence manifests from the
large payloads currently stored beneath the notebook tree.

## Authority rules

1. A current strategy must appear in the research portfolio; a session's local
   "next step" cannot authorize itself.
2. Ideas and workspaces may be speculative. They become authoritative only
   through review and integration into the portfolio, evidence registry, or
   canonical theory.
3. A correct instance-level lemma does not automatically justify another
   instance-level investigation.
4. Nontrivial computation, candidate promotion, novelty claims, and canonical
   theorem claims cross strict evidence gates.
5. Documentation cleanup does not create research sessions or append entries
   to the historical decision log.
