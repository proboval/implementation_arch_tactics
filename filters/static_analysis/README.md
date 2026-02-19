# Static Analysis Filter

Radon-based maintainability assessment for Python repositories.

## Files

| File | Purpose |
|------|---------|
| `before.py` | Runs static analysis on pre-transformation code |

## Metrics Computed

- **Maintainability Index (MI)** — `radon mi` per file, averaged
- **Architecture maintainability** — Module-level coupling (fan-out), package structure
- **Code maintainability** — Cyclomatic Complexity, Halstead metrics
- **Documentation maintainability** — Docstring coverage and quality

## Output

JSON files per repo stored in `artifacts_create_dataset/artifacts/static_analysis/BEFORE/<repo>/`.
