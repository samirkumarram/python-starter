from datetime import datetime

import pytest
from log_analyser.models import LogEntry, LogParseError
from log_analyser.parser import parse_line


def test_parse_valid_log_line() -> None:
    """Check that a valid log line is parsed correctly."""
    line = "2026-10-29 09:15:00 INFO Application started"

    result = parse_line(line)

    assert isinstance(result, LogEntry)
    assert result.timestamp == datetime(2026, 10, 29, 9, 15, 0)
    assert result.level == "INFO"
    assert result.message == "Application started"


def test_parse_error_log_line() -> None:
    """Check that an ERROR log line is parsed correctly."""
    line = "2026-10-29 09:16:00 ERROR Database connection failed"

    result = parse_line(line)

    assert result.level == "ERROR"
    assert result.message == "Database connection failed"


def test_parse_invalid_log_line() -> None:
    """Check that an incorrectly formated line raises an exception."""
    line = "THIS IS A BAD LOG LINE"

    with pytest.raises(LogParseError):
        parse_line(line)


def test_parse_invalid_timestamp() -> None:
    """Check that an impossible timestamp is rejected."""
    line = "2026-15-40 09:15:00 INFO Application started"
    with pytest.raises(LogParseError):
        parse_line(line)
