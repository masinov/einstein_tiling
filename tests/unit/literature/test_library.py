from __future__ import annotations

import json

from einstein.literature.library import sync_library


def test_library_sync_reuses_and_hashes_an_existing_pdf(tmp_path):
    catalog = tmp_path / "docs/literature/SOURCES.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_text(
        json.dumps(
            {
                "snapshot_date": "2026-07-29",
                "sources": [
                    {
                        "id": "control-paper",
                        "arxiv": "0000.00000",
                        "download_url": "https://invalid.example/paper.pdf",
                        "local_filename": "control.pdf",
                    }
                ],
            }
        )
    )
    pdf = tmp_path / "data/literature/papers/control.pdf"
    pdf.parent.mkdir(parents=True)
    pdf.write_bytes(b"%PDF-1.4\ncontrol\n")

    lock = sync_library(tmp_path, extract_text=False)
    assert [entry["id"] for entry in lock["entries"]] == ["control-paper"]
    assert lock["entries"][0]["bytes"] == len(pdf.read_bytes())
    assert json.loads(
        (tmp_path / "data/literature/library-lock.json").read_text()
    )["entries"] == lock["entries"]
