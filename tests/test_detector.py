"""Unit tests for the detection logic."""

from __future__ import annotations

import numpy as np
import pytest

from green_line_counter.config import GREEN_REFERENCE_RGB, LINE_GAP_PX
from green_line_counter.detector import _count_lines_on_page, _green_mask


def _blank_page(height: int = 200, width: int = 200) -> np.ndarray:
    return np.full((height, width, 3), 255, dtype=np.int16)


def _paint_row(image: np.ndarray, y: int, colour: tuple[int, int, int]) -> None:
    image[y, :, :] = colour


def test_green_mask_matches_reference_colour() -> None:
    img = _blank_page()
    _paint_row(img, 50, GREEN_REFERENCE_RGB)
    mask = _green_mask(img)
    assert mask[50, :].all()
    assert not mask[0, :].any()


def test_no_green_lines_on_blank_page() -> None:
    img = _blank_page()
    assert _count_lines_on_page(img) == 0


def test_single_green_line() -> None:
    img = _blank_page()
    for y in range(60, 63):
        _paint_row(img, y, GREEN_REFERENCE_RGB)
    assert _count_lines_on_page(img) == 1


def test_two_separated_green_lines() -> None:
    img = _blank_page()
    _paint_row(img, 40, GREEN_REFERENCE_RGB)
    _paint_row(img, 40 + LINE_GAP_PX + 10, GREEN_REFERENCE_RGB)
    assert _count_lines_on_page(img) == 2


def test_two_close_lines_counted_as_one() -> None:
    img = _blank_page()
    _paint_row(img, 40, GREEN_REFERENCE_RGB)
    _paint_row(img, 45, GREEN_REFERENCE_RGB)
    assert _count_lines_on_page(img) == 1


@pytest.mark.parametrize("colour", [(255, 0, 0), (0, 0, 255), (128, 128, 128)])
def test_non_green_colours_are_ignored(colour: tuple[int, int, int]) -> None:
    img = _blank_page()
    _paint_row(img, 50, colour)
    assert _count_lines_on_page(img) == 0