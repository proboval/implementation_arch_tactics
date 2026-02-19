# Architectural Tactics: Detection vs Implementation Gap — Cross-Paper Synthesis

**Source:** NLM cross-paper synthesis across 34 sources
**Date:** 2026-02-16

## 1. Current Tactic Detection Approaches

| Approach | Tool/Method | Source |
|----------|-------------|--------|
| NLP/BERT text analysis | Classification of docs | Marquez 2022 |
| ML classifiers (SVM, Decision Tree) | Code analysis | Marquez 2022 |
| Archie (Eclipse plugin) | Code→requirement traceability | Marquez 2022 |
| ArchEngine | Code segment classification | Marquez 2022 |
| ARCODE | API spec models (FSpec) for deviation detection | Marquez 2022 |
| RBML mapping | Microservice→tactic qualitative mapping | Bogner 2019 |

## 2. Critical Gaps: Detection → Implementation

| Gap | Description |
|-----|-------------|
| **Traceability Gap** | Design decisions in docs rarely trace back to source code |
| **Complexity Gap** | Developers struggle to implement tactics — cross-cutting, need framework knowledge (e.g., JAAS) |
| **Intent Gap** | Architect claims tactic is implemented but code analysis finds no evidence |
| **Transformation Gap** | Tools detect violations but don't provide the architectural solution; no cost/impact info |

## 3. Available Datasets

| Dataset | Size | Domain | Source |
|---------|------|--------|--------|
| IPSynth | 20 tactic implementation tasks | JAAS security tactics | Shokri 2024 |
| Refactoring Oracle | 12,526 refactorings (905 pure structural) from 188 projects | Open-source Java | MANTRA (Xu 2025) |
| SO Mining | 1,165 posts, 1,203 tactic instances | Stack Overflow practitioner knowledge | Bi 2021 |
| Kádár et al. 2016 | 145 validated refactoring cases | Maintainability-linked | Referenced |

## 4. Static Analysis for Measuring Tactic Impact

| Finding | Detail |
|---------|--------|
| SonarQube SQALE model | Estimates fix effort in minutes → Technical Debt Ratio |
| **Tool agreement** | **< 0.4% agreement** between SonarQube, PMD, Checkstyle (Lenarduzzi 2023) |
| Precision | SonarQube 18%, PMD 52% — unreliable for absolute measurements |
| Iterative LLM+SonarQube | 58% average defect reduction (Goncalves 2025) |
| **Implication** | Need multi-tool validation, not single-tool reliance |

## 5. Automated Architecture-Level Transformation

| Approach | Success | Level |
|----------|---------|-------|
| IPSynth (program synthesis) | **85% semantic correctness** | Inter-procedural tactic implementation |
| MANTRA (agentic LLM) | **82.8% compile+test pass** | Method-level refactoring |
| DeepSeek-V3 + instructions | 48/61 refactoring types | Method-level with step-by-step prompts |
| PerOpteryx | Meta-heuristic optimization | Architecture model optimization |

## Key Implications for Thesis

1. **The transformation gap is the thesis contribution** — tools detect but don't implement tactics
2. **IPSynth (85%) is the closest baseline** — but uses program synthesis, not LLMs
3. **MANTRA (82.8%) proves agentic approach works** — but at method level, not architecture level
4. **Multi-tool validation needed** — SonarQube alone has 18% precision
5. **Existing datasets are small** — IPSynth has only 20 tasks; thesis can create larger benchmark
6. **Prompt structure critical** — step-by-step instructions dramatically improve success rates
