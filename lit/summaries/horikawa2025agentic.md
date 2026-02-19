## Agentic Refactoring: An Empirical Study of AI Coding Agents

| Field | Value |
|-------|-------|
| **Key** | `horikawa2025agentic` |
| **Authors** | Horikawa, K., Li, H., Kashiwa, Y., Adams, B., Iida, H., Hassan, A.E. |
| **Venue** | Preprint / arXiv (November 2025) |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** Agentic coding tools (OpenAI Codex, Claude Code, Devin, Cursor) are rapidly being adopted as autonomous coding teammates, yet there is no empirical understanding of how agentic refactoring is used in practice, how it compares to human-driven refactoring, and what impact it has on code quality.
- **Gap:** While prior research has studied LLM-based code generation and prompt-based refactoring, no study has examined AI agent participation in refactoring at scale, nor how AI-generated refactorings differ from human refactoring in frequency, type, intent, and quality impact. This is the first large-scale empirical analysis of refactoring in agentic commits.

### Contribution
First large-scale empirical study of refactoring performed by AI coding agents (OpenAI Codex, Claude Code, Devin, Cursor) in real-world open-source Java projects. Analyzes 15,451 refactoring instances across 12,256 pull requests and 14,998 commits from the AIDev dataset, examining four dimensions: prevalence, types, purposes, and impact on code quality. Establishes that agents are active refactoring participants but are limited to low-level, localized edits rather than high-level architectural restructuring.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 2  | 2  |   5   |  5  |   4    | 18/25 |

**Relevance:** HIGH

Directly validates the thesis premise that LLM-based agents can improve maintainability through code refactoring, while simultaneously exposing their key limitation: agents excel at low-level consistency edits but struggle with high-level architectural changes (exactly the gap the thesis aims to address with architectural tactics). The empirical evidence on maintainability metrics (DesigniteJava, LOC, WMC, fan-in/fan-out) and the finding that medium-level structural refactorings yield the largest quality gains informs the thesis evaluation methodology. The recommendation to equip agents with design-smell detection tools via MCP aligns directly with the thesis pipeline approach.

### Method & Validation
- **Type:** Large-scale empirical mining study
- **Validation:** Statistical tests (Mann-Whitney U, Wilcoxon signed-rank, Kruskal-Wallis), effect sizes (Cliff's delta, rank-biserial), FDR correction (Benjamini-Hochberg), inter-rater reliability (Cohen's kappa = 0.77-0.83 for purpose classification)

### Models & Tools
- **LLM/AI models:** Analyzed outputs from OpenAI Codex (89.3% of commits), Devin (5.7%), Cursor (4.4%), Claude Code (0.6%); GPT-4.1-mini used for automated purpose classification of refactoring commits
- **Tools:** RefactoringMiner 3.0.11 (refactoring detection, F-score 99.5%, 103 distinct refactoring types), DesigniteJava 2.0 (code quality metrics and design/implementation smell detection, 27 smell types), GitHub REST API (commit mining)
- **Languages:** Java

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Refactoring prevalence | 26.1% of agentic commits explicitly target refactoring |
| Total instances | 15,451 refactoring instances across 14,998 commits |
| Dominant refactoring types | Change Variable Type (11.8%), Rename Parameter (10.4%), Rename Variable (8.5%) -- low-level edits dominate |
| Agent vs. human abstraction | Agents: 35.8% low-level, 21.2% medium, 43.0% high-level; Humans: 24.4% low, 20.7% medium, 54.9% high |
| Primary purpose: maintainability | 52.5% of agentic refactoring is motivated by maintainability (vs. 11.7% for humans) |
| Secondary purpose: readability | 28.1% readability (similar to human 25.7%) |
| Design-level purposes rare | Duplication (1.1%), Repurpose/Reuse (4.6%) are negligible for agents vs. significant for humans (13.7%, 12.9%) |
| Structural metric improvements | Class LOC median delta = -15.25, WMC median delta = -2.07 (medium-level refactorings) |
| Smell count reduction | Negligible -- median delta = 0.00 for both design and implementation smells; effect sizes negligible (Cohen's d ~ -0.027) |
| Medium-level refactorings most effective | Medium-level changes (Extract Method, Inline Method) yield largest quality gains |
| Structural decomposition best | Extract Subclass: Class LOC delta = -87.5, WMC delta = -11.5; Split Class: LOC delta = -16.0, WMC delta = -4.0 |
| PR merge rate | 86.9% of agentic PRs merged, indicating high acceptance of agent-generated code |
| Tangled commits | 53.9% of refactoring instances occur in commits without explicit refactoring intent |
| Agent distribution | OpenAI Codex dominates (89.3% commits), Devin (5.7%), Cursor (4.4%), Claude Code (0.6%) |
| Tools used | RefactoringMiner 3.0 (refactoring detection, F-score 99.5%), DesigniteJava (metrics and smell detection) |

### Dataset / Benchmark
AIDev dataset: 932,791 pull requests from 61,000+ repositories by five coding agents. Filtered to 1,613 unique non-fork Java repositories with 14,998 non-merge commits modifying Java files, yielding 15,451 refactoring instances across 12,256 PRs. Agentic refactoring commits: 3,907 (26.1%). Agent distribution: OpenAI Codex (89.3%), Devin (5.7%), Cursor (4.4%), Claude Code (0.6%). Human baseline from Horikawa et al. (2025) prior work. Replication package available at GitHub (Mont9165/Agent_Refactoring_Analysis).

### Challenges & Limitations
- **Low-level dominance:** Agents overwhelmingly perform low-level consistency edits (renaming, type changes) rather than high-level architectural restructuring, limiting their impact on design quality.
- **Smell reduction failure:** Despite explicit maintainability goals, agentic refactoring fails to consistently reduce design and implementation smell counts (median delta = 0.00, negligible effect sizes).
- **Tangled commits:** 53.9% of refactoring instances occur in commits without explicit refactoring intent, increasing review burden and making it hard to attribute quality changes.
- **Java only:** Analysis limited to Java files; patterns may differ in other language ecosystems.
- **Agent attribution ambiguity:** Difficult to ascertain the precise extent of human intervention in agentic commits; developers may modify, accept, or reject parts of AI-generated code before committing.
- **Open-source only:** Based on the AIDev dataset of OSS projects; industrial/closed-source practices may differ.

### Key Quotes
> "Agentic coding tools effectively serve as incremental cleanup partners, excelling at localized refactoring and consistency improvements necessary for long-term maintainability. However, to realize the vision of agents as 'software architects,' significant advancements are needed to enable autonomous, architecturally-aware restructuring that consistently addresses higher-level design smells." (Section 8, Conclusion)

> "Are these agents merely acting as 'code janitors,' automating low-level syntactic cleanup, or are they beginning to function as 'software architects,' executing deep structural design improvements essential for long-term maintainability?" (Section 4.2)

### Key Takeaway
Current LLM-based coding agents function as effective "incremental cleanup partners" for low-level maintainability improvements but cannot perform the high-level architectural restructuring that the thesis targets. This empirical gap -- agents doing renaming/type changes but not Extract Class, Split Class, or dependency restructuring -- is precisely the opportunity the thesis addresses by guiding LLM agents with explicit architectural tactic knowledge. The finding that medium-level and structural decomposition refactorings produce the largest measurable quality gains validates the thesis strategy of targeting architecture-level tactics rather than cosmetic edits. The recommendation to integrate design-smell detection tools (e.g., DesigniteJava via MCP) into agent planning loops directly supports the thesis pipeline architecture.
