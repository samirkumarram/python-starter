import logging
from collections import Counter
from datetime import datetime
from pathlib import Path

from log_analyser.models import BadLine, LogFileError, LogParseError
from log_analyser.parser import parse_line

logger = logging.getLogger(__name__)


def analyse_file(file_path: Path) -> dict[str, object]:
    """Analyse a log file and return a summery."""
    level_counts: Counter[str] = Counter()
    error_counts: Counter[str] = Counter()
    bad_lines: list[BadLine] = []
    timestamps: list[datetime] = []

    try:
        with file_path.open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    entry = parse_line(line)
                except LogParseError:
                    bad_lines.append(BadLine(line_number=line_number, content=line.strip()))
                    logger.warning("Invalid log entry at line %d", line_number)
                    continue
                level_counts[entry.level] += 1
                timestamps.append(entry.timestamp)

                if entry.level == "ERROR":
                    error_counts[entry.message] += 1
    except OSError as exc:
        raise LogFileError(f"Unable to read log file: {file_path}") from exc

    top_errors = [
        {"message": message, "count": count} for message, count in error_counts.most_common(5)
    ]

    time_range = {
        "start": min(timestamps).isoformat() if timestamps else None,
        "end": max(timestamps).isoformat() if timestamps else None,
    }
    return {
        "counts_by_level": dict(level_counts),
        "top_errors": top_errors,
        "time_range": time_range,
        "bad_line_count": len(bad_lines),
        "bad_lines": [
            {"line_number": bad.line_number, "content": bad.content} for bad in bad_lines
        ],
    }
