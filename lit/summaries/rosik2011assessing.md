## Assessing Architectural Drift in Commercial Software Development: A Case Study

| Field | Value |
|-------|-------|
| **Key** | `rosik2011assessing` |
| **Authors** | Jacek Rosik, Andrew Le Gear, Jim Buckley, Muhammad Ali Babar, Dave Connolly |
| **Venue** | Software: Practice and Experience, 41(1):63-86 (2011) |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** Implementations commonly diverge from designed architectures (architectural drift), but existing empirical studies are mostly single-session post-deployment evaluations on finished systems. There is little evidence that detecting architectural inconsistencies actually leads to their removal in real-life development scenarios.
- **Gap:** No longitudinal, in vivo case study had investigated whether architectural drift occurs during initial (de novo) implementation of a commercial system, nor whether detection of inconsistencies prompts developers to actually remove them.

### Contribution
This paper presents a 2-year longitudinal case study conducted at IBM Dublin Software Lab, assessing architectural drift during the de novo development of a commercial system (DAP 2.0) using Reflexion Modelling. The main contribution is twofold: (1) empirical evidence that architectural drift occurs even during initial implementation when the architect is also the sole developer, and (2) the critical finding that inconsistency identification alone does not lead to inconsistency removal -- developers chose to tolerate violations due to risk of ripple effects, time pressure, and legacy code constraints. Additionally, the study reveals that Reflexion Modelling can actively conceal inconsistencies within convergent edges (false negatives), directly contradicting the technique's assumed reliability.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 2  | 5  |   4   |  0  |   3    | 14/25 |

**Relevance:** MEDIUM

This paper is relevant to the thesis in two ways: (1) it provides empirical evidence of how architectural drift degrades maintainability, which motivates the need for automated architectural tactic implementation; (2) it demonstrates that manual detection of architecture violations is insufficient without enforcement mechanisms -- a gap that LLM-driven automated refactoring could potentially address by lowering the cost and risk of inconsistency removal.

### Method & Validation
- **Type:** Case Study (longitudinal, in vivo, action research)
- **Validation:** 2-year industrial case study at IBM with 3 participants, 6 sessions, content analysis of think-aloud data, video/audio recordings, retrospective interview; Reflexion Modelling with jRMTool Eclipse plugin

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** jRMTool Eclipse plugin (Reflexion Modelling tool for Java), Eclipse Java IDE
- **Languages:** Java (DAP 2.0 system: 28,500 LOC, 16 packages, 95 classes, 509 files in DAP 1.x; comparable size expected for DAP 2.0)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Drift occurs during initial implementation | 5 inconsistencies found in first session, even with single architect-developer |
| Total inconsistencies over 2 years | 9 divergent edges reflecting 15 violating source-code relationships |
| Inconsistency identification ≠ removal | None of the identified inconsistencies were explicitly removed by developers |
| Convergent edges hide violations (false negatives) | 5 of 8 analysed convergent edges hid divergent source-code relationships; one edge had 41/44 inconsistent relationships masked |
| Developers tolerate trivial violations | Risk of ripple effects from refactoring outweighed perceived benefit of fixing minor violations |
| Categories of drift | Legacy code reuse, genuine DA omissions, trivial (misplaced functionality, constant access) |
| Batch processing inadequate | Periodic evaluation sessions (4-5 months apart) insufficient; real-time notification recommended |
| Developer surprise at violations | 13 utterances of surprise recorded, indicating violations would have gone unnoticed without the tool |

### Dataset / Benchmark
Single commercial system: Domino Application Portlet (DAP) 2.0, developed at IBM Dublin Software Lab. 2-year longitudinal case study (November 2005 - October 2007), 6 sessions, 3 participants. Over 6 hours of audio/video recordings transcribed and analysed using content analysis. System architecture: 10 main components with interconnections tracked via Reflexion Models.

### Challenges & Limitations
- Single system, relatively small size; results may not generalize to larger systems or different organizational contexts.
- Only 3 participants, limiting population-level conclusions.
- Batch-processing nature of periodic evaluation sessions (4-5 months apart) may be insufficient for catching drift in real-time; real-time notification is recommended but not implemented.
- Reflexion Modelling was found to conceal inconsistencies within convergent edges (false negatives), directly contradicting the technique's assumed reliability.
- Developer-introduced mappings that hide inconsistencies (adding divergences to the DA) can corrupt future analyses and mislead new team members.
- The jRMTool is a prototype with GUI and memory issues, contributing to adoption barriers.
- The study cannot distinguish whether inconsistency persistence is due to batch processing delays or deliberate developer tolerance.

### Key Quotes
> "You've seen my surprise the last time, when we ran the tool against the existing code base." (Participant A, Session AB)

> "Maybe trying to fix these 'minor' issues would've possibly caused larger issues to appear and so made them not worth exploring..." (Participant B1, retrospective interview)

> "If performance can be gained by breaking an architectural design, then this can sometimes be acceptable... time pressure is probably the main factor in some of the decision making that goes on during such a development." (Participant B1, retrospective interview)

### Key Takeaway
Manual detection of architectural inconsistencies is necessary but not sufficient for maintaining architecture consistency -- developers need low-cost, low-risk remediation paths. This directly motivates the thesis approach: LLM-automated implementation of architectural tactics could reduce the cost and risk barrier that prevents developers from acting on detected violations, turning detection into actual architecture improvement.
