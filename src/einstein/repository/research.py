"""Mechanical contracts at research commitment and promotion boundaries.

Free mathematical exploration is intentionally absent.  This module validates
versioned proposals, separate human-admission records, reproducibility pins,
and promotion dossiers.  It cannot judge whether a mathematical thesis is
good; it can prevent self-admission and mutable evidence from masquerading as
authorization.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


PROPOSAL_KINDS = {"research-program", "experiment", "promotion"}
PROPOSAL_STATUSES = {"draft", "ready", "closed"}
SCOPE_LEVELS = {
    "field-level-problem",
    "architecture-independent-class",
    "recognized-mathematical-family",
    "specific-construction",
    "single-instance",
}
PROMOTION_KINDS = {"candidate", "theorem", "method", "novelty"}
EXECUTION_STATUSES = {
    "completed",
    "process_error",
    "resource_stop_wall",
    "resource_stop_artifact",
    "supervisor_error",
    "interrupted",
}
PLACEHOLDERS = ("[replace", "todo", "tbd", "example-only")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
REVISION_RE = re.compile(r"[0-9a-f]{40}")
PROPOSAL_ID_RE = re.compile(r"RP-[0-9]{4}-[0-9]{2}-[0-9]{2}-[A-Z0-9-]+")
ISO_UTC_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_bytes(path: Path) -> int:
    """Total bytes in a file tree, treating an absent root as empty."""

    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _load_json(path: Path, errors: list[str], label: str = "proposal") -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is not readable JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{label} root must be a JSON object")
        return {}
    return value


def _nonempty_text(
    value: Any,
    field: str,
    errors: list[str],
    *,
    minimum: int = 30,
) -> None:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        errors.append(f"{field} must contain at least {minimum} characters")
        return
    lowered = value.lower()
    if any(marker in lowered for marker in PLACEHOLDERS):
        errors.append(f"{field} contains a placeholder")


def _safe_relative_path(value: Any, field: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a nonempty repository-relative path")
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or str(path) in {"", "."}:
        errors.append(f"{field} must stay inside the repository and name a path")
        return None
    return str(path)


def _valid_sha(value: Any, field: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        errors.append(f"{field} must be a lowercase SHA-256 digest")
        return False
    return True


def _portfolio_program_ids(root: Path, errors: list[str]) -> set[str]:
    path = root / "docs" / "research" / "portfolio.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        return {item["id"] for item in document["programs"]}
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        errors.append(f"current research portfolio is invalid: {exc}")
        return set()


def _literature_source_ids(root: Path, errors: list[str]) -> set[str]:
    path = root / "docs" / "literature" / "SOURCES.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        return {item["id"] for item in document["sources"]}
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        errors.append(f"literature source catalog is invalid: {exc}")
        return set()


def _validate_catalog_sources(
    values: Any,
    field: str,
    errors: list[str],
    source_ids: set[str] | None,
) -> None:
    if not isinstance(values, list) or not values or not all(
        isinstance(item, str) and item.strip() for item in values
    ):
        errors.append(f"{field} must be a nonempty list of catalog IDs")
        return
    if source_ids is not None:
        unknown = sorted(set(values) - source_ids)
        if unknown:
            errors.append(f"{field} contains unknown source IDs: {unknown}")


def _validate_file_pin(
    pin: Any,
    field: str,
    errors: list[str],
    root: Path | None,
) -> None:
    if not isinstance(pin, dict):
        errors.append(f"{field} must be an object")
        return
    relative = _safe_relative_path(pin.get("path"), f"{field}.path", errors)
    valid_digest = _valid_sha(pin.get("sha256"), f"{field}.sha256", errors)
    if root is None or relative is None or not valid_digest:
        return
    path = root / relative
    if not path.is_file():
        errors.append(f"{field}.path does not exist: {relative}")
    elif sha256_file(path) != pin["sha256"]:
        errors.append(f"{field}.sha256 does not match {relative}")


def _validate_pin_list(
    values: Any,
    field: str,
    errors: list[str],
    root: Path | None,
    *,
    allow_empty: bool,
) -> None:
    if not isinstance(values, list) or (not allow_empty and not values):
        qualifier = "a list" if allow_empty else "a nonempty list"
        errors.append(f"{field} must be {qualifier}")
        return
    paths: list[str] = []
    for index, pin in enumerate(values):
        _validate_file_pin(pin, f"{field}[{index}]", errors, root)
        if isinstance(pin, dict) and isinstance(pin.get("path"), str):
            paths.append(pin["path"])
    if len(paths) != len(set(paths)):
        errors.append(f"{field} contains duplicate paths")


def _validate_common(
    proposal: dict[str, Any],
    errors: list[str],
    root: Path | None,
) -> tuple[str | None, set[str] | None]:
    if proposal.get("schema_version") != 2:
        errors.append("schema_version must be 2")

    proposal_id = proposal.get("id")
    if not isinstance(proposal_id, str) or not PROPOSAL_ID_RE.fullmatch(proposal_id):
        errors.append("id must match RP-YYYY-MM-DD-NAME")

    kind = proposal.get("kind")
    if kind not in PROPOSAL_KINDS:
        errors.append(f"kind must be one of {sorted(PROPOSAL_KINDS)}")

    status = proposal.get("status")
    if status not in PROPOSAL_STATUSES:
        errors.append(f"status must be one of {sorted(PROPOSAL_STATUSES)}")

    _nonempty_text(proposal.get("title"), "title", errors, minimum=8)
    _nonempty_text(proposal.get("thesis"), "thesis", errors)
    _nonempty_text(proposal.get("mission_connection"), "mission_connection", errors)
    _nonempty_text(
        proposal.get("alternatives_considered"), "alternatives_considered", errors
    )
    _nonempty_text(proposal.get("failure_or_pivot"), "failure_or_pivot", errors)

    scope = proposal.get("scope_level")
    if scope not in SCOPE_LEVELS:
        errors.append(f"scope_level must be one of {sorted(SCOPE_LEVELS)}")

    if not isinstance(proposal.get("program_id"), str) or not proposal["program_id"].strip():
        errors.append("program_id must be a nonempty string")

    source_ids: set[str] | None = None
    if root is not None:
        if proposal.get("program_id") not in _portfolio_program_ids(root, errors):
            errors.append("program_id is not present in the current portfolio")
        source_ids = _literature_source_ids(root, errors)

    prior_art = proposal.get("prior_art")
    if not isinstance(prior_art, dict):
        errors.append("prior_art must be an object")
    else:
        snapshot = str(prior_art.get("snapshot_date", ""))
        try:
            datetime.strptime(snapshot, "%Y-%m-%d")
        except ValueError:
            errors.append("prior_art.snapshot_date must be a real YYYY-MM-DD date")
        _validate_catalog_sources(
            prior_art.get("primary_sources"),
            "prior_art.primary_sources",
            errors,
            source_ids,
        )
        _nonempty_text(prior_art.get("non_redundancy"), "prior_art.non_redundancy", errors)
        facts = prior_art.get("user_facts_resolved")
        if not isinstance(facts, list):
            errors.append("prior_art.user_facts_resolved must be a list")
        else:
            for index, fact in enumerate(facts):
                if not isinstance(fact, dict):
                    errors.append(f"prior_art.user_facts_resolved[{index}] must be an object")
                    continue
                _nonempty_text(
                    fact.get("statement"),
                    f"prior_art.user_facts_resolved[{index}].statement",
                    errors,
                )
                _validate_catalog_sources(
                    fact.get("source_ids"),
                    f"prior_art.user_facts_resolved[{index}].source_ids",
                    errors,
                    source_ids,
                )
                _nonempty_text(
                    fact.get("consequence"),
                    f"prior_art.user_facts_resolved[{index}].consequence",
                    errors,
                )

    outcomes = proposal.get("outcomes")
    if not isinstance(outcomes, list) or len(outcomes) < 2:
        errors.append("outcomes must contain at least two result/action branches")
    else:
        actions: list[str] = []
        for index, outcome in enumerate(outcomes):
            if not isinstance(outcome, dict):
                errors.append(f"outcomes[{index}] must be an object")
                continue
            _nonempty_text(outcome.get("result"), f"outcomes[{index}].result", errors)
            _nonempty_text(outcome.get("action"), f"outcomes[{index}].action", errors)
            if isinstance(outcome.get("action"), str):
                actions.append(outcome["action"].strip())
        if len(set(actions)) != len(actions):
            errors.append("outcome actions must be distinct")

    stop_rule = proposal.get("stop_rule")
    if not isinstance(stop_rule, dict):
        errors.append("stop_rule must be an object")
    else:
        _nonempty_text(stop_rule.get("condition"), "stop_rule.condition", errors)
        if stop_rule.get("no_automatic_escalation") is not True:
            errors.append("stop_rule.no_automatic_escalation must be true")

    return kind if isinstance(kind, str) else None, source_ids


def _validate_experiment(
    proposal: dict[str, Any], errors: list[str], root: Path | None
) -> None:
    experiment = proposal.get("experiment")
    if not isinstance(experiment, dict):
        errors.append("experiment proposal requires an experiment object")
        return
    _nonempty_text(experiment.get("proposition"), "experiment.proposition", errors)
    command = experiment.get("command")
    if not isinstance(command, list) or not command or not all(
        isinstance(item, str) and item for item in command
    ):
        errors.append("experiment.command must be a nonempty argv list")

    budget = experiment.get("budget")
    if not isinstance(budget, dict):
        errors.append("experiment.budget must be an object")
    else:
        for name in ("wall_time_seconds", "memory_bytes"):
            value = budget.get(name)
            if not isinstance(value, int) or value <= 0:
                errors.append(f"experiment.budget.{name} must be positive")
        artifact_bytes = budget.get("max_new_artifact_bytes")
        if not isinstance(artifact_bytes, int) or artifact_bytes < 0:
            errors.append("experiment.budget.max_new_artifact_bytes must be nonnegative")
        roots = budget.get("artifact_roots")
        if not isinstance(roots, list) or not roots:
            errors.append("experiment.budget.artifact_roots must be a nonempty list")
        else:
            normalized: list[str] = []
            for index, item in enumerate(roots):
                relative = _safe_relative_path(
                    item, f"experiment.budget.artifact_roots[{index}]", errors
                )
                if relative is not None:
                    normalized.append(relative)
            if len(normalized) != len(set(normalized)):
                errors.append("experiment.budget.artifact_roots contains duplicates")
        if budget.get("external_supervision") is not True:
            errors.append("experiment.budget.external_supervision must be true")

    reproducibility = experiment.get("reproducibility")
    if not isinstance(reproducibility, dict):
        errors.append("experiment.reproducibility must be an object")
    else:
        revision = reproducibility.get("code_revision")
        if not isinstance(revision, str) or not REVISION_RE.fullmatch(revision):
            errors.append("experiment.reproducibility.code_revision must be a 40-hex commit")
        if reproducibility.get("require_clean_tree") is not True:
            errors.append("experiment.reproducibility.require_clean_tree must be true")
        code_paths = reproducibility.get("code_paths")
        if not isinstance(code_paths, list) or not code_paths:
            errors.append("experiment.reproducibility.code_paths must be nonempty")
        else:
            normalized_code_paths: list[str] = []
            for index, item in enumerate(code_paths):
                relative = _safe_relative_path(
                    item, f"experiment.reproducibility.code_paths[{index}]", errors
                )
                if relative is not None:
                    normalized_code_paths.append(relative)
                    if root is not None and not (root / relative).exists():
                        errors.append(
                            "experiment.reproducibility.code_paths"
                            f"[{index}] does not exist: {relative}"
                        )
            if len(normalized_code_paths) != len(set(normalized_code_paths)):
                errors.append("experiment.reproducibility.code_paths contains duplicates")
            for governance_path in (
                "scripts/run_research.py",
                "src/einstein/repository/research.py",
            ):
                if governance_path not in normalized_code_paths:
                    errors.append(
                        "experiment.reproducibility.code_paths must pin "
                        f"{governance_path}"
                    )
        inputs = reproducibility.get("inputs")
        _validate_pin_list(
            inputs,
            "experiment.reproducibility.inputs",
            errors,
            root,
            allow_empty=True,
        )
        if inputs == []:
            _nonempty_text(
                reproducibility.get("no_external_inputs_reason"),
                "experiment.reproducibility.no_external_inputs_reason",
                errors,
            )
        _validate_pin_list(
            reproducibility.get("environment_files"),
            "experiment.reproducibility.environment_files",
            errors,
            root,
            allow_empty=False,
        )
        executables = reproducibility.get("executables")
        if not isinstance(executables, list) or not executables:
            errors.append("experiment.reproducibility.executables must be nonempty")
        else:
            paths: list[str] = []
            for index, executable in enumerate(executables):
                field = f"experiment.reproducibility.executables[{index}]"
                if not isinstance(executable, dict):
                    errors.append(f"{field} must be an object")
                    continue
                relative = _safe_relative_path(executable.get("path"), f"{field}.path", errors)
                if relative is not None:
                    paths.append(relative)
                    if root is not None and not (root / relative).is_file():
                        errors.append(f"{field}.path does not exist: {relative}")
                valid_digest = _valid_sha(
                    executable.get("sha256"), f"{field}.sha256", errors
                )
                if (
                    root is not None
                    and relative is not None
                    and valid_digest
                    and (root / relative).is_file()
                    and sha256_file(root / relative) != executable["sha256"]
                ):
                    errors.append(f"{field}.sha256 does not match {relative}")
                version_command = executable.get("version_command")
                if not isinstance(version_command, list) or not version_command or not all(
                    isinstance(item, str) and item for item in version_command
                ):
                    errors.append(f"{field}.version_command must be a nonempty argv list")
                elif relative is not None and version_command[0] != relative:
                    errors.append(f"{field}.version_command[0] must equal path")
                _valid_sha(executable.get("version_output_sha256"), f"{field}.version_output_sha256", errors)
            if len(paths) != len(set(paths)):
                errors.append("experiment.reproducibility.executables contains duplicate paths")
            if isinstance(command, list) and command and command[0] not in paths:
                errors.append("experiment.command[0] must have an executable pin")

    evidence = experiment.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("experiment.evidence must be an object")
    else:
        _nonempty_text(
            evidence.get("certificate_or_verifier"),
            "experiment.evidence.certificate_or_verifier",
            errors,
        )
        _nonempty_text(
            evidence.get("promotion_boundary"),
            "experiment.evidence.promotion_boundary",
            errors,
        )
        verifier = evidence.get("verifier")
        reason = evidence.get("no_verifier_reason")
        if verifier is None:
            _nonempty_text(reason, "experiment.evidence.no_verifier_reason", errors)
        else:
            _validate_file_pin(verifier, "experiment.evidence.verifier", errors, root)

    run_record = experiment.get("run_record")
    if not isinstance(run_record, dict):
        errors.append("experiment.run_record must be an object")
    else:
        output_paths: list[str] = []
        for name in ("manifest_path", "stdout_path", "stderr_path"):
            relative = _safe_relative_path(
                run_record.get(name), f"experiment.run_record.{name}", errors
            )
            if relative is not None:
                output_paths.append(relative)
        if len(output_paths) != len(set(output_paths)):
            errors.append("experiment.run_record paths must be distinct")
        if isinstance(budget, dict) and isinstance(budget.get("artifact_roots"), list):
            roots = [PurePosixPath(item) for item in budget["artifact_roots"] if isinstance(item, str)]
            for path in map(PurePosixPath, output_paths):
                if not any(path == root_path or root_path in path.parents for root_path in roots):
                    errors.append(f"experiment.run_record path is outside artifact_roots: {path}")


def _validate_promotion(
    proposal: dict[str, Any],
    errors: list[str],
    root: Path | None,
    source_ids: set[str] | None,
) -> None:
    promotion = proposal.get("promotion")
    if not isinstance(promotion, dict):
        errors.append("promotion proposal requires a promotion object")
        return
    claim_kind = promotion.get("claim_kind")
    if claim_kind not in PROMOTION_KINDS:
        errors.append(f"promotion.claim_kind must be one of {sorted(PROMOTION_KINDS)}")
    _nonempty_text(promotion.get("claim_id"), "promotion.claim_id", errors, minimum=4)
    _nonempty_text(promotion.get("requested_label"), "promotion.requested_label", errors, minimum=4)
    _validate_file_pin(promotion.get("source_document"), "promotion.source_document", errors, root)
    _validate_pin_list(
        promotion.get("evidence"), "promotion.evidence", errors, root, allow_empty=False
    )
    _validate_catalog_sources(
        promotion.get("literature_sources"),
        "promotion.literature_sources",
        errors,
        source_ids,
    )

    dossier = promotion.get("candidate_dossier")
    if claim_kind != "candidate":
        if dossier is not None:
            errors.append("candidate_dossier is allowed only for candidate promotion")
        return
    if not isinstance(dossier, dict):
        errors.append("candidate promotion requires candidate_dossier")
        return
    _validate_file_pin(dossier.get("geometry"), "promotion.candidate_dossier.geometry", errors, root)
    if dossier.get("allowed_isometries") not in {"full-E2", "orientation-preserving"}:
        errors.append("candidate_dossier.allowed_isometries must declare the motion convention")
    identity = dossier.get("identity_status")
    if identity not in {"known", "unclassified", "novel-after-audit"}:
        errors.append("candidate_dossier.identity_status is invalid")
    _validate_pin_list(
        dossier.get("identity_evidence"),
        "promotion.candidate_dossier.identity_evidence",
        errors,
        root,
        allow_empty=False,
    )
    periodicity = dossier.get("periodicity_status")
    if periodicity not in {"periodic", "no-periodic-certificate", "aperiodic-proved"}:
        errors.append("candidate_dossier.periodicity_status is invalid")
    for evidence_name in (
        "periodicity_evidence",
        "tilability_evidence",
        "contact_evidence",
        "aperiodicity_evidence",
    ):
        _validate_file_pin(
            dossier.get(evidence_name),
            f"promotion.candidate_dossier.{evidence_name}",
            errors,
            root,
        )
    for name, allowed in {
        "whole_plane_tilability": {"proved", "not-proved"},
        "contact_language": {"complete", "partial", "absent"},
        "all_tilings_aperiodicity": {"proved", "not-proved"},
        "total_decoder": {"proved", "not-proved", "not-applicable"},
    }.items():
        if dossier.get(name) not in allowed:
            errors.append(f"candidate_dossier.{name} is invalid")
    if periodicity == "periodic":
        errors.append("a candidate with a periodic tiling certificate cannot be promoted")
    if promotion.get("requested_label") == "aperiodic-monotile":
        required = {
            "periodicity_status": "aperiodic-proved",
            "whole_plane_tilability": "proved",
            "contact_language": "complete",
            "all_tilings_aperiodicity": "proved",
        }
        for name, expected in required.items():
            if dossier.get(name) != expected:
                errors.append(f"aperiodic-monotile promotion requires {name}={expected}")
    if dossier.get("total_decoder") == "proved":
        _validate_file_pin(
            dossier.get("decoder_evidence"),
            "promotion.candidate_dossier.decoder_evidence",
            errors,
            root,
        )


def validate_research_proposal(
    path: Path,
    *,
    root: Path | None = None,
    require_admitted: bool = False,
    require_experiment: bool = False,
    require_promotion: bool = False,
    admission_path: Path | None = None,
) -> list[str]:
    """Return every mechanical proposal or admission error."""

    errors: list[str] = []
    proposal = _load_json(path, errors)
    if not proposal:
        return errors
    kind, source_ids = _validate_common(proposal, errors, root)
    if require_experiment and kind != "experiment":
        errors.append("the research launcher accepts experiment proposals only")
    if require_promotion and kind != "promotion":
        errors.append("the promotion gate accepts promotion proposals only")
    if kind == "experiment":
        _validate_experiment(proposal, errors, root)
    elif kind == "promotion":
        _validate_promotion(proposal, errors, root, source_ids)
    elif kind == "research-program" and (
        "experiment" in proposal or "promotion" in proposal
    ):
        errors.append("research-program proposals cannot contain experiment or promotion objects")
    if proposal.get("status") == "ready" and require_admitted and root is not None:
        record = admission_path or admission_record_path(root, proposal.get("id", "INVALID"))
        errors.extend(validate_admission_record(path, record, root=root))
    elif require_admitted:
        errors.append("proposal status must be ready and have a valid admission record")
    return errors


def admission_record_path(root: Path, proposal_id: str) -> Path:
    return root / "docs" / "research" / "admissions" / f"{proposal_id}.json"


def validate_admission_record(
    proposal_path: Path,
    admission_path: Path,
    *,
    root: Path,
) -> list[str]:
    errors: list[str] = []
    proposal = _load_json(proposal_path, errors)
    record = _load_json(admission_path, errors, label="admission record")
    if not proposal or not record:
        return errors
    if record.get("schema_version") != 1:
        errors.append("admission.schema_version must be 1")
    if record.get("status") != "active":
        errors.append("admission.status must be active")
    if record.get("proposal_id") != proposal.get("id"):
        errors.append("admission.proposal_id does not match proposal")
    try:
        actual_relative = proposal_path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        errors.append("proposal must be stored inside the repository before admission")
        actual_relative = None
    if actual_relative is not None and record.get("proposal_path") != actual_relative:
        errors.append("admission.proposal_path does not match proposal location")
    if not _valid_sha(record.get("proposal_sha256"), "admission.proposal_sha256", errors):
        pass
    elif sha256_file(proposal_path) != record["proposal_sha256"]:
        errors.append("admission proposal hash no longer matches; re-authorization required")
    admitted_by = record.get("admitted_by")
    if not isinstance(admitted_by, str) or not admitted_by.startswith("human:"):
        errors.append("admission.admitted_by must identify a human authority")
    _nonempty_text(record.get("authorization_ref"), "admission.authorization_ref", errors)
    _nonempty_text(record.get("authorized_scope"), "admission.authorized_scope", errors)
    if not isinstance(record.get("admitted_at"), str) or not ISO_UTC_RE.fullmatch(record["admitted_at"]):
        errors.append("admission.admitted_at must use YYYY-MM-DDTHH:MM:SSZ")
    return errors


def git_head(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def verify_runtime_pins(proposal: dict[str, Any], root: Path) -> list[str]:
    """Verify mutable runtime state immediately before an experiment launch."""

    errors: list[str] = []
    experiment = proposal["experiment"]
    reproducibility = experiment["reproducibility"]
    revision = reproducibility["code_revision"]
    revision_check = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"], cwd=root, capture_output=True
    )
    if revision_check.returncode:
        errors.append("pinned code_revision is not a repository commit")
    else:
        for relative in reproducibility["code_paths"]:
            exists = subprocess.run(
                ["git", "cat-file", "-e", f"{revision}:{relative}"],
                cwd=root,
                capture_output=True,
            )
            if exists.returncode:
                errors.append(f"pinned code path is absent at code_revision: {relative}")
        diff = subprocess.run(
            ["git", "diff", "--quiet", revision, "--", *reproducibility["code_paths"]],
            cwd=root,
        )
        if diff.returncode:
            errors.append("pinned code paths differ from code_revision")
    if reproducibility["require_clean_tree"]:
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        if status.strip():
            errors.append("working tree is not clean")
    for field in ("inputs", "environment_files"):
        for pin in reproducibility[field]:
            path = root / pin["path"]
            if not path.is_file() or sha256_file(path) != pin["sha256"]:
                errors.append(f"runtime pin mismatch: {pin['path']}")
    for executable in reproducibility["executables"]:
        executable_path = root / executable["path"]
        if (
            not executable_path.is_file()
            or sha256_file(executable_path) != executable["sha256"]
        ):
            errors.append(f"executable byte mismatch: {executable['path']}")
            continue
        result = subprocess.run(
            executable["version_command"], cwd=root, capture_output=True, check=False
        )
        digest = sha256_bytes(result.stdout + result.stderr)
        if result.returncode or digest != executable["version_output_sha256"]:
            errors.append(f"executable version mismatch: {executable['path']}")
    verifier = experiment["evidence"].get("verifier")
    if verifier is not None:
        path = root / verifier["path"]
        if not path.is_file() or sha256_file(path) != verifier["sha256"]:
            errors.append(f"verifier pin mismatch: {verifier['path']}")
    return errors


def load_admitted_experiment(path: Path, root: Path) -> dict[str, Any]:
    """Load one launcher-ready proposal or raise ``ValueError``."""

    errors = validate_research_proposal(
        path, root=root, require_admitted=True, require_experiment=True
    )
    if errors:
        raise ValueError("\n".join(errors))
    proposal = json.loads(path.read_text(encoding="utf-8"))
    runtime_errors = verify_runtime_pins(proposal, root)
    if runtime_errors:
        raise ValueError("\n".join(runtime_errors))
    return proposal


def validate_run_manifest(path: Path, *, root: Path) -> list[str]:
    """Cold-check one supervisor-owned execution record and its pinned logs."""

    errors: list[str] = []
    manifest = _load_json(path, errors, label="run manifest")
    if not manifest:
        return errors
    if manifest.get("schema_version") != 1:
        errors.append("run manifest schema_version must be 1")
    if manifest.get("research_verdict") is not None:
        errors.append("run manifest research_verdict must remain null")
    status = manifest.get("execution_status")
    if status not in EXECUTION_STATUSES:
        errors.append(f"run manifest execution_status is invalid: {status}")

    proposal_relative = _safe_relative_path(
        manifest.get("proposal_path"), "run manifest proposal_path", errors
    )
    admission_relative = _safe_relative_path(
        manifest.get("admission_path"), "run manifest admission_path", errors
    )
    proposal_path = root / proposal_relative if proposal_relative else None
    admission_path = root / admission_relative if admission_relative else None
    if proposal_path is None or not proposal_path.is_file():
        errors.append("run manifest proposal is missing")
        return errors
    if admission_path is None or not admission_path.is_file():
        errors.append("run manifest admission record is missing")
        return errors
    if manifest.get("proposal_sha256") != sha256_file(proposal_path):
        errors.append("run manifest proposal hash mismatch")
    if manifest.get("admission_sha256") != sha256_file(admission_path):
        errors.append("run manifest admission hash mismatch")
    errors.extend(
        validate_research_proposal(
            proposal_path,
            require_experiment=True,
        )
    )
    errors.extend(validate_admission_record(proposal_path, admission_path, root=root))

    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    experiment = proposal.get("experiment", {})
    if manifest.get("proposal_id") != proposal.get("id"):
        errors.append("run manifest proposal_id mismatch")
    if manifest.get("command") != experiment.get("command"):
        errors.append("run manifest command mismatch")
    if manifest.get("pinned_code_revision") != experiment.get("reproducibility", {}).get("code_revision"):
        errors.append("run manifest code revision mismatch")
    launch_revision = manifest.get("launch_head_revision")
    if not isinstance(launch_revision, str) or not REVISION_RE.fullmatch(launch_revision):
        errors.append("run manifest launch_head_revision must be a 40-hex commit")
    elif subprocess.run(
        ["git", "cat-file", "-e", f"{launch_revision}^{{commit}}"],
        cwd=root,
        capture_output=True,
    ).returncode:
        errors.append("run manifest launch_head_revision is not in this repository")
    expected_manifest = experiment.get("run_record", {}).get("manifest_path")
    try:
        actual_manifest = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        actual_manifest = None
    if actual_manifest != expected_manifest:
        errors.append("run manifest is not at the proposal-pinned path")

    expected_record = experiment.get("run_record", {})
    for name in ("stdout", "stderr"):
        relative = _safe_relative_path(
            manifest.get(f"{name}_path"), f"run manifest {name}_path", errors
        )
        if relative != expected_record.get(f"{name}_path"):
            errors.append(f"run manifest {name}_path differs from the proposal")
        if relative is None or not (root / relative).is_file():
            errors.append(f"run manifest {name} log is missing")
        elif manifest.get(f"{name}_sha256") != sha256_file(root / relative):
            errors.append(f"run manifest {name} hash mismatch")

    limits = manifest.get("limits", {})
    artifacts = manifest.get("artifact_bytes", {})
    if not isinstance(limits, dict):
        errors.append("run manifest limits must be an object")
        limits = {}
    if not isinstance(artifacts, dict):
        errors.append("run manifest artifact_bytes must be an object")
        artifacts = {}
    budget = experiment.get("budget", {})
    expected_limits = {
        "wall_time_seconds": budget.get("wall_time_seconds"),
        "memory_bytes": budget.get("memory_bytes"),
        "max_new_artifact_bytes": budget.get("max_new_artifact_bytes"),
    }
    if limits != expected_limits:
        errors.append("run manifest limits differ from the admitted proposal")
    for name in ("baseline", "final_before_manifest"):
        values = artifacts.get(name)
        if not isinstance(values, dict) or not all(
            isinstance(key, str) and isinstance(value, int) and value >= 0
            for key, value in values.items()
        ):
            errors.append(f"run manifest artifact_bytes.{name} is invalid")
    baseline = artifacts.get("baseline", {})
    final = artifacts.get("final_before_manifest", {})
    if isinstance(baseline, dict) and set(baseline) != set(budget.get("artifact_roots", [])):
        errors.append("run manifest artifact roots differ from the proposal")
    if isinstance(final, dict) and set(final) != set(budget.get("artifact_roots", [])):
        errors.append("run manifest final artifact roots differ from the proposal")
    elapsed = manifest.get("elapsed_seconds")
    growth = artifacts.get("final_growth")
    peak_growth = artifacts.get("peak_observed_growth")
    if not isinstance(elapsed, (int, float)) or elapsed < 0:
        errors.append("run manifest elapsed_seconds must be nonnegative")
    if not isinstance(growth, int) or growth < 0:
        errors.append("run manifest final_growth must be nonnegative")
    if not isinstance(peak_growth, int) or peak_growth < 0:
        errors.append("run manifest peak_observed_growth must be nonnegative")
    elif isinstance(growth, int) and peak_growth < growth:
        errors.append("run manifest peak growth is below final growth")
    if isinstance(baseline, dict) and isinstance(final, dict):
        derived_growth = max(0, sum(final.values()) - sum(baseline.values()))
        if growth != derived_growth:
            errors.append("run manifest final_growth does not match artifact maps")
    return_code = manifest.get("process_return_code")
    if return_code is not None and not isinstance(return_code, int):
        errors.append("run manifest process_return_code must be integer or null")
    if status == "completed":
        if return_code != 0:
            errors.append("completed execution must have return code zero")
        if not isinstance(elapsed, (int, float)) or elapsed >= limits.get("wall_time_seconds", -1):
            errors.append("completed execution exceeds its wall limit")
        if not isinstance(growth, int) or growth > limits.get("max_new_artifact_bytes", -1):
            errors.append("completed execution exceeds its artifact limit")
    if status == "resource_stop_wall" and isinstance(elapsed, (int, float)):
        if elapsed < limits.get("wall_time_seconds", float("inf")):
            errors.append("wall resource stop occurred below the declared limit")
    if status == "resource_stop_artifact" and isinstance(peak_growth, int):
        if peak_growth <= limits.get("max_new_artifact_bytes", peak_growth):
            errors.append("artifact resource stop did not exceed the declared limit")
    if status == "process_error" and (return_code is None or return_code == 0):
        errors.append("process_error execution must have a nonzero return code")
    if status == "supervisor_error" and not manifest.get("supervisor_error"):
        errors.append("supervisor_error execution must explain the supervisor failure")
    return errors
