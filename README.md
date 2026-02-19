# Automated Implementation of Architectural Tactics for Software Quality Improvement

Thesis project at Innopolis University (MS, 2026).

## Research Objectives

1. Identify architectural tactics that directly influence maintainability (ISO/IEC 25010)
2. Implement selected tactics in open-source backend projects using LLMs
3. Evaluate impact of LLM-generated changes on maintainability via static analysis + architecture metrics
4. Compare maintainability before/after LLM-driven transformations
5. Formulate recommendations for applying architectural tactics using LLMs

## Project Structure

```
├── diploma/latex_diploma/     # Thesis document (LaTeX, biber)
├── lit/                       # Literature review (37 papers, 12 synthesis docs)
├── paper/sections/            # Paper section drafts
├── filters/                   # Pipeline filter implementations
│   ├── agent_filters/         #   LLM-based (architecture detection, tactic selection, implementation)
│   ├── github_filters/        #   GitHub search and clone
│   ├── dataset_filters/       #   Dataset preparation and enrichment
│   └── static_analysis/       #   Radon-based maintainability metrics
├── pipes_and_filters/         # Pipeline framework (Filter, Pipeline, Repository)
├── artifacts_create_dataset/  # Experiment data, artifacts, logs
├── experiments/               # Experiment prompts and notes
├── work/comprehensive/        # Study guide (Markdown → PDF/PPTX)
├── main.py                    # Pipeline entry point
└── docker-compose.yml         # Ollama service (LLM inference)
```

## Pipeline

The pipeline follows a Pipes-and-Filters architecture:

1. **GitHub Search** — Find backend Python repos matching star-count criteria
2. **Clone** — Clone selected repositories
3. **Static Analysis (BEFORE)** — Radon-based maintainability metrics
4. **Architecture Detection** — LLM identifies architecture type (layered, MVC, hexagonal, etc.)
5. **Tactic Selection** — LLM selects applicable maintainability tactics from catalog
6. **Tactic Implementation** — LLM generates and applies code changes
7. **Static Analysis (AFTER)** — Re-measure and compare

## Quick Start

```bash
# Start Ollama LLM service
docker-compose up -d

# Run the full pipeline
python main.py
```

## Tools

| Tool | Purpose |
|------|---------|
| Radon | Maintainability Index, Cyclomatic Complexity |
| Ollama (gemma3) | LLM inference for architecture detection and code transformation |
| Pandoc + XeLaTeX | Study guide PDF compilation |
| PptxGenJS | Presentation generation |
