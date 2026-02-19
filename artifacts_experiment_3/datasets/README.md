# Versioned Datasets

CSV datasets segmented by GitHub repository star-count ranges.

## Files

- `dataset_1_20.csv` — Repos with 1-20 stars
- `dataset_1_120.csv` — Repos with 1-120 stars
- `dataset_100_1200.csv` — Repos with 100-1200 stars
- `stars_dataset.csv` — Base dataset with GitHub metadata

## Schema

| Column | Description |
|--------|-------------|
| `full_name` | GitHub owner/repo |
| `clone_url` | Git clone URL |
| `stars` | Star count |
| `mi_avg` | Average Maintainability Index |
| `files_analyzed` | Number of Python files |
| `packages` | Number of packages |
| `avg_fan_out` | Average fan-out (coupling) |
| `docstring_coverage` | Documentation coverage ratio |
| `has_readme` | Boolean |
