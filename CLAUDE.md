# implementation_arch_tactics

Thesis project: **Automated Implementation of Architectural Tactics for Software Quality Improvement** (Innopolis University, 2026).

## Project Structure

```
├── diploma/latex_diploma/  # Thesis document (LaTeX, biber)
│   ├── thesis.tex          # Main document
│   ├── ref.bib             # Bibliography (biber)
│   └── chapters/           # Chapter files (chapter1-6, abstract, appex)
├── lit/                    # Literature review workspace
│   ├── CLAUDE.md           # ← Lit review workflow instructions
│   ├── status.md           # Paper inventory & progress tracker
│   ├── readings.md         # Prioritized reading list (Tier 1/2/3)
│   ├── references.bib      # Verified BibTeX entries (MCP-checked)
│   ├── pdfs/               # 22+ downloaded research papers
│   ├── converted/          # PDF→Markdown conversions
│   ├── summaries/          # Per-paper summaries
│   └── insights/           # Cross-paper topic synthesis
├── paper/sections/         # Paper section drafts
├── filters/                # Pipeline filter implementations
│   ├── agent_filters/      # LLM-based (architecture detection, tactic selection, implementation)
│   ├── github_filters/     # GitHub search and clone
│   ├── dataset_filters/    # Dataset preparation and enrichment
│   ├── static_analysis/    # Radon-based maintainability metrics
│   ├── help_methods.py     # Shared utilities (tree, file collection, JSON parsing)
│   ├── logger.py           # Centralized logging
│   └── config.py           # Global config (GITHUB_TOKEN, MODEL_NAME, etc.)
├── pipes_and_filters/      # Pipeline framework (Filter, Pipeline, Repository)
├── experiments/            # Experiment prompts and notes
├── work/                   # Working notes
├── main.py                 # Pipeline entry point
├── docker-compose.yml      # Ollama service (LLM inference)
└── .claude/                # Claude Code agent definitions and skill plugins
```

## Taskflow Routing

| Task | Working Dir | Load |
|------|-------------|------|
| Literature review | `lit/` | `lit/CLAUDE.md` |
| Paper search & download | `lit/` | `lit/CLAUDE.md` Phase 2-3 |
| Summarize papers | `lit/` | `lit/CLAUDE.md` Phase 3 |
| Synthesize insights | `lit/` | `lit/CLAUDE.md` Phase 4 |
| Write thesis sections | `paper/` | `lit/CLAUDE.md` Phase 5 |
| Web scraping | anywhere | Web scraper skill |

## Research Objectives

1. Identify architectural tactics that directly influence maintainability (ISO/IEC 25010)
2. Implement selected tactics in open-source backend projects using LLM
3. Evaluate impact of LLM-generated changes on maintainability using static analysis + architecture metrics
4. Compare maintainability before/after LLM-driven transformations
5. Evaluate advantages and limitations of LLM for architecture-level modifications
6. Formulate recommendations for applying architectural tactics using LLM

## Tools Available

| Tool | Trigger |
|------|---------|
| Paper Search MCP | `search_semantic`, `search_arxiv`, `search_crossref`, `search_google_scholar` |
| NotebookLM | `/notebooklm` — query notebooks, deep research |
| PDF skill | `/pdf` — extract text/tables, create/merge PDFs |
| Web Scraper | `/web-scraper` — scrape pages, crawl sites, extract tables |

## Critical Rules

### DO NOT READ PDFs DIRECTLY

**NEVER use the Read tool on `.pdf` files.** Always convert to Markdown first, then analyse the converted version:

```bash
# Convert PDF to Markdown
python -m markitdown lit/pdfs/paper.pdf > lit/converted/paper.md

# Then read and analyse the .md file
```

Alternative: use MCP `read_*_paper` tools (e.g., `read_arxiv_paper`, `read_semantic_paper`) which extract text automatically.

## Conventions

- **BibTeX keys:** `[author][year][keyword]` lowercase (e.g., `kim2009qualitydriven`)
- **PDF naming:** `[topic]_[##]_[author][year]_[description].pdf`
- **Topics:** `at`, `sa`, `maint`, `llm`, `refac`, `static`, `pipe`
- **Always check existing papers** before searching (read `lit/status.md` first)
