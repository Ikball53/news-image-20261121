# Poster courier for the 21 November 2026 news-image entry.
# Ships the bundled artwork byte-for-byte; nothing is rendered here.
# Deterministic by design: identical input bytes, identical output bytes.
from pathlib import Path
import os


def deliver() -> None:
    bundle_dir = Path(__file__).resolve().parent
    artwork = bundle_dir / "entry.png"
    payload = artwork.read_bytes()

    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / "entry.png"
    destination.write_bytes(payload)


if __name__ == "__main__":
    deliver()
