#!/usr/bin/env python3
"""Discover and dispatch retained exact certificate operations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys

from einstein.certificates import FAMILIES, family, validate_registry


ROOT = Path(__file__).resolve().parents[1]


def command(item, operation: str, arguments: list[str]) -> list[str]:
    script = item.builder if operation == "build" else item.verifier
    return [sys.executable, str(ROOT / script), *arguments]


def main() -> None:
    raw_arguments = sys.argv[1:]
    if "--" in raw_arguments:
        separator = raw_arguments.index("--")
        cli_arguments = raw_arguments[:separator]
        forwarded_arguments = raw_arguments[separator + 1 :]
    else:
        cli_arguments = raw_arguments
        forwarded_arguments = []

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    describe = subparsers.add_parser("describe")
    describe.add_argument("family")
    run = subparsers.add_parser("run")
    run.add_argument("family")
    run.add_argument("operation", choices=("build", "verify"))
    run.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(cli_arguments)

    validate_registry(ROOT)
    if args.command == "list":
        for item in FAMILIES:
            print(f"{item.name:30} {item.artifact}")
        return

    item = family(args.family)
    if args.command == "describe":
        print(json.dumps(item.as_dict(), indent=2))
        return

    invocation = command(item, args.operation, forwarded_arguments)
    print(shlex.join(invocation))
    if not args.dry_run:
        subprocess.run(invocation, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
