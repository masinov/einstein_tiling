"""Exact colored Spectre parent-interface controls."""

import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.tilings.spectre.colored_interfaces import (
    colored_corona_from_json,
    colored_local_overlap_witnesses,
    colored_reciprocal_domains,
    prune_colored_unsupported,
    reciprocal_color,
)


ROOT = repository_root(Path(__file__))
ARTIFACT = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"


def test_contact_color_reversal_is_an_involution():
    color = (2, 11, 7, 3)
    assert reciprocal_color(reciprocal_color(color)) == color


def test_generated_colored_language_is_locally_self_supporting():
    artifact = json.loads(ARTIFACT.read_text())
    states = tuple(map(
        colored_corona_from_json, artifact["generated_colored_states"],
    ))
    assert len(states) == 17
    assert all(all(domain for domain in colored_reciprocal_domains(states, i))
               for i in range(len(states)))
    assert all(colored_local_overlap_witnesses(states, i, limit=1)
               for i in range(len(states)))
    assert prune_colored_unsupported(states) == (tuple(range(17)), ())


def test_generated_one_sided_language_is_locally_self_supporting():
    artifact = json.loads(ARTIFACT.read_text())
    states = tuple(map(
        colored_corona_from_json, artifact["generated_one_sided_states"],
    ))
    assert len(states) == 17
    assert all(colored_local_overlap_witnesses(states, i, limit=1)
               for i in range(len(states)))
    assert prune_colored_unsupported(states) == (tuple(range(17)), ())
