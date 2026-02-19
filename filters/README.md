# Pipeline Filters

Implementation of individual pipeline stages following the Pipes-and-Filters pattern.

## Structure

```
├── config.py            # Global config (GITHUB_TOKEN, MODEL_NAME, ARTIFACTS_DIR, star ranges)
├── logger.py            # Centralized logging factory
├── help_methods.py      # Shared utilities (tree builder, file collector, JSON parsing)
├── agent_filters/       # LLM-based filters (architecture detection, tactic selection, implementation)
├── dataset_filters/     # Dataset preparation and enrichment
├── github_filters/      # GitHub API search and clone
└── static_analysis/     # Radon-based maintainability metrics
```

## Configuration

Key settings in `config.py`:
- `MODEL_NAME` — LLM model for inference (default: `gemma3:latest`)
- `GITHUB_TOKEN` — GitHub API token for search
- `ARTIFACTS_DIR` — Output directory for analysis artifacts
- Star-count ranges for dataset segmentation
