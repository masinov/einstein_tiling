#!/usr/bin/env python
"""Compile and run exact first-corona screening on one A1 survivor stream.

Usage:
  venv/bin/python scripts/archive/run_a2_fast.py INPUT [SURVIVORS] [WITNESSES]
      [--node-budget N]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE = ROOT / "tools" / "a2_corona.rs"
BINARY = ROOT / "target" / "a2_corona"
HEADER = struct.Struct("<4sBBHQ")
STATS = re.compile(
    r"below_cap=(?P<below_cap>\d+) witnessed=(?P<witnessed>\d+) "
    r"exhausted=(?P<exhausted>\d+) survivors=(?P<survivors>\d+)"
)


def _metadata(path):
    with path.open("rb") as source:
        magic, version, n, reserved, count = HEADER.unpack(
            source.read(HEADER.size)
        )
    if magic != b"A0PK" or version != 1 or reserved != 0:
        raise ValueError("unsupported compiled A0/A1 input")
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("survivors", nargs="?", type=Path)
    parser.add_argument("witnesses", nargs="?", type=Path)
    parser.add_argument("--exhausted", type=Path)
    parser.add_argument("--node-budget", type=int, default=100_000)
    parser.add_argument("--depth-cap", type=int, default=1)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--chunk-size", type=int, default=25_000)
    args = parser.parse_args()
    if args.jobs < 1 or args.chunk_size < 1:
        raise SystemExit("--jobs and --chunk-size must be positive")
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
    n, count = _metadata(args.input)
    if args.jobs == 1 or count <= args.chunk_size:
        command = [
            str(BINARY),
            str(args.input),
            str(args.survivors) if args.survivors else "-",
            str(args.witnesses) if args.witnesses else "-",
            str(args.exhausted) if args.exhausted else "-",
            str(args.depth_cap),
            str(args.node_budget),
        ]
        return subprocess.run(command).returncode

    with tempfile.TemporaryDirectory(prefix="a2-corona-") as directory:
        temporary = Path(directory)
        chunks = []
        for chunk, start in enumerate(range(0, count, args.chunk_size)):
            size = min(args.chunk_size, count - start)
            survivor = temporary / f"survivors-{chunk:06}.bin"
            witness = temporary / f"witnesses-{chunk:06}.jsonl"
            exhausted = temporary / f"exhausted-{chunk:06}.bin"
            chunks.append((
                chunk, start, size, survivor, witness, exhausted
            ))

        def run_chunk(item):
            chunk, start, size, survivor, witness, exhausted = item
            result = subprocess.run(
                [
                    str(BINARY),
                    str(args.input),
                    str(survivor) if args.survivors else "-",
                    str(witness) if args.witnesses else "-",
                    str(exhausted) if args.exhausted else "-",
                    str(args.depth_cap),
                    str(args.node_budget),
                    str(start),
                    str(size),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            match = STATS.search(result.stdout)
            if match is None:
                raise RuntimeError(
                    f"missing A2 worker stats for chunk {chunk}: "
                    f"{result.stdout!r}"
                )
            return chunk, {
                key: int(match.group(key))
                for key in (
                    "below_cap", "witnessed", "exhausted", "survivors"
                )
            }

        totals = {
            "below_cap": 0,
            "witnessed": 0,
            "exhausted": 0,
            "survivors": 0,
        }
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.jobs
        ) as executor:
            for _, stats in executor.map(run_chunk, chunks):
                for key in totals:
                    totals[key] += stats[key]
        if args.survivors:
            _merge_stream(
                [item[3] for item in chunks],
                args.survivors,
                n,
                totals["survivors"],
            )
        if args.witnesses:
            with args.witnesses.open("wb") as output:
                for item in chunks:
                    output.write(item[4].read_bytes())
        if args.exhausted:
            _merge_stream(
                [item[5] for item in chunks],
                args.exhausted,
                n,
                totals["exhausted"],
            )
        print(
            f"n={n} total={count} depth_cap={args.depth_cap} "
            f"below_cap={totals['below_cap']} "
            f"witnessed={totals['witnessed']} "
            f"exhausted={totals['exhausted']} "
            f"survivors={totals['survivors']} jobs={args.jobs} "
            f"chunks={len(chunks)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
