from dataclasses import dataclass
from datetime import datetime


class LogAnalyserError(Exception):
    """Base exception for log analyser errors."""


class LogParseError(LogAnalyserError):
    """Raised when a log line cannot be parsed."""


class LogFileError(LogAnalyserError):
    """Raised when a log file cannot be read."""


@dataclass
class LogEntry:
    """Represent one valid log entry."""

    timestamp: datetime
    level: str
    message: str


@dataclass
class BadLine:
    """Represent a malformed log line"""

    line_number: int
    content: str
