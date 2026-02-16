## Exploring ChatGPT's Code Refactoring Capabilities: An Empirical Study

| Field | Value |
|-------|-------|
| **Key** | `depalma2024exploring` |
| **Authors** | Kayla DePalma, Izabel Miminoshvili, Chiara Henselder, Kate Moss, Eman Abdullah AlOmar |
| **Venue** | Expert Systems with Applications (2024) |
| **Tier** | Q1 |
| **Citations** | 43 |
| **DOI** | 10.1016/j.eswa.2024.123602 |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** ChatGPT has shown potential in software engineering tasks including code generation, but its ability to interpret and refactor code has been deemed unreliable and faulty, and its specific capabilities for code refactoring targeting different quality attributes are unknown.
- **Motivation:** Refactoring is a critical software maintenance activity constituting up to 75% of total development efforts. While prior studies explored ChatGPT's code syntax understanding and summarization abilities, no study had systematically evaluated its code refactoring capabilities across multiple quality attributes with static analysis validation.
- **Gap:** No prior empirical study had assessed ChatGPT's effectiveness in refactoring code across specific quality attributes (performance, complexity, coupling, cohesion, design size, readability, reusability, understandability), its ability to preserve behavior after refactoring, or its accuracy in generating refactoring documentation.

### Contribution

This paper empirically evaluates ChatGPT (GPT-3.5) on three dimensions of code refactoring: (1) effectiveness in performing refactoring across eight quality attributes (performance, complexity, coupling, cohesion, design size, readability, reusability, understandability), (2) preservation of code behavior after refactoring, and (3) ability to generate accurate documentation (commit messages describing goals, refactoring changes, and quality impacts). The study uses 40 Java code segments refactored across 8 quality attributes (320 total trials), validated with PMD static analysis and a 15-participant user survey. It provides one of the first systematic evaluations of LLM-driven refactoring with quality-attribute-specific prompts.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 1  |   4   |  5  |   3    | 14/25 |

**Relevance:** HIGH

This paper directly informs the thesis on LLM capabilities and limitations for code refactoring targeting specific quality attributes. Its findings on behavior preservation (97.2% success), prompt sensitivity to quality attribute keywords, and the gap between requested quality attributes and ChatGPT's actual improvements (defaulting to readability/maintainability) are critical for designing the thesis pipeline's LLM-based tactic implementation stage. The PMD-based validation approach also provides a methodological template for the thesis's static analysis evaluation.

### Method & Validation
- **Type:** Experiment
- **Validation:** Static analysis (PMD) + User survey (15 CS students) + Qualitative analysis
- **Evidence:** 320 refactoring trials (40 Java files x 8 quality attributes); PMD violation analysis across 8 categories (Best Practices, Code Style, Design, Documentation, Error Prone, Performance, Multithreading, Security); behavior preservation testing via ChatGPT self-evaluation; commit message accuracy analysis; user survey with 5 randomly selected code segments rated on 0-7 agreement scale.

### Models & Tools
- **LLM/AI models:** ChatGPT 3.5 (GPT-3.5)
- **Tools/frameworks:** PMD (Programming Mistake Detector) for static analysis with 8 violation categories (Best Practices, Code Style, Design, Documentation, Error Prone, Performance, Multithreading, Security); user survey (15 CS students, 0-7 agreement scale)
- **Languages:** Java (40 code segments, 20-50 LOC each, single class with 1-2 methods)

### Key Findings

| Finding | Value/Detail |
|---------|-------------|
| Refactoring success rate | 319/320 (99.7%) -- ChatGPT failed to refactor only 1 code segment |
| Behavior preservation rate | 311/320 (97.2%) -- behavior preserved in vast majority of cases |
| Documentation accuracy (goals) | 316/320 (98.8%) -- accurate goal identification |
| Documentation accuracy (changes) | 315/320 (98.4%) -- accurate refactoring change identification |
| Documentation accuracy (impact) | 319/320 (99.7%) -- accurate impact description |
| Most common refactoring type | Variable/method renaming to follow Java conventions, code reformatting |
| Most common PMD violation category | Code Style (55-65% of all violations across attributes) |
| Quality attribute recognition gap | ChatGPT predominantly identifies readability and maintainability as improved, regardless of which attribute was requested (e.g., coupling and cohesion improvement was never recognized) |
| Prompt keyword sensitivity | Including specific quality attribute keywords (e.g., "quality and performance") triggers more significant refactoring than generic "quality" alone |
| Most effective attributes for prompting | Performance and reusability prompted the most specific/unique changes |
| Behavior failure causes | Wrong variable calls (6/9), incorrect loop parameters (2/9), data type conversion errors (1/9) |
| PMD total violations range | 500 (reusability, lowest) to 552 (readability, highest) across quality attributes |
| User survey agreement | 85.8% of participants rated ChatGPT's refactoring at 5 or 6 (out of 7); 92.9% said additional refactoring still needed |
| Compiler errors | Coupling had the most (15), cohesion had zero |

### Key Quotes

> "ChatGPT offered improved versions of the provided code segments 39 out of 40 times even if it is as simple as suggesting clearer names for variables or better formatting." (Abstract)

> "ChatGPT will do major refactoring if we enforce some quality attribute keywords." (Section 2.1.1)

> "The two primary attributes ChatGPT reported were readability and maintainability which suggests that ChatGPT has a limited ability to refactor code segments to improve more sophisticated quality attributes like cohesion and coupling because ChatGPT was not able to recognize their improvement in the refactored code." (Section 4.7)

> "ChatGPT's strengths and accuracy were in suggesting minor changes because it had difficulty addressing and understanding complex errors and operations." (Abstract)

> "ChatGPT should be used as an aid to programmers since we cannot completely depend on it yet." (Abstract)

> "Our observation indicates that ChatGPT offers generic refactoring operations but does not provide specific refactoring operations as defined by Fowler." (Section 3.3)

### Challenges & Limitations

1. **Small and simple dataset**: Only 40 Java files with 20-50 lines each, containing single classes with 1-2 methods. The simplicity limited the range of refactoring ChatGPT could perform, often resulting in only variable renaming and reformatting.

2. **ChatGPT unpredictability/non-determinism**: The same prompt yields different results across runs, making it difficult to fully assess capabilities. Context from previous chat messages also influences subsequent responses, requiring new chat sessions for each trial.

3. **Limited broader context understanding**: ChatGPT cannot grasp the architectural context in which code segments are used, leading to suggestions based on misunderstandings or false assumptions.

4. **Training data dependency**: ChatGPT's effectiveness is tied to training data quality. Limited diversity in training data restricts its ability to suggest complex refactoring techniques.

5. **Quality attribute confusion**: ChatGPT could not distinguish between the specific quality attribute it was asked to improve and defaulted to readability/maintainability improvements. It failed to recognize improvements for coupling, cohesion, and design size entirely.

6. **Self-evaluation bias**: Behavior preservation was evaluated by ChatGPT itself rather than through test execution or formal verification, introducing potential bias.

7. **Single LLM version**: Only ChatGPT 3.5 was tested; newer models (GPT-4, etc.) may perform differently.

### Dataset / Benchmark
- **Name:** Java refactoring dataset from Ma et al. (2023) "The Scope of ChatGPT in Software Engineering"
- **Size:** 40 Java files (20-50 LOC each, single class, 1-2 methods); 320 refactored code segments (40 files x 8 quality attributes)
- **Domain:** General-purpose Java code segments covering performance, complexity, coupling, cohesion, design size, readability, reusability, understandability
- **Availability:** Replication package at https://sites.google.com/stevens.edu/chatgptdataanalysis/home

### Key Takeaway

When using LLMs to implement architectural tactics targeting specific quality attributes, explicit quality attribute keywords in prompts are essential to steer the LLM beyond generic readability/naming improvements. However, even with specific prompting, ChatGPT (3.5) defaults to superficial refactoring (renaming, formatting) and struggles with complex architectural quality attributes like coupling and cohesion -- precisely the attributes most relevant to architectural tactics. The thesis pipeline must therefore: (a) use more advanced models or multi-step prompting strategies, (b) combine LLM output with static analysis validation (as this paper does with PMD), and (c) not rely on the LLM's self-assessment of which quality attributes it improved.

### Snowball References

**Backward:**
- `aldallal2017empirical` -- Empirical evaluation of impact of OO code refactoring on quality attributes (SLR)
- `alomar2021preserving` -- On preserving the behavior in software refactoring: systematic mapping study
- `fowler2018refactoring` -- Refactoring (2nd edition, foundational catalog of 72 refactoring types)
- `ma2023scope` -- The scope of ChatGPT in software engineering (source of the 40 Java file dataset)
- `tian2023chatgpt` -- Is ChatGPT the ultimate programming assistant? (LLM capabilities/limitations)
- `xia2023keep` -- Conversation-driven program repair using ChatGPT (iterative LLM prompting)
- `alomar2023pmd` -- On the use of static analysis (PMD) to engage students with software quality improvement
- `romano2022static` -- Do static analysis tools affect software quality when using TDD?

**Forward:** Check Google Scholar for papers citing this (43 citations as of Feb 2026) -- particularly look for studies using GPT-4/Claude for refactoring, and studies addressing the quality attribute recognition gap identified here.
