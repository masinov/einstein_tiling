"""Compiled A2 first-corona screen must reproduce the n=8 census."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from einstein.funnel.a2_heesch import verify_heesch_certificate
from einstein.substrate.kitegrid import transform_cell

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


def test_compiled_a2_matches_n8_h0_split_and_certifies_survivors(tmp_path):
    rustc = shutil.which("rustc")
    if rustc is None:
        pytest.skip("rustc is not installed")
    a0 = tmp_path / "a0"
    a1 = tmp_path / "a1"
    a2 = tmp_path / "a2"
    _compile(rustc, "tools/a0_polykites.rs", a0)
    _compile(rustc, "tools/a1_torus.rs", a1)
    _compile(rustc, "tools/a2_corona.rs", a2)
    dump = tmp_path / "dump"
    subprocess.run([str(a0), "8", str(dump)], check=True)
    a1_survivors = tmp_path / "a1-survivors.bin"
    subprocess.run(
        [
            str(a1),
            str(dump / "polykites-08.bin"),
            str(a1_survivors),
        ],
        check=True,
    )
    a2_survivors = tmp_path / "a2-survivors.bin"
    witnesses = tmp_path / "witnesses.jsonl"
    output = subprocess.run(
        [
            str(a2),
            str(a1_survivors),
            str(a2_survivors),
            str(witnesses),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert "h0=720 witnessed=114 exhausted=0 survivors=114" in output
    rows = [json.loads(line) for line in witnesses.read_text().splitlines()]
    assert len(rows) == 114
    for row in rows:
        shape = _unpack_shape(row["shape"])
        corona = []
        for op, tx, ty in row["placements"]:
            corona.append([
                (cell[0] + tx, cell[1] + ty, cell[2])
                for cell in (
                    transform_cell(original, op) for original in shape
                )
            ])
        assert verify_heesch_certificate(shape, [corona])
