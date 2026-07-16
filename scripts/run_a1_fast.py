#!/usr/bin/env python
"""Compile and run exact A1 torus screening on one compiled A0 level.

Usage:
  venv/bin/python scripts/run_a1_fast.py INPUT [SURVIVORS] [CERTIFICATES]
      [--jobs N] [--k-max K] [--node-budget N]
"""

from __future__ import annotations

import argparse
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "tools" / "a1_torus.rs"
BINARY = ROOT / "target" / "a1_torus"


HEADER = struct.Struct("<4sBBHQ")
STATS = re.compile(
    r"periodic=(?P<periodic>\d+) survivors=(?P<survivors>\d+) "
    r"exhausted=(?P<exhausted>\d+)"
)


def _parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("survivors", nargs="?", type=Path)
    parser.add_argument("certificates", nargs="?", type=Path)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--k-max", type=int, default=12)
    parser.add_argument("--node-budget", type=int, default=200_000)
    return parser


def _compile():
    BINARY.parent.mkdir(parents=True, exist_ok=True)
    if (
        not BINARY.exists()
        or BINARY.stat().st_mtime < SOURCE.stat().st_mtime
    ):
        subprocess.run(
            [
                "rustc",
                "--edition=2021",
                "-C",
                "opt-level=3",
                str(SOURCE),
                "-o",
                str(BINARY),
            ],
            check=True,
        )


def _metadata(path):
    with path.open("rb") as source:
        magic, version, n, reserved, count = HEADER.unpack(
            source.read(HEADER.size)
        )
    if magic != b"A0PK" or version != 1 or reserved != 0:
        raise ValueError("unsupported compiled A0 input")
    return n, count


def _merge_stream(parts, destination, n, count):
    with destination.open("wb") as output:
        output.write(HEADER.pack(b"A0PK", 1, n, 0, count))
        for part in parts:
            with part.open("rb") as source:
                _, _, part_n, _, part_count = HEADER.unpack(
                    source.read(HEADER.size)
                )
                assert part_n == n
                copied = 0
                while block := source.read(1024 * 1024):
                    output.write(block)
                    copied += len(block)
                assert copied == part_count * n * 2


def main() -> int:
    args = _parser().parse_args()
    if args.jobs < 1:
        raise SystemExit("--jobs must be positive")
    _compile()
    n, count = _metadata(args.input)
    jobs = min(args.jobs, count)
    if jobs == 1:
        command = [
            str(BINARY),
            str(args.input),
            str(args.survivors) if args.survivors else "-",
            str(args.certificates) if args.certificates else "-",
            str(args.k_max),
            str(args.node_budget),
        ]
        return subprocess.run(command).returncode

    with tempfile.TemporaryDirectory(prefix="a1-torus-") as directory:
        temporary = Path(directory)
        processes = []
        survivor_parts = []
        certificate_parts = []
        base, extra = divmod(count, jobs)
        start = 0
        for job in range(jobs):
            size = base + (job < extra)
            survivor = temporary / f"survivors-{job:03}.bin"
            certificate = temporary / f"certificates-{job:03}.jsonl"
            survivor_parts.append(survivor)
            certificate_parts.append(certificate)
            command = [
                str(BINARY),
                str(args.input),
                str(survivor) if args.survivors else "-",
                str(certificate) if args.certificates else "-",
                str(args.k_max),
                str(args.node_budget),
                str(start),
                str(size),
            ]
            processes.append(subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                text=True,
            ))
            start += size
        totals = {"periodic": 0, "survivors": 0, "exhausted": 0}
        for process in processes:
            stdout, _ = process.communicate()
            if process.returncode:
                return process.returncode
            match = STATS.search(stdout)
            if match is None:
                raise RuntimeError(f"missing A1 worker stats: {stdout!r}")
            for key in totals:
                totals[key] += int(match.group(key))
        if args.survivors:
            _merge_stream(
                survivor_parts,
                args.survivors,
                n,
                totals["survivors"],
            )
        if args.certificates:
            with args.certificates.open("wb") as output:
                for part in certificate_parts:
                    output.write(part.read_bytes())
        print(
            f"n={n} total={count} periodic={totals['periodic']} "
            f"survivors={totals['survivors']} "
            f"exhausted={totals['exhausted']} jobs={jobs}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
