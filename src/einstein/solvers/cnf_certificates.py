"""Reusable exact primitives for CNF witness and DRAT certificate handling."""

from __future__ import annotations

import gzip
from hashlib import sha256
from pathlib import Path


def clause_hash(cnf) -> str:
    """Hash a CNF's ordered clause stream in DIMACS body form."""

    digest = sha256()
    for clause in cnf.clauses:
        digest.update(" ".join(map(str, clause)).encode())
        digest.update(b" 0\n")
    return digest.hexdigest()


def parse_dimacs_clauses(value: bytes, *, sort_literals: bool = True):
    """Parse DIMACS bytes, including clauses continued across lines."""

    clauses = []
    pending = []
    for raw_line in value.decode().splitlines():
        if not raw_line or raw_line[0] in "cp":
            continue
        for token in map(int, raw_line.split()):
            if token:
                pending.append(token)
                continue
            clause = tuple(sorted(pending)) if sort_literals else tuple(pending)
            clauses.append(clause)
            pending = []
    if pending:
        raise ValueError("unterminated DIMACS clause")
    return clauses


def read_dimacs_clauses(path: Path, *, sort_literals: bool = True):
    return parse_dimacs_clauses(
        path.read_bytes(), sort_literals=sort_literals
    )


def gzip_deterministic(source: Path, target: Path) -> None:
    """Compress an artifact reproducibly (empty filename, epoch mtime)."""

    with source.open("rb") as input_file, target.open("wb") as raw_output:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw_output, mtime=0
        ) as output:
            while chunk := input_file.read(1024 * 1024):
                output.write(chunk)


def verify_clause_model(cnf, true_variables) -> bool:
    """Evaluate every CNF clause under a sparse set of true variables."""

    truth = frozenset(true_variables)
    if any(variable <= 0 or variable > cnf.nv for variable in truth):
        return False
    return all(
        any(
            literal in truth if literal > 0 else -literal not in truth
            for literal in clause
        )
        for clause in cnf.clauses
    )
