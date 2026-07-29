"""D-0005 cross-validation of the vendored spectre generator + our
rank-4 module port (einstein.geometry.cyclotomic).

Three independent artifacts must agree:
  1. vendor/spectre/ref_leaves_n3_delta.json -- leaf poses from the
     *reference float algorithm* (upstream's port of the SMKGS
     supplementary generator),
  2. tests/data/spectre-anchors-n3-delta.csv -- exact integer identities
     emitted by the vendored Rust traversal (our anchors binary),
  3. our own Python module12 projection of those integers.

Agreement means the Rust generator's exact output, projected by *our*
math, reproduces the published-algorithm float coordinates -- the vendored
code is then trusted as reference/calibration data (never as evidence
about candidate shapes).
"""

import csv
import json
from pathlib import Path

from einstein.geometry.cyclotomic import apply_sr, mirror_y, rot30, to_xy

VENDOR = Path(__file__).parent.parent / "vendor" / "spectre"
FIXTURE = Path(__file__).parent / "data" / "spectre-anchors-n3-delta.csv"

LABELS = ["Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi"]
RULES = {
    "Gamma":  ["Pi", "Delta", None, "Theta", "Sigma", "Xi", "Phi", "Gamma"],
    "Delta":  ["Xi", "Delta", "Xi", "Phi", "Sigma", "Pi", "Phi", "Gamma"],
    "Theta":  ["Psi", "Delta", "Pi", "Phi", "Sigma", "Pi", "Phi", "Gamma"],
    "Lambda": ["Psi", "Delta", "Xi", "Phi", "Sigma", "Pi", "Phi", "Gamma"],
    "Xi":     ["Psi", "Delta", "Pi", "Phi", "Sigma", "Psi", "Phi", "Gamma"],
    "Pi":     ["Psi", "Delta", "Xi", "Phi", "Sigma", "Psi", "Phi", "Gamma"],
    "Sigma":  ["Xi", "Delta", "Xi", "Phi", "Sigma", "Pi", "Lambda", "Gamma"],
    "Phi":    ["Psi", "Delta", "Psi", "Phi", "Sigma", "Pi", "Phi", "Gamma"],
    "Psi":    ["Psi", "Delta", "Psi", "Phi", "Sigma", "Psi", "Phi", "Gamma"],
}
# anchors.csv kind: 0=Gamma1, 1=Gamma2, then Delta..Psi shifted by one
KIND_TO_LABEL = ["Gamma1", "Gamma2"] + LABELS[1:]


def _fixture_rows():
    with open(FIXTURE) as f:
        return [
            (int(r["kind"]), int(r["s"]), int(r["r"]),
             (int(r["t0"]), int(r["t1"]), int(r["t2"]), int(r["t3"])))
            for r in csv.DictReader(f)
        ]


def test_module_ops_orders():
    vs = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (3, -2, 5, 7)]
    for v in vs:
        w = v
        for _ in range(12):
            w = rot30(w)
        assert w == v  # rot30 has order 12
        assert mirror_y(mirror_y(v)) == v
        # projection consistency: rot30 really rotates by 30 degrees
        import math
        x, y = to_xy(v)
        xr, yr = to_xy(rot30(v))
        c, s = math.cos(math.pi / 6), math.sin(math.pi / 6)
        assert abs(xr - (c * x - s * y)) < 1e-12
        assert abs(yr - (s * x + c * y)) < 1e-12
        xm, ym = to_xy(mirror_y(v))
        assert abs(xm + x) < 1e-12 and abs(ym - y) < 1e-12


def test_anchor_dump_matches_reference_float_leaves():
    ref = json.load(open(VENDOR / "ref_leaves_n3_delta.json"))
    rows = _fixture_rows()
    assert len(ref) == len(rows) == 559
    # multiset match on (label, s, r, x, y) with x, y from OUR projection
    def key(lab, s, r, x, y):
        return (lab, s, r, round(x, 6), round(y, 6))

    ref_keys = sorted(
        key(d["label"] if d["label"] not in ("Gamma1", "Gamma2") else d["label"],
            d["s"], d["r"], d["x"], d["y"])
        for d in ref
    )
    got_keys = sorted(
        key(KIND_TO_LABEL[kind], s, r, *to_xy(t)) for kind, s, r, t in rows
    )
    assert ref_keys == got_keys


def test_single_chirality():
    # spectre tilings use one chirality only: every leaf carries the same
    # mirror flag (the substitution flips parity once per level, uniformly)
    rows = _fixture_rows()
    assert len({s for _, s, _, _ in rows}) == 1


def test_counts_match_substitution_recurrence():
    cnt = {lab: (2 if lab == "Gamma" else 1) for lab in LABELS}
    seq = [cnt["Delta"]]
    for _ in range(8):
        cnt = {lab: sum(cnt[s] for s in RULES[lab] if s) for lab in RULES}
        seq.append(cnt["Delta"])
    # against vendored TILE_COUNTS (tables.rs) and the fixture
    assert seq == [1, 9, 71, 559, 4401, 34649, 272791, 2147679, 16908641]
    assert len(_fixture_rows()) == seq[3]
