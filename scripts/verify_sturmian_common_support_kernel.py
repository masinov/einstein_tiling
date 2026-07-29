#!/usr/bin/env python3
"""Cold-verify the exact AHI common-support kernel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.sturmian import verify_common_support_kernel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("kernel", type=Path)
    args = parser.parse_args()
    verify_common_support_kernel(
        json.loads(args.kernel.read_text()),
        json.loads(args.atlas.read_text()),
    )
    print("common-support kernel: VERIFIED")


if __name__ == "__main__":
    main()
