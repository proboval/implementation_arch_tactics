## A Contemporary Survey of Large Language Model Assisted Program Analysis

| Field | Value |
|-------|-------|
| **Key** | `wang2025llmpa` |
| **Authors** | Wang et al. |
| **Venue** | arXiv preprint, 2502.18714 (2025) |
| **Level** | L3-Thesis-Specific |

### Motivation & Gap
Traditional program analysis methods face substantial challenges in handling dynamic behaviors, cross-language interactions, and large-scale codebases. While LLMs show promise for program analysis, comprehensive reviews specifically addressing their role in this domain remain scarce.

### Contribution
A systematic survey categorizing LLM-assisted program analysis into three areas: static analysis (vulnerability detection, malware detection, program verification, static analysis enhancement), dynamic analysis (malware detection, fuzzing, penetration testing), and hybrid approaches (unit test generation). Identifies key challenges including token limitations, hallucinations, non-determinism, and path explosion. Notably covers LLM-assisted Extract Method refactoring (EM-Assist) and LLM integration with static analysis tools for bug warning inspection.

**Relevance:** MEDIUM

### Models & Tools
- **LLM/AI models:** GPT-3.5, GPT-4, CodeBERT, CodeLlama, StarCoder, and numerous domain-specific fine-tuned models surveyed
- **Tools:** LLift, DeGPT, EM-Assist, LLM4SA, E&V, CrashTracker, and others surveyed
- **Dataset:** N/A -- survey paper reviewing 160+ studies

### Challenges
LLMs face token limitations when analyzing large codebases; hallucinations generate fabricated information misleading vulnerability detection; non-deterministic outputs complicate repeatability; prompt engineering requires significant expertise; LLMs struggle with complex logic vulnerabilities involving intricate control flows and nested structures.

### Key Quotes
> "LLMs surpass traditional deep learning methods and have been applied to various tasks, including automated vulnerability and malware detection, code generation and repair, and providing scalable solutions that integrate static and dynamic analysis methods." (p. 1)

### Key Takeaway
The survey confirms that LLM integration with static analysis is an active and promising research direction -- the thesis's approach of using LLMs for architecture-level code transformation (tactic implementation) followed by static analysis evaluation aligns with the emerging pattern of LLM-static analysis hybrid workflows, though the architecture-level focus remains a novel contribution not covered by existing work.
