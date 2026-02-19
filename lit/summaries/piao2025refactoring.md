## Refactoring with LLMs: Bridging Human Expertise and Machine Understanding

| Field | Value |
|-------|-------|
| **Key** | `piao2025refactoring` |
| **Authors** | Chen Kuang Piao, Jean Carlors Paul, Leuson Da Silva, Arghavan Moradi Dakhel, Mohammad Hamdaqa, Foutse Khomh |
| **Venue** | Preprint / arXiv (2025) |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** Despite the importance of code refactoring for maintainability, developers often neglect it due to the significant time, effort, and resources required, as well as the lack of immediate functional rewards. Existing automated refactoring tools (IDE-based, rule-based) remain limited in supporting a broad spectrum of refactoring types, and LLMs tend to perform well on simpler transformations but struggle with more complex refactoring types requiring deeper reasoning about design intent.
- **Gap:** No systematic study has evaluated how different instruction strategies (derived from established refactoring guidelines like Fowler's catalog) affect LLM performance across all 61 refactoring types. Prior work focused on narrow subsets of refactoring types and did not compare human-oriented vs. machine-oriented instruction formulations.

### Contribution
This study systematically evaluates five instruction strategies (Zero-Shot, Two-Shot, Step-by-Step, Rule-based, and Objective Learning) for guiding LLMs (GPT-4o-mini and DeepSeek-V3) to perform code refactoring across all 61 refactoring types from Fowler's catalog. The authors demonstrate that instruction design significantly impacts LLM refactoring success, with rule-based instructions derived from automated detection tools outperforming human-oriented step-by-step descriptions for GPT-4o-mini, while DeepSeek-V3 achieves 100% success on benchmark scenarios with both Step-by-Step and Rule-based strategies. Notably, Objective Learning (providing only the high-level goal of refactoring without specifying a type) yields the best code quality metrics despite lower correctness of intended transformations.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 2  | 1  |   4   |  5  |   3    | 15/25 |

**Relevance:** HIGH

This paper directly informs the thesis prompt engineering strategy for LLM-driven architectural transformations. The finding that rule-based instructions outperform descriptive ones suggests that formalizing architectural tactic application as structured rules (rather than natural language steps) may improve LLM performance. The Objective Learning result -- where LLMs improve quality metrics when given freedom rather than prescribed transformations -- is particularly relevant to the thesis approach of specifying architectural quality goals (maintainability improvement) rather than dictating exact code changes.

### Method & Validation
- **Type:** Empirical experiment (controlled, multi-run)
- **Validation:** Manual validation (2 researchers, Cohen's Kappa 0.774-0.864) for benchmark scenarios; automated compilation + test suite execution for real scenarios (ANTLR4, JUnit); 5 runs per scenario per instruction; CodeBLEU, LOC, CC, FOUT metrics; Mann-Whitney U test (alpha = 0.05)

### Models & Tools
- **LLM/AI models:** GPT-4o-mini (OpenAI, closed-source), DeepSeek-V3 (open-source); both accessed via API with default hyperparameters
- **Tools:** Ref-Finder (rule-based refactoring detection, 63/72 refactoring types from Fowler's first edition), RefactoringMiner 2.0 (refactoring detection, 99.6% precision/94% recall), JavaParser (AST parsing for automated code integration), pyccmetrics and codebleu Python libraries (metric computation)
- **Languages:** Java (benchmark scenarios from Fowler's catalog in JavaScript, translated to Java for evaluation)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Best benchmark success rate | DeepSeek-V3 achieves 100% with Step-by-Step and Rule-based instructions; GPT-4o-mini peaks at 83.6% with Step-by-Step |
| DeepSeek coverage | 48/61 refactoring types at 100% success rate across instruction strategies |
| Rule-based vs. Step-by-Step | Rule-based (machine-oriented) instructions match or outperform human-oriented Step-by-Step for GPT-4o-mini; both achieve 100% for DeepSeek |
| Objective Learning paradox | Lowest correctness (29.5%-36.1%) but best quality metrics (lowest CC and LOC) -- LLMs improve code quality when given freedom |
| Semantic preservation | DeepSeek consistently produces zero new test failures/errors once code compiles; GPT-4o-mini introduces more semantic errors |
| Compilation rates (real scenarios) | 38%-51% across strategies; variable-level refactorings (Split Variable, Extract Variable) easiest; Inline Variable and Introduce Special Case never compile |
| LLM hallucinations | Most compilation errors caused by referencing undeclared variables/methods (hallucinations from insufficient context) |
| CodeBLEU similarity | Low scores (0.296-0.597) suggest LLMs generate novel solutions rather than memorized code |
| CC reduction (real) | Objective Learning yields CC of 5.82 for GPT-4o-mini, matching ground truth post-refactoring baseline |

### Dataset / Benchmark
Two datasets: (1) **Benchmark Scenarios** -- all 61 refactoring types from Fowler's Catalog of Refactorings (2nd edition), using illustrative pre/post code snippets as ground truth. (2) **Real Scenarios** -- 53 real refactoring instances across 11 refactoring types from ANTLR4 and JUnit GitHub projects, sourced from Kadar et al. (2016) using Ref-Finder, manually validated (145 TP cases from 7,872 samples across 7 projects, then expanded with 18 additional validated cases). Pre- and post-refactoring versions are compilable. Complete replication package with datasets, scripts, and automated evaluation framework publicly available.

### Challenges & Limitations
- **Low compilation rates in real scenarios:** Only 38-51% of LLM-generated refactorings compile successfully in real projects, primarily due to hallucinations (referencing undeclared variables/methods from insufficient context).
- **Objective Learning paradox:** While Objective Learning produces the best code quality metrics (lowest CC, LOC), it has the lowest correctness rate (29.5-36.1%) because LLMs cannot reliably infer the specific intended transformation from a high-level goal alone.
- **Limited real-scenario scale:** Only 53 real scenarios across 2 projects (ANTLR4, JUnit); many refactoring types have very few or no real examples due to compilation difficulties.
- **Java dependency complexity:** High dependency management requirements of Java projects made it difficult to compile pre/post versions for many potential real scenarios.
- **Rule coverage gap:** Only 46 of 61 refactoring types could be matched to Ref-Finder rules, leaving 15 types without Rule-based instruction evaluation.
- **Single language:** All evaluations in Java; generalizability to other languages unknown.

### Key Quotes
> "Interestingly, allowing models to focus on the overall goal of refactoring, rather than prescribing a fixed transformation type, can yield even greater improvements in code quality." (Abstract)

> "Rule-based instructions -- adapted from heuristics used in automated refactoring detection -- enable GPT-4o-mini to produce compilable, semantically preserved code more effectively than step-by-step, human-oriented instructions." (Section 1, Introduction)

### Key Takeaway
For the thesis pipeline, architectural tactic instructions should be formulated as **rule-based specifications** (formal pre/post conditions, structural transformation rules) rather than natural language step-by-step guides, since LLMs perform better with machine-oriented instruction formats. Additionally, consider a **two-phase approach**: first apply specific tactic transformations with rule-based prompts for correctness, then use objective-based prompting ("improve maintainability") for additional quality optimization -- leveraging the finding that unconstrained LLMs produce better quality metrics even when they do not apply the exact prescribed transformation.
