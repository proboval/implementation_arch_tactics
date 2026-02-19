# Agent Filters (LLM-Based)

LLM-powered pipeline stages for architecture detection, tactic selection, and code transformation.

## Files

| File | Purpose |
|------|---------|
| `architecture_definition.py` | Detects architecture type from code metrics (layered, hexagonal, MVC, etc.) |
| `tactic_definition.py` | Selects applicable architectural tactics from catalog |
| `tactic_implementation.py` | Generates and applies code changes (max 100 iterations) |
| `maintainability_improvement_filter.py` | Orchestrates before/after maintainability comparison |
| `call_llm.py` | LLM inference wrapper (Ollama API) |
| `architectural_tactics_complete_catalog.csv` | Master catalog of architectural tactic definitions |

## Pipeline Flow

```
Code → architecture_definition → tactic_definition → tactic_implementation → metrics
```

Each stage calls the LLM via `call_llm.py` and stores results as JSON artifacts.
