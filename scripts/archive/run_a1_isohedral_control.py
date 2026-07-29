#!/usr/bin/env python
"""Run Kaplan's isohedral-surround SAT control over all n<=8 polykites."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from einstein.db import serialize_cells
from einstein.e1_candidates import HAT_OUTLINE, TURTLE_OUTLINE
from einstein.enumeration.polyform import enumerate_free_polykites
from einstein.funnel.a1_isohedral import find_isohedral_surround
from einstein.funnel.a1_torus import find_periodic_tiling
from einstein.substrate.kitegrid import canonical_form, cells_in_polygon


ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT = ROOT / "docs/notebook/assets/a1-isohedral-control.json"
SVG = ROOT / "docs/notebook/assets/a1-isohedral-control.svg"
MYERS_ISOHEDRAL = {1: 1, 2: 1, 3: 4, 4: 4, 5: 0, 6: 70, 7: 52, 8: 37}
MYERS_PERIODIC = {1: 1, 2: 1, 3: 4, 4: 5, 5: 1, 6: 71, 7: 55, 8: 39}


def digest(keys) -> str:
    return hashlib.sha256(("\n".join(sorted(keys)) + "\n").encode()).hexdigest()


def render_svg(rows) -> str:
    width, height = 1050, 570
    left, right, top, bottom = 80, 990, 80, 420
    max_value = 75
    step = (right - left) / len(rows)
    bar_width = step * 0.62
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
        '<text x="525" y="34" text-anchor="middle" fill="#f0f6fc" font-family="sans-serif" font-size="22" font-weight="700">Isohedral-surround SAT control · complete polykite census n≤8</text>',
        '<text x="525" y="59" text-anchor="middle" fill="#8b949e" font-family="sans-serif" font-size="13">Kaplan Proposition 1 · observed counts equal Myers at every order</text>',
    ]
    for value in (0, 15, 30, 45, 60, 75):
        y = bottom - value / max_value * (bottom - top)
        lines.append(f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" stroke="#21262d"/>')
        lines.append(f'<text x="{left - 10}" y="{y + 4:.2f}" text-anchor="end" fill="#8b949e" font-family="monospace" font-size="11">{value}</text>')
    for offset, row in enumerate(rows):
        x = left + (offset + 0.5) * step
        iso = row["isohedral"]
        aniso = row["periodic_anisohedral"]
        iso_height = iso / max_value * (bottom - top)
        aniso_height = aniso / max_value * (bottom - top)
        lines.append(f'<rect x="{x - bar_width/2:.2f}" y="{bottom - iso_height:.2f}" width="{bar_width:.2f}" height="{iso_height:.2f}" fill="#3fb950"/>')
        lines.append(f'<rect x="{x - bar_width/2:.2f}" y="{bottom - iso_height - aniso_height:.2f}" width="{bar_width:.2f}" height="{aniso_height:.2f}" fill="#a371f7"/>')
        lines.append(f'<text x="{x:.2f}" y="{bottom + 24}" text-anchor="middle" fill="#f0f6fc" font-family="monospace" font-size="13">n={row["n"]}</text>')
        lines.append(f'<text x="{x:.2f}" y="{bottom - iso_height - aniso_height - 8:.2f}" text-anchor="middle" fill="#f0f6fc" font-family="monospace" font-size="12">{iso}+{aniso}</text>')
    lines.extend([
        '<rect x="280" y="468" width="16" height="16" fill="#3fb950"/><text x="305" y="481" fill="#c9d1d9" font-family="sans-serif" font-size="13">isohedral</text>',
        '<rect x="470" y="468" width="16" height="16" fill="#a371f7"/><text x="495" y="481" fill="#c9d1d9" font-family="sans-serif" font-size="13">periodic but anisohedral</text>',
        '<text x="525" y="521" text-anchor="middle" fill="#f2cc60" font-family="sans-serif" font-size="12">Hat excluded from n=8 periodic-anisohedral count; it is aperiodic.</text>',
        '<text x="525" y="548" text-anchor="middle" fill="#8b949e" font-family="monospace" font-size="11">full vertex halo · inverse closure · composition conflicts · simply-connected patch cuts</text>',
        '</svg>',
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    started = time.monotonic()
    rows = []
    positives = []
    negative_digests = {}
    shapes_by_n = {}
    for n, forms in enumerate_free_polykites(8):
        shapes_by_n[n] = forms
        positive_keys = []
        negative_keys = []
        for shape in forms:
            result = find_isohedral_surround(shape)
            assert not result["exhausted"]
            key = serialize_cells(shape)
            if result["isohedral"]:
                positive_keys.append(key)
                positives.append({
                    "n": n,
                    "key": key,
                    "certificate": result["certificate"],
                })
            else:
                negative_keys.append(key)
        observed = len(positive_keys)
        assert observed == MYERS_ISOHEDRAL[n]
        rows.append({
            "n": n,
            "shapes": len(forms),
            "isohedral": observed,
            "periodic_anisohedral": MYERS_PERIODIC[n] - observed,
            "myers_isohedral": MYERS_ISOHEDRAL[n],
            "positive_keys_sha256": digest(positive_keys),
            "negative_keys_sha256": digest(negative_keys),
        })
        negative_digests[str(n)] = digest(negative_keys)
        print(f"n={n}: {observed}/{len(forms)} isohedral", flush=True)

    anisohedral = []
    for shape in shapes_by_n[4]:
        if find_isohedral_surround(shape)["isohedral"]:
            continue
        certificate, exhausted = find_periodic_tiling(shape, k_max=12)
        assert not exhausted
        if certificate:
            anisohedral.append({
                "key": serialize_cells(shape),
                "periodic_certificate": certificate,
            })
    assert len(anisohedral) == 1

    hat = canonical_form(cells_in_polygon(HAT_OUTLINE))
    turtle = canonical_form(cells_in_polygon(TURTLE_OUTLINE))
    controls = {}
    for name, shape in (("hat", hat), ("turtle", turtle)):
        result = find_isohedral_surround(shape)
        assert result["isohedral"] is False
        controls[name] = {
            "key": serialize_cells(shape),
            "verdict": "not-isohedral",
            "stats": result["stats"],
        }

    payload = {
        "kind": "a1-isohedral-surround-control",
        "schema_version": 1,
        "source_id": "kaplan-isohedral-sat-2024",
        "scope": "grid-aligned polykites; isohedral tilings only",
        "criterion": "simply connected 1-patch with every neighbour extendable",
        "encoding": [
            "full vertex-halo exact cover",
            "pairwise placement conflicts",
            "inverse-neighbour closure",
            "direct composition-conflict clauses",
            "lazy hole cuts",
        ],
        "rows": rows,
        "positive_certificates": positives,
        "negative_key_digests": negative_digests,
        "periodic_anisohedral_control_n4": anisohedral[0],
        "aperiodic_controls": controls,
        "wall_seconds": round(time.monotonic() - started, 3),
        "verdict": "pass" if all(
            row["isohedral"] == row["myers_isohedral"] for row in rows
        ) else "fail",
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    SVG.write_text(render_svg(rows))
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    print(f"wrote {SVG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
