# Pipes and Filters Framework

Core pipeline framework implementing the Pipes-and-Filters architectural pattern.

## Files

- `pipes_and_filters.py` — Framework classes

## Classes

| Class | Purpose |
|-------|---------|
| `Repository` | Dataclass holding repo metadata, metrics, and analysis results |
| `Filter` | Abstract base class with `process()` method, logging, and timing |
| `Pipeline` | Chains filters sequentially, passing `Repository` through each stage |

## Usage

```python
from pipes_and_filters import Pipeline, Repository

pipeline = Pipeline([
    GitHubSearchFilter(),
    StaticAnalysisFilter(),
    ArchitectureDefinitionFilter(),
    TacticImplementationFilter(),
])
pipeline.run(Repository(...))
```
