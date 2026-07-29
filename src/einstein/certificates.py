"""Declarative registry and execution engine for retained JSON certificates.

Certificate mathematics belongs to the module that defines the construction.
This module owns the reusable boundary around it: dependency resolution,
external-path inputs, deterministic JSON serialization and cold-verifier
dispatch.  The command in ``scripts/certificates.py`` is intentionally only an
argument parser over this API.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib import import_module
import json
from pathlib import Path
from typing import Callable, Literal, Mapping


InputKind = Literal["json", "path"]
InputSource = Literal["artifact", "dependency", "external"]


@dataclass(frozen=True)
class CertificateInput:
    """One positional argument supplied to a certificate operation."""

    name: str
    source: InputSource
    kind: InputKind
    family: str | None = None
    default: str | None = None

    @classmethod
    def artifact(cls) -> "CertificateInput":
        return cls("artifact", "artifact", "json")

    @classmethod
    def dependency(cls, name: str, family: str) -> "CertificateInput":
        return cls(name, "dependency", "json", family=family)

    @classmethod
    def external_path(
        cls, name: str, default: str | None = None
    ) -> "CertificateInput":
        return cls(name, "external", "path", default=default)


@dataclass(frozen=True)
class CertificateOperation:
    """A callable plus its ordered, declaratively resolved inputs."""

    callable: str
    inputs: tuple[CertificateInput, ...]


@dataclass(frozen=True)
class CertificateFamily:
    name: str
    description: str
    artifact: str
    build: CertificateOperation
    verify: CertificateOperation

    @property
    def dependencies(self) -> tuple[str, ...]:
        return tuple(
            item.family
            for operation in (self.build, self.verify)
            for item in operation.inputs
            if item.source == "dependency" and item.family is not None
        )

    def as_dict(self) -> dict:
        data = asdict(self)
        data["dependencies"] = list(dict.fromkeys(self.dependencies))
        data["commands"] = {
            "build": f"scripts/certificates.py build {self.name}",
            "verify": f"scripts/certificates.py verify {self.name}",
        }
        return data


def _call(name: str, *inputs: CertificateInput) -> CertificateOperation:
    return CertificateOperation(name, tuple(inputs))


ATLAS = CertificateInput.dependency("atlas", "source-atlas")
KERNEL = CertificateInput.dependency("kernel", "contact-kernel")
PAIRS = CertificateInput.dependency("pairs", "interchangeable-pairs")
REP3 = CertificateInput.dependency("rep3", "seventeen-rep3")
ARTIFACT = CertificateInput.artifact()
ARCHIVE = CertificateInput.external_path("archive")
STADE_ANCHOR = CertificateInput.external_path(
    "source-anchor", "docs/literature/anchors/stade-stick-rules.json"
)


FAMILIES = (
    CertificateFamily(
        "source-atlas",
        "Normalized exact AHI Section 10.1 support atlas.",
        "data/sturmian-source/ahi-section10-supports.json",
        _call("einstein.tilings.sturmian:build_atlas", ARCHIVE),
        _call("einstein.tilings.sturmian:verify_atlas", ARTIFACT),
    ),
    CertificateFamily(
        "contact-kernel",
        "Exact 31-state physical contact kernel.",
        "data/sturmian-source/ahi-section10-contact-kernel.json",
        _call("einstein.tilings.sturmian:build_contact_kernel", ATLAS),
        _call("einstein.tilings.sturmian:verify_contact_kernel", ARTIFACT, ATLAS),
    ),
    CertificateFamily(
        "periodic-scaffold",
        "Periodic scaffold control for the reconstructed source.",
        "data/sturmian-source/ahi-periodic-scaffold.json",
        _call("einstein.tilings.sturmian:build_periodic_scaffold", ATLAS),
        _call("einstein.tilings.sturmian:verify_periodic_scaffold", ARTIFACT, ATLAS),
    ),
    CertificateFamily(
        "corridor-quotient",
        "Finite exact corridor-state quotient.",
        "data/sturmian-source/ahi-corridor-quotient.json",
        _call("einstein.tilings.sturmian:build_corridor_quotient", ARCHIVE, ATLAS),
        _call(
            "einstein.tilings.sturmian:verify_corridor_quotient",
            ARTIFACT,
            ARCHIVE,
            ATLAS,
        ),
    ),
    CertificateFamily(
        "l-anchor-selector",
        "Exact rooted L-anchor selector.",
        "data/sturmian-source/ahi-l-anchor-selector.json",
        _call("einstein.tilings.sturmian:build_l_anchor_selector", ATLAS),
        _call("einstein.tilings.sturmian:verify_l_anchor_selector", ARTIFACT, ATLAS),
    ),
    CertificateFamily(
        "unit-apex-compiler",
        "Unit-apex compiler control.",
        "data/sturmian-source/ahi-unit-apex-compiler.json",
        _call("einstein.tilings.sturmian:build_unit_apex_compiler", ATLAS),
        _call("einstein.tilings.sturmian:verify_unit_apex_compiler", ARTIFACT, ATLAS),
    ),
    CertificateFamily(
        "common-support-kernel",
        "Exact common-support classification kernel.",
        "data/sturmian-source/ahi-common-support-kernel.json",
        _call("einstein.tilings.sturmian:build_common_support_kernel", ATLAS),
        _call("einstein.tilings.sturmian:verify_common_support_kernel", ARTIFACT, ATLAS),
    ),
    CertificateFamily(
        "interchangeable-pairs",
        "Exact interchangeable assembly pairs.",
        "data/sturmian-source/ahi-interchangeable-pairs.json",
        _call("einstein.tilings.sturmian:build_interchangeable_pairs", ARCHIVE, ATLAS),
        _call(
            "einstein.tilings.sturmian:verify_interchangeable_pairs",
            ARTIFACT,
            ARCHIVE,
            ATLAS,
        ),
    ),
    CertificateFamily(
        "interchangeable-periodicity",
        "Periodicity certificate for interchangeable pairs.",
        "data/sturmian-source/ahi-interchangeable-periodicity.json",
        _call("einstein.tilings.sturmian:build_interchangeable_pair_periodicity", PAIRS),
        _call(
            "einstein.tilings.sturmian:verify_interchangeable_pair_periodicity",
            ARTIFACT,
            PAIRS,
        ),
    ),
    CertificateFamily(
        "seventeen-compiler",
        "Seventeen-rhombus source compiler.",
        "data/sturmian-source/ahi-seventeen-rhombus-compiler.json",
        _call("einstein.tilings.sturmian:build_seventeen_rhombus_source_compiler", ATLAS, KERNEL),
        _call(
            "einstein.tilings.sturmian:verify_seventeen_rhombus_source_compiler",
            ARTIFACT,
            ATLAS,
            KERNEL,
        ),
    ),
    CertificateFamily(
        "seventeen-full-germs",
        "Complete seventeen-rhombus local germ language.",
        "data/sturmian-source/ahi-seventeen-rhombus-full-germs.json",
        _call(
            "einstein.tilings.sturmian:build_seventeen_rhombus_full_germs",
            ARCHIVE,
            ATLAS,
            KERNEL,
        ),
        _call(
            "einstein.tilings.sturmian:verify_seventeen_rhombus_full_germs",
            ARTIFACT,
            ARCHIVE,
            ATLAS,
            KERNEL,
        ),
    ),
    CertificateFamily(
        "p17-all-m",
        "All-M obstruction for the P17 carrier.",
        "data/sturmian-source/ahi-p17-all-m-obstruction.json",
        _call("einstein.tilings.sturmian:build_p17_all_m_obstruction", ATLAS, KERNEL),
        _call(
            "einstein.tilings.sturmian:verify_p17_all_m_obstruction",
            ARTIFACT,
            ATLAS,
            KERNEL,
        ),
    ),
    CertificateFamily(
        "sub30-carriers",
        "Carrier-local classification below area 30.",
        "data/sturmian-source/ahi-sub30-carrier-classification.json",
        _call("einstein.tilings.sturmian:build_sub30_carrier_classification", ATLAS),
        _call(
            "einstein.tilings.sturmian:verify_sub30_carrier_classification",
            ARTIFACT,
            ATLAS,
        ),
    ),
    CertificateFamily(
        "area30-carriers",
        "Exact area-30 carrier-local classification.",
        "data/sturmian-source/ahi-area30-carrier-classification.json",
        _call("einstein.tilings.sturmian:build_area30_carrier_classification", ATLAS),
        _call(
            "einstein.tilings.sturmian:verify_area30_carrier_classification",
            ARTIFACT,
            ATLAS,
        ),
    ),
    CertificateFamily(
        "seventeen-periodicity",
        "Translation-periodicity certificate for the seventeen-rhombus carrier.",
        "data/sturmian-source/ahi-seventeen-rhombus-periodicity.json",
        _call("einstein.tilings.sturmian:build_seventeen_rhombus_periodicity", ATLAS, KERNEL),
        _call(
            "einstein.tilings.sturmian:verify_seventeen_rhombus_periodicity",
            ARTIFACT,
            ATLAS,
            KERNEL,
        ),
    ),
    CertificateFamily(
        "seventeen-rep3",
        "Three-copy representation certificate for the seventeen-rhombus carrier.",
        "data/sturmian-source/ahi-seventeen-rhombus-rep3.json",
        _call("einstein.tilings.sturmian:build_seventeen_rhombus_rep3", ATLAS, KERNEL, PAIRS),
        _call(
            "einstein.tilings.sturmian:verify_seventeen_rhombus_rep3",
            ARTIFACT,
            ATLAS,
            KERNEL,
            PAIRS,
        ),
    ),
    CertificateFamily(
        "fiftyone-periodicity",
        "Periodicity certificate for the 51-rhombus envelope.",
        "data/sturmian-source/ahi-fiftyone-envelope-periodicity.json",
        _call("einstein.tilings.sturmian:build_fiftyone_envelope_periodicity", PAIRS, REP3),
        _call(
            "einstein.tilings.sturmian:verify_fiftyone_envelope_periodicity",
            ARTIFACT,
            PAIRS,
            REP3,
        ),
    ),
    CertificateFamily(
        "stade-physical-contacts",
        "Exact physical-contact quotient for the audited Stade construction.",
        "data/sturmian-source/stade-physical-contact-quotient.json",
        _call("einstein.tilings.stade.contacts:build_contact_quotient", STADE_ANCHOR),
        _call(
            "einstein.tilings.stade.contacts:verify_contact_quotient",
            ARTIFACT,
            STADE_ANCHOR,
        ),
    ),
)

BY_NAME = {item.name: item for item in FAMILIES}


def family(name: str) -> CertificateFamily:
    try:
        return BY_NAME[name]
    except KeyError as error:
        raise KeyError(f"unknown certificate family: {name}") from error


def resolve_callable(reference: str) -> Callable:
    module_name, separator, attribute = reference.partition(":")
    if not separator:
        raise ValueError(f"invalid callable reference: {reference}")
    value = getattr(import_module(module_name), attribute)
    if not callable(value):
        raise TypeError(f"certificate target is not callable: {reference}")
    return value


def _input_path(
    root: Path,
    owner: CertificateFamily,
    item: CertificateInput,
    overrides: Mapping[str, Path],
    artifact_path: Path,
) -> Path:
    if item.name in overrides:
        return overrides[item.name]
    if item.source == "artifact":
        return artifact_path
    if item.source == "dependency":
        if item.family is None:
            raise ValueError(f"dependency input lacks a family: {item.name}")
        return root / family(item.family).artifact
    if item.default is not None:
        return root / item.default
    raise ValueError(f"{owner.name} requires --{item.name.replace('_', '-')}")


def _load(path: Path, kind: InputKind):
    return json.loads(path.read_text()) if kind == "json" else path


def execute(
    root: Path,
    family_name: str,
    operation_name: Literal["build", "verify"],
    *,
    artifact_path: Path | None = None,
    overrides: Mapping[str, Path] | None = None,
):
    """Build or cold-verify one registered family.

    Dependency inputs default to the canonical artifacts of their registered
    families.  ``overrides`` changes paths, never values, so all decoding and
    verification remains in the exact source implementation.
    """

    owner = family(family_name)
    operation = owner.build if operation_name == "build" else owner.verify
    target = artifact_path or root / owner.artifact
    paths = overrides or {}
    arguments = [
        _load(_input_path(root, owner, item, paths, target), item.kind)
        for item in operation.inputs
    ]
    result = resolve_callable(operation.callable)(*arguments)
    if operation_name == "build":
        if not isinstance(result, dict):
            raise TypeError(f"builder did not return a JSON object: {owner.name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def validate_registry(root: Path) -> None:
    assert len(BY_NAME) == len(FAMILIES), "duplicate certificate family"
    for item in FAMILIES:
        assert (root / item.artifact).is_file(), item.artifact
        for operation in (item.build, item.verify):
            resolve_callable(operation.callable)
            for input_item in operation.inputs:
                if input_item.source == "dependency":
                    assert input_item.family in BY_NAME, (
                        item.name,
                        input_item.family,
                    )
                if input_item.default is not None:
                    assert (root / input_item.default).is_file(), input_item.default
