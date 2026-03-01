#!/usr/bin/env bash
# Generate PDF from main.tex (run from paper/v1/)
# Usage: bash paper/v1/scripts/gen_pdf.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PAPER_DIR"

echo "=== Pass 1: pdflatex ==="
pdflatex -interaction=nonstopmode main.tex

echo "=== bibtex ==="
bibtex main

echo "=== Pass 2: pdflatex ==="
pdflatex -interaction=nonstopmode main.tex

echo "=== Pass 3: pdflatex ==="
pdflatex -interaction=nonstopmode main.tex

echo "=== Done: main.pdf ==="
ls -lh main.pdf
