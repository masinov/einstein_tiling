# Test suites

Tests remain at their stable paths, but every module now receives one primary
marker from `TEST_TIERS.json`:

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
