# Einstein tiling research

This repository studies when finite symbolic aperiodic tiling systems can be
realized by one connected unmarked Euclidean polygon. Its current central
question is the Sturmian realization problem:

> Construct a connected unmarked polygon whose every tiling admits a total
> finite-radius map to an aperiodic Sturmian tiling system; or prove
> nonexistence/undecidability for a clearly defined realization family.

No new monotile has been found here. The historical Hat/Turtle, Spectre and
polykite computations are retained as exact controls and reproductions.

## Start here

- [Documentation and authority map](docs/README.md) — current research,
  canonical theory, evidence and historical provenance.
- [Research charter](docs/research/charter.md) — field-level mission, creative
  exploration, sustained programs and strict promotion boundaries.
- [Research portfolio](docs/research/portfolio.json) and
  [current status](docs/research/status.md) — the program-level option set and
  concise present state.
- [General realization theory](docs/theory/realization/general_theory.md)
  — the reusable mathematics independent of one source construction.
- [Sturmian realization boundary](docs/theory/research/sturmian_realization.md)
  — the open problem, known boundary, exact AHI benchmark and future proof
  obligations.
- [Theory guide](docs/theory/README.md) — evidence levels and provenance.
- [Literature](docs/literature/README.md) — primary-source catalog, reviews
  and novelty permissions.
- [Consolidation map](docs/consolidation/README.md) — temporary claim, file and
  artifact migration control.
- [Historical archive guide](docs/archive/README.md) — provenance and frozen
  research without treating it as the live program.

The chronological [status](docs/STATUS.md),
[decisions](docs/DECISIONS.md), [experiments](docs/EXPERIMENTS.md) and
[notebooks](docs/notebook/) are retained as research history rather than
reader-facing mathematical authority.

## What the repository contains

- exact lattice/polyform geometry and canonicalization;
- bounded periodicity, Heesch, patch and hierarchy controls;
- certificate schemas and independent cold verifiers;
- exact Spectre reconstruction controls;
- one reconstructed AHI `sqrt(2)-1` source presentation;
- general results on total decoding, periodic carriers, marked compiler
  undecidability, two-body erasure and multi-participant contact languages;
- a large historical collection of frozen experiments and scoped geometric
  derivations, currently being consolidated.

## Code and tests

The Python package is under `src/einstein/`; its domain architecture is mapped
in [src/einstein/README.md](src/einstein/README.md). Exact performance tools
are under `tools/`. The package is validated against published Hat/Turtle coordinates,
OEIS polyform counts, Myers's polykite census, Kaplan's public Heesch data and
vendored Spectre controls.

```sh
venv/bin/pip install -e .
venv/bin/python -m pytest          # default exact/certificate suite
venv/bin/python -m pytest -m slow  # optional slower controls
venv/bin/python -m pytest -m tier_unit
venv/bin/python -m pytest -m tier_certificate
```

See [the test tiers](tests/README.md), [data boundary](data/README.md), and
[script boundary](scripts/README.md) before adding new material.
