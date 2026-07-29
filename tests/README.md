# Test suites

Tests are organized first by evidence role and then by mathematical domain.
Every module receives one primary marker from `TEST_TIERS.json`:

- `tier_unit`: reusable exact primitives;
- `tier_certificate`: retained certificate and source-reconstruction checks;
- `tier_control`: known systems and historical pipeline regressions; and
- `tier_provenance`: governance, literature and external anchors.

Run a tier with, for example:

```bash
venv/bin/python -m pytest -m tier_unit
venv/bin/python -m pytest -m tier_certificate
```

The default remains every non-slow test.  Tiering changes selection and
navigation only; it does not weaken or rewrite an assertion.

Directory responsibilities are deliberately distinct:

- `unit/` tests reusable source primitives without historical artifacts;
- `certificates/` cold-verifies retained exact certificate families;
- `controls/` reproduces named systems and frozen historical pipelines; and
- `provenance/` verifies repository architecture, literature, governance and
  external-anchor integrity.

Test filenames describe behavior rather than old research stages. Shared
fixtures live in `fixtures/`; small external-anchor records live in `data/`.
