# Thesis Validation, Datasets, Motivation, Challenges & Gaps

**Source:** NLM cross-paper synthesis across 34 sources
**Date:** 2026-02-16

## 1. VALIDATION Methodologies & Metrics

### Functional Correctness
| Metric | Description | Source |
|--------|-------------|--------|
| Pass@K (K=1,3,5) | Unit test pass rate for refactored code | Liu 2025, Xu 2025 |
| Semantic Preservation | New Failed Tests / New Test Errors count | Xu 2025, Horikawa 2025 |
| Compilation Rate | % of syntactically valid transformed code | Multiple |
| RefactoringMiner | Verifies intended transformation actually occurred | Liu 2025, Piao 2025 |

### Structural & Semantic Similarity
| Metric | Threshold | Source |
|--------|-----------|--------|
| Dice Coefficient | >= 0.5 overlap with ground truth | Shokri 2024 |
| CodeBLEU | Grammatical + semantic consistency | Liu 2025 |
| AST Diff (P/R) | Node matching accuracy | Liu 2025 |
| HR@K / MRR | Tactic implementation point location accuracy | Shokri 2024 |

### Quality & Impact Metrics
| Metric | Thresholds | Source |
|--------|------------|--------|
| Smell Reduction Rate (SRR) | Via DesigniteJava / SonarQube | Horikawa 2025, Cordeiro 2024 |
| Maintainability Index (MI) | >85 easy, <65 difficult | Radon/Halstead |
| Technical Debt Ratio (TDR) | Rating A if < 5% | SonarQube SQALE |
| Scott-Knott Test | Statistical partitioning of techniques | Piao 2025 |
| Cliff's Delta (d) | Negligible <= 0.147, Large > 0.474 | Multiple |

## 2. DATASETS & Benchmarks

| Dataset | Size | Language | URL |
|---------|------|----------|-----|
| **IPSynth** | 20 tactic tasks (JAAS) | Java | anonymous.4open.science/r/Anonymous-82DE22 |
| **Refactoring Oracle** | 703 pure refactorings (10 projects) | Java | github.com/.../MANTRA |
| **Fowler Benchmark** | 61 refactoring types | Java/JS | github.com/arghavanMor/Refactoring_LLM_Benchmark |
| **StarCoder2 Eval** | 5,194 commits (30 Apache projects) | Java | github.com/.../LLM_Refactoring_Evaluation |
| **SO QA-AT** | 1,165 posts, 1,203 tactic instances | N/A | github.com/QA-AT/Mining-QA-AT-Knowledge-in-SO |
| **AIDev** | 15,451 agent-generated refactorings | Java | Horikawa 2025 |
| **Iterative Pipeline** | Commons Lang, IO, Guava | Java | zenodo.org/10.5281/zenodo.15278368 |

## 3. MOTIVATION Evidence

| Evidence | Numbers | Source |
|----------|---------|--------|
| Maintenance cost | **60-80% of system costs** | Multiple foundational |
| Refactoring effort | Up to **75% of development effort** | Fowler 2018 |
| Knowledge barrier | Novices struggle with cross-cutting tactics + framework knowledge | Shokri 2024 |
| Design decay | Implementations diverge from intended architecture | Li 2021, Rosik 2011 |
| Manual effort | "Tedious, time-consuming, error-prone" | Shokri 2024, Kim 2009 |

## 4. CHALLENGES for LLM Architecture Transformation

| Challenge | Detail |
|-----------|--------|
| **Context blindness** | LLMs lack broader system context, cross-document dependencies |
| **Hallucinations** | Reference nonexistent variables, methods, symbols |
| **Token/length limits** | Performance drops > 300 LOC |
| **Complexity gap** | Excel at local edits, struggle with Extract Class, context-sensitive logic |
| **Non-determinism** | Same prompt → divergent results, unreliable for automated engines |

## 5. RESEARCH GAPS for Thesis

| Gap | Evidence | Thesis Response |
|-----|----------|-----------------|
| **70% of studies don't describe tactic identification method** | Marquez 2022 | Automated tactic detection pipeline |
| **Design rationale doesn't trace to code** | Multiple | LLM bridges intent→implementation |
| **Agents are "tactical cleanup partners" only** | Horikawa 2025 | Elevate to architectural planners |
| **No cost-benefit quantification** | Multiple | Before/after metric comparison |
| **LLM + formal verification integration** | Multiple | Static analysis feedback loop |

## Key Thesis Positioning

The thesis fills the **transformation gap**: existing work either *detects* tactics (Marquez, Shokri) or performs *code-level* refactoring with LLMs (DePalma, Liu, MANTRA). No work uses LLMs to *implement architectural tactics* — the thesis uniquely bridges architecture-level design decisions with automated code transformation.
