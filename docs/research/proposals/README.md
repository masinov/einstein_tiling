# Research commitment proposals

This directory is for sustained research commitments and nontrivial
experiments. It is not an inbox for every mathematical idea.

Free exploration belongs in `../ideas/` or a problem-centered workspace and
requires no proposal. Ordinary proof development within an admitted program
also requires no proposal per lemma.

A proposal is required when the project:

- commits sustained effort to a new construction or realization class;
- launches a nontrivial census, solver campaign, parameter search, or other
  research computation;
- crosses from exploratory evidence to candidate or theorem promotion; or
- changes the strategic scope of an existing program.

The contracts are deliberately separate:

- [`PROGRAM_TEMPLATE.json`](PROGRAM_TEMPLATE.json) specifies sustained proof work;
- [`TEMPLATE.json`](TEMPLATE.json) specifies one reproducibly pinned experiment;
- [`PROMOTION_TEMPLATE.json`](PROMOTION_TEMPLATE.json) governs candidate,
  theorem, method, or novelty promotion.

Experiment reproducibility pins include both the research implementation and
the gate/supervisor implementation, the exact executable bytes and version
output, environment files, inputs, and any cold verifier. Changing any pinned
object requires a new proposal hash and a new admission.

The corresponding machine contracts live in `../../harness/schemas/`. A
completed proposal uses status `ready`; that word does not authorize it.
Authorization is a separate hash-pinned record under `../admissions/`, created
only after explicit human approval. Editing the proposal invalidates that
record.

Validate an authorized proposal with:

```bash
venv/bin/python scripts/check_research_proposal.py \
  docs/research/proposals/RP-....json
```

For an experiment, the exact command must also pass the compatibility-named
experiment gate and must be launched through the supervised runner:

```bash
venv/bin/python scripts/check_experiment_gate.py PROPOSAL.json
venv/bin/python scripts/run_research.py PROPOSAL.json -- COMMAND ...
```

Candidate or theorem promotion additionally uses:

```bash
venv/bin/python scripts/check_promotion.py PROPOSAL.json
```

The runner accepts only the exact frozen argument vector after verifying the
admission hash, pinned code paths, inputs, environment files, executable
versions, verifier, and clean working tree. It supervises wall-clock, memory,
and artifact-growth budgets and writes a non-overwritable result manifest.
