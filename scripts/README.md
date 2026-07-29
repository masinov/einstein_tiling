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
  history. Ninety-two uncoupled programs now live under `archive/`, with old
  and new paths hash-pinned in `archive/MANIFEST.json`.

The retained AHI and Stade certificate families are discoverable through one
interface:

```bash
venv/bin/python scripts/certificates.py list
venv/bin/python scripts/certificates.py describe contact-kernel
venv/bin/python scripts/certificates.py run contact-kernel verify -- ATLAS KERNEL
```

The dispatcher invokes the existing builder or cold verifier; it does not
weaken their exact checks or promote their source-specific conclusions.

New reusable behavior belongs in `src/einstein/` with tests.  A new nontrivial
research runner still requires the admission and launcher rules in
`CLAUDE.md`.
