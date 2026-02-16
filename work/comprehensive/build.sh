#!/bin/bash
# Build study guide PDF from Markdown sections using pandoc
# Requirements: pandoc, xelatex (via texlive), pandoc-citeproc

cd "$(dirname "$0")"

pandoc metadata.yaml \
  00_frontmatter.md \
  01_motivation.md \
  02_sa_foundations.md \
  03_quality_maintainability.md \
  04_architectural_tactics.md \
  05_architecture_erosion.md \
  06_assessment_methods.md \
  07_llm_refactoring.md \
  08_challenges.md \
  09_research_gaps.md \
  --pdf-engine=xelatex \
  --citeproc \
  --number-sections \
  -o study_guide.pdf

echo "Build complete: study_guide.pdf"
