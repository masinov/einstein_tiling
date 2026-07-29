from __future__ import annotations

import gzip

import pytest
from pysat.formula import CNF

from einstein.solvers.cnf_certificates import (
    clause_hash,
    gzip_deterministic,
    parse_dimacs_clauses,
    verify_clause_model,
)


def test_sparse_clause_model_verification_is_exact():
    cnf = CNF(from_clauses=[[1, -2], [2, 3]])
    assert verify_clause_model(cnf, {1, 2})
    assert not verify_clause_model(cnf, {2})
    assert not verify_clause_model(cnf, {1, cnf.nv + 1})


def test_dimacs_parser_handles_continuations_and_rejects_truncation():
    value = b"c comment\np cnf 3 2\n3 -1\n2 0\n-2 0\n"
    assert parse_dimacs_clauses(value) == [(-1, 2, 3), (-2,)]
    with pytest.raises(ValueError, match="unterminated"):
        parse_dimacs_clauses(b"p cnf 1 1\n1\n")


def test_clause_hash_and_gzip_are_deterministic(tmp_path):
    cnf = CNF(from_clauses=[[1, -2], [2]])
    assert clause_hash(cnf) == clause_hash(cnf)
    source = tmp_path / "source"
    source.write_bytes(b"exact certificate\n")
    left, right = tmp_path / "left.gz", tmp_path / "right.gz"
    gzip_deterministic(source, left)
    gzip_deterministic(source, right)
    assert left.read_bytes() == right.read_bytes()
    assert gzip.decompress(left.read_bytes()) == source.read_bytes()
