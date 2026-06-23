"""Tests for 4-hour thesis rotation."""

from datetime import UTC, datetime
from pathlib import Path

from scripts.schedule_thesis import thesis_for_slot


def test_thesis_rotation_by_slot(tmp_path: Path) -> None:
    theses = [tmp_path / "thesis_a.yaml", tmp_path / "thesis_b.yaml", tmp_path / "thesis_c.yaml"]
    for p in theses:
        p.write_text("name: x\nvertical: v\nicp: {}\nproblem_hypothesis: p\n", encoding="utf-8")

    at_0 = datetime(2026, 6, 9, 1, 0, tzinfo=UTC)  # slot 0
    at_4 = datetime(2026, 6, 9, 5, 0, tzinfo=UTC)  # slot 1

    assert thesis_for_slot(theses=theses, at=at_0) == theses[0]
    assert thesis_for_slot(theses=theses, at=at_4) == theses[1]


def test_archive_digest_path() -> None:
    from signal_engine.digest import archive_digest_path

    at = datetime(2026, 6, 9, 12, 30, tzinfo=UTC)
    path = archive_digest_path("soc2_compliance", Path("/docs/digests"), at=at)
    assert path == Path("/docs/digests/soc2_compliance/2026-06-09-1200UTC.md")
