"""Compiled A0 must reproduce the Python/OEIS census and stream its forms."""

import shutil
import subprocess
from pathlib import Path

import pytest

from einstein.polykites.enumeration import (
    OEIS_A057786,
    read_compiled_polykites,
)
from einstein.geometry.kite_grid import canonical_form

ROOT = Path(__file__).parent.parent


def test_compiled_a0_matches_oeis_and_binary_roundtrip(tmp_path):
    rustc = shutil.which("rustc")
    if rustc is None:
        pytest.skip("rustc is not installed")
    binary = tmp_path / "a0_polykites"
    subprocess.run(
        [
            rustc,
            "--edition=2021",
            "-C",
            "opt-level=3",
            str(ROOT / "tools" / "a0_polykites.rs"),
            "-o",
            str(binary),
        ],
        check=True,
    )
    dump = tmp_path / "dump"
    output = subprocess.run(
        [str(binary), "10", str(dump)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    counts = [int(line.split()[1]) for line in output.splitlines()]
    assert counts == OEIS_A057786[:10]
    forms = list(read_compiled_polykites(dump / "polykites-08.bin"))
    assert len(forms) == OEIS_A057786[7]
    assert len(set(forms)) == len(forms)
    assert all(len(form) == 8 and form == tuple(sorted(form)) for form in forms)
    assert all(canonical_form(form) == form for form in forms)
