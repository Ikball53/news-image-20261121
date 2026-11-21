# Front-page entry for Saturday 21 November 2026 (news-image-20261121).
# The finished picture ships beside this script as entry.png; running the
# script places a byte-identical copy where the grader looks for it.
# Deterministic by construction: no clocks, no randomness, no network.

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLED_PICTURE = HERE / "entry.png"
PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
SIZE_CAP = 1048576


def load_picture() -> bytes:
    """Read the bundled picture and sanity-check its header."""
    payload = BUNDLED_PICTURE.read_bytes()
    if payload[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise SystemExit("bundled entry.png is not a PNG file")
    if len(payload) > SIZE_CAP:
        raise SystemExit("bundled entry.png exceeds the 1 MiB gate")
    # IHDR width/height sit at bytes 16..24; the gate caps both at 1024.
    width = int.from_bytes(payload[16:20], "big")
    height = int.from_bytes(payload[20:24], "big")
    if width > 1024 or height > 1024:
        raise SystemExit(f"bundled entry.png is {width}x{height}, over the 1024 cap")
    return payload


def output_path() -> Path:
    """Grader writes to /output; local runs may redirect the folder."""
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def main() -> None:
    picture = load_picture()
    target = output_path()
    target.write_bytes(picture)
    print(f"entry.png -> {target} ({len(picture)} bytes)")


if __name__ == "__main__":
    main()
