"""Entry program for the news-image-20261121 bounty.

The artwork ships inside the repository as ``entry.png`` next to this
file. The grader expects the finished picture at ``/output/entry.png``,
so this script simply copies the bundled image there, byte for byte.
No network, no randomness: every run produces the identical file.
"""

import shutil
from pathlib import Path


def find_source() -> Path:
    """Locate the bundled entry.png beside this script."""
    here = Path(__file__).resolve().parent
    candidate = here / "entry.png"
    if not candidate.is_file():
        raise FileNotFoundError(f"bundled image missing: {candidate}")
    return candidate


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_png(path: Path) -> None:
    """Refuse to ship anything that is not really a PNG file."""
    with path.open("rb") as handle:
        magic = handle.read(len(PNG_SIGNATURE))
    if magic != PNG_SIGNATURE:
        raise ValueError(f"{path} does not start with the PNG signature")


def main() -> None:
    source = find_source()
    check_png(source)
    destination = Path("/output/entry.png")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    print(f"wrote {destination} ({destination.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
