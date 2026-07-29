#!/usr/bin/env python3
"""Build the exact 31-state source contact kernel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import build_contact_kernel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    atlas = json.loads(args.atlas.read_text())
    kernel = build_contact_kernel(atlas)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(kernel, indent=2, sort_keys=True) + "\n")
    verdict = kernel["binary_domain_wall"]
    internal = kernel["internal_opposite_handedness"]
    print(
        f"states={len(kernel['states'])} "
        f"internal={len(kernel['internal_contacts'])} "
        f"exposed_states={len(kernel['exposed_state_ids'])} "
        f"internal_opposite={internal['satisfiable']} "
        f"binary_domain_wall={verdict['satisfiable']}"
    )


if __name__ == "__main__":
    main()
