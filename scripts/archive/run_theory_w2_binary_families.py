#!/usr/bin/env python
"""Compose W1 period certificates into W2 binary quotient families."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.polykites.database import code_version
from einstein.polykites.periodic_quotients import sublattices
from einstein.periodicity.binary_families import (
    finalist_thin_family_orbit,
    lattice_norm2,
    quotient_period_obstruction,
    verify_finalist_thin_family_orbit,
    verify_quotient_period_obstruction,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "notebook" / "assets" / "theory-w2-binary-families.json"
W1_FILES = (
    ROOT / "docs/notebook/assets/theory-w1-finalist-norm25.json",
    ROOT / "docs/notebook/assets/theory-w1-finalist-norm26-36.json",
)


def load_excluded_vectors():
    vectors = set()
    provenance = []
    for path in W1_FILES:
        payload = json.loads(path.read_text())
        if not payload["summary"]["complete_requested_range"]:
            raise AssertionError(f"incomplete W1 dependency: {path}")
        if payload["summary"]["resource_exhaustions"]:
            raise AssertionError(f"exhausted W1 dependency: {path}")
        for orbit in payload["orbits"]:
            if orbit["verdict"] != "cycle-free" or not orbit["independently_verified"]:
                raise AssertionError(f"unverified W1 orbit in {path}")
            vectors.update(tuple(vector) for vector in orbit["orbit"])
        provenance.append({
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "vectors_covered": payload["summary"]["vectors_covered"],
        })
    if len(vectors) != 126 or max(map(lattice_norm2, vectors)) != 36:
        raise AssertionError("W1 dependencies do not cover the expected norm ball")
    return tuple(sorted(vectors)), provenance


def main():
    vectors, dependencies = load_excluded_vectors()

    complete_prefix = []
    first_survivors = None
    for index in range(1, 38):
        results = []
        for hnf in sublattices(index):
            certificate = quotient_period_obstruction(hnf, vectors)
            if certificate and not verify_quotient_period_obstruction(certificate):
                raise AssertionError(f"bad composed certificate {hnf}")
            results.append({"hnf": list(hnf), "certificate": certificate})
        survivors = [row for row in results if row["certificate"] is None]
        if survivors and first_survivors is None:
            first_survivors = {"index": index, "hnfs": [row["hnf"] for row in survivors]}
        complete_prefix.append({
            "index": index,
            "hnfs": len(results),
            "killed": len(results) - len(survivors),
            "surviving": len(survivors),
        })

    admissible = []
    killed = 0
    total = 0
    for index in range(5, 216, 5):
        rows = []
        for hnf in sublattices(index):
            certificate = quotient_period_obstruction(hnf, vectors)
            if certificate and not verify_quotient_period_obstruction(certificate):
                raise AssertionError(f"bad composed certificate {hnf}")
            rows.append({"hnf": list(hnf), "certificate": certificate})
        count = sum(row["certificate"] is not None for row in rows)
        killed += count
        total += len(rows)
        admissible.append({
            "index": index,
            "hnfs": len(rows),
            "killed_by_period_family": count,
            "surviving": len(rows) - count,
            "results": rows,
        })

    thin_checks = []
    for index in range(4, 1001):
        certificate = finalist_thin_family_orbit(index)
        if not verify_finalist_thin_family_orbit(index, certificate):
            raise AssertionError(f"bad thin orbit certificate at {index}")
        if index in (4, 5, 10, 100, 1000):
            thin_checks.append({"index": index, "certificate": certificate})

    source = ROOT / "src/einstein/periodicity/binary_families.py"
    payload = {
        "kind": "theory-w2-binary-period-families",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "geometric_scope": "grid-aligned finalist tilings",
            "binary_basis": (
                "complete W1 transfer graphs exclude each period vector; "
                "every quotient lattice containing that vector is excluded"
            ),
            "family_formula": (
                "for HNF (a,b,d) and v=(x,y): d divides y and "
                "a divides x-(y/d)b"
            ),
            "failure_polarity": (
                "a missing bounded-period certificate says only that this "
                "family class does not decide the quotient"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "source": str(source.relative_to(ROOT)),
            "source_sha256": sha256(source.read_bytes()).hexdigest(),
            "w1_dependencies": dependencies,
        },
        "period_vectors": [list(vector) for vector in vectors],
        "universal_prefix": {
            "complete_through_index": 36,
            "by_index": complete_prefix,
            "first_unresolved": first_survivors,
        },
        "admissible_horizon": {
            "maximum_index": 215,
            "area_admissible_step": 5,
            "hnfs": total,
            "killed_by_period_family": killed,
            "surviving_this_certificate_class": total - killed,
            "by_index": admissible,
        },
        "thin_orbit_theorem": {
            "statement": (
                "T2.C1 extends by exact D6 maps to HNF (1,0,k), (k,0,1), "
                "and (k,k-1,1) for every k>=4"
            ),
            "regression_range": [4, 1000],
            "sample_certificates": thin_checks,
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({
        "period_vectors": len(vectors),
        "universal_prefix": payload["universal_prefix"],
        "admissible_horizon": {
            key: value for key, value in payload["admissible_horizon"].items()
            if key != "by_index"
        },
    }, indent=1))


if __name__ == "__main__":
    main()
