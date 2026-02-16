## Understanding Software Architecture Erosion: A Systematic Mapping Study

| Field | Value |
|-------|-------|
| **Key** | `li2021understanding` |
| **Authors** | Ruiyin Li, Peng Liang, Mohamed Soliman, Paris Avgeriou |
| **Venue** | Journal of Software: Evolution and Process (2022), DOI: 10.1002/smr.2423 |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** Architecture erosion (AEr) adversely affects software development and has been described using various terms and definitions across the literature (software erosion, design decay, architecture degeneration, code decay, etc.), leading to ambiguous understanding. Despite significant attention over the last decade, there was no comprehensive overview consolidating definitions, symptoms, reasons, consequences, and countermeasures.
- **Gap:** No systematic mapping study dedicated exclusively to architecture erosion existed. The diverse and perplexing research landscape lacked a unified conceptual model linking AEr definitions, symptoms, reasons, consequences, detection approaches, and handling measures.

### Contribution
This paper presents the first systematic mapping study dedicated to architecture erosion (AEr), analyzing 73 primary studies (2006-2019) to consolidate the understanding of AEr definitions, symptoms, reasons, consequences, detection approaches, handling measures, difficulties, and lessons learned. The authors propose a refined definition of AEr from four complementary perspectives (violation, structure, quality, evolution), provide a conceptual model linking these aspects, and classify 13 categories of AEr reasons into technical, non-technical, and mixed factors. The study also catalogs detection approaches (consistency-based, evolution-based, metric-based, defect-based) and 35 tools used for AEr identification.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 3  | 5  |   4   |  1  |   3    | 16/25 |

**Relevance:** HIGH

### Method & Validation
- **Type:** Systematic Mapping Study (SMS)
- **Validation:** Rigorous protocol with 7 electronic databases, 22 supplementary venues, 3-round selection with inter-rater agreement (Cohen's Kappa 0.82-0.92), snowballing, constant comparison coding, replication package available

### Models & Tools
- **LLM/AI models:** N/A (systematic mapping study; no ML models used)
- **Tools:** 35 tools identified across the 73 primary studies for AEr detection; 57.1% based on Architecture Conformance Checking (ACC); notable tools include Axivion, Structure101, Lattix, SAVE, ArchJava, and Reflexion Modelling tools
- **Languages:** Tools primarily support Java; over 50% of identified tools support only one programming language

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Studies analyzed | 73 primary studies from 49 publication venues (2006-2019) |
| AEr definition perspectives | Four perspectives: violation (30 studies), structure (9), quality (6), evolution (3) |
| Refined AEr definition | "AEr happens when the implemented architecture violates the intended architecture with flawed internal structure or when architecture becomes resistant to change" |
| AEr symptom categories | Structural (code anomaly agglomeration, architectural smells), violation (design decision/constraint breaches), quality (high defect rate, declining productivity), evolution (rigidity, difficulty of change) |
| Top technical reasons | Architecture violation (24.7%), evolution issues (23.3%), technical debt (17.8%) |
| Top non-technical reason | Knowledge vaporization (15.1% of studies) |
| Consequences | 83.8% of consequence-mentioning studies report quality degradation; maintainability, evolvability, and extensibility most affected |
| Detection approaches | Consistency-based (62.5% of detection studies), evolution-based (22.5%), defect-based (15.0%) |
| Tool landscape | 35 tools identified; 57.1% based on Architecture Conformance Checking (ACC); >50% support only one programming language |
| Technical debt feedback loop | Technical debt is both a cause and consequence of AEr, forming a vicious cycle |
| Research-practice gap | Developers report no dedicated AEr tools, despite academic proposals (e.g., Axivion, Structure101, Lattix) |
| Lessons learned | 5 categories: tackling AEr (39.7%), manifestation (32.9%), detection (27.4%), understanding (24.7%), prevention (11.0%) |
| Future direction | Authors suggest leveraging machine learning to automatically detect AEr symptoms as a promising alternative to manual source code analysis |

### Dataset / Benchmark
73 primary studies selected from 7 electronic databases (ACM Digital Library, EI Compendex, IEEE Xplore, ISI Web of Science, Springer Link, Science Direct, Wiley InterScience) and 22 supplementary venues (9 journals, 10 conferences, 2 workshops, plus snowballing). Time period: January 2006 to May 2019. Full replication package available online with extracted data for all 16 data items across 73 studies.

### Challenges & Limitations
- Detection of AEr: Lack of dedicated techniques and tools specifically designed for AEr detection; most existing tools support only one programming language and one detection paradigm.
- Hard to establish mapping relations between source code and architectural elements due to lack of documentation and developer turnover.
- Handling of AEr: Even when erosion is detected, it is still challenging to handle -- keeping the implemented architecture aligned with the intended architecture is very hard during maintenance phases.
- Labor and time constraints make manual architecture consistency checking error-prone and impractical even for smaller systems.
- Technical debt forms a vicious cycle with AEr: it is both a cause and a consequence.
- 82.2% of studies are from academia, indicating a significant research-practice gap; developers report no dedicated AEr tools in practice despite academic proposals.
- The SMS search period starts from 2006, potentially missing some relevant earlier work.

### Key Quotes
> "Architecture erosion happens when the implemented architecture violates the intended architecture with flawed internal structure or when architecture becomes resistant to change." (Section 2.1, refined definition)

> "83.8% of consequence-mentioning studies report quality degradation; maintainability, evolvability, and extensibility most affected." (Section 4.5)

> "Technical debt is both a cause and consequence of AEr, forming a vicious cycle." (Section 5.1)

### Key Takeaway
Architecture erosion is the central degradation phenomenon that architectural tactics aim to prevent or reverse. This paper's taxonomy of 13 AEr reasons (especially architecture violation, technical debt, and knowledge vaporization) and four symptom categories provides a concrete framework for defining what "before" metrics should capture in the thesis evaluation pipeline. The finding that most detection tools are language-specific and consistency-focused, combined with the identified research-practice gap, directly motivates using LLM-based approaches to implement architectural tactics as an automated, language-aware alternative to existing AEr remediation tools.
