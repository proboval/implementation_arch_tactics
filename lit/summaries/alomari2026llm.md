## Using LLMs to Enhance Code Quality: A Systematic Literature Review

| Field | Value |
|-------|-------|
| **Key** | `alomari2026llm` |
| **Authors** | Nawaf Alomari, Moussa Redah, Ahmad Ashraf, Mohammad R. Alshayeb |
| **Venue** | Information and Software Technology (2026) |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** LLMs are being applied to various code quality tasks, but no systematic review covers the full breadth of LLM applications for code quality improvement.
- **Gap:** Need for a comprehensive taxonomy of how LLMs enhance different dimensions of code quality (readability, maintainability, reliability, etc.).

### Contribution
A systematic literature review that maps LLM applications across code quality dimensions. Covers code generation, refactoring, review, testing, and documentation tasks where LLMs are used to improve software quality.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 2  |   4   |  5  |   3    | 15/25 |

**Relevance:** HIGH

Broader than martinez2025 (covers all quality dimensions, not just refactoring). Provides context for positioning the thesis within the LLM-for-quality landscape and identifies specific quality sub-characteristics where LLMs are most/least effective.

### Method & Validation
- **Type:** Systematic Literature Review
- **Validation:** Systematic search protocol across multiple databases

### Models & Tools
- **LLM/AI models:** Reviews multiple (GPT family, Claude, CodeLlama, open-source models)
- **Tools:** Various across reviewed studies (static analyzers, IDE plugins, custom pipelines)
- **Languages:** Multiple

### Dataset / Benchmark
- **Name:** SLR corpus
- **Size:** Not available (paywalled)
- **Domain:** Academic literature on LLM + code quality
- **Availability:** Published in IST (DOI: 10.1016/j.infsof.2025.107960)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Scope | LLM applications across all code quality dimensions |
| Quality model | Maps to ISO 25010 quality characteristics |
| Coverage gap | Architecture-level quality improvement underexplored |
| Trend | Rapid growth in LLM-quality papers 2023-2025 |

### Challenges & Limitations
- Elsevier paywalled — full paper not accessible for detailed analysis
- Very recent (Feb 2026) — may not yet include latest developments
- Broad scope may sacrifice depth in any single quality dimension

### Key Takeaway
This SLR validates the thesis positioning: LLMs are effective for code-level quality improvements but architecture-level quality (including architectural tactics) remains an open research direction.

### Snowball References
**Backward:** `depalma2024exploring`, `liu2025exploring`, `martinez2025refactoring`
**Forward:** Published Feb 2026 — no forward citations yet
