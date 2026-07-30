"""The canonical Python namespace is organized by mathematical domain."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
import sys

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
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
    "literature",
    "periodicity",
    "polykites",
    "repository",
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


def test_script_root_is_a_small_stable_command_surface():
    root_commands = {
        path.name for path in (ROOT / "scripts").glob("*.py") if path.is_file()
    }
    assert root_commands == {
        "certificates.py",
        "check_experiment_gate.py",
        "check_research_proposal.py",
        "fetch_literature.py",
        "run_research.py",
    }

    responsibility_directories = {
        path.name
        for path in (ROOT / "scripts").iterdir()
        if path.is_dir() and not path.name.startswith((".", "__"))
    }
    assert responsibility_directories == {
        "analysis",
        "archive",
        "benchmarks",
        "certificate_tools",
        "historical",
        "maintenance",
        "visualize",
    }


def test_active_script_names_do_not_encode_retired_research_stages():
    scripts = ROOT / "scripts"
    forbidden = ("a1_", "a2_", "a3_", "a4_", "a6_", "w2_", "k16w_", "hc")
    for path in scripts.rglob("*.py"):
        relative = path.relative_to(scripts)
        if relative.parts[0] in {"archive", "historical"}:
            continue
        assert not path.stem.startswith(forbidden), path


def test_tests_are_grouped_by_evidence_role():
    tests = ROOT / "tests"
    assert {path.name for path in tests.glob("test_*.py")} == set()
    for path in tests.rglob("test_*.py"):
        assert path.relative_to(tests).parts[0] in {
            "unit",
            "certificates",
            "controls",
            "provenance",
        }, path


def test_every_nonarchived_command_is_importable():
    scripts = ROOT / "scripts"
    for index, path in enumerate(sorted(scripts.rglob("*.py"))):
        if "archive" in path.relative_to(scripts).parts:
            continue
        name = f"_einstein_command_contract_{index}"
        specification = importlib.util.spec_from_file_location(name, path)
        assert specification is not None and specification.loader is not None
        module = importlib.util.module_from_spec(specification)
        sys.modules[name] = module
        try:
            specification.loader.exec_module(module)
        finally:
            sys.modules.pop(name, None)
