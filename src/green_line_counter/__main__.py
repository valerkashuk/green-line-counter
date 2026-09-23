"""Entry point for `python -m green_line_counter`."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())