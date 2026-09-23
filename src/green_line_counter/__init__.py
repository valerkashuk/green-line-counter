"""green-line-counter: count horizontal green lines in PDF documents."""

from .detector import (
    DocumentResult,
    PageResult,
    PDFProcessingError,
    analyse_pdf,
)

__version__ = "0.1.0"
__all__ = [
    "DocumentResult",
    "PageResult",
    "PDFProcessingError",
    "analyse_pdf",
]