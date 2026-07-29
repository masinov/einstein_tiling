"""Location-independent discovery of the Einstein repository root."""

from __future__ import annotations

from pathlib import Path


def repository_root(start: str | Path) -> Path:
    """Return the nearest ancestor containing this repository's source tree.

    Commands may move between responsibility-oriented subdirectories without
    changing their path arithmetic.  A missing root fails explicitly instead
    of silently selecting the wrong parent depth.
    """

    path = Path(start).resolve()
    if path.is_file():
        path = path.parent
    for candidate in (path, *path.parents):
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "src/einstein"
        ).is_dir():
            return candidate
    raise FileNotFoundError(f"no Einstein repository root above {start}")
