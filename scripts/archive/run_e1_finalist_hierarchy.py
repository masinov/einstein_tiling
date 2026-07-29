#!/usr/bin/env python
"""Blind first-composition search for the E1 finalist.

This is deliberately stricter than mining one attractive finite disk.  Small
candidate macrotile templates are proposed from the largest nested patch, then
the same exact template family must cover protected cores in all five
independently phase-biased patches and in the large patch.  No substitution
ancestry or candidate-specific scale is supplied.

Passing this screen is only the first A6 obligation.  A rule must subsequently
close recursively and be locally recognizable before it can support an
aperiodicity proof.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.tilings.substitution import (
    _canonical_colored_cluster,
    canonical_cluster,
    deletion_variants,
    template_occurrences,
)
from einstein.polykites.hierarchy import (
    _hex_nearest_groups,
    frequent_hex_nearest_templates,
    forced_typed_core_options,
    mine_joint_option_state_recursive_library,
    placement_poses,
    typed_core_backbone,
    verify_option_state_recursive_library,
)

ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS = ROOT / "docs" / "notebook" / "assets"
ROBUSTNESS = ASSETS / "e1-finalist-robustness.json"
NESTED = ASSETS / "e1-finalist-nested.json"
FINALIST = ASSETS / "e1-finalist-results.json"
OUTPUT = ASSETS / "e1-finalist-hierarchy-screen.json"


def _norm2(pose):
    x, y = pose[2][0], pose[2][2]
    return x * x + x * y + y * y


def _template_json(template):
    return [[s, r, list(t)] for s, r, t in template]


def _template_from_json(rows):
    return tuple((s, r, tuple(t)) for s, r, t in rows)


def _cover_solutions(occurrences, core, limit=2):
    """Exact-cover multiplicity capped at ``limit`` for a protected core."""
    core = set(core)
    occurrences = tuple(sorted(
        {group for group in occurrences if group & core},
        key=lambda group: tuple(sorted(group)),
    ))
    by_item = defaultdict(list)
    for variable, group in enumerate(occurrences, 1):
        for item in group:
            by_item[item].append(variable)
    uncovered = sum(not by_item[item] for item in core)
    if uncovered:
        return 0, (), len(occurrences), uncovered
    clauses = []
    for item, variables in by_item.items():
        if item in core:
            clauses.append(variables)
        for i, left in enumerate(variables):
            for right in variables[i + 1:]:
                clauses.append([-left, -right])
    solutions = []
    with Cadical195(bootstrap_with=clauses) as solver:
        while len(solutions) < limit and solver.solve():
            positive = {value for value in solver.get_model() if value > 0}
            chosen = tuple(
                occurrences[variable - 1]
                for variable in range(1, len(occurrences) + 1)
                if variable in positive
            )
            solutions.append(chosen)
            solver.add_clause([
                -variable
                for variable in range(1, len(occurrences) + 1)
                if variable in positive
            ])
    return len(solutions), solutions[0] if solutions else (), len(occurrences), 0


def _observed_recursive_language(option_samples, group_sizes):
    """All exact typed nearest-group patterns observed in the samples."""
    values = sorted({
        value for _, options in option_samples for value in options.values()
    })
    value_states = {value: state for state, value in enumerate(values)}
    patterns = set()
    for _, options in option_samples:
        poses = tuple(sorted(options))
        states = tuple(value_states[options[pose]] for pose in poses)
        for group in _hex_nearest_groups(poses, group_sizes):
            patterns.add(_canonical_colored_cluster(
                [poses[i] for i in group],
                [states[i] for i in group],
            ))
    selected = [
        [
            {"pose": [s, r, list(t)], "state": state}
            for (s, r, t), state in pattern
        ]
        for pattern in sorted(patterns)
    ]
    return values, selected


def _load_samples():
    robustness = json.loads(ROBUSTNESS.read_text())
    nested = json.loads(NESTED.read_text())
    samples = []
    for row in robustness["results"]:
        phase = row["phase_seed"]
        label = "production" if phase is None else f"phase-{phase}"
        poses = placement_poses(row["certificate"]["placements"])
        samples.append({
            "label": label,
            "poses": poses,
            "core_r2": 5_000,
            "core": tuple(i for i, pose in enumerate(poses) if _norm2(pose) <= 5_000),
        })
    original = json.loads(FINALIST.read_text())["a3"]["certificate"]
    poses = placement_poses(original["placements"])
    samples.append({
        "label": "production-r2-50000",
        "poses": poses,
        "core_r2": 30_000,
        "core": tuple(i for i, pose in enumerate(poses) if _norm2(pose) <= 30_000),
    })
    large_cert = nested["nested_chain"][-1]["certificate"]
    poses = placement_poses(large_cert["placements"])
    samples.append({
        "label": "nested-r2-100000",
        "poses": poses,
        "core_r2": 30_000,
        "core": tuple(i for i, pose in enumerate(poses) if _norm2(pose) <= 30_000),
    })
    return robustness["candidate"], samples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=30)
    parser.add_argument("--min-arity", type=int, default=6)
    parser.add_argument("--max-arity", type=int, default=12)
    args = parser.parse_args()

    candidate, samples = _load_samples()
    proposal_sample = samples[-1]
    histogram = frequent_hex_nearest_templates(
        proposal_sample["poses"],
        min_size=args.min_arity,
        max_size=args.max_arity,
        top=args.top,
    )
    occurrence_cache = [dict() for _ in samples]

    def occurrences(sample_index, template):
        cache = occurrence_cache[sample_index]
        if template not in cache:
            cache[template] = template_occurrences(
                template, samples[sample_index]["poses"]
            )
        return cache[template]

    screened = Counter()
    accepted = []
    for arity in range(args.min_arity, args.max_arity + 1):
        for proposal_rank, (full, frequency) in enumerate(histogram[arity], 1):
            variants = (full, *deletion_variants(full))
            for variant_index, missing in enumerate(variants):
                screened["rules"] += 1
                sample_results = []
                rejected = False
                for sample_index, sample in enumerate(samples):
                    combined = (
                        *occurrences(sample_index, full),
                        *occurrences(sample_index, missing),
                    )
                    multiplicity, cover, n_occurrences, uncovered = _cover_solutions(
                        combined, sample["core"]
                    )
                    if uncovered:
                        screened["coverage_rejects"] += 1
                        rejected = True
                        break
                    if not multiplicity:
                        screened["sat_rejects"] += 1
                        rejected = True
                        break
                    sample_results.append({
                        "label": sample["label"],
                        "core_r2": sample["core_r2"],
                        "core_tiles": len(sample["core"]),
                        "occurrences": n_occurrences,
                        "solutions_capped_at_2": multiplicity,
                        "groups": len(cover),
                        "full_groups": sum(len(group) == len(full) for group in cover),
                        "exception_groups": sum(
                            len(group) == len(missing) for group in cover
                        ),
                    })
                if rejected:
                    continue
                screened["accepted"] += 1
                accepted.append({
                    "arity": arity,
                    "proposal_rank": proposal_rank,
                    "proposal_frequency": frequency,
                    "variant": "full-only" if variant_index == 0 else "one-deletion",
                    "full": _template_json(full),
                    "missing": _template_json(missing),
                    "samples": sample_results,
                    "all_unique": all(
                        row["solutions_capped_at_2"] == 1
                        for row in sample_results
                    ),
                })
                print(
                    "ACCEPT",
                    f"arity={arity}",
                    f"rank={proposal_rank}",
                    f"variant={variant_index}",
                    "unique=" + str(accepted[-1]["all_unique"]),
                    flush=True,
                )

    payload = {
        "kind": "blind-first-composition-screen",
        "candidate": candidate,
        "scope": {
            "proposal_patch": proposal_sample["label"],
            "arities": [args.min_arity, args.max_arity],
            "top_templates_per_arity": args.top,
            "template_family": "full scaffold plus zero/one child deletion",
            "samples": [
                {
                    "label": sample["label"],
                    "tiles": len(sample["poses"]),
                    "core_r2": sample["core_r2"],
                    "core_tiles": len(sample["core"]),
                }
                for sample in samples
            ],
        },
        "proposal_frequencies": {
            str(arity): [frequency for _, frequency in histogram[arity]]
            for arity in histogram
        },
        "screened": dict(screened),
        "accepted": accepted,
        "status": "FIRST-COMPOSITION" if accepted else "NO-COMPOSITION",
        "interpretation": (
            "A surviving first composition remains a heuristic until recursive "
            "closure and finite local recognizability are proved."
        ),
    }
    physical_option_samples = [
        (sample["label"], {pose: (0,) for pose in sample["poses"]})
        for sample in samples
    ]
    general_physical = []
    options_by_label = dict(physical_option_samples)
    physical_group_sizes = [(arity,) for arity in range(6, 13)]
    physical_group_sizes.extend((arity, arity + 1) for arity in range(6, 12))
    for group_sizes in physical_group_sizes:
        print("GENERAL physical-library arities", group_sizes, flush=True)
        fit = mine_joint_option_state_recursive_library(
            physical_option_samples,
            training_r2=2_500,
            forcing_r2=1_500,
            group_sizes=group_sizes,
        )
        wide_confirmations = []
        if fit.get("satisfiable"):
            option_values = [
                tuple(value) for value in fit["option_state_values"]
            ]
            for sample in samples:
                if sample["core_r2"] != 30_000:
                    continue
                confirmation = verify_option_state_recursive_library(
                    options_by_label[sample["label"]],
                    fit["selected_patterns"],
                    training_r2=8_000,
                    forcing_r2=6_000,
                    group_sizes=group_sizes,
                    option_state_values=option_values,
                )
                confirmation["label"] = sample["label"]
                wide_confirmations.append(confirmation)
        general_physical.append({
            "group_sizes": list(group_sizes),
            "fit": fit,
            "wide_confirmations": wide_confirmations,
        })
    payload["general_physical_library"] = {
        "single_arity_fits": general_physical,
        "proof_status": (
            "blind arbitrary 6-12-child nearest-cluster library; recursive "
            "closure and recognizability remain required"
        ),
    }
    if (
        len(accepted) == 2
        and accepted[0]["full"] == accepted[1]["full"]
        and accepted[0]["missing"] != accepted[1]["missing"]
    ):
        templates = (
            _template_from_json(accepted[0]["full"]),
            _template_from_json(accepted[0]["missing"]),
            _template_from_json(accepted[1]["missing"]),
        )
        physical = []
        option_samples = []
        for sample in samples:
            base_r2 = 2_500 if sample["core_r2"] == 5_000 else 15_000
            print("FORCING", sample["label"], flush=True)
            backbone = typed_core_backbone(
                sample["poses"], sample["core"], templates, base_r2
            )
            options = forced_typed_core_options(
                sample["poses"], sample["core"], templates, base_r2
            )
            physical.append({
                "label": sample["label"],
                "base_r2": base_r2,
                "backbone": backbone,
                "forced_parent_anchors": len(options),
            })
            option_samples.append((sample["label"], options))

        print("RECURSIVE common-radius", flush=True)
        recursive = mine_joint_option_state_recursive_library(
            option_samples,
            training_r2=1_500,
            forcing_r2=1_000,
        )
        wide_confirmations = []
        if recursive.get("satisfiable"):
            option_values = [
                tuple(value) for value in recursive["option_state_values"]
            ]
            options_by_label = dict(option_samples)
            for sample in samples:
                if sample["core_r2"] != 30_000:
                    continue
                print("RECURSIVE wide", sample["label"], flush=True)
                confirmation = verify_option_state_recursive_library(
                    options_by_label[sample["label"]],
                    recursive["selected_patterns"],
                    training_r2=8_000,
                    forcing_r2=6_000,
                    option_state_values=option_values,
                )
                confirmation["label"] = sample["label"]
                wide_confirmations.append(confirmation)

        options_by_label = dict(option_samples)
        large_option_samples = [
            (sample["label"], options_by_label[sample["label"]])
            for sample in samples
            if sample["core_r2"] == 30_000
        ]
        recursive_feasibility = []
        size_sets = [(size,) for size in range(4, 13)]
        size_sets.extend(((7, 8), tuple(range(4, 13))))
        for group_sizes in size_sets:
            print("RECURSIVE feasibility", group_sizes, flush=True)
            option_values, observed_patterns = _observed_recursive_language(
                large_option_samples, group_sizes
            )
            confirmations = []
            for label, options in large_option_samples:
                confirmation = verify_option_state_recursive_library(
                    options,
                    observed_patterns,
                    training_r2=8_000,
                    forcing_r2=6_000,
                    group_sizes=group_sizes,
                    option_state_values=option_values,
                )
                confirmation["label"] = label
                confirmations.append(confirmation)
            recursive_feasibility.append({
                "group_sizes": list(group_sizes),
                "observed_patterns": len(observed_patterns),
                "samples": confirmations,
                "all_satisfiable": all(
                    row.get("satisfiable", False) for row in confirmations
                ),
                "all_forced": all(
                    row.get("inner_grouping_forced", False)
                    for row in confirmations
                ),
            })

        next_recursive = None
        if (
            wide_confirmations
            and all(row.get("inner_grouping_forced") for row in wide_confirmations)
        ):
            next_samples = []
            for confirmation in wide_confirmations:
                next_samples.append((
                    confirmation["label"],
                    {
                        (
                            group["base"][0],
                            group["base"][1],
                            tuple(group["base"][2]),
                        ): (group["pattern"],)
                        for group in confirmation["forced_groups"]
                    },
                ))
            print("RECURSIVE next-scale", flush=True)
            next_recursive = mine_joint_option_state_recursive_library(
                next_samples,
                training_r2=2_500,
                forcing_r2=1_500,
            )

        payload["rule_family"] = {
            "template_types": ["full-8", "exception-a-7", "exception-b-7"],
            "templates": [_template_json(template) for template in templates],
            "physical_forcing": physical,
            "recursive_common_radius": recursive,
            "recursive_wide_confirmations": wide_confirmations,
            "recursive_wide_feasibility": recursive_feasibility,
            "next_recursive_probe": next_recursive,
            "proof_status": (
                "finite hierarchy evidence only; no stationary substitution "
                "closure or all-collars recognizability theorem"
            ),
        }
        payload["status"] = "RULE-FAMILY"
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps(payload["screened"], sort_keys=True))
    print(OUTPUT.relative_to(ROOT))
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
