#!/usr/bin/env python3
"""Crosswalk Kaplan's public 8-kite PDF to this repository's exact keys."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import subprocess
from pathlib import Path

from einstein.repository import repository_root

from einstein.polykites.database import serialize_cells
from einstein.polykites.known_shapes import HAT_KEY, decode_compiled_key
from einstein.geometry.kite_grid import canonical_form, is_center


ROOT = repository_root(Path(__file__))
PDF = ROOT / "data/literature/papers/8kites.pdf"
DB = ROOT / "tests/fixtures/polykites-n8.sqlite"
OUTPUT = ROOT / "docs/notebook/assets/kaplan-8kite-crosswalk.json"
EXPECTED_SHA256 = "8e710b8d9418ca5ab6d4510fb6dba36080eac980166e1b355ed491e6304e8f12"
ORIGINS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
HAT_DB_KEY = serialize_cells(decode_compiled_key(HAT_KEY))


def kaplan_point_to_cell(point: tuple[int, int]) -> tuple[int, int, int]:
    """Invert Kaplan KiteGrid::getVertexCentre/getOrigin exactly."""
    x, y = point
    candidates = []
    for direction, (ox, oy) in enumerate(ORIGINS):
        center = (x - ox, y - oy)
        if is_center(center):
            candidates.append((center[0], center[1], direction))
    if len(candidates) != 1:
        raise ValueError(f"Kaplan point {point} has {len(candidates)} cell images")
    return candidates[0]


def parse_pdf() -> list[dict]:
    digest = hashlib.sha256(PDF.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"unexpected 8kites.pdf SHA-256: {digest}")
    text = subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    records = []
    for page_number, page in enumerate(text.split("\f"), start=1):
        lines = [line.strip() for line in page.splitlines() if line.strip()]
        if not lines:
            continue
        if len(lines) != 3 or lines[0] != "Polykite":
            raise ValueError(f"unexpected PDF page {page_number}: {lines!r}")
        values = [int(value) for value in lines[1].split()]
        if len(values) != 16:
            raise ValueError(f"page {page_number} does not contain eight cells")
        points = list(zip(values[::2], values[1::2]))
        cells = [kaplan_point_to_cell(point) for point in points]
        key = serialize_cells(canonical_form(cells))
        match = re.fullmatch(r"Nontiler, Hc = (\d+), Hh = (\d+)", lines[2])
        if match:
            status = "nontiler"
            hc, hh = int(match.group(1)), int(match.group(2))
        elif lines[2] == "Analysis inconclusive":
            status, hc, hh = "inconclusive", None, None
        else:
            raise ValueError(f"unexpected classification on page {page_number}")
        records.append({
            "page": page_number,
            "kaplan_status": status,
            "kaplan_hc": hc,
            "kaplan_hh": hh,
            "key": key,
        })
    if len(records) != 116:
        raise ValueError(f"expected 116 PDF records, got {len(records)}")
    return records


def latest_verdict(conn, shape_id: int, stage: str):
    row = conn.execute(
        "SELECT verdict, certificate FROM verdicts WHERE shape_id=? AND stage=? "
        "ORDER BY id DESC LIMIT 1",
        (shape_id, stage),
    ).fetchone()
    if row is None:
        return None
    return row[0], json.loads(row[1]) if row[1] else None


def main() -> None:
    records = parse_pdf()
    if len({record["key"] for record in records}) != 116:
        raise ValueError("Kaplan PDF contains duplicate canonical shapes")

    conn = sqlite3.connect(f"{DB.resolve().as_uri()}?mode=ro", uri=True)
    counts = {"hc1": 0, "hc2": 0, "periodic_anisohedral": 0, "hat": 0}
    for record in records:
        row = conn.execute(
            "SELECT id, n FROM shapes WHERE key=?", (record["key"],)
        ).fetchone()
        if row is None or row[1] != 8:
            raise ValueError(f"page {record['page']} has no repository 8-kite")
        shape_id = row[0]
        a1 = latest_verdict(conn, shape_id, "A1-torus")
        a2 = latest_verdict(conn, shape_id, "A2-heesch")
        record["shape_id"] = shape_id
        record["a1_verdict"] = a1[0] if a1 else None
        record["a2_verdict"] = a2[0] if a2 else None
        record["a2_depth"] = a2[1].get("depth") if a2 and a2[1] else None

        if record["kaplan_status"] == "nontiler":
            if not a1 or a1[0] != "no-periodic-at-budget":
                raise ValueError(f"page {record['page']} disagrees with A1")
            if not a2 or a2[0] != "heesch-exact":
                raise ValueError(f"page {record['page']} lacks exact A2 result")
            if record["a2_depth"] != record["kaplan_hc"]:
                raise ValueError(f"page {record['page']} disagrees on Hc")
            counts[f"hc{record['kaplan_hc']}"] += 1
            record["role"] = f"nontiler-hc{record['kaplan_hc']}"
        elif record["key"] == HAT_DB_KEY:
            if not a1 or a1[0] != "no-periodic-at-budget":
                raise ValueError("Hat page disagrees with A1")
            counts["hat"] += 1
            record["role"] = "hat"
        else:
            if not a1 or a1[0] != "periodic":
                raise ValueError(f"inconclusive page {record['page']} is not periodic")
            counts["periodic_anisohedral"] += 1
            record["role"] = "periodic-anisohedral"
    conn.close()

    expected = {"hc1": 108, "hc2": 5, "periodic_anisohedral": 2, "hat": 1}
    if counts != expected:
        raise ValueError(f"classification mismatch: {counts}")
    payload = {
        "kind": "kaplan-8kite-per-shape-crosswalk",
        "schema_version": 1,
        "source_id": "kaplan-8kites-2023",
        "source_sha256": EXPECTED_SHA256,
        "source_pages": 116,
        "conversion": "Kaplan point p maps to unique (p-origin[d], d) with a legal hex center",
        "counts": counts,
        "unique_bijection": True,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps({"unique_bijection": True, "counts": counts}))
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
