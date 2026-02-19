## An Empirical Study on the Effectiveness of Iterative LLM-Based Improvements for Static Analysis Issues

| Field | Value |
|-------|-------|
| **Key** | `goncalves2025sonarqube` |
| **Authors** | Goncalves, J.C. and Maia, M.A. |
| **Venue** | SBES '25 (Brazilian Symposium on Software Engineering), September 2025, Recife, Brazil |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** Software maintenance and evolution consume more resources than initial development. SonarQube effectively detects code quality issues but does not automatically apply fixes, leaving developers responsible for manually resolving reported issues -- a time-consuming and error-prone process, especially in large-scale projects.
- **Gap:** Prior work on LLM-based code repair has not systematically investigated the iterative use of LLMs guided by static analysis tools, nor evaluated the impact of different configurations (model, temperature, prompt, iterations) on improvement quality. The intersection of static analysis feedback loops with LLM-driven code improvement remains underexplored.

### Contribution
This paper presents an automated iterative pipeline that integrates SonarQube static analysis with LLMs (GPT-4-mini and Gemini) to reduce code quality issues in Java projects. The pipeline feeds SonarQube-detected issues as prompts to LLMs, replaces the code with the LLM-generated version, and re-analyzes iteratively until convergence or a maximum iteration count is reached. The study evaluates the impact of model choice, temperature, prompt style, and iteration count on issue reduction, technical debt, and functional preservation across three open-source Java repositories (Commons Lang, Commons IO, Google Guava).

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 1  |   4   |  5  |   5    | 16/25 |

**Relevance:** HIGH

This paper directly validates the thesis's core pipeline concept -- using static analysis feedback to guide LLM-driven code improvement in iterative cycles. While it operates at the code-smell/issue level rather than at the architectural tactic level, the methodology (iterative SonarQube-LLM loop, metric-based evaluation, behavior preservation concern) is closely analogous to the thesis pipeline. The findings on configuration sensitivity (model, temperature, prompt, iterations) provide actionable design parameters.

### Method & Validation
- **Type:** Experiment (controlled, multi-configuration)
- **Validation:** Quantitative metrics from SonarQube (issue count, severity, technical debt in minutes) across 8 experimental configurations x 3 datasets. Fractional Factorial Design (FFD) used for systematic parameter exploration. Functional correctness assessed manually via inspection and execution (no automated test suite integration).

### Models & Tools
- **LLM/AI models:** GPT-4-mini (OpenAI), Gemini (Google)
- **Tools:** SonarQube (static analysis -- issue detection, severity classification, technical debt estimation), SonarScanner (analysis execution), custom Python pipeline (orchestrating iterative analysis-prompt-replace-reanalyze cycles), Docker (SonarQube containerization)
- **Languages:** Java

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Average issue reduction | >58% across all experiments; best config reached 81.29% |
| Best configuration | Gemini, temperature 0.1, Prompt 1 (zero-shot), 5 iterations (Exp. 7) |
| Worst configuration | GPT-4-mini, temperature 0.3, Prompt 2 (role-based), 2 iterations (Exp. 2): 49.49% |
| Technical debt vs. issue reduction | Not proportional -- Commons Lang: 58.81% issue reduction but only 42.08% debt reduction (ratio 0.71) |
| Severity handling | MAJOR and CRITICAL issues corrected effectively; BLOCKER issues showed slight increase in some cases |
| Iteration effect | 5 iterations consistently outperformed 2 iterations, but only when other parameters were well-tuned |
| Temperature-prompt interaction | Higher temperature (0.3) requires clearer prompts; vague prompts + high temperature = worst results |
| Model comparison | Gemini more robust and consistent across configs; GPT-4-mini more sensitive to parameter tuning |
| Functional preservation | No functional breakages observed in manual evaluation; LLMs performed conservative changes (renaming, method extraction) |
| Key limitation | No automated test suite integration; functional verification was manual only |
| Construct validity concern | SonarQube as sole quality metric misses architectural design issues, readability aspects not mapped to rules |
| LLM black-box limitation | LLMs lack awareness of broader architecture; improvements are localized, potentially ignoring cross-component dependencies |

### Dataset / Benchmark
Three open-source Java repositories: Apache Commons Lang, Apache Commons IO, and Google Guava. Classes from each repository processed individually through the iterative pipeline. Commons Lang used as primary dataset with all 8 configurations executed 3 times for statistical robustness; Commons IO and Google Guava used for exploratory single-run experiments. No formal benchmark -- evaluated on real production code from actively maintained projects. No public replication package mentioned.

### Challenges & Limitations
- **No automated test integration:** Functional correctness was assessed manually only; the absence of automated test suite integration means behavior preservation cannot be guaranteed at scale.
- **SonarQube as sole quality metric:** Reliance on SonarQube alone misses architectural design issues and readability aspects not mapped to rules; construct validity threat.
- **LLM black-box limitation:** LLMs operate without explicit reasoning about the software's broader architecture and context, producing only localized changes while potentially ignoring cross-component dependencies.
- **BLOCKER issues resistant:** LLMs could not efficiently handle BLOCKER-severity issues, which even showed slight increases in some experiments; deeper structural improvements remain challenging.
- **Technical debt disproportionality:** Issue reduction does not proportionally translate to technical debt reduction (ratio as low as 0.71), suggesting LLMs prioritize fixing low-effort issues.
- **Limited configuration space:** Only two LLMs, two temperatures, two prompts, and two iteration counts were explored; the parameter space is much larger.
- **Java-only, three repositories:** External validity limited to Java ecosystem and three well-known projects.

### Key Quotes
> "The results demonstrate that combining SonarQube with LLMs is effective in reducing code issues -- achieving over 58% average reduction in key scenarios -- while preserving functionality." (Abstract)

> "The evaluated LLMs operate as black-box systems, lacking explicit reasoning regarding the software's broader architecture and context. As a result, the generated improvements are primarily focused on localized changes, potentially ignoring dependencies and interactions among components." (Section 6.4, Conclusion Validity)

### Key Takeaway
The iterative SonarQube-LLM feedback loop is empirically validated as effective for reducing code-level issues (>58% on average), but the thesis should extend this approach to the architectural level -- addressing the acknowledged limitation that LLMs produce only localized fixes and ignore broader architectural context. The finding that more iterations amplify quality gains (when other parameters are calibrated) supports designing the thesis pipeline with configurable iteration depth. The technical debt / issue reduction gap (ratio as low as 0.71) warns that counting resolved issues alone is insufficient; the thesis must track maintainability-weighted metrics (e.g., Maintainability Index, architectural coupling) rather than simple issue counts.
