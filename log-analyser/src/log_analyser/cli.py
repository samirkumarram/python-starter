import argparse
import json
import logging
from pathlib import Path

from log_analyser.analyser import analyse_file
from log_analyser.models import LogAnalyserError

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the log analyser command-line application."""

    parser = argparse.ArgumentParser(description="Analyse a log file and generate a JSON summary.")

    parser.add_argument("input_file", type=Path, help="Path to the input log file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("summary.json"),
        help="Path for the output JSON file",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        summary = analyse_file(args.input_file)
        with args.output.open("w", encoding="utf-8") as output_file:
            json.dump(summary, output_file, indent=2)
        logger.info("Analysis completed successfully.")
        logger.info("Summary saved to %s", args.output)
    except (LogAnalyserError, OSError) as exc:
        logger.error("%s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
