from pathlib import Path

import pytest
from log_analyser.analyser import analyse_file
from log_analyser.models import LogFileError


def test_count_log_levels(tmp_path: Path) -> None:
    """Check that log levels are counted correctly."""

    log_file = tmp_path / "server.log"
    log_file.write_text(
        "2026-10-29 09:15:00 INFO Application started\n"
        "2026-10-29 09:16:00 ERROR Database failed\n"
        "2026-10-29 09:17:00 WARNING High memory usage\n"
        "2026-10-29 09:18:00 INFO Request completed\n",
        encoding="utf-8",
    )

    result = analyse_file(log_file)

    assert result["counts_by_level"] == {"INFO": 2, "ERROR": 1, "WARNING": 1}


def test_top_errors(tmp_path: Path) -> None:
    """Check that repeated error messages are counted."""
    log_file = tmp_path / "server.log"
    log_file.write_text(
        "2026-10-29 09:15:00 ERROR Database connection failed\n"
        "2026-10-29 09:16:00 ERROR Database connection failed\n"
        "2026-10-29 09:17:00 ERROR Server unavailable\n",
        encoding="utf-8",
    )

    result = analyse_file(log_file)

    assert result["top_errors"] == [
        {"message": "Database connection failed", "count": 2},
        {"message": "Server unavailable", "count": 1},
    ]


def test_time_range(tmp_path: Path) -> None:
    """Check that earliest and latest timestamps are identified."""
    log_file = tmp_path / "server.log"
    log_file.write_text(
        "2026-10-29 09:15:00 INFO First event\n"
        "2026-10-29 09:20:00 INFO Last event\n"
        "2026-10-29 09:17:00 WARNING Middle event\n",
        encoding="utf-8",
    )

    result = analyse_file(log_file)

    assert result["time_range"] == {"start": "2026-10-29T09:15:00", "end": "2026-10-29T09:20:00"}


def test_malformed_lines_are_recorded(tmp_path: Path) -> None:
    """Check that malformed lines are counted and reported."""
    log_file = tmp_path / "server.log"
    log_file.write_text(
        "2026-10-29 09:15:00 INFO Application started\n"
        "THIS IS A BAD LOG LINE\n"
        "2026-10-29 09:17:00 ERROR Database failed\n",
        encoding="utf-8",
    )

    result = analyse_file(log_file)

    assert result["bad_line_count"] == 1
    assert result["bad_lines"] == [{"line_number": 2, "content": "THIS IS A BAD LOG LINE"}]
    assert result["counts_by_level"]["ERROR"] == 1


def test_empty_file(tmp_path: Path) -> None:
    """Check that an empty file produces an empty summary."""
    log_file = tmp_path / "server.log"
    log_file.write_text("", encoding="utf-8")

    result = analyse_file(log_file)

    assert result["counts_by_level"] == {}
    assert result["top_errors"] == []
    assert result["time_range"] == {"start": None, "end": None}
    assert result["bad_line_count"] == 0
    assert result["bad_lines"] == []


def test_missing_file() -> None:
    """Check that a missing file raises LogFileError."""
    missing_file = Path("missing_server.log")

    with pytest.raises(LogFileError):
        analyse_file(missing_file)
