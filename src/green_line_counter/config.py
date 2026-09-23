"""Configuration constants for green line detection."""

from typing import Final

# --- Rendering ---
RENDER_ZOOM: Final[float] = 2.0
"""Scale factor for rendering PDF pages. 2.0 ≈ 144 DPI."""

# --- Column sampling (fractions of page width) ---
SAMPLE_COLUMNS_X: Final[tuple[float, ...]] = (0.15, 0.5, 0.85)
"""Relative X positions used to sample each row."""

MIN_GREEN_SAMPLES_PER_ROW: Final[int] = 2
"""How many sampled columns must be green for a row to count as green."""

# --- Color detection (RGB distance to reference green) ---
GREEN_REFERENCE_RGB: Final[tuple[int, int, int]] = (0, 180, 0)
GREEN_TOLERANCE: Final[int] = 80
"""Max Euclidean distance in RGB space to consider a pixel 'green'."""

# --- Line grouping ---
LINE_GAP_PX: Final[int] = 20
"""Vertical gap (in rendered pixels) that separates two distinct lines."""