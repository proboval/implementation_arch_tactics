# Pipeline Execution Logs

Detailed logs from each pipeline stage.

## Log Files

| File | Pipeline Stage |
|------|---------------|
| `searchRepositories.log` | GitHub search and repository discovery |
| `backend_dataset_preparation.log` | Dataset preparation from cloned repos |
| `StaticAnalysis.log` | Radon-based maintainability assessment |
| `architectureDefinition.log` | LLM architecture type detection |
| `architecture_tactic_selection.log` | Tactic selection process |
| `tacticImplementation.log` | Code generation and implementation |
| `dataset_maintainability_enricher.log` | Metric enrichment stages |
| `dataset_merge_and_enrich.log` | CSV merging and final enrichment |
| `DatasetLLMImprovementRunner.log` | LLM improvement execution |
