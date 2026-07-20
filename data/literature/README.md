# Local literature source library

The PDFs, extracted text, and checksum lock in this directory are deliberately
ignored by Git. They are reproducible from the tracked catalog:

```bash
venv/bin/python scripts/fetch_literature.py
```

Tracked metadata and reviews live in `docs/literature/`. The split avoids
pushing large third-party documents while keeping the exact reading corpus
available locally and auditable by URL and SHA-256.
