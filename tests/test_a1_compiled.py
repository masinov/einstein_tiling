"""Compiled A1 must reproduce and certify the n=8 Myers anchor."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from einstein.enumeration.polyform import read_compiled_polykites
from einstein.funnel.a1_torus import verify_certificate

ROOT = Path(__file__).parent.parent


def _compile(rustc, source, output):
    subprocess.run(
        [
            rustc,
            "--edition=2021",
            "-C",
            "opt-level=3",
            str(ROOT / source),
            "-o",
            str(output),
        ],
        check=True,
    )


def _unpack_shape(key):
    cells = []
    for offset in range(0, len(key), 4):
        code = int(key[offset:offset + 4], 16)
        cells.append((
            2 * ((code >> 9) & 63),
            2 * (((code >> 3) & 63) - 32),
            code & 7,
        ))
    return tuple(cells)


def test_compiled_a1_matches_n8_anchor_and_certifies_positives(tmp_path):
    rustc = shutil.which("rustc")
    if rustc is None:
        pytest.skip("rustc is not installed")
    a0 = tmp_path / "a0"
    a1 = tmp_path / "a1"
    _compile(rustc, "tools/a0_polykites.rs", a0)
    _compile(rustc, "tools/a1_torus.rs", a1)
    dump = tmp_path / "dump"
    subprocess.run([str(a0), "8", str(dump)], check=True)
    survivors = tmp_path / "survivors.bin"
    certificates = tmp_path / "periodic.jsonl"
    output = subprocess.run(
        [
            str(a1),
            str(dump / "polykites-08.bin"),
            str(survivors),
            str(certificates),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert "periodic=39 survivors=834 exhausted=0" in output
    assert sum(1 for _ in read_compiled_polykites(survivors)) == 834
    rows = [json.loads(line) for line in certificates.read_text().splitlines()]
    assert len(rows) == 39
    for row in rows:
        assert verify_certificate(
            _unpack_shape(row["shape"]),
            {
                "hnf": row["hnf"],
                "placements": row["placements"],
            },
        )
