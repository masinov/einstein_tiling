# Research harness

The harness gates commitment and evidence, not mathematical creativity.

- [`policies/research_admission.md`](policies/research_admission.md) explains
  when a proposal is required.
- [`schemas/research_proposal.schema.json`](schemas/research_proposal.schema.json)
  documents the proposal data contract.
- `scripts/check_research_proposal.py` validates admitted sustained work.
- `scripts/check_experiment_gate.py` applies the stricter experiment boundary.
- `scripts/run_research.py` executes only the frozen command under external
  wall-clock and artifact supervision.

The meta-research layer is deliberately small:

- [`mechanisms/registry.json`](mechanisms/registry.json) records each active or
  proposed control, the failure it addresses, and where it may intervene.
- [`evaluation/drift_cases.json`](evaluation/drift_cases.json) freezes real
  failures from this repository as regression cases.
- [`evaluation/README.md`](evaluation/README.md) defines the review protocol.

This layer evaluates changes to the harness; it does not score mathematical
ideas or inject live changes automatically. A mechanism is useful only if it
changes a decision at a real commitment boundary without suppressing free
exploration.
