#!/usr/bin/env python3
"""Deliver the finished poster for the 21 November 2026 news-image bounty.

The artwork ships beside this file as entry.png. At grading time the
repository sits on a read-only mount and only the output folder is
writable, so this program simply carries the shipped bytes across to
the output folder. Standard library only, no network, deterministic:
every run writes exactly the same file.
"""

import os
import sys
from pathlib import Path

PNG_MAGIC = bytes((137, 80, 78, 71, 13, 10, 26, 10))
ARTWORK_NAME = "entry.png"


def pick_destination():
    """Return the folder the grader expects the picture in."""
    env_value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if env_value:
        return Path(env_value)
    grader_folder = Path("/output")
    if grader_folder.is_dir():
        return grader_folder
    return Path.cwd()


def load_artwork():
    """Read the shipped picture from next to this script."""
    here = Path(__file__).resolve().parent
    payload = (here / ARTWORK_NAME).read_bytes()
    if not payload.startswith(PNG_MAGIC):
        raise ValueError("shipped artwork is not a PNG file")
    return payload


def main():
    picture_bytes = load_artwork()
    target_folder = pick_destination()
    try:
        target_folder.mkdir(parents=True, exist_ok=True)
        (target_folder / ARTWORK_NAME).write_bytes(picture_bytes)
    except OSError:
        # Last resort: the working directory itself.
        target_folder = Path.cwd()
        (target_folder / ARTWORK_NAME).write_bytes(picture_bytes)
    print(f"delivered {ARTWORK_NAME} ({len(picture_bytes)} bytes) to {target_folder}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
