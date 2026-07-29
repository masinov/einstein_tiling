from __future__ import annotations

import ast
from pathlib import Path

from einstein.theory import sturmian_source


ROOT = Path(__file__).resolve().parents[1]
THEORY = ROOT / "src/einstein/theory"

MODULE_ORDER = {
    "sturmian_source_core": 0,
    "sturmian_contacts": 1,
    "sturmian_geometry": 2,
    "sturmian_compiler": 3,
    "sturmian_classification": 4,
}


def test_compatibility_facade_exports_unique_live_symbols():
    assert len(sturmian_source.__all__) == len(set(sturmian_source.__all__))
    assert all(hasattr(sturmian_source, name) for name in sturmian_source.__all__)
    assert sturmian_source.verify_atlas.__module__.endswith("sturmian_source_core")
    assert sturmian_source.verify_contact_kernel.__module__.endswith("sturmian_contacts")
    assert sturmian_source.verify_common_support_kernel.__module__.endswith("sturmian_geometry")
    assert sturmian_source.verify_seventeen_rhombus_source_compiler.__module__.endswith(
        "sturmian_compiler"
    )
    assert sturmian_source.verify_area30_carrier_classification.__module__.endswith(
        "sturmian_classification"
    )


def test_sturmian_modules_form_an_acyclic_dependency_ladder():
    for module, rank in MODULE_ORDER.items():
        tree = ast.parse((THEORY / f"{module}.py").read_text())
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or node.level != 1:
                continue
            dependency = node.module
            if dependency in MODULE_ORDER:
                assert MODULE_ORDER[dependency] < rank, (module, dependency)


def test_compatibility_facade_is_navigation_not_implementation():
    facade = THEORY / "sturmian_source.py"
    assert len(facade.read_text().splitlines()) < 300
    for module in MODULE_ORDER:
        assert len((THEORY / f"{module}.py").read_text().splitlines()) < 1100
