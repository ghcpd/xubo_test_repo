
"""CLI entry point for processing sales data."""

from __future__ import annotations

import argparse
from pathlib import Path

from sales_processor.processor import process_sales_data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Process raw sales data JSON and export aggregated artefacts.",
    )
    parser.add_argument("input", type=Path, help="Path to the input sales JSON file")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Directory where the output JSON files will be written (default: current directory)",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    process_sales_data(args.input, args.output)


if __name__ == "__main__":
    main()
