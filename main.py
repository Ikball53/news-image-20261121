"""Deliver the bundled poster image to the grader output location."""

import os
import shutil
import sys
from pathlib import Path


def resolve_destination() -> Path:
    override = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    base = Path(override) if override else Path("/output")
    return base / "entry.png"


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"missing bundled image: {source}", file=sys.stderr)
        return 1
    target = resolve_destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.resolve() != source.resolve():
        shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
