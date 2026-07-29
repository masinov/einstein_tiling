"""Registry of retained exact certificate families and their command paths."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class CertificateFamily:
    name: str
    description: str
    artifact: str
    builder: str
    verifier: str
    dependencies: tuple[str, ...] = ()

    def as_dict(self) -> dict:
        data = asdict(self)
        data["dependencies"] = list(self.dependencies)
        return data


FAMILIES = (
    CertificateFamily(
        "source-atlas",
        "Normalized exact AHI Section 10.1 support atlas.",
        "data/sturmian-source/ahi-section10-supports.json",
        "scripts/extract_sturmian_source.py",
        "scripts/verify_sturmian_source.py",
    ),
    CertificateFamily(
        "contact-kernel",
        "Exact 31-state physical contact kernel.",
        "data/sturmian-source/ahi-section10-contact-kernel.json",
        "scripts/build_sturmian_contact_kernel.py",
        "scripts/verify_sturmian_contact_kernel.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "periodic-scaffold",
        "Periodic scaffold control for the reconstructed source.",
        "data/sturmian-source/ahi-periodic-scaffold.json",
        "scripts/build_sturmian_periodic_scaffold.py",
        "scripts/verify_sturmian_periodic_scaffold.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "corridor-quotient",
        "Finite exact corridor-state quotient.",
        "data/sturmian-source/ahi-corridor-quotient.json",
        "scripts/build_sturmian_corridor_quotient.py",
        "scripts/verify_sturmian_corridor_quotient.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "l-anchor-selector",
        "Exact rooted L-anchor selector.",
        "data/sturmian-source/ahi-l-anchor-selector.json",
        "scripts/build_sturmian_l_anchor_selector.py",
        "scripts/verify_sturmian_l_anchor_selector.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "unit-apex-compiler",
        "Unit-apex compiler control.",
        "data/sturmian-source/ahi-unit-apex-compiler.json",
        "scripts/build_sturmian_unit_apex_compiler.py",
        "scripts/verify_sturmian_unit_apex_compiler.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "common-support-kernel",
        "Exact common-support classification kernel.",
        "data/sturmian-source/ahi-common-support-kernel.json",
        "scripts/build_sturmian_common_support_kernel.py",
        "scripts/verify_sturmian_common_support_kernel.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "interchangeable-pairs",
        "Exact interchangeable assembly pairs.",
        "data/sturmian-source/ahi-interchangeable-pairs.json",
        "scripts/build_sturmian_interchangeable_pairs.py",
        "scripts/verify_sturmian_interchangeable_pairs.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "interchangeable-periodicity",
        "Periodicity certificate for interchangeable pairs.",
        "data/sturmian-source/ahi-interchangeable-periodicity.json",
        "scripts/build_sturmian_interchangeable_periodicity.py",
        "scripts/verify_sturmian_interchangeable_periodicity.py",
        ("interchangeable-pairs",),
    ),
    CertificateFamily(
        "seventeen-compiler",
        "Seventeen-rhombus source compiler.",
        "data/sturmian-source/ahi-seventeen-rhombus-compiler.json",
        "scripts/build_sturmian_seventeen_compiler.py",
        "scripts/verify_sturmian_seventeen_compiler.py",
        ("source-atlas", "common-support-kernel"),
    ),
    CertificateFamily(
        "seventeen-full-germs",
        "Complete seventeen-rhombus local germ language.",
        "data/sturmian-source/ahi-seventeen-rhombus-full-germs.json",
        "scripts/build_sturmian_seventeen_full_germs.py",
        "scripts/verify_sturmian_seventeen_full_germs.py",
        ("source-atlas", "common-support-kernel"),
    ),
    CertificateFamily(
        "p17-all-m",
        "All-M obstruction for the P17 carrier.",
        "data/sturmian-source/ahi-p17-all-m-obstruction.json",
        "scripts/build_sturmian_p17_all_m.py",
        "scripts/verify_sturmian_p17_all_m.py",
        ("source-atlas", "common-support-kernel"),
    ),
    CertificateFamily(
        "sub30-carriers",
        "Carrier-local classification below area 30.",
        "data/sturmian-source/ahi-sub30-carrier-classification.json",
        "scripts/build_sturmian_sub30_carriers.py",
        "scripts/verify_sturmian_sub30_carriers.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "area30-carriers",
        "Exact area-30 carrier-local classification.",
        "data/sturmian-source/ahi-area30-carrier-classification.json",
        "scripts/build_sturmian_area30_carriers.py",
        "scripts/verify_sturmian_area30_carriers.py",
        ("source-atlas",),
    ),
    CertificateFamily(
        "seventeen-periodicity",
        "Translation-periodicity certificate for the seventeen-rhombus carrier.",
        "data/sturmian-source/ahi-seventeen-rhombus-periodicity.json",
        "scripts/build_sturmian_seventeen_periodicity.py",
        "scripts/verify_sturmian_seventeen_periodicity.py",
        ("seventeen-compiler",),
    ),
    CertificateFamily(
        "seventeen-rep3",
        "Three-copy representation certificate for the seventeen-rhombus carrier.",
        "data/sturmian-source/ahi-seventeen-rhombus-rep3.json",
        "scripts/build_sturmian_seventeen_rep3.py",
        "scripts/verify_sturmian_seventeen_rep3.py",
        ("seventeen-compiler",),
    ),
    CertificateFamily(
        "fiftyone-periodicity",
        "Periodicity certificate for the 51-rhombus envelope.",
        "data/sturmian-source/ahi-fiftyone-envelope-periodicity.json",
        "scripts/build_sturmian_fiftyone_periodicity.py",
        "scripts/verify_sturmian_fiftyone_periodicity.py",
        ("seventeen-compiler",),
    ),
    CertificateFamily(
        "stade-physical-contacts",
        "Exact physical-contact quotient for the audited Stade construction.",
        "data/sturmian-source/stade-physical-contact-quotient.json",
        "scripts/stade_physical_contacts.py",
        "scripts/verify_stade_physical_contacts.py",
    ),
)

BY_NAME = {family.name: family for family in FAMILIES}


def family(name: str) -> CertificateFamily:
    try:
        return BY_NAME[name]
    except KeyError as error:
        raise KeyError(f"unknown certificate family: {name}") from error


def validate_registry(root: Path) -> None:
    assert len(BY_NAME) == len(FAMILIES), "duplicate certificate family"
    for item in FAMILIES:
        assert (root / item.artifact).is_file(), item.artifact
        assert (root / item.builder).is_file(), item.builder
        assert (root / item.verifier).is_file(), item.verifier
        for dependency in item.dependencies:
            assert dependency in BY_NAME, (item.name, dependency)
