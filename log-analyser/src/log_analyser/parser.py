import re
from datetime import datetime

from log_analyser.models import LogEntry, LogParseError

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<level>[A-Z]+) "
    r"(?P<message>.+)$"
)


def parse_line(line: str) -> LogEntry:
    """Parse one log line into a LogEntry."""
    match = LOG_PATTERN.match(line.strip())
    if match is None:
        raise LogParseError("Log line doesn't match the expected format.")
    timestamp_text = match.group("timestamp")
    level = match.group("level")
    message = match.group("message")

    try:
        timestamp = datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise LogParseError("Log line conatins an invalid timestamp") from exc
    return LogEntry(timestamp=timestamp, level=level, message=message)
