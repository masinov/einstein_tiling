# Command boundary

`scripts/` contains operator-facing entry points, not the reusable
implementation. Shared algorithms, parsers, repository discovery and
certificate construction live in `src/einstein/` and are tested there.

The five root commands are the stable public surface:

- `certificates.py` discovers, builds and cold-verifies retained exact
  certificate families;
- `check_experiment_gate.py` validates research preregistrations;
- `run_research.py` launches admitted research commands;
- `fetch_literature.py` maintains the pinned primary-source cache; and
- this `README.md` documents the boundary.

Commands below the root are grouped by responsibility:

- `maintenance/` rebuilds and validates repository catalogs;
- `analysis/` runs retained numerical diagnostics outside certificate paths;
- `benchmarks/` cross-checks implementations against external controls;
- `certificate_tools/` contains older evidence-format-specific cold
  verifiers that have not yet been absorbed by the generic registry;
- `visualize/` renders retained control artifacts; and
- `historical/` contains coupled runners for frozen research systems.

The retained AHI and Stade JSON certificate families use one interface:

```bash
venv/bin/python scripts/certificates.py list
venv/bin/python scripts/certificates.py describe contact-kernel
venv/bin/python scripts/certificates.py build contact-kernel
venv/bin/python scripts/certificates.py verify contact-kernel
```

The CLI only parses arguments. Dependency resolution, deterministic JSON
writing and callable dispatch are implemented by
`einstein.certificates`; family mathematics stays in the named tiling module.

Ninety-two uncoupled one-off runners remain byte/hash-pinned in `archive/`.
They are provenance, not examples to copy. A new nontrivial research runner
still requires the admission and launcher rules in `CLAUDE.md`.
