## Exploring the Potential of General Purpose LLMs in Automated Software Refactoring: An Empirical Study

| Field | Value |
|-------|-------|
| **Key** | `liu2025exploring` |
| **Authors** | Bo Liu, Yanjie Jiang, Yuxia Zhang, Nan Niu, Guangjie Li, Hui Liu |
| **Venue** | Automated Software Engineering, 32:26 (2025) |
| **Tier** | Q1 (Springer, top SE journal) |
| **Citations** | N/A (published March 2025) |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** Despite the existence of numerous automated/semi-automated refactoring tools (IntelliJ IDEA, JDeodorant), developers still must explicitly specify which code to refactor, what kind of refactoring to apply, and the detailed parameters -- making the process challenging and time-consuming.
- **Motivation:** Large language models have demonstrated promising results in code generation, fault location, and program repair, making them potentially feasible for automated software refactoring. However, it remained unclear how well LLMs perform compared to human experts in identifying refactoring opportunities and recommending solutions.
- **Gap:** No prior comprehensive empirical study had evaluated general-purpose LLMs on both refactoring opportunity identification and solution recommendation using a high-quality, expert-validated dataset of real-world refactorings, with quantification of the safety risks (semantic bugs and syntax errors) introduced by LLM-suggested refactorings.

### Contribution
This paper presents the first comprehensive empirical study evaluating LLMs (GPT-4 and Gemini-1.0 Pro) on two core refactoring tasks: (1) identifying refactoring opportunities and (2) recommending refactoring solutions. The authors construct a high-quality dataset of 180 real-world refactorings across 9 types from 20 open-source Java projects, validated by three human experts. They demonstrate that while LLMs with generic prompts achieve only 15.6% recall in opportunity identification, tailored prompts specifying refactoring subcategories and narrowing search scope boost success rates to 86.7%. For solution recommendation, 63.6% of GPT-4's suggestions were rated comparable to or better than human expert solutions, though 7.4% introduced unsafe changes (semantic bugs or syntax errors).

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 2  | 2  |   4   |  5  |   2    | 15/25 |

**Relevance:** HIGH

This paper directly validates the feasibility of using general-purpose LLMs for automated code-level refactoring, which is a prerequisite capability for the thesis goal of LLM-driven architectural tactic implementation. The findings on prompt engineering strategies (specifying refactoring types, narrowing search scope) and the quantification of LLM safety risks (7.4% buggy rate) are directly applicable to designing the thesis pipeline's LLM-based transformation filters. The paper's evidence that LLMs struggle with complex, large-scope refactorings (>300 LOC) informs scope limitations for the thesis approach.

### Method & Validation
- **Type:** Empirical Study
- **Validation:** Expert Review (3 independent experts for dataset validation + 3 independent developers for solution quality assessment, Fleiss' kappa = 0.82) + Automated Unit Testing (102 tests) + Statistical Tests (Wilcoxon signed-rank, Cliff's Delta)
- **Evidence:** Quantitative performance metrics (recall, precision, accuracy) across 180 refactoring instances; human expert quality ratings on 5-point scale (Excellent/Good/Poor/Failed/Buggy); statistical significance tests confirming improvements from prompt strategies

### Models & Tools
- **LLM/AI models:** GPT-4 (version gpt-4-1106-preview), Gemini-1.0 Pro
- **Tools/frameworks:** ReExtractor and RefactoringMiner 2.0 (for mining refactorings from commits); IntelliJ IDEA and JDeodorant (mentioned as baseline refactoring engines); automated unit test generation tool (Yaron 2024); 102 unit tests (59 inherent + 43 auto-generated) for behavior preservation validation
- **Languages:** Java (180 refactorings from 20 open-source Java projects, 160 unique Java documents)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Generic prompt recall (RQ1-1) | GPT: 15.6%, Gemini: 3.9% -- LLMs exhibit limited effectiveness with generic prompts |
| Type-specified prompt recall (RQ1-2) | GPT: 52.2% (+235%), Gemini: 21.1% (+441%) -- specifying refactoring types significantly improves identification |
| Optimized prompt recall (RQ1-4) | GPT: 86.7% -- specifying subcategories + narrowing search space achieves best results |
| Code size effect (RQ1-3) | Moderate negative correlation (-0.38 GPT, -0.28 Gemini); LLMs limited to <300 LOC for practical use |
| Solution quality (RQ2-1) | GPT: 63.6% comparable/better than human experts; Gemini: 56.2% comparable/better |
| Identical to ground truth | GPT: 48/176 (27.3%) solutions identical to developer solutions |
| Unsafe solutions (RQ2-2) | GPT: 13/176 (7.4%) buggy; Gemini: 9/137 (6.6%) buggy; 18/22 were semantic changes, 4/22 syntax errors |
| Best refactoring types for solution quality | Inline-related (87.5% good/excellent) and extract-related (70% good/excellent) |
| Worst refactoring types for solution quality | Rename refactorings -- only 43.8% comparable to or better than humans |
| False positive tendency | LLMs tend to suggest extract method refactorings more than other types; both models produced highest FPs for extract method |
| Extract class identification | Both GPT and Gemini achieved 0% recall for extract class with generic prompts; class-level decomposition remains challenging |

### Key Quotes
> "LLMs are best used as suggestive auxiliary tools rather than precise and reliable code refactoring tools." (p. 32)

> "The practicality of LLMs in identifying refactoring is confined to small code fragments of less than 300 LOC." (p. 16)

> "With proper prompts, LLMs have the potential to identify up to 86.7% of the refactoring opportunities with high accuracy." (p. 35)

> "63.6% of the recommended solutions were comparable to (even better than) those constructed by human experts." (p. 1, Abstract)

> "22 out of the 313 solutions suggested by ChatGPT and Gemini were unsafe in that they either changed the functionality of the source code or introduced syntax errors." (p. 3)

> "Semantic changes cannot be identified by compilers. Regression testing has the potential to identify functional changes, but software projects in the wild rarely have sufficient regression unit tests." (p. 29)

### Challenges & Limitations
1. **Limited to within-document refactoring:** Only 9 types of single-file refactorings studied due to LLM context length limitations; cross-document refactorings (e.g., move class, move method) not evaluated.
2. **Java-only:** Confined to Java because state-of-the-art refactoring detection tools do not support other languages.
3. **Small dataset:** Only 180 refactoring instances (20 per type) due to the high cost of manual expert validation (42 man-days total).
4. **Only two LLMs tested:** GPT-4 and Gemini-1.0 Pro; findings may not generalize to other models.
5. **No comparison with traditional tools:** The study does not compare LLM-based refactoring against existing semi-automated approaches (JDeodorant, PMD, IntelliJ IDEA) in terms of cost-effectiveness.
6. **LLM stochasticity:** Inherent randomness of LLM outputs means results may vary across runs.
7. **Safety risk:** 7.4% buggy rate with semantic changes being more dangerous than syntax errors because they are harder to detect (compilers catch syntax errors but not behavioral changes).

### Dataset / Benchmark
- **Name:** ref-Dataset (LLM4Refactoring)
- **Size:** 180 real-world refactorings from 20 open-source Java projects (160 unique Java documents) + 20 negative samples + 102 unit tests; 9 within-document refactoring types (extract class/method/variable, inline method/variable, rename attribute/method/parameter/variable)
- **Domain:** Open-source Java projects; refactorings mined from commits after April 2023 (post GPT-4 training cutoff) using ReExtractor and RefactoringMiner, validated by 3 independent human experts (42 man-days total)
- **Availability:** Publicly available at https://github.com/bitselab/LLM4Refactoring

### Key Takeaway
For the thesis pipeline, LLM-driven architectural tactic implementation should adopt a structured, multi-stage prompting strategy rather than relying on generic instructions: (1) specify the exact transformation type (refactoring subcategory), (2) narrow the search scope to the relevant code unit (<300 LOC), and (3) always validate LLM outputs with automated testing and static analysis to catch the ~7% unsafe transformation rate. The evidence that LLMs perform well on extract-related and inline-related refactorings but struggle with class-level decomposition suggests that architectural tactics requiring structural reorganization (e.g., extract class for modularity) will need additional safeguards or hybrid approaches.

### Snowball References
**Backward:** `depalma2024exploring` (ChatGPT refactoring capabilities -- less rigorous predecessor), `fowler1999refactoring` (refactoring foundations), `pomian2024emassist` (EM-Assist: LLM + IDE for safe extract method), `dilhara2024unprecedented` (LLM + transformation by example at FSE'24), `guo2024exploring` (ChatGPT for automated code refinement at ICSE'24), `shirafuji2023refactoring` (LLM program simplification), `tsantalis2022refactoringminer` (RefactoringMiner 2.0)
**Forward:** Check Google Scholar for papers citing this (published March 2025)
