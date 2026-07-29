#!/usr/bin/env python
"""Fetch the tracked literature catalog into the ignored local source cache.

The Git repository stores metadata and reviews, not third-party PDFs.  This
script downloads catalogued open copies, validates the PDF signature, extracts
plain text when ``pdftotext`` is available, and writes a local SHA-256 lock.

Usage:
  venv/bin/python scripts/fetch_literature.py
  venv/bin/python scripts/fetch_literature.py --id smkgs-hat-2024 --force
"""

from __future__ import annotations

import argparse
from pathlib import Path

from einstein.literature import sync_library
from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", action="append", dest="ids")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-text", action="store_true")
    args = parser.parse_args()

    try:
        lock = sync_library(
            ROOT,
            source_ids=args.ids or (),
            force=args.force,
            extract_text=not args.no_text,
        )
    except ValueError as error:
        parser.error(str(error))
    print(f"wrote data/literature/library-lock.json ({len(lock['entries'])} PDFs)")


if __name__ == "__main__":
    main()
