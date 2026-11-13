import json
import sys
from pathlib import Path

import pytest
from log_analyser.cli import main


def test_cli_creates_json_summary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Check that the CLI creates a JSON summary."""
    input_file = tmp_path / "server.log"
    output_file = tmp_path / "summary.json"

    input_file.write_text(
        "2026-10-29 09:15:00 INFO Application started\n"
        "2026-10-29 09:16:00 ERROR Database failed\n"
        "INVALID LOG LINE\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys, "argv", ["log-analyser", str(input_file), "--output", str(output_file)]
    )

    main()

    assert output_file.exists()

    summary = json.loads(output_file.read_text(encoding="utf-8"))
    assert summary["counts_by_level"] == {"INFO": 1, "ERROR": 1}
    assert summary["bad_line_count"] == 1


def test_cli_missing_input_files_exit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Check that the CLI exit when the input file is missing."""

    missing_file = tmp_path / "missing.log"
    output_file = tmp_path / "summary.json"

    monkeypatch.setattr(
        sys, "argv", ["log-analyser", str(missing_file), "--output", str(output_file)]
    )
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
