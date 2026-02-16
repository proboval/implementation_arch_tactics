# LLM Refactoring Effectiveness — Cross-Paper Synthesis

**Source:** NLM cross-paper synthesis across 34 sources
**Date:** 2026-02-16

## 1. Success Rates

| Study | Task | Rate | Notes |
|-------|------|------|-------|
| Piao 2025 | GPT-4 identification (generic prompt) | 15.6% (28/180) | Gemini only 3.9% |
| Piao 2025 | GPT-4 identification (subcategory prompt) | **86.7%** | Narrowing search space critical |
| Xu 2025 (MANTRA) | Agentic framework success | **82.8%** | vs 8.7% standalone RawGPT |
| Liu 2025 | StarCoder2 Pass@5 | 57.15% | Pass@1 only 28.36% |
| Liu 2025 | DeepSeek-V3 | **100% on 48/61 types** | vs 14/61 for GPT-4o-mini |
| DePalma 2024 | ChatGPT behavior preservation | **97.2%** (311/320) | High behavioral fidelity |

## 2. Best Performing Models

| Model | Strength | Key Number |
|-------|----------|------------|
| DeepSeek-V3 | Diverse refactoring types | 48/61 perfect |
| GPT-4/4o | Baseline high performance | 63.6% >= human expert |
| Gemini | Iterative improvement | 81.29% issue reduction (5 iterations) |
| StarCoder2 | Code smell reduction | 44.36% reduction (vs 24.27% human) |

## 3. What LLMs Handle Well vs Poorly

### Well (Localized/Low-level)
- Renaming parameters (10.4%), variables (8.5%), type changes (11.8%)
- Split Variable (1.0), Extract Variable (0.94), Extract Method
- Systematic, repetitive, rule-based edits

### Poorly (Architectural/Complex)
- **Extract Class: 0% success with generic prompts**
- Move Method: RawGPT failed entirely
- Broken modularization, deficient encapsulation
- Inline Variable and Introduce Special Case often produce uncompilable code
- **Code > 300 LOC: performance degrades significantly**

## 4. Common Failure Modes

| Failure | Rate/Detail |
|---------|-------------|
| Unsafe solutions (semantic/syntactic bugs) | 7.4% GPT, 6.6% Gemini |
| Hallucinations | Reference nonexistent variables/methods |
| Context blindness | Lack broader codebase understanding |
| Input length limits | Performance drops > 300 LOC |
| Lexical/parsing errors | Faulty string literals, invalid tokens |

## 5. Evaluation Metrics Used Across Studies

| Category | Metrics |
|----------|---------|
| Functional correctness | Compilation, unit test Pass@K, RefactoringMiner |
| Code similarity | CodeBLEU (< 0.6 typical), AST Diff P/R |
| Quality metrics | Cyclomatic Complexity, LOC, Fan-out |
| Smell reduction | SRR via SonarQube/DesigniteJava |
| Human-likeness | Comparison to developer "pure refactoring" commits |

## Key Implications for Thesis

1. **Agentic frameworks critical**: MANTRA's 82.8% vs RawGPT's 8.7% proves multi-agent pipeline essential
2. **Prompt specificity matters**: Generic → 15.6%, subcategory-specific → 86.7% (5.5x improvement)
3. **Architecture-level refactoring is the gap**: Extract Class 0%, Move Method fails → thesis targets exactly this gap
4. **300 LOC limit**: Pipeline must chunk code into manageable units
5. **Iterative approach works**: Gemini + 5 iterations = 81.29% issue reduction
6. **Behavior preservation is high**: 97.2% suggests LLMs can maintain functionality during refactoring
