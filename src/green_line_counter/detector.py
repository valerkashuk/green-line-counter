"""Core logic for detecting and counting green lines in PDF pages."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import fitz  # PyMuPDF
import numpy as np
from PIL import Image

from .config import (
    GREEN_REFERENCE_RGB,
    GREEN_TOLERANCE,
    LINE_GAP_PX,
    MIN_GREEN_SAMPLES_PER_ROW,
    RENDER_ZOOM,
    SAMPLE_COLUMNS_X,
)


class PDFProcessingError(Exception):
    """Raised when a PDF cannot be opened or rendered."""


@dataclass
class PageResult:
    """Detection result for a single PDF page."""

    page_number: int
    green_lines: int
    height_px: int
    width_px: int


@dataclass
class DocumentResult:
    """Detection result for a whole PDF document."""

    source: Path
    pages: list[PageResult] = field(default_factory=list)

    @property
    def total_green_lines(self) -> int:
        return sum(p.green_lines for p in self.pages)


def _render_page_to_array(page: fitz.Page) -> np.ndarray:
    """Render a PDF page into an RGB numpy array (H, W, 3)."""
    matrix = fitz.Matrix(RENDER_ZOOM, RENDER_ZOOM)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return np.asarray(img, dtype=np.int16)


def _green_mask(image: np.ndarray) -> np.ndarray:
    """Return a 2D boolean mask of pixels close to the reference green."""
    ref = np.array(GREEN_REFERENCE_RGB, dtype=np.int16)
    diff = image - ref
    distance_sq = np.sum(diff * diff, axis=2)
    return distance_sq <= GREEN_TOLERANCE ** 2


def _count_lines_on_page(image: np.ndarray) -> int:
    """Count distinct horizontal green lines on a rendered page."""
    height, width = image.shape[:2]
    mask = _green_mask(image)

    sample_cols = [int(width * frac) for frac in SAMPLE_COLUMNS_X]
    hits_per_row = mask[:, sample_cols].sum(axis=1)
    green_rows = np.where(hits_per_row >= MIN_GREEN_SAMPLES_PER_ROW)[0]

    if green_rows.size == 0:
        return 0

    lines = 1
    prev = green_rows[0]
    for y in green_rows[1:]:
        if y - prev > LINE_GAP_PX:
            lines += 1
        prev = y
    return lines


def analyse_pdf(pdf_path: Path) -> DocumentResult:
    """Run green-line detection on a single PDF file."""
    result = DocumentResult(source=pdf_path)

    try:
        document = fitz.open(pdf_path)
    except (fitz.FileDataError, RuntimeError) as exc:
        raise PDFProcessingError(f"Cannot open {pdf_path}: {exc}") from exc

    try:
        for page_index in range(len(document)):
            page = document.load_page(page_index)
            image = _render_page_to_array(page)
            result.pages.append(
                PageResult(
                    page_number=page_index + 1,
                    green_lines=_count_lines_on_page(image),
                    height_px=image.shape[0],
                    width_px=image.shape[1],
                )
            )
    finally:
        document.close()

    return result