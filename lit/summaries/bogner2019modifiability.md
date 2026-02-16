## Using Architectural Modifiability Tactics to Examine Evolution Qualities of Service- and Microservice-Based Systems

| Field | Value |
|-------|-------|
| **Key** | `bogner2019modifiability` |
| **Authors** | Justus Bogner, Stefan Wagner, Alfred Zimmermann |
| **Venue** | SICS Software-Intensive Cyber-Physical Systems (Springer), 2019 |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** Service- and Microservice-Based Systems allegedly provide a high degree of evolvability, but many software professionals lack systematic understanding of the reasons and preconditions for this. A blind belief in the inherent modifiability of service-based systems without clear understanding of the influencing factors can lead to violations of important principles.
- **Gap:** Existing work on architectural tactics in service-oriented systems either stays on a very high level, requires intensive preparation and modeling, or focuses on availability rather than modifiability. No systematic mapping of modifiability tactics to both SOA and Microservices principles and patterns existed, and no data was shared publicly.

### Contribution
This paper systematically maps 15 architectural modifiability tactics (organized in three categories: Increase Cohesion, Reduce Coupling, Defer Binding Time) onto principles and design patterns of both SOA and Microservice-Based Systems. The qualitative mapping produces a matrix relating general modifiability guidelines to concrete service-oriented patterns, enabling practitioners to understand which service-oriented patterns realize which modifiability tactics. The work also provides a comparative analysis of how SOA and Microservices achieve evolvability through different strategies (governance and standardization vs. evolutionary design and infrastructure automation).

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 5  | 4  |   4   |  0  |   0    | 13/25 |

**Relevance:** HIGH

### Method & Validation
- **Type:** Framework / Qualitative Mapping
- **Validation:** Expert judgment (author-driven qualitative mapping); publicly shared dataset on GitHub (xjreb/research-modifiability-tactics)

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** N/A (qualitative mapping study; publicly shared dataset on GitHub at xjreb/research-modifiability-tactics)
- **Languages:** N/A (architecture-level analysis, technology-agnostic; patterns drawn from SOA and Microservices catalogs)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Modifiability tactic taxonomy | 15 tactics in 3 categories: Increase Cohesion (5), Reduce Coupling (4), Defer Binding Time (6), compiled from Bass et al. (2003, 2012) and Bachmann et al. (2007) |
| SOA principle-to-tactic mappings | 26 out of 120 possible mappings (8 principles x 15 tactics); "Service Loose Coupling" had most mappings (7) |
| Microservices principle-to-tactic mappings | 15 out of 120 possible; "Evolutionary Design" had most mappings (5) |
| Dominant tactic category (both styles) | "Reduce Coupling" had most principle mappings for both SOA (16) and Microservices (7) |
| SOA pattern coverage | 47 of 118 SOA patterns (~40%) mapped to modifiability tactics; "Reduce Coupling" dominant with 23 patterns (~49%) |
| Microservices pattern coverage | 21 of 42 Microservices patterns (50%) mapped; "Defer Binding Time" dominant with 11 patterns (~52%) |
| SOA vs. Microservices strategy difference | SOA achieves modifiability through governance, standardization, intermediaries, and interface preservation; Microservices through evolutionary design, infrastructure automation, and runtime discovery |
| Tactic with most SOA pattern matches | "Use an Intermediary" (9 patterns: Service Facade, Proxy Capability, Service Broker, etc.) |
| Tactic with most Microservices pattern matches | "Runtime Registration and Dynamic Lookup" (5 patterns: Self Registration, Client-side Discovery, Server-side Discovery, etc.) |
| Only tactic with zero pattern mappings in both styles | "Compile Time Binding" -- no service-oriented pattern in either SOA or Microservices catalogs |
| Cohesion gap in Microservices | Only 3 of 21 mapped Microservices patterns are in "Increase Cohesion," despite small cohesive services being a key Microservices philosophy |

### Dataset / Benchmark
Qualitative mapping dataset combining: 15 modifiability tactics from Bass et al. (2003, 2012) and Bachmann et al. (2007); 8 SOA principles from Erl; 8 Microservices principles from Lewis and Fowler; 118 SOA patterns from Erl and Rotem-Gal-Oz; 42 Microservices patterns from Richardson's catalog. Complete mapping data publicly available on GitHub (xjreb/research-modifiability-tactics).

### Challenges & Limitations
- The qualitative nature of the approach ties results to the personal experience and judgment of the authors, introducing potential subjective bias and limiting reproducibility.
- Microservices are much younger than SOA and therefore cannot provide as established a foundation of principles and patterns, potentially adding an uneven and temporary connotation to the comparison.
- Several principles and patterns are applicable in both architectural styles or exist under different names, making clean separation difficult.
- Results scrutinize "theoretical" modifiability; in practice, software developers can create systems of arbitrary evolvability in both styles.
- The practical value depends on how well results can be transferred to design and implementation activities, which the authors identify as the main difficulty.
- The strength of each mapping was not quantified; a weak and strong mapping count the same.

### Key Quotes
> "An architectural modifiability tactic therefore is a design decision or an architectural transformation that positively affects system properties related to modifiability with the final goal of reducing the time and effort necessary to introduce future changes." (Section 2.1)

> "A blind belief in the inherent modifiability of a Service-Based System -- without having a clear understanding of the factors that influence this quality attribute -- can lead to violations of important principles and therefore negatively impact software evolution." (Section 1)

### Key Takeaway
The compiled list of 15 modifiability tactics across three categories (Increase Cohesion, Reduce Coupling, Defer Binding Time) and their concrete mappings to service-oriented patterns provides a directly reusable tactic catalog for the thesis. The finding that specific patterns realize specific tactics gives the LLM pipeline actionable targets: when implementing a modifiability tactic like "Use an Intermediary" or "Split Module," the pipeline can reference the corresponding service-oriented patterns as implementation blueprints. The identified gap in cohesion patterns for Microservices also highlights an area where LLM-driven tactic implementation could add particular value.
