#!/usr/bin/env python3
"""Deliver the finished news poster to the grader's output slot.

The poster artwork ships beside this script as entry.png. This runner
moves a byte-for-byte copy into the destination folder so the sealed
scorer can pick it up under the required name.
"""

import os
import sys
from pathlib import Path


def resolve_destination() -> Path:
    """Pick the output folder, honouring the harness override if present."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if override:
        return Path(override)
    return Path("/output")


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"missing shipped poster: {source}", file=sys.stderr)
        return 1

    target_dir = resolve_destination()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"

    payload = source.read_bytes()
    # The bounty caps the poster at 1 MiB; fail loudly rather than
    # handing the scorer an oversized file it would mark invalid.
    if len(payload) > 1048576:
        print(f"poster too large: {len(payload)} bytes", file=sys.stderr)
        return 1
    target.write_bytes(payload)
    print(f"wrote {target} ({len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
