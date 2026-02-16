## Does ChatGPT Help Novice Programmers Write Better Code? Results From Static Code Analysis

| Field | Value |
|-------|-------|
| **Key** | `haindl2024chatgpt` |
| **Authors** | Haindl and Weinberger |
| **Venue** | IEEE Access (2024) |
| **Level** | L3-Thesis-Specific |

### Motivation & Gap
There is growing interest in using LLMs in programming education, but limited empirical evidence on whether ChatGPT actually improves measurable code quality metrics (beyond correctness) such as adherence to coding conventions and code complexity.

### Contribution
A controlled study comparing code quality of 16 students (without ChatGPT) vs. 22 students (with ChatGPT) in an introductory Java course, measured via static code analysis (Checkstyle, SonarQube). The ChatGPT-assisted group had significantly fewer coding convention violations and lower cyclomatic and cognitive complexity (p < 0.005).

**Relevance:** MEDIUM

### Models & Tools
- **LLM/AI models:** ChatGPT (GPT-3.5 and GPT-4, free version)
- **Tools:** Checkstyle (rule violations), SonarQube (cognitive complexity), PMD
- **Dataset:** 38 students total (16 control, 22 treatment), introductory Java course, identical exercises

### Challenges
Small sample size (38 students) limits generalizability; participants were novices (no prior Java experience), so results may not transfer to experienced developers or architecture-level code; static analysis captures coding conventions and complexity but does not assess architectural quality.

### Key Quotes
> "The treatment group demonstrated greater adherence to rules LineLength, FinalParameters, HiddenField, MissingSwitchDefault, DesignForExtension, MagicNumber, VisibilityModifier, RightCurly, NeedBraces, LocalVariableName across all programming exercises with statistical significance." (p. 114150)

### Key Takeaway
ChatGPT demonstrably reduces cyclomatic and cognitive complexity at the code level -- the thesis can reference this as evidence that LLMs can improve low-level maintainability metrics, while arguing that the thesis extends this to architecture-level tactics where the impact on maintainability is expected to be even more significant.
