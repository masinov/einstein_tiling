#!/usr/bin/env python
"""Produce the W3 physical-to-parent component-language audit."""

try:
    from scripts.probe_theory_w3_spectre_component_language import main
except ModuleNotFoundError:  # direct ``python scripts/...`` execution
    from probe_theory_w3_spectre_component_language import main


if __name__ == "__main__":
    main()
