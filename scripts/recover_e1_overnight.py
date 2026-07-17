#!/usr/bin/env python
"""Normalize the interrupted 2026-07-17 E1 overnight campaign logs.

The machine lost power after the screen jobs had run for several hours.  Raw
logs are append-only evidence, but two contain terminal escape sequences and
none contains a campaign-level summary.  This script parses only explicit
``refuted`` completion lines, records source hashes, and deliberately makes no
claim about work that had not emitted a completion line.

Usage:
    venv/bin/python scripts/recover_e1_overnight.py
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs" / "overnight-2026-07-17"
OUT = ROOT / "docs" / "notebook" / "assets" / "e1-overnight-recovered.json"
HIERARCHY = (
    ROOT / "docs" / "notebook" / "assets" / "e1-finalist-hierarchy-screen.json"
)

ANSI = re.compile(rb"\x1b\[[0-?]*[ -/]*[@-~]")
GENERIC = re.compile(r"k=\s*(\d+): refuted \(([0-9.]+)s\)")
PERIOD47 = re.compile(r"a=\s*(\d+) index=\s*(\d+): refuted \(([0-9.]+)s\)")
RETURN = re.compile(
    r"hnf=\((\d+),\s*(\d+),\s*(\d+)\) index=(\d+): refuted \(([0-9.]+)s\)"
)


def read_clean(path: Path) -> str:
    return ANSI.sub(b"", path.read_bytes()).decode("utf-8", errors="replace")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hnf_count(index: int) -> int:
    """Number of 2D HNFs of determinant ``index``: sigma_1(index)."""
    return sum(d for d in range(1, index + 1) if index % d == 0)


def main() -> None:
    paths = {
        "generic_tori": LOG_DIR / "generic_tori.log",
        "period47": LOG_DIR / "period47.log",
        "return_lattices": LOG_DIR / "return_lattices.log",
        "hierarchy": LOG_DIR / "hierarchy.log",
    }

    generic = [
        {
            "index": int(k),
            "hnf_quotients": hnf_count(int(k)),
            "elapsed_seconds": float(seconds),
            "verdict": "refuted",
        }
        for k, seconds in GENERIC.findall(read_clean(paths["generic_tori"]))
    ]
    period47 = [
        {
            "transverse_width": int(a),
            "index": int(index),
            "elapsed_seconds": float(seconds),
            "verdict": "refuted",
        }
        for a, index, seconds in PERIOD47.findall(read_clean(paths["period47"]))
    ]
    returns = [
        {
            "hnf": [int(a), int(b), int(d)],
            "index": int(index),
            "elapsed_seconds": float(seconds),
            "verdict": "refuted",
        }
        for a, b, d, index, seconds in RETURN.findall(
            read_clean(paths["return_lattices"])
        )
    ]

    hierarchy = json.loads(HIERARCHY.read_text())
    generic_quotients = sum(row["hnf_quotients"] for row in generic)
    targeted_quotients = len(period47) + len(returns)

    result = {
        "kind": "interrupted-campaign-recovery",
        "date": "2026-07-17",
        "candidate": hierarchy["candidate"],
        "provenance": {
            "cause": "host power loss terminated all screen sessions",
            "policy": (
                "Only explicit completed/refuted log lines are counted. "
                "Started or planned jobs without such a line remain unknown."
            ),
            "sources": {
                name: {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path),
                }
                for name, path in paths.items()
            }
            | {
                "hierarchy_artifact": {
                    "path": str(HIERARCHY.relative_to(ROOT)),
                    "sha256": sha256(HIERARCHY),
                }
            },
        },
        "periodicity": {
            "generic_indices": generic,
            "generic_indices_completed": len(generic),
            "generic_hnf_quotients_refuted": generic_quotients,
            "period47_targeted_quotients": period47,
            "return_scale_targeted_quotients": returns,
            "targeted_quotients_refuted": targeted_quotients,
            "completed_quotient_instances_refuted": (
                generic_quotients + targeted_quotients
            ),
            "periodic_certificates_found": 0,
            "campaign_complete": False,
            "claim": (
                "All explicitly completed quotient instances are exact UNSAT; "
                "this finite evidence neither proves aperiodicity nor classifies "
                "unreturned jobs."
            ),
        },
        "hierarchy": {
            "campaign_complete": True,
            "rules_screened": hierarchy["screened"]["rules"],
            "coverage_rejects": hierarchy["screened"]["coverage_rejects"],
            "sat_rejects": hierarchy["screened"]["sat_rejects"],
            "first_composition_rules_accepted": hierarchy["screened"]["accepted"],
            "accepted_rules_all_unique": all(
                row["all_unique"] for row in hierarchy["accepted"]
            ),
            "general_physical_library_closed": any(
                row["fit"]["satisfiable"]
                for row in hierarchy["general_physical_library"][
                    "single_arity_fits"
                ]
            ),
            "recursive_probe": hierarchy["rule_family"]["next_recursive_probe"],
            "claim": hierarchy["rule_family"]["proof_status"],
        },
    }

    OUT.write_text(json.dumps(result, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(
        f"completed quotient instances: {generic_quotients} generic + "
        f"{targeted_quotients} targeted = {generic_quotients + targeted_quotients}"
    )


if __name__ == "__main__":
    main()
