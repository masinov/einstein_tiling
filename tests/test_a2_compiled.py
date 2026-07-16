"""Compiled A2 first-corona screen must reproduce the n=8 census."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from einstein.funnel.a2_heesch import verify_heesch_certificate
from einstein.substrate.kitegrid import (
    canonical_form,
    cells_in_polygon,
    transform_cell,
)
from tests.test_hat import HAT_OUTLINE

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
    assert (
        "depth_cap=1 below_cap=720 witnessed=114 "
        "exhausted=0 survivors=114"
    ) in output
    rows = [json.loads(line) for line in witnesses.read_text().splitlines()]
    assert len(rows) == 114
    for row in rows:
        shape = _unpack_shape(row["shape"])
        corona = []
        for encoded_corona in row["coronas"]:
            corona.append([
                [
                    (cell[0] + tx, cell[1] + ty, cell[2])
                    for cell in (
                        transform_cell(original, op) for original in shape
                    )
                ]
                for op, tx, ty in encoded_corona
            ])
        assert verify_heesch_certificate(shape, corona)

    depth2_survivors = tmp_path / "depth2-survivors.bin"
    depth2_witnesses = tmp_path / "depth2-witnesses.jsonl"
    depth2_exhausted = tmp_path / "depth2-exhausted.bin"
    output = subprocess.run(
        [
            str(a2),
            str(a2_survivors),
            str(depth2_survivors),
            str(depth2_witnesses),
            str(depth2_exhausted),
            "2",
            "100000",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert (
        "depth_cap=2 below_cap=107 witnessed=6 "
        "exhausted=1 survivors=7"
    ) in output
    rows = [
        json.loads(line)
        for line in depth2_witnesses.read_text().splitlines()
    ]
    assert len(rows) == 6
    for row in rows:
        shape = _unpack_shape(row["shape"])
        chain = []
        for encoded_corona in row["coronas"]:
            chain.append([
                [
                    (cell[0] + tx, cell[1] + ty, cell[2])
                    for cell in (
                        transform_cell(original, op) for original in shape
                    )
                ]
                for op, tx, ty in encoded_corona
            ])
        assert len(chain) == 2
        assert verify_heesch_certificate(shape, chain)

    depth3_survivors = tmp_path / "depth3-survivors.bin"
    depth3_witnesses = tmp_path / "depth3-witnesses.jsonl"
    output = subprocess.run(
        [
            str(a2),
            str(depth2_survivors),
            str(depth3_survivors),
            str(depth3_witnesses),
            "-",
            "3",
            "1000000",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert (
        "depth_cap=3 below_cap=6 witnessed=1 "
        "exhausted=0 survivors=1"
    ) in output
    row = json.loads(depth3_witnesses.read_text())
    shape = _unpack_shape(row["shape"])
    assert canonical_form(shape) == canonical_form(
        cells_in_polygon(HAT_OUTLINE)
    )
    chain = []
    for encoded_corona in row["coronas"]:
        chain.append([
            [
                (cell[0] + tx, cell[1] + ty, cell[2])
                for cell in (
                    transform_cell(original, op) for original in shape
                )
            ]
            for op, tx, ty in encoded_corona
        ])
    assert len(chain) == 3
    assert verify_heesch_certificate(shape, chain)
