"""Command-line interface for green-line-counter."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .detector import DocumentResult, PDFProcessingError, analyse_pdf

logger = logging.getLogger(__name__)


def _find_pdfs(folder: Path) -> list[Path]:
    """Return a sorted list of PDF files in *folder*."""
    return sorted(folder.glob("*.pdf"))


def _print_report(result: DocumentResult) -> None:
    print(f"\n📄 File: {result.source.name}")
    print("-" * 60)
    for page in result.pages:
        print(
            f"  Page {page.page_number:>3}  |  "
            f"{page.width_px}×{page.height_px} px  |  "
            f"green lines: {page.green_lines}"
        )
    print("-" * 60)
    print(f"  TOTAL green lines: {result.total_green_lines}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="green-line-counter",
        description="Count horizontal green lines on each page of PDF files.",
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        type=Path,
        help="Folder containing PDF files (default: current directory).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s  %(levelname)-7s  %(message)s",
    )

    folder: Path = args.folder.resolve()
    if not folder.is_dir():
        logger.error("Not a directory: %s", folder)
        return 2

    pdfs = _find_pdfs(folder)
    if not pdfs:
        logger.error("No PDF files found in %s", folder)
        return 1

    logger.info("Found %d PDF file(s) in %s", len(pdfs), folder)

    exit_code = 0
    for pdf in pdfs:
        logger.info("Processing %s", pdf.name)
        try:
            result = analyse_pdf(pdf)
        except PDFProcessingError as exc:
            logger.error("Skipping %s: %s", pdf.name, exc)
            exit_code = 1
            continue
        _print_report(result)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())