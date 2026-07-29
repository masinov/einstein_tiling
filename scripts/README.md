# Script boundary

The script directory contains four different kinds of program.  Their exact
per-file classification is in `docs/consolidation/FILE_DISPOSITIONS.json`.

- `check_*`, `fetch_*`, `extract_*` and `run_research.py` are reusable
  governance or source tools.
- `verify_*` programs are cold certificate verifiers and remain part of the
  retained toolbox.
- `build_*` programs construct particular artifacts.  They are retained until
  their schemas, builders and verifiers can be exposed through a coherent
  certificate interface.
- most `run_*` and `probe_*` programs are frozen session-specific research
  history.  Their presence is provenance, not an invitation to resume their
  parameter ladders.

New reusable behavior belongs in `src/einstein/` with tests.  A new nontrivial
research runner still requires the admission and launcher rules in
`CLAUDE.md`.
