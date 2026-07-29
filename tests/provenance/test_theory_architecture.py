import json
import re
from pathlib import Path
from urllib.parse import unquote

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
THEORY = ROOT / "docs" / "theory"
ARCHIVE = ROOT / "docs" / "archive" / "theory_sources"
SOURCE_MAP = THEORY / "reference" / "SOURCE_MAP.json"


def _source_map() -> dict:
    return json.loads(SOURCE_MAP.read_text())


def test_theory_source_map_covers_every_former_number_once():
    numbers = [
        number
        for group in _source_map()["groups"]
        for number in group["former_note_numbers"]
    ]
    assert sorted(numbers) == list(range(1, 84))
    assert len(numbers) == len(set(numbers))


def test_theory_source_map_points_only_to_existing_documents():
    for group in _source_map()["groups"]:
        assert group["canonical_documents"], group["id"]
        assert group["source_documents"], group["id"]
        assert len(group["source_documents"]) == len(group["former_note_numbers"]), group["id"]
        for relative in group["canonical_documents"] + group["source_documents"]:
            assert (ROOT / relative).is_file(), (group["id"], relative)
        for number, relative in zip(
            group["former_note_numbers"], group["source_documents"], strict=True
        ):
            if relative.startswith("docs/archive/theory_sources/"):
                assert Path(relative).name.startswith(f"{number:02d}_"), (number, relative)


def test_chronological_sources_are_complete_and_outside_active_theory():
    archived_numbers = sorted(
        int(match.group(1))
        for path in ARCHIVE.glob("[0-9][0-9]_*.md")
        if (match := re.match(r"^(\d\d)_", path.name))
    )
    assert archived_numbers == list(range(7, 83))
    assert not list(THEORY.glob("[0-9][0-9]_*.md"))


def test_active_theory_has_only_named_mathematical_domains():
    assert {path.name for path in THEORY.iterdir()} == {
        "README.md",
        "case_studies",
        "controls",
        "foundations",
        "realization",
        "reference",
        "research",
        "sturmian",
    }


def test_canonical_documents_do_not_link_to_retired_numbered_paths():
    retired = re.compile(r"docs/theory/(?:\d\d_|GENERAL_REALIZATION_THEOREMS|"
                         r"STURMIAN_REALIZATION_BOUNDARY|83_ahi_branch_closure|"
                         r"PROOF_LEDGER|W1_TRANSFER_SPEC|MONOGRAPH_OUTLINE)")
    offenders = []
    for path in THEORY.rglob("*"):
        if path.is_file() and path != THEORY / "reference" / "proof_ledger.md":
            if retired.search(path.read_text()):
                offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []


def test_relative_markdown_links_in_active_theory_resolve():
    link = re.compile(r"\[[^]]*\]\(([^)]+)\)")
    missing = []
    for path in THEORY.rglob("*.md"):
        for raw_target in link.findall(path.read_text()):
            target = raw_target.strip().strip("<>")
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target and not (path.parent / target).resolve().exists():
                missing.append((str(path.relative_to(ROOT)), raw_target))
    assert missing == []
