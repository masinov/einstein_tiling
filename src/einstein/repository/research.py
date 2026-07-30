"""Mechanical admission primitives shared by research command entry points.

Free mathematical exploration is not represented here.  This module validates
the boundary at which a sustained program launches a nontrivial computation.
"""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Any


PROPOSAL_KINDS = {"research-program", "experiment"}
PROPOSAL_STATUSES = {"draft", "admitted", "closed"}
SCOPE_LEVELS = {
    "field-level-problem",
    "architecture-independent-class",
    "recognized-mathematical-family",
    "specific-construction",
    "single-instance",
}
PLACEHOLDERS = ("[replace", "todo", "tbd", "example-only")


def tree_bytes(path: Path) -> int:
    """Total bytes in a file tree, treating an absent root as empty."""

    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"proposal is not readable JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append("proposal root must be a JSON object")
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


def _safe_relative_path(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a nonempty repository-relative path")
        return
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{field} must stay inside the repository")


def _portfolio_program_ids(root: Path, errors: list[str]) -> set[str]:
    path = root / "docs" / "research" / "portfolio.json"
    try:
        document = json.loads(path.read_text())
        return {item["id"] for item in document["programs"]}
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        errors.append(f"current research portfolio is invalid: {exc}")
        return set()


def validate_research_proposal(
    path: Path,
    *,
    root: Path | None = None,
    require_admitted: bool = False,
    require_experiment: bool = False,
) -> list[str]:
    """Return every mechanical admission error in one proposal.

    The gate deliberately cannot decide whether a mathematical idea is good.
    It checks that a committed campaign states its scope and consequences and,
    for computation, freezes a command and externally supervised budget.
    """

    errors: list[str] = []
    proposal = _load_json(path, errors)
    if not proposal:
        return errors

    if proposal.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    proposal_id = proposal.get("id")
    if not isinstance(proposal_id, str) or not re.fullmatch(
        r"RP-[0-9]{4}-[0-9]{2}-[0-9]{2}-[A-Z0-9-]+", proposal_id
    ):
        errors.append("id must match RP-YYYY-MM-DD-NAME")

    kind = proposal.get("kind")
    if kind not in PROPOSAL_KINDS:
        errors.append(f"kind must be one of {sorted(PROPOSAL_KINDS)}")
    if require_experiment and kind != "experiment":
        errors.append("the research launcher accepts experiment proposals only")

    status = proposal.get("status")
    if status not in PROPOSAL_STATUSES:
        errors.append(f"status must be one of {sorted(PROPOSAL_STATUSES)}")
    if require_admitted and status != "admitted":
        errors.append("proposal status must be admitted")

    _nonempty_text(proposal.get("title"), "title", errors, minimum=8)
    _nonempty_text(proposal.get("thesis"), "thesis", errors)
    _nonempty_text(
        proposal.get("mission_connection"), "mission_connection", errors
    )
    _nonempty_text(
        proposal.get("alternatives_considered"),
        "alternatives_considered",
        errors,
    )
    _nonempty_text(
        proposal.get("failure_or_pivot"), "failure_or_pivot", errors
    )

    scope = proposal.get("scope_level")
    if scope not in SCOPE_LEVELS:
        errors.append(f"scope_level must be one of {sorted(SCOPE_LEVELS)}")

    if root is not None:
        program_ids = _portfolio_program_ids(root, errors)
        if proposal.get("program_id") not in program_ids:
            errors.append("program_id is not present in the current portfolio")

    prior_art = proposal.get("prior_art")
    if not isinstance(prior_art, dict):
        errors.append("prior_art must be an object")
    else:
        if not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}",
            str(prior_art.get("snapshot_date", "")),
        ):
            errors.append("prior_art.snapshot_date must use YYYY-MM-DD")
        sources = prior_art.get("primary_sources")
        if not isinstance(sources, list) or not sources or not all(
            isinstance(item, str) and item.strip() for item in sources
        ):
            errors.append("prior_art.primary_sources must be a nonempty list")
        _nonempty_text(
            prior_art.get("non_redundancy"),
            "prior_art.non_redundancy",
            errors,
        )
        facts = prior_art.get("user_facts_resolved")
        if not isinstance(facts, list):
            errors.append("prior_art.user_facts_resolved must be a list")

    outcomes = proposal.get("outcomes")
    if not isinstance(outcomes, list) or len(outcomes) < 2:
        errors.append("outcomes must contain at least two result/action branches")
    else:
        actions: list[str] = []
        for index, outcome in enumerate(outcomes):
            if not isinstance(outcome, dict):
                errors.append(f"outcomes[{index}] must be an object")
                continue
            _nonempty_text(
                outcome.get("result"), f"outcomes[{index}].result", errors
            )
            _nonempty_text(
                outcome.get("action"), f"outcomes[{index}].action", errors
            )
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

    if kind == "experiment":
        experiment = proposal.get("experiment")
        if not isinstance(experiment, dict):
            errors.append("experiment proposal requires an experiment object")
        else:
            _nonempty_text(
                experiment.get("proposition"), "experiment.proposition", errors
            )
            command = experiment.get("command")
            if not isinstance(command, list) or not command or not all(
                isinstance(item, str) and item for item in command
            ):
                errors.append("experiment.command must be a nonempty argv list")

            budget = experiment.get("budget")
            if not isinstance(budget, dict):
                errors.append("experiment.budget must be an object")
            else:
                wall = budget.get("wall_time_seconds")
                artifact_bytes = budget.get("max_new_artifact_bytes")
                if not isinstance(wall, int) or wall <= 0:
                    errors.append(
                        "experiment.budget.wall_time_seconds must be positive"
                    )
                if not isinstance(artifact_bytes, int) or artifact_bytes < 0:
                    errors.append(
                        "experiment.budget.max_new_artifact_bytes must be nonnegative"
                    )
                roots = budget.get("artifact_roots")
                if not isinstance(roots, list) or not roots:
                    errors.append(
                        "experiment.budget.artifact_roots must be a nonempty list"
                    )
                else:
                    for index, item in enumerate(roots):
                        _safe_relative_path(
                            item,
                            f"experiment.budget.artifact_roots[{index}]",
                            errors,
                        )
                if budget.get("external_supervision") is not True:
                    errors.append(
                        "experiment.budget.external_supervision must be true"
                    )

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

    return errors


def load_admitted_experiment(path: Path, root: Path) -> dict[str, Any]:
    """Load one launcher-ready proposal or raise ``ValueError``."""

    errors = validate_research_proposal(
        path,
        root=root,
        require_admitted=True,
        require_experiment=True,
    )
    if errors:
        raise ValueError("\n".join(errors))
    return json.loads(path.read_text())
