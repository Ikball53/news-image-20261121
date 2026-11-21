#!/usr/bin/env python3
"""news-image-20261121 entry v5: emit the pre-built poster image.

Stdlib only. The grader sandbox has no Pillow/matplotlib/network, so this
script simply copies the bundled poster.png into the output directory.
"""

from pathlib import Path
import shutil
import sys


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "poster.png"
    if not source.is_file():
        print(f"poster.png not found next to main.py: {source}", file=sys.stderr)
        return 1
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "poster.png"
    shutil.copyfile(source, dest)
    size = dest.stat().st_size
    print(f"Wrote {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
