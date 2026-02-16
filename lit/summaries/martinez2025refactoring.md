## Software Refactoring Research with Large Language Models: A Systematic Literature Review

| Field | Value |
|-------|-------|
| **Key** | `martinez2025refactoring` |
| **Authors** | Sofia Martinez, Luo Xu, Mariam Elnaggar, Eman Alomar |
| **Venue** | Journal of Systems and Software (2025) |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** LLMs are increasingly used for code refactoring tasks, but no systematic review synthesizes the existing body of work on LLM-based refactoring.
- **Gap:** Lack of a comprehensive mapping of how LLMs are applied across different refactoring activities, what models are used, and what evaluation approaches are employed.

### Contribution
A systematic literature review covering the intersection of LLMs and software refactoring. Categorizes research by refactoring type, LLM model used, evaluation methodology, and reported effectiveness. Identifies gaps and future directions.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 2  |   4   |  5  |   3    | 15/25 |

**Relevance:** HIGH

Directly maps the landscape of LLM-based refactoring research, providing the thesis with a validated taxonomy of approaches, evaluation methods, and identified gaps. Confirms no work combines LLMs with architectural tactic implementation.

### Method & Validation
- **Type:** Systematic Literature Review
- **Validation:** Systematic search protocol, inclusion/exclusion criteria

### Models & Tools
- **LLM/AI models:** Reviews multiple (GPT-3.5, GPT-4, CodeLlama, StarCoder, etc.)
- **Tools:** Various across reviewed studies
- **Languages:** Multiple (Java, Python primarily)

### Dataset / Benchmark
- **Name:** SLR corpus
- **Size:** Not available (paywalled)
- **Domain:** Academic literature on LLM + refactoring
- **Availability:** Published in JSS (DOI: 10.1016/j.jss.2025.112762)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Scope | LLM applications across refactoring activities |
| Key gap | No work on architecture-level LLM refactoring |
| Models reviewed | Multiple commercial and open-source LLMs |
| Evaluation | Varied — functional correctness, quality metrics, human evaluation |

### Challenges & Limitations
- Elsevier paywalled — full paper not accessible for detailed numerical findings
- SLR limited to papers available at time of review
- Rapid evolution of LLM capabilities may date findings quickly

### Key Takeaway
This SLR provides the most comprehensive mapping of LLM+refactoring landscape; the thesis should position itself relative to the taxonomy and gaps identified here, particularly the absence of architecture-level refactoring.

### Snowball References
**Backward:** `depalma2024exploring`, `liu2025exploring` (primary studies reviewed)
**Forward:** Recently published — forward citations still accumulating
