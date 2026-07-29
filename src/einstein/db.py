"""Mutable shape stores and read-only access to immutable database fixtures.

Content-addressed by canonical form. Every funnel verdict is stored with its
certificate, budget, and code version, so any claim resolves to a database
row plus a rerunnable job. Negative results are first-class data.

SQLite is deliberate for v0: zero services and inspectable with standard
tools. Mutable runs use a workspace path under data/. Versioned snapshots must
be opened with ``read_only=True`` from the fixture namespace.
"""

from __future__ import annotations

import json
import sqlite3
import subprocess
import time
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS shapes (
    id       INTEGER PRIMARY KEY,
    key      TEXT NOT NULL UNIQUE,   -- canonical form, serialized
    n        INTEGER NOT NULL,       -- cell count
    substrate TEXT NOT NULL DEFAULT 'kite'
);
CREATE TABLE IF NOT EXISTS verdicts (
    id          INTEGER PRIMARY KEY,
    shape_id    INTEGER NOT NULL REFERENCES shapes(id),
    stage       TEXT NOT NULL,       -- e.g. 'A1-torus'
    verdict     TEXT NOT NULL,       -- e.g. 'periodic', 'no-periodic-at-budget'
    certificate TEXT,                -- JSON; machine-verified before storage
    budget      TEXT,                -- JSON description of resource bounds used
    code_version TEXT,
    created_at  REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_shapes_n ON shapes(n);
CREATE INDEX IF NOT EXISTS idx_verdicts_shape ON verdicts(shape_id, stage);
"""


def serialize_cells(cells) -> str:
    return ";".join(f"{cx},{cy},{d}" for cx, cy, d in cells)


def deserialize_cells(key: str) -> tuple:
    return tuple(
        tuple(int(t) for t in part.split(",")) for part in key.split(";")
    )


def code_version() -> str:
    try:
        out = subprocess.run(
            ["git", "describe", "--always", "--dirty"],
            capture_output=True, text=True, cwd=Path(__file__).parent,
        )
        return out.stdout.strip() or "unknown"
    except OSError:
        return "unknown"


class ShapeDB:
    def __init__(self, path: str | Path, *, read_only: bool = False):
        self.path = Path(path)
        self.read_only = read_only
        if read_only:
            uri = f"{self.path.resolve().as_uri()}?mode=ro"
            self.conn = sqlite3.connect(uri, uri=True)
        else:
            self.conn = sqlite3.connect(str(self.path))
            self.conn.executescript(_SCHEMA)
        self._version = code_version()

    def close(self):
        self.conn.close()

    def add_shape(self, canonical_cells, substrate: str = "kite") -> int:
        """Insert (or find) a shape by its canonical form; returns shape id."""
        if self.read_only:
            raise RuntimeError(f"database fixture is read-only: {self.path}")
        key = serialize_cells(canonical_cells)
        cur = self.conn.execute(
            "INSERT INTO shapes(key, n, substrate) VALUES (?, ?, ?) "
            "ON CONFLICT(key) DO NOTHING",
            (key, len(canonical_cells), substrate),
        )
        if cur.lastrowid:
            row = cur.lastrowid
        else:
            row = self.conn.execute(
                "SELECT id FROM shapes WHERE key = ?", (key,)
            ).fetchone()[0]
        return row

    def record_verdict(self, shape_id: int, stage: str, verdict: str,
                       certificate=None, budget=None) -> None:
        if self.read_only:
            raise RuntimeError(f"database fixture is read-only: {self.path}")
        self.conn.execute(
            "INSERT INTO verdicts(shape_id, stage, verdict, certificate, "
            "budget, code_version, created_at) VALUES (?,?,?,?,?,?,?)",
            (
                shape_id, stage, verdict,
                json.dumps(certificate) if certificate is not None else None,
                json.dumps(budget) if budget is not None else None,
                self._version, time.time(),
            ),
        )

    def commit(self):
        if self.read_only:
            raise RuntimeError(f"database fixture is read-only: {self.path}")
        self.conn.commit()

    def latest_verdict(self, shape_id: int, stage: str):
        row = self.conn.execute(
            "SELECT verdict, certificate, budget FROM verdicts "
            "WHERE shape_id = ? AND stage = ? ORDER BY id DESC LIMIT 1",
            (shape_id, stage),
        ).fetchone()
        if row is None:
            return None
        return {
            "verdict": row[0],
            "certificate": json.loads(row[1]) if row[1] else None,
            "budget": json.loads(row[2]) if row[2] else None,
        }

    def verdict_counts(self, stage: str, n: int | None = None):
        q = ("SELECT v.verdict, COUNT(DISTINCT s.id) FROM shapes s "
             "JOIN verdicts v ON v.shape_id = s.id AND v.stage = ?")
        args: list = [stage]
        if n is not None:
            q += " WHERE s.n = ?"
            args.append(n)
        q += " GROUP BY v.verdict"
        return dict(self.conn.execute(q, args).fetchall())
