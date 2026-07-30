# Admitted research proposals

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

The machine contract is documented by
`../../harness/schemas/research_proposal.schema.json`. Start from
[`TEMPLATE.json`](TEMPLATE.json). A template remains deliberately invalid until
its status is `admitted` and every placeholder is replaced.

Validate an admitted proposal with:

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

The runner accepts only the exact argument vector frozen in the proposal. It
supervises the complete process group against the declared wall-clock and
artifact-growth budgets.
