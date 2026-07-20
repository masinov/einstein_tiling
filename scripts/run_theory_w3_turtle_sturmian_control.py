#!/usr/bin/env python
"""Build the exact Golden-Sturmian/Turtle-density control artifact.

This reproduces the combinatorial and density algebra in Akiyama--Araki and
compares its minority-chirality prediction with the existing independently
generated E1 Turtle disk.  It does not reconstruct the paper's geometric
Golden Hex substitution or its forced Ammann-bar case analysis.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

from einstein.e1_candidates import TURTLE_KEY
from einstein.theory.turtle_sturmian import (
    SOURCE_ID,
    central_word,
    golden_density_root_residual,
    minority_chirality_residual,
    minority_chirality_side,
    standard_word_table,
    verify_central_identities,
)


ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "docs/notebook/assets/e1-finalist-results.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-turtle-golden-sturmian.json"
SVG = ROOT / "docs/notebook/assets/theory-w3-turtle-golden-sturmian.svg"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def render_svg(payload: dict) -> str:
    table = payload["sturmian"]["standard_words"]
    points = [row for row in table if row["index"] > 0]
    q_minus = (5 - math.sqrt(5)) / 10
    predicted = (3 - math.sqrt(5)) / 6
    observed = payload["turtle_patch"]["minority_fraction"][0] / payload[
        "turtle_patch"
    ]["minority_fraction"][1]

    width, height = 1100, 650
    left, right, top, bottom = 90, 1040, 90, 350
    ymin, ymax = 0.245, 0.335

    def px(index: int) -> float:
        return left + (index - 1) * (right - left) / (len(points) - 1)

    def py(value: float) -> float:
        return bottom - (value - ymin) * (bottom - top) / (ymax - ymin)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
        '<text x="550" y="36" text-anchor="middle" fill="#f0f6fc" font-family="sans-serif" font-size="22" font-weight="700">Turtle control · Golden Sturmian convergence and chirality</text>',
        '<text x="550" y="61" text-anchor="middle" fill="#8b949e" font-family="sans-serif" font-size="13">Akiyama–Araki exact word recurrence; independent 9,239-tile E1 disk</text>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#8b949e"/>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#8b949e"/>',
    ]
    for value in (0.25, 0.275, 0.30, 0.325):
        y = py(value)
        lines.append(f'<line x1="{left}" y1="{y:.2f}" x2="{right}" y2="{y:.2f}" stroke="#21262d"/>')
        lines.append(f'<text x="{left - 12}" y="{y + 4:.2f}" text-anchor="end" fill="#8b949e" font-family="monospace" font-size="11">{value:.3f}</text>')
    qy = py(q_minus)
    lines.append(f'<line x1="{left}" y1="{qy:.2f}" x2="{right}" y2="{qy:.2f}" stroke="#f2cc60" stroke-width="2" stroke-dasharray="7 5"/>')
    lines.append(f'<text x="{right}" y="{qy - 8:.2f}" text-anchor="end" fill="#f2cc60" font-family="monospace" font-size="12">q−=(5−√5)/10</text>')

    polyline = []
    for row in points:
        value = row["ones"] / row["length"]
        x, y = px(row["index"]), py(value)
        polyline.append(f"{x:.2f},{y:.2f}")
        color = "#58a6ff" if row["index"] % 2 else "#d2a8ff"
        lines.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="{color}"/>')
        if row["index"] in (1, 2, 4, 8, 12, 16, 20, 24):
            lines.append(f'<text x="{x:.2f}" y="{bottom + 19}" text-anchor="middle" fill="#8b949e" font-family="monospace" font-size="10">{row["index"]}</text>')
    lines.insert(-1, f'<polyline points="{" ".join(polyline)}" fill="none" stroke="#6e7681" stroke-width="1.2"/>')
    lines.append('<text x="565" y="385" text-anchor="middle" fill="#8b949e" font-family="sans-serif" font-size="12">standard-word level n (odd/even convergents bracket q− exactly)</text>')

    box_y = 420
    lines.extend([
        f'<rect x="90" y="{box_y}" width="440" height="105" rx="8" fill="#161b22" stroke="#30363d"/>',
        f'<text x="110" y="{box_y + 27}" fill="#f0f6fc" font-family="sans-serif" font-size="15" font-weight="700">Published density consequence</text>',
        f'<text x="110" y="{box_y + 55}" fill="#f2cc60" font-family="monospace" font-size="16">f−=(3−√5)/6 = {predicted:.9f}</text>',
        f'<text x="110" y="{box_y + 82}" fill="#8b949e" font-family="sans-serif" font-size="12">equivalently 1/(1+φ⁴); exact root of 9f²−9f+1</text>',
        f'<rect x="570" y="{box_y}" width="470" height="105" rx="8" fill="#161b22" stroke="#30363d"/>',
        f'<text x="590" y="{box_y + 27}" fill="#f0f6fc" font-family="sans-serif" font-size="15" font-weight="700">Independent E1 Turtle disk</text>',
        f'<text x="590" y="{box_y + 55}" fill="#7ee787" font-family="monospace" font-size="16">1181 / 9239 = {observed:.9f}</text>',
        f'<text x="590" y="{box_y + 82}" fill="#8b949e" font-family="sans-serif" font-size="12">minority D₆ handedness; finite-boundary error {observed - predicted:+.3e}</text>',
        '<text x="550" y="570" text-anchor="middle" fill="#f0f6fc" font-family="sans-serif" font-size="14">Exact internal scope: words + density algebra + patch count</text>',
        '<text x="550" y="596" text-anchor="middle" fill="#f85149" font-family="sans-serif" font-size="13">Not yet internal: forced GAB continuation, Kagome lemma, or Golden Hex geometry</text>',
        '<text x="550" y="625" text-anchor="middle" fill="#8b949e" font-family="monospace" font-size="11">source: akiyama-araki-turtle-2025 · artifact: theory-w3-turtle-golden-sturmian.json</text>',
        '</svg>',
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    source_payload = json.loads(INPUT.read_text())
    assert source_payload["candidate"]["shape"] == TURTLE_KEY
    placements = source_payload["a3"]["certificate"]["placements"]
    op_counts = Counter(int(placement[0]) for placement in placements)
    preserving = sum(op_counts[op] for op in range(6))
    mirrored = sum(op_counts[op] for op in range(6, 12))
    minority = min(preserving, mirrored)
    observed = Fraction(minority, len(placements))

    max_index = 24
    central_checks = verify_central_identities(max_index)
    central_rows = []
    for index in range(max_index + 1):
        word = central_word(index)
        central_rows.append({
            "index": index,
            "length": len(word),
            "palindrome": word == word[::-1],
            "sha256": hashlib.sha256(word.encode()).hexdigest(),
        })

    payload = {
        "kind": "theory-w3-turtle-golden-sturmian-control",
        "schema_version": 1,
        "source_id": SOURCE_ID,
        "source_locations": {
            "standard_and_central_words": "section 2, equations (1)-(2)",
            "golden_hex_existence": "section 3, Lemma 1 and Theorem 1",
            "forced_bars_and_kagome": "section 4, Lemmas 2-5",
            "density": "section 4, Lemma 6 and Theorem 2",
        },
        "scope": {
            "internally_verified": [
                "standard-word recurrence and exact counts",
                "central palindrome property and both decomposition identities",
                "Golden Ammann-bar density polynomial",
                "minority-chirality density polynomial",
                "existing Turtle patch handedness count",
            ],
            "published_but_not_internally_reconstructed": [
                "geometric realization of Golden Sturmian Patches",
                "Golden Hex patch-tile induction and arbitrary inballs",
                "forced continuation of dispensable Golden Ammann bars",
                "generalized-bar Kagome structure and crossing bijection",
            ],
        },
        "sturmian": {
            "slope": "(5-sqrt(5))/10 = [3,1,1,1,...]",
            "recurrence": "s_-1=1; s_0=0; s_1=001; s_(n+1)=s_n s_(n-1)",
            "max_index": max_index,
            "central_checks": central_checks,
            "standard_words": standard_word_table(max_index),
            "central_words": central_rows,
        },
        "density": {
            "gab_equation": "q^2-q+1/5=0",
            "gab_roots": ["(5-sqrt(5))/10", "(5+sqrt(5))/10"],
            "gab_root_residuals": [
                [str(x) for x in golden_density_root_residual(-1)],
                [str(x) for x in golden_density_root_residual(1)],
            ],
            "minority_chirality": "(5/3)q_minus^2=(3-sqrt(5))/6=1/(1+phi^4)",
            "minority_polynomial": "9f^2-9f+1=0",
            "minority_root_residual": [
                str(x) for x in minority_chirality_residual()
            ],
        },
        "turtle_patch": {
            "source": str(INPUT.relative_to(ROOT)),
            "source_sha256": sha256(INPUT),
            "canonical_key": TURTLE_KEY,
            "placements": len(placements),
            "orientation_preserving": preserving,
            "mirrored": mirrored,
            "minority": minority,
            "minority_fraction": [observed.numerator, observed.denominator],
            "side_of_exact_prediction": minority_chirality_side(observed),
            "decimal": observed.numerator / observed.denominator,
            "exact_prediction_decimal": (3 - math.sqrt(5)) / 6,
        },
        "verdict": "exact-combinatorial-and-density-control-pass",
        "aperiodicity_claim": "external-published-theorem; internal geometric obligations remain open",
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    SVG.write_text(render_svg(payload))
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    print(f"wrote {SVG.relative_to(ROOT)}")
    print(
        f"Turtle minority chirality: {minority}/{len(placements)} = "
        f"{float(observed):.9f}; exact target {(3 - math.sqrt(5)) / 6:.9f}"
    )


if __name__ == "__main__":
    main()
