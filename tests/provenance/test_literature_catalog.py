"""Structural checks for the prior-art catalog and review gate."""

import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
LITERATURE = ROOT / "docs" / "literature"
CATALOG = LITERATURE / "SOURCES.json"


def load_catalog():
    return json.loads(CATALOG.read_text())


def test_catalog_schema_and_identifiers_are_unambiguous():
    catalog = load_catalog()
    assert catalog["schema_version"] == 1
    assert catalog["snapshot_date"] == "2026-07-28"
    assert len(catalog["sources"]) >= 18

    ids = [source["id"] for source in catalog["sources"]]
    arxiv = [source["arxiv"] for source in catalog["sources"] if source["arxiv"]]
    filenames = [
        source["local_filename"]
        for source in catalog["sources"]
        if source["local_filename"]
    ]
    assert len(ids) == len(set(ids))
    assert len(arxiv) == len(set(arxiv))
    assert len(filenames) == len(set(filenames))

    allowed_evidence = set(catalog["evidence_classes"])
    for source in catalog["sources"]:
        assert source["id"]
        assert source["title"]
        assert source["authors"]
        assert source["evidence_class"] in allowed_evidence
        assert source["record_url"].startswith("https://")
        assert source["review_status"]
        assert source["themes"]
        assert set(source["workstreams"]) <= {"A", "B", "C", "D"}
        if source["download_url"]:
            assert source["local_filename"].endswith(".pdf")
        review_note = source.get("review_note")
        if review_note:
            note = ROOT / review_note
            assert note.is_file()
            assert source["id"] in note.read_text()


def test_technical_parent_links_resolve():
    sources = load_catalog()["sources"]
    ids = {source["id"] for source in sources}
    for source in sources:
        parent = source.get("technical_parent")
        if parent:
            assert parent in ids
            assert parent != source["id"]


def test_required_prior_art_controls_are_catalogued():
    sources = load_catalog()["sources"]
    ids = {source["id"] for source in sources}
    assert {
        "smkgs-hat-2024",
        "smkgs-chiral-2024",
        "akiyama-araki-turtle-2025",
        "kaplan-isohedral-sat-2024",
        "kaplan-heesch-sat-code",
        "kaplan-8kites-2023",
        "baake-gaehler-sadun-hat-2025",
        "baake-et-al-spectre-order-2025",
        "labbe-selinger-markov-2026",
        "tatham-transducers-2026",
        "walton-recognisability-2026",
        "akiyama-hamada-ito-sturmian-2026",
        "coulbois-et-al-groups-2026",
    } <= ids
    by_id = {source["id"]: source for source in sources}
    assert (
        by_id["kaplan-heesch-2022"]["doi"]
        == "10.55016/ojs/cdm.v17i2.72886"
    )


def test_every_source_is_routed_into_the_review_documents():
    review_text = "\n".join(
        (LITERATURE / name).read_text()
        for name in (
            "STATE_OF_THE_ART.md",
            "METHODS_MATRIX.md",
            "READING_QUEUE.md",
            "POLYKITE_BASELINE.md",
        )
    )
    for source in load_catalog()["sources"]:
        assert source["id"] in review_text, source["id"]


def test_protocol_forbids_registry_absence_as_novelty():
    protocol = (LITERATURE / "NOVELTY_PROTOCOL.md").read_text()
    assert "Not in our registry" in protocol
    assert "single generated substitution tiling proves neither" in protocol
    assert "Turtle as a blinded positive control" in protocol
