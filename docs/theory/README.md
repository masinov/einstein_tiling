# Mathematical theory

This directory is organized by mathematical dependency, not by the order in
which results were discovered.  It is the reader-facing theory layer of the
repository.

## Reading order

1. [Sturmian realization problem](research/sturmian_realization.md) states the
   open construction, nonexistence and undecidability targets and the exact
   all-tilings proof contract.
2. [Periodic completion](foundations/periodic_completion.md) gives the basic
   finite-type and period-completion theorem.
3. [General realization theory](realization/general_theory.md) integrates the
   source-independent results on total local factors, symbolic quotients,
   undecidability, two-body erasure, additive obstructions, contact topology
   and finite-state T-junction compilation.
4. [AHI source and carrier theory](sturmian/ahi_source_and_carriers.md) records
   the exact Section 10.1 benchmark and the complete carrier-local reduction.
5. [AHI realization case study](case_studies/ahi_realization.md) explains what
   that branch establishes, what it refutes, and what remains open.
6. [Geometric carrier case studies](case_studies/geometric_carriers.md)
   condenses the retiling, lens, docking, hinge and parity-zipper work into
   reusable lemmas and scoped family results.

The [control theory](controls/README.md) retains exact Turtle periodicity and
Spectre hierarchy reconstructions.  They validate methods against published
tiles; they are not new einstein proofs.

## Status and provenance

- [Result catalog](reference/result_catalog.md) is the compact status index.
- [Proof ledger](reference/proof_ledger.md) retains every historical result
  identifier, exact scope, dependency and evidence path.
- [Source map](reference/SOURCE_MAP.json) maps every former numbered note to a
  canonical synthesis and to its preserved proof source. Notes 07--82 are
  byte-identical in the chronological archive; moved canonical sources retain
  their mathematics and may contain repaired navigation links.
- [Chronological theory sources](../archive/theory_sources/README.md) contain
  the original derivations.  They are proof provenance, not eighty-two active
  research directions.

## Evidence vocabulary

- **Theorem / proof draft:** a complete internal argument at its stated scope.
- **Machine-verified finite result:** a finite claim with a preserved artifact
  and independent cold verifier.
- **External theorem:** authority rests on a cited primary source.
- **Conditional theorem:** a logically complete implication with an explicit
  unresolved hypothesis or external preprint dependency.
- **Control / benchmark:** exact work on a known system.
- **Open obligation:** neither proved nor refuted.

Archiving a derivation never retracts its mathematics.  Conversely, a correct
local lemma does not become relevant to the monotile problem unless its
hypotheses connect to the unrestricted all-tilings quantifier.
