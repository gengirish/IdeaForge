"""Pick thesis YAML for the current 4-hour UTC slot (round-robin)."""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"
SLOT_HOURS = 4


def thesis_for_slot(
    *,
    theses: list[Path] | None = None,
    at: datetime | None = None,
) -> Path:
    paths = theses or sorted(CONFIG_DIR.glob("thesis_*.yaml"))
    if not paths:
        raise FileNotFoundError(f"No thesis_*.yaml configs in {CONFIG_DIR}")
    now = at or datetime.now(UTC)
    slot = now.hour // SLOT_HOURS
    return paths[slot % len(paths)]


def main() -> None:
    print(thesis_for_slot())


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
