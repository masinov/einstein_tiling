#!/usr/bin/env python
"""Compile and run the exact Rust A0 polykite census.

Usage: venv/bin/python scripts/run_a0_fast.py [n_max] [dump_directory]
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "tools" / "a0_polykites.rs"
BINARY = ROOT / "target" / "a0_polykites"


def main() -> int:
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    dump_directory = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if len(sys.argv) > 3:
        raise SystemExit(__doc__)
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
    command = [str(BINARY), str(n_max)]
    if dump_directory is not None:
        command.append(str(dump_directory))
    return subprocess.run(command).returncode


if __name__ == "__main__":
    raise SystemExit(main())
