## Dealing with SonarQube Cloud: Initial Results from a Mining Software Repository Study

| Field | Value |
|-------|-------|
| **Key** | `nocera2025sonarqube` |
| **Authors** | Nocera, Fucci, Scanniello |
| **Venue** | IEEE (2025) — likely ICSE/MSR workshop or conference short paper |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** Despite the growing adoption of SonarQube Cloud in open-source development (used by more than 22k GitHub users), there is limited empirical understanding of how developers configure and use it in practice. Questions remain about the extent to which predefined configurations are retained, how quality gates are customized, and which quality conditions are prioritized.
- **Gap:** Prior studies examined SCA tool configuration from the developer perspective (surveys, small-scale studies of 20 projects), but no study had systematically mined actual SonarQube Cloud usage patterns and quality gate configurations at scale across hundreds of open-source GitHub projects. The gap between tool design and actual practice remained uncharacterized.

### Contribution
This paper presents a mining study of 321 GitHub projects that use SonarQube Cloud via GitHub Actions, investigating usage patterns, quality gate customization, and the specific quality conditions enforced. The study reveals that while 55% of projects use the built-in "Sonar way" quality gate, 45% customize their quality gates, and the most commonly enforced conditions target security, maintainability, and reliability ratings on new code following the "Clean as You Code" principle.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 1  |   3   |  0  |   5    | 10/25 |

**Relevance:** MEDIUM

This paper provides empirical evidence on how SonarQube Cloud is actually used in open-source projects, which directly informs the thesis methodology for using static analysis tools (specifically SonarQube-family metrics) to evaluate maintainability before and after LLM-driven architectural tactic implementation. The finding that maintainability rating on new code is enforced in ~89% of quality gates validates that maintainability is a priority quality attribute in practice.

### Method & Validation
- **Type:** Mining Software Repository Study
- **Validation:** Manual inspection of 321 GitHub repositories; cross-validation of SonarQube Cloud API data with manual repository inspection; open-coding for usage pattern identification

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** SonarQube Cloud (formerly SonarCloud) -- SaaS automated code review and static code analysis platform; GitHub Actions (sonarcloud-github-action, sonarqube-scan-action); SonarQube Cloud API for data collection; GitHub dependency graph for repository discovery; SonarLint (IDE integration, found in 3.4% of projects)
- **Languages:** Language-agnostic study (SonarQube Cloud supports multiple programming languages); projects analyzed across diverse open-source GitHub repositories

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Projects correctly connected to SonarQube Cloud | 81% (260/321) |
| Projects using organization default quality gate | 75% (198/265) |
| Projects using built-in "Sonar way" quality gate | 55% (145/265) |
| Projects with fully customized (non-default, non-built-in) quality gates | 24% (63/265) |
| Most enforced condition: security rating on new code | 90.94% of projects |
| Maintainability rating on new code | 89.06% of projects |
| Reliability rating on new code | 88.68% of projects |
| Duplicated lines density on new code | 88.30% of projects |
| Coverage on new code (least common built-in condition) | 77.36% of projects |
| Non-built-in conditions adoption | Each used by <10% of projects |
| Projects with SonarQube Cloud absent or private | 14.6% |
| Projects connected to multiple SonarQube Cloud projects | 5.3% |

### Dataset / Benchmark
321 unique GitHub projects using SonarQube Cloud through sonarcloud-github-action and/or sonarqube-scan-action. Filtered from 34,975 + 12,986 dependent repositories using criteria: not archived, at least one commit in preceding month (April 2025), at least 100 stars, 100 commits, 1 fork, not a fork. Of these, 265 SonarQube Cloud projects were accessible via API (63 restricted due to organization permissions). Replication package available at: https://doi.org/10.6084/m9.figshare.29097383.

### Challenges & Limitations
- **Construct validity:** Identification of SonarQube Cloud usage relies on GitHub's dependency graph and manual inspection of configuration files; GitHub's dependency graph is prone to inaccuracies.
- **Conclusion validity:** Analysis correctness depends on SonarQube Cloud API accuracy and quality gate interpretation; mitigated by cross-validating data sources and manual inspection.
- **External validity:** Only open-source GitHub projects meeting specific activity and popularity thresholds were studied; findings may not generalize to private or enterprise projects.
- **Restricted access:** 63 SonarQube Cloud projects (connected to 30 GitHub projects) could not be queried due to organization permissions, potentially introducing selection bias.
- **Initial results:** Authors explicitly frame this as "initial results" -- a future agenda linking quality gate configurations to actual software outcomes remains to be investigated.

### Key Quotes
> "While 55% of the projects use the built-in quality gate provided by SonarQube Cloud, 45% of them customize their quality gate with different conditions." (Abstract)

> "This would enable evidence-based recommendations for configuring SCA tools like SonarQube Cloud in various contexts." (Abstract)

> "Predefined SCA tool configurations might not always be suitable and projects might require dynamic configurations." (Section V-A)

### Key Takeaway
SonarQube Cloud's built-in quality gate conditions -- particularly maintainability rating, reliability rating, and security rating on new code -- represent industry-standard quality thresholds adopted by the vast majority of open-source projects. The thesis should use these same conditions (or their underlying metrics) as evaluation criteria when measuring the impact of LLM-applied architectural tactics, since they reflect what practitioners actually prioritize for code quality enforcement in CI/CD pipelines.
