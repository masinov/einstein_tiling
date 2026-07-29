"""Pins for nested—not merely independent—growth of the E1 finalist."""

import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.polykites.patches import (
    certificate_cells,
    verify_patch_certificate,
)
from einstein.geometry.kite_grid import cell_centroid4, norm2

ROOT = repository_root(Path(__file__))
RESULTS = ROOT / "docs/notebook/assets/e1-finalist-nested.json"


def _frozen(shape, certificate, cutoff_r2):
    return [
        placement
        for placement, group in zip(
            certificate["placements"],
            certificate_cells(shape, certificate),
        )
        if max(norm2(cell_centroid4(cell)) for cell in group)
        <= 16 * cutoff_r2
    ]


def test_finalist_has_verified_growing_nested_cores():
    payload = json.loads(RESULTS.read_text())
    assert payload["full_crown_extension"] == {
        "from_r2": 12_800,
        "to_r2": 16_000,
        "patches_tested": 5,
        "refuted": 5,
        "unknown": 0,
    }
    shape = decode_compiled_key(payload["candidate"]["shape"])
    steps = payload["nested_chain"]
    assert [step["target_r2"] for step in steps] == [50_000, 100_000]
    previous = next(
        row["certificate"]
        for row in json.loads(
            (ROOT / "docs/notebook/assets/e1-finalist-robustness.json").read_text()
        )["results"]
        if row["phase_seed"] == 1
    )
    for step in steps:
        outer = step["certificate"]
        assert verify_patch_certificate(shape, outer)
        frozen = _frozen(shape, previous, step["frozen_cutoff_r2"])
        assert len(frozen) == step["frozen_placements"]
        assert {tuple(row) for row in frozen} <= {
            tuple(row) for row in outer["placements"]
        }
        previous = outer
    diffraction = payload["nested_outer_diffraction"]["result"]
    assert diffraction["n_points"] == 18_386
    assert diffraction["rank"] == 4
    assert diffraction["symmetry"] == 6
    assert diffraction["verdict"] == "quasicrystal-candidate"
    svg = (
        ROOT / "docs/notebook/assets/e1-finalist-nested-cores.svg"
    ).read_text()
    assert svg.count("<polygon ") == 9_235 + 18_386
    assert svg.count('fill="#51cf66"') == 1_576 + 5_317
