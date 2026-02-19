# Dataset Creation & Experiment Artifacts

Stores all experimental data produced by the pipeline: datasets, analysis artifacts, and execution logs.

## Structure

```
├── maintainability_dataset.csv            # Main enriched dataset (repos + metrics)
├── improvement_maintainability_dataset.csv # Before/after LLM improvement results
├── artifacts/                             # Per-repo analysis outputs
│   ├── ai_analysis_qwen3-coder/           #   LLM-generated architecture & tactic JSON
│   └── static_analysis/BEFORE/            #   Radon metrics per repo (pre-transformation)
├── datasets/                              # Versioned CSV datasets by star-count range
└── logs/                                  # Pipeline execution logs
```

## Key Datasets

- `maintainability_dataset.csv` — Columns: `full_name`, `clone_url`, `stars`, `mi_avg`, `files_analyzed`, `packages`, `avg_fan_out`, `docstring_coverage`, `has_readme`
- `improvement_maintainability_dataset.csv` — Before/after maintainability comparison
