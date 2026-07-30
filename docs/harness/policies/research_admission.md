# Research admission policy

## No proposal required

- speculative ideas and conjectures;
- hand calculations and proof sketches;
- reading and literature synthesis;
- counterexample attempts on paper;
- ordinary definitions and lemmas inside an admitted program;
- read-only diagnostics and repository maintenance; and
- small unit or cold-verifier regression tests that do not produce research
  evidence.

## Proposal required

- a sustained new construction, family, or realization campaign;
- a nontrivial research computation;
- candidate promotion;
- canonical theorem or novelty promotion; or
- a strategic change to the active research portfolio.

The proposal gate checks whether a commitment has an explicit program, scope,
prior-art boundary, distinct outcomes, and stopping logic. It does not score
the creativity or truth of the mathematical thesis.

A proposal author may mark a proposal `ready` but cannot admit it. Admission is
a separate human-authorization record that pins the proposal path and SHA-256;
editing either invalidates authorization.

Experiment proposals additionally pin the supervisor and research code paths
to a Git revision, exact inputs, environment files, executable bytes and
version output, verifier bytes, command,
artifact roots, wall-clock and memory budgets, run-record paths, and promotion
boundary. Resource exhaustion and runner termination remain no-result
outcomes. The runner produces its own hash-bearing execution manifest.

Candidate, theorem, method and novelty promotion uses a separate promotion
contract. An experiment result never promotes itself.

The legacy human-checkpoint cadence and numbered-session distance are not part
of this policy.
