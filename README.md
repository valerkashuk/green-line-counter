# Green Line Counter

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python CLI tool that counts the number of **horizontal green lines** on each page of a PDF document.

It renders pages with PyMuPDF, analyzes pixels with NumPy, and groups vertically close green rows into distinct lines.

## Features

- 🔍 Processes all PDF files in a given folder
- 🎨 Robust detection of "green" via RGB distance to a reference colour
- ⚡ Fast NumPy-based analysis
- 🧪 Covered by unit tests (pytest)
- 🖥️ Friendly CLI built on `argparse` with logging
- 📦 Installs as a package, includes `__main__` and a console entry point

## Installation

```bash
git clone https://github.com/valerkashuk/green-line-counter.git
cd green-line-counter
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# PDFs in the current folder
green-line-counter

# PDFs in a specific folder
green-line-counter ./samples

# Verbose logging
green-line-counter ./samples --verbose



Пример вывода:

```
📄 File: drawing.pdf
------------------------------------------------------------
  Page   1  |  1190×1684 px  |  green lines: 3
  Page   2  |  1190×1684 px  |  green lines: 5
------------------------------------------------------------
  TOTAL green lines: 8
```

## Как это работает

##How it works
Each page is rendered into an RGB array with the RENDER_ZOOM scale factor.

A mask of "green" pixels is built using Euclidean distance to the reference colour.

Several columns are sampled for every row.

A row counts as green if enough sampled points are green.

Consecutive green rows separated by ≤ LINE_GAP_PX are merged into a single line.

All parameters are stored in src/green_line_counter/config.py.

All param. are in `src/green_line_counter/config.py`.



`Python 3.10+`, `PyMuPDF`, `Pillow`, `NumPy`, `pytest`.


MIT