#!/usr/bin/env python
"""Audit the uncolored contracted parent-corona overlap language."""

from __future__ import annotations

import ast
import json
from pathlib import Path

from einstein.theory.spectre_parent_interface import (
    local_overlap_witnesses,
    prune_locally_unsupported,
    reciprocal_domains,
)
from einstein.theory.spectre_patch_language import pose_json
from einstein.theory.substitution_certificate import file_sha256

try:
    from scripts.probe_theory_w3_spectre_component_language import (
        generated_parent_coronas,
        source,
    )
except ModuleNotFoundError:
    from probe_theory_w3_spectre_component_language import (
        generated_parent_coronas,
        source,
    )


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/notebook/assets/theory-w3-spectre-component-language.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-parent-interface.json"


def analyze():
    component = json.loads(SOURCE.read_text())
    generated = generated_parent_coronas(source())
    extras = tuple(ast.literal_eval(signature) for signature in component[
        "contraction_audit"
    ]["nongenerated_signature_histogram_through_radius7"])
    states = (*generated, *extras)
    if len(states) != len(set(states)):
        raise ValueError("generated and extra parent states overlap")
    rows = []
    for index, state in enumerate(states):
        domains = reciprocal_domains(states, index)
        witnesses = local_overlap_witnesses(states, index, limit=2)
        rows.append({
            "state": index,
            "kind": "generated" if index < len(generated) else "extra",
            "corona": [pose_json(pose) for pose in state],
            "reciprocal_domain_sizes": [len(domain) for domain in domains],
            "triangle_consistent_witnesses_capped_at_2": [
                list(witness) for witness in witnesses
            ],
        })
    alive, rounds = prune_locally_unsupported(states)
    return {
        "generated_states": len(generated),
        "extra_states": len(extras),
        "total_states": len(states),
        "records": rows,
        "support_pruning_rounds": [list(row) for row in rounds],
        "surviving_states": list(alive),
        "surviving_extra_states": [
            index - len(generated) for index in alive if index >= len(generated)
        ],
        "verdict": "uncolored-reciprocal-triangle-language-insufficient",
    }


def main():
    analysis = analyze()
    artifact = {
        "schema": "einstein.w3.spectre-parent-interface",
        "version": 1,
        "status": "ALL_26_UNCOLORED_STATES_SURVIVE",
        "provenance": {
            "component_source": str(SOURCE.relative_to(ROOT)),
            "component_sha256": file_sha256(SOURCE),
        },
        "analysis": analysis,
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        f"W3 parent interface: {analysis['total_states']} states, "
        f"{len(analysis['surviving_states'])} survive; uncolored overlap is insufficient"
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
