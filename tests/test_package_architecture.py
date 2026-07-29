"""The canonical Python namespace is organized by mathematical domain."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src/einstein"

REMOVED_NAMESPACES = {
    "enum",
    "enumeration",
    "funnel",
    "reference",
    "render",
    "substrate",
    "theory",
}

CANONICAL_PACKAGES = {
    "analysis",
    "combinatorics",
    "geometry",
    "historical",
    "holonomy",
    "periodicity",
    "polykites",
    "solvers",
    "tilings",
    "visualization",
}


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
    return imported


def test_top_level_packages_are_domain_named():
    tracked_packages = {
        path.name
        for path in PACKAGE.iterdir()
        if path.is_dir() and (path / "__init__.py").is_file()
    }
    assert not tracked_packages.intersection(REMOVED_NAMESPACES)
    assert CANONICAL_PACKAGES <= tracked_packages


def test_python_sources_do_not_import_removed_namespaces():
    forbidden = tuple(f"einstein.{name}" for name in REMOVED_NAMESPACES)
    for root in (ROOT / "src", ROOT / "scripts", ROOT / "tests"):
        for path in root.rglob("*.py"):
            for imported in _imports(path):
                assert not imported.startswith(forbidden), (path, imported)


def test_general_layers_do_not_depend_on_named_or_historical_systems():
    for package in ("geometry", "combinatorics"):
        for path in (PACKAGE / package).rglob("*.py"):
            for imported in _imports(path):
                assert not imported.startswith("einstein.tilings"), (path, imported)
                assert not imported.startswith("einstein.historical"), (path, imported)

    for path in PACKAGE.rglob("*.py"):
        if "historical" in path.parts:
            continue
        assert not any(
            imported.startswith("einstein.historical")
            for imported in _imports(path)
        ), path


def test_chronological_stage_codes_are_absent_from_canonical_module_names():
    for path in PACKAGE.rglob("*.py"):
        if "historical" in path.parts:
            continue
        assert not path.stem.startswith(("a1_", "a2_", "a3_", "a4_", "a6_", "w2_", "k16w_")), path
