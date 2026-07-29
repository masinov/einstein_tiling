#!/usr/bin/env python3
"""Discover, build and cold-verify retained exact certificate families."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.certificates import FAMILIES, execute, family, validate_registry


ROOT = repository_root(Path(__file__))


def _operation_parser(
    subparsers, operation: str, family_name: str
) -> argparse.ArgumentParser:
    item = family(family_name)
    command = subparsers.add_parser(family_name, help=item.description)
    artifact_flag = "--output" if operation == "build" else "--input"
    command.add_argument(
        artifact_flag,
        dest="artifact",
        type=Path,
        default=ROOT / item.artifact,
        help=f"artifact path (default: {item.artifact})",
    )
    specification = item.build if operation == "build" else item.verify
    seen = set()
    for input_item in specification.inputs:
        if input_item.source == "artifact" or input_item.name in seen:
            continue
        seen.add(input_item.name)
        option = f"--{input_item.name.replace('_', '-')}"
        kwargs = {"type": Path}
        if input_item.source == "dependency":
            dependency = family(input_item.family)
            kwargs["help"] = (
                f"override {input_item.name} dependency "
                f"(default: {dependency.artifact})"
            )
        elif input_item.default is not None:
            kwargs["default"] = ROOT / input_item.default
            kwargs["help"] = f"external input (default: {input_item.default})"
        else:
            kwargs["required"] = True
            kwargs["help"] = "required external input"
        command.add_argument(option, dest=input_item.name, **kwargs)
    command.set_defaults(operation=operation, family=family_name)
    return command


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="list registered certificate families")
    describe = commands.add_parser("describe", help="show one family contract")
    describe.add_argument("family", choices=tuple(item.name for item in FAMILIES))
    for operation in ("build", "verify"):
        operation_parser = commands.add_parser(
            operation, help=f"{operation} one registered family"
        )
        families = operation_parser.add_subparsers(required=True)
        for item in FAMILIES:
            _operation_parser(families, operation, item.name)
    return result


def main() -> None:
    args = parser().parse_args()
    validate_registry(ROOT)
    if args.command == "list":
        for item in FAMILIES:
            print(f"{item.name:30} {item.artifact}")
        return
    if args.command == "describe":
        print(json.dumps(family(args.family).as_dict(), indent=2))
        return

    item = family(args.family)
    specification = item.build if args.operation == "build" else item.verify
    overrides = {
        input_item.name: getattr(args, input_item.name)
        for input_item in specification.inputs
        if input_item.source != "artifact"
        and hasattr(args, input_item.name)
        and getattr(args, input_item.name) is not None
    }
    execute(
        ROOT,
        args.family,
        args.operation,
        artifact_path=args.artifact,
        overrides=overrides,
    )
    verb = "built" if args.operation == "build" else "verified"
    print(f"{verb} {args.family}: {args.artifact}")


if __name__ == "__main__":
    main()
