# Analysis Artifacts

Per-repository analysis outputs from the pipeline.

## Structure

```
├── ai_analysis_qwen3-coder/
│   ├── architecture/            # LLM-detected architecture type (JSON per repo)
│   └── architecture_tactics/    # Selected and implemented tactics (JSON per repo)
└── static_analysis/
    └── BEFORE/                  # Radon maintainability metrics pre-transformation
```

## AI Analysis Format

Each repo produces JSON files with detected architecture type (layered, hexagonal, modular_monolith, MVC, microservices_like, etc.) and recommended tactics.

## Static Analysis Metrics

Each repo under `BEFORE/` contains:
- `radon_mi.json` — Maintainability Index per file
- `architecture_maintainability.json` — Module-level architecture metrics
- `code_maintainability.json` — Code-level metrics (CC, Halstead)
- `documentation_maintainability.json` — Docstring coverage and documentation quality
