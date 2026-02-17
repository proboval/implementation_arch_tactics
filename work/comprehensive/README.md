# Comprehensive Study Guide

"Automated Implementation of Architectural Tactics for Software Quality Improvement" — a study guide for MS students at Innopolis University.

## Outputs

- `study_guide.pdf` — Compiled PDF (~150 pages, with TOC, citations, mermaid diagrams)
- `study_guide.pptx` — PowerPoint presentation (33 slides)

## Chapters

| File | Chapter | Topic |
|------|---------|-------|
| `00_frontmatter.md` | — | Title page, abstract, how to use |
| `01_motivation.md` | 1 | Motivation & Context |
| `02_sa_foundations.md` | 2 | Software Architecture Foundations |
| `03_quality_maintainability.md` | 3 | Quality & Maintainability |
| `04_architectural_tactics.md` | 4 | Architectural Tactics |
| `05_architecture_erosion.md` | 5 | Architecture Erosion & Drift |
| `06_assessment_methods.md` | 6 | Maintainability Assessment Methods |
| `07_llm_refactoring.md` | 7 | LLMs for Code Refactoring |
| `08_challenges.md` | 8 | Challenges & Limitations |
| `09_research_gaps.md` | 9 | Research Gaps & Future Directions |

## Building the PDF

```bash
bash build.sh
```

Requires: `pandoc`, `xelatex` (texlive), `pandoc-citeproc`, `mermaid-filter` (npm).

## Configuration

- `metadata.yaml` — Pandoc metadata (title, fonts, TOC, citation config)
- `references.bib` — Bibliography (40 entries)
- `ieee.csl` — IEEE citation style
- `build.sh` — Build script (handles Windows mermaid-filter .cmd wrapper)
