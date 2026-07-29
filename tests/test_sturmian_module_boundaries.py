from __future__ import annotations

import ast
from pathlib import Path

from einstein.tilings import sturmian


ROOT = Path(__file__).resolve().parents[1]
STURMIAN = ROOT / "src/einstein/tilings/sturmian"

MODULE_ORDER = {
    "atlas": 0,
    "contacts": 1,
    "carriers": 2,
    "compiler": 3,
    "classification": 4,
}


def test_compatibility_facade_exports_unique_live_symbols():
    assert len(sturmian.__all__) == len(set(sturmian.__all__))
    assert all(hasattr(sturmian, name) for name in sturmian.__all__)
    assert sturmian.verify_atlas.__module__.endswith(".atlas")
    assert sturmian.verify_contact_kernel.__module__.endswith(".contacts")
    assert sturmian.verify_common_support_kernel.__module__.endswith(".carriers")
    assert sturmian.verify_seventeen_rhombus_source_compiler.__module__.endswith(
        ".compiler"
    )
    assert sturmian.verify_area30_carrier_classification.__module__.endswith(
        ".classification"
    )


def test_sturmian_modules_form_an_acyclic_dependency_ladder():
    for module, rank in MODULE_ORDER.items():
        tree = ast.parse((STURMIAN / f"{module}.py").read_text())
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or node.level != 1:
                continue
            dependency = node.module
            if dependency in MODULE_ORDER:
                assert MODULE_ORDER[dependency] < rank, (module, dependency)


def test_compatibility_facade_is_navigation_not_implementation():
    facade = STURMIAN / "__init__.py"
    assert len(facade.read_text().splitlines()) < 300
    for module in MODULE_ORDER:
        assert len((STURMIAN / f"{module}.py").read_text().splitlines()) < 1100
