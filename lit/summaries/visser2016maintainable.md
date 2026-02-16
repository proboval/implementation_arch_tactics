## Building Maintainable Software (Java Edition)

| Field | Value |
|-------|-------|
| **Key** | `visser2016maintainable` |
| **Authors** | Joost Visser (SIG) |
| **Venue** | O'Reilly (2016) |
| **Level** | L1-Foundational |

### Motivation & Gap
Provides a practitioner-oriented framework mapping 10 code guidelines to measurable metrics, benchmarked against hundreds of real systems. Bridges the gap between abstract quality models (ISO 25010) and actionable coding practices.

### Contribution
Defines 10 guidelines for maintainability, each mapped to specific metrics and SIG benchmark thresholds. Creates a measurement-driven approach to maintainability with star ratings (1-5) based on empirical benchmarks.

**Relevance:** HIGH (Reference — from NLM)

### 10 Guidelines with Metrics

| # | Guideline | Metric | Threshold |
|---|-----------|--------|-----------|
| 1 | Write Short Units of Code | Unit Length (LOC) | <= 15 lines |
| 2 | Write Simple Units of Code | McCabe Cyclomatic Complexity | <= 5 |
| 3 | Write Code Once | Code Duplication % | Low % |
| 4 | Keep Unit Interfaces Small | Parameters per unit | <= 4 |
| 5 | Separate Concerns in Modules | Module Coupling (fan-in) | Low coupling |
| 6 | Couple Architecture Components Loosely | Component Independence (hidden code %) | High % hidden |
| 7 | Keep Architecture Components Balanced | Component count (6-12) + Gini coefficient | Balanced |
| 8 | Keep Codebase Small | Total LOC / rebuild value | Minimize |
| 9 | Automate Tests | Test coverage | >= 80% |
| 10 | Write Clean Code | Code smells count | Minimize |

### SIG Assessment Model
- **Quality Profiles:** Code divided into 4 risk categories (low/moderate/high/very high)
- **Star Ratings:** 1-5 stars based on benchmark of hundreds of real systems (top 5% = 5 stars)
- **ISO 25010 Alignment:** Aggregated into Analyzability, Modifiability, Testability, Modularity, Reusability
- **Recalibration:** Benchmark thresholds updated yearly
- **Predictive Power:** Issue resolution 2x faster in 4-star vs 2-star systems

### Mapping to Bass Modifiability Tactics

| Visser Guidelines | Bass Tactic Group |
|-------------------|-------------------|
| Short Units, Simple Units, Separate Concerns | **Increase Cohesion** |
| Loose Coupling (module + architecture) | **Reduce Coupling** (Restrict Dependencies, Encapsulation) |
| Write Code Once, Small Interfaces | **Abstract Common Functionality** |
| Boy Scout Rule (incremental cleanup) | Evolutionary architecture maintenance |

### Key Insight
Unit-level guidelines take precedence over architecture-level guidelines — architecture properties are aggregated effects of unit-level decisions.

### Key Takeaway
The SIG metric thresholds provide concrete, benchmarked targets for evaluating LLM-generated tactic implementations. The 10 guidelines map directly to modifiability tactics, creating a bridge between what the LLM implements (tactics) and how we measure success (metrics).
