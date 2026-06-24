# OSF project metadata — ICTSS 2026 replication package

> For **double-blind review**: create the project, upload `replication.zip`, leave
> contributors off the public view, and share a **view-only link with
> "Anonymize" checked** (Settings → View-only Links). De-anonymize + add a DOI at
> camera-ready.

**Title**
Replication Package — "Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation"

**Description**
Replication package for the ICTSS 2026 paper. An LLM pipeline selects and implements maintainability-oriented architectural tactics in 56 open-source Python projects and gates every edit on the project's existing test suite. The package contains: the 56-repository outcome dataset; per-repository static-analysis artifacts (Radon Maintainability Index, architecture proxies) and per-step pytest/gating records; the pipeline source (Pipes-and-Filters); the prompt templates; and the behavioral-validation experiment (coverage of LLM-edited code plus a seeded-fault positive control) that measures whether the gate could fire. Scripts reproduce the maintainability statistics (Wilcoxon W=81, p=0.028, r̂=0.50) and the test-adequacy results (54% of modified repos had no test suite; 79% had no adequate oracle for the edit). Anonymized for double-blind review.

**Category:** Software  (component-level: `dataset/` → Data; `pipeline_source/` + `coverage_experiment/` → Software)

**Discipline / Subjects:** Computer Sciences → Software Engineering

**Tags / Keywords**
software testing; regression testing; test oracles; test adequacy; code coverage; generative-AI validation; large language models; automated refactoring; architectural tactics; software maintainability; empirical software engineering; replication

**License**
- Code (`pipeline_source/`, `coverage_experiment/`): MIT
- Data/artifacts (`dataset/`, `artifacts/`): CC-BY-4.0

**Contributors:** none shown for review (add at camera-ready). Affiliation withheld.

**Public/visibility:** keep private; share via anonymized view-only link for reviewers; make public on acceptance.

**Related identifiers:** link the published paper DOI at camera-ready; mint an OSF DOI for the project then.

**Suggested component structure (optional)**
- "Dataset" — `dataset/` + `artifacts/`
- "Pipeline source" — `pipeline_source/` + `prompts/`
- "Behavioral-validation experiment" — `coverage_experiment/`

**Files to upload:** `replication.zip` (831 files, ~0.9 MB; repo-file backups omitted; `GITHUB_TOKEN` is a placeholder; no author-identifying strings).
