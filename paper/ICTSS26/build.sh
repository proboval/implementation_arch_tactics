#!/usr/bin/env bash
# Build the ICTSS 2026 paper PDF with TinyTeX (no sudo required).
# Usage: ./build.sh [basename]   (default basename: main)
set -uo pipefail

# TinyTeX lives in the user's home dir; add it to PATH for this run.
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
cd "$(dirname "$0")"
DOC="${1:-main}"

if ! command -v pdflatex >/dev/null 2>&1; then
  echo "ERROR: pdflatex not found. Install TinyTeX:" >&2
  echo "  curl -sL https://yihui.org/tinytex/install-bin-unix.sh | sh" >&2
  exit 1
fi

# Ensure required LaTeX packages are present (idempotent; needs network the first time).
tlmgr install \
  pgf pgfplots algorithms algorithmicx float placeins underscore \
  booktabs enumitem xcolor hyperref infwarerr kvoptions etoolbox \
  babel-english aliascnt >/dev/null 2>&1 || true

# llncs.cls and splncs04.bst are bundled in this directory, so they are found automatically.
set -e
pdflatex -interaction=nonstopmode "$DOC".tex
bibtex   "$DOC" || true          # bibtex returns non-zero on warnings
pdflatex -interaction=nonstopmode "$DOC".tex
pdflatex -interaction=nonstopmode "$DOC".tex

echo "=== Built $DOC.pdf ==="
if command -v mdls >/dev/null 2>&1; then
  echo "Pages: $(mdls -name kMDItemNumberOfPages -raw "$DOC".pdf 2>/dev/null)"
fi
