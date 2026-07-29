# Repository maintenance commands

These are thin entry points over `einstein.repository`:

```bash
venv/bin/python scripts/maintenance/build_catalog.py
venv/bin/python scripts/maintenance/check_catalog.py
```

They inventory or validate repository state; they do not run mathematical
experiments.
