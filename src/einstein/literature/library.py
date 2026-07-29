"""Synchronize catalogued open papers into the ignored local source cache."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_pdf(url: str, destination: Path) -> None:
    """Atomically fetch one URL after checking its PDF signature."""

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


def sync_library(
    root: Path,
    *,
    source_ids=(),
    force: bool = False,
    extract_text: bool = True,
) -> dict:
    """Fetch selected catalog entries and write the reproducibility lock."""

    catalog_path = root / "docs/literature/SOURCES.json"
    library = root / "data/literature"
    papers = library / "papers"
    text_root = library / "text"
    lock_path = library / "library-lock.json"
    catalog = json.loads(catalog_path.read_text())
    wanted = set(source_ids)
    known = {source["id"] for source in catalog["sources"]}
    missing = wanted - known
    if missing:
        raise ValueError(f"unknown source IDs: {', '.join(sorted(missing))}")

    papers.mkdir(parents=True, exist_ok=True)
    text_root.mkdir(parents=True, exist_ok=True)
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
        pdf = papers / filename
        if force or not pdf.exists():
            print(f"fetch {source['id']}: {url}", flush=True)
            fetch_pdf(url, pdf)
        else:
            print(f"keep  {source['id']}: {pdf.relative_to(root)}")

        text_path = text_root / f"{pdf.stem}.txt"
        if extract_text and pdftotext and (
            force
            or not text_path.exists()
            or text_path.stat().st_mtime < pdf.stat().st_mtime
        ):
            subprocess.run(
                [pdftotext, "-layout", str(pdf), str(text_path)], check=True
            )
        entries.append(
            {
                "id": source["id"],
                "arxiv": source.get("arxiv"),
                "url": url,
                "pdf": str(pdf.relative_to(root)),
                "text": (
                    str(text_path.relative_to(root))
                    if text_path.exists()
                    else None
                ),
                "bytes": pdf.stat().st_size,
                "sha256": sha256(pdf),
            }
        )

    lock = {
        "schema_version": 1,
        "catalog_snapshot_date": catalog["snapshot_date"],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }
    lock_path.write_text(json.dumps(lock, indent=2) + "\n")
    return lock
