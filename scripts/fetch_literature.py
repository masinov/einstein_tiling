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
import hashlib
import json
import shutil
import subprocess
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "docs" / "literature" / "SOURCES.json"
LIBRARY = ROOT / "data" / "literature"
PAPERS = LIBRARY / "papers"
TEXT = LIBRARY / "text"
LOCK = LIBRARY / "library-lock.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "einstein-tiling-literature-audit/1.0"},
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=destination.parent, prefix=destination.name, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
        with urllib.request.urlopen(request, timeout=120) as response:
            shutil.copyfileobj(response, temporary)
    try:
        if temporary_path.read_bytes()[:5] != b"%PDF-":
            raise RuntimeError(f"download is not a PDF: {url}")
        temporary_path.replace(destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", action="append", dest="ids")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-text", action="store_true")
    args = parser.parse_args()

    catalog = json.loads(CATALOG.read_text())
    wanted = set(args.ids or ())
    known = {source["id"] for source in catalog["sources"]}
    missing = wanted - known
    if missing:
        parser.error(f"unknown source IDs: {', '.join(sorted(missing))}")

    PAPERS.mkdir(parents=True, exist_ok=True)
    TEXT.mkdir(parents=True, exist_ok=True)
    pdftotext = shutil.which("pdftotext")
    entries = []
    for source in catalog["sources"]:
        if wanted and source["id"] not in wanted:
            continue
        url = source.get("download_url")
        filename = source.get("local_filename")
        if not url or not filename:
            print(f"skip {source['id']}: no catalogued open PDF")
            continue
        pdf = PAPERS / filename
        if args.force or not pdf.exists():
            print(f"fetch {source['id']}: {url}", flush=True)
            fetch(url, pdf)
        else:
            print(f"keep  {source['id']}: {pdf.relative_to(ROOT)}")

        text_path = TEXT / f"{pdf.stem}.txt"
        if not args.no_text and pdftotext and (
            args.force
            or not text_path.exists()
            or text_path.stat().st_mtime < pdf.stat().st_mtime
        ):
            subprocess.run(
                [pdftotext, "-layout", str(pdf), str(text_path)],
                check=True,
            )
        entries.append({
            "id": source["id"],
            "arxiv": source.get("arxiv"),
            "url": url,
            "pdf": str(pdf.relative_to(ROOT)),
            "text": (
                str(text_path.relative_to(ROOT)) if text_path.exists() else None
            ),
            "bytes": pdf.stat().st_size,
            "sha256": sha256(pdf),
        })

    lock = {
        "schema_version": 1,
        "catalog_snapshot_date": catalog["snapshot_date"],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }
    LOCK.write_text(json.dumps(lock, indent=2) + "\n")
    print(f"wrote {LOCK.relative_to(ROOT)} ({len(entries)} PDFs)")


if __name__ == "__main__":
    main()
