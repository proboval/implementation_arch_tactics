## Software Architecture in Practice (4th ed.)

| Field | Value |
|-------|-------|
| **Key** | `bass2021software` |
| **Authors** | Len Bass, Paul Clements, Rick Kazman |
| **Venue** | Addison-Wesley (2021) |
| **Level** | L1-Foundational |

### Motivation & Gap
The definitive textbook defining architectural tactics as design primitives for achieving quality attributes. Establishes the canonical taxonomy used by nearly all subsequent tactics research.

### Contribution
Defines architectural tactics as fine-grained "building blocks" focusing on a single quality attribute response. Provides complete taxonomies for 7 quality attributes, formal distinction between tactics and patterns, and validation methods (ATAM, checklists, prototypes).

**Relevance:** CRITICAL (Reference)

### Modifiability Tactics (Complete Catalog)

**Increase Cohesion (localize changes):**
| Tactic | Description |
|--------|-------------|
| Increase Semantic Coherence | Ensure module responsibilities are related and unified |
| Anticipate Expected Changes | Organize so likely changes affect limited modules |
| Split Module | Break module with multiple responsibilities into smaller pieces |
| Generalize Module | Make module generic via parameters/broad interfaces |
| Abstract Common Functionality | Move common logic to shared entity to avoid duplication |

**Reduce Coupling (prevent ripple effects):**
| Tactic | Description |
|--------|-------------|
| Use Encapsulation | Hide implementation behind stable interface |
| Maintain Existing Interface | Use versioning/adapters for interface evolution |
| Restrict Dependencies | Limit which modules communicate |
| Use an Intermediary | Introduce indirection (broker, facade) to decouple |

**Defer Binding Time (increase flexibility):**
| Tactic | Description |
|--------|-------------|
| Runtime Registration & Dynamic Lookup | Services discover/connect at runtime |
| Runtime Binding | Late binding/reflection for behavior change |
| Publish-Subscribe | Decouple producers/consumers via events |
| Start-Up Time Binding | Configuration files at system start |
| Deployment Time Binding | Binding at installation (e.g., DB driver) |
| Compile Time Binding | Traditional build-time binding |

### Quality Attribute Tactics Taxonomy (7 Categories)
1. **Availability** — Detect Faults, Recover from Faults, Prevent Faults
2. **Interoperability** — Locate Services, Manage Interfaces
3. **Modifiability** — Increase Cohesion, Reduce Coupling, Defer Binding
4. **Performance** — Control Resource Demand, Manage Resources
5. **Security** — Resist Attacks, Detect Attacks, Recover from Attacks
6. **Testability** — Observe and Control System State
7. **Usability** — User Initiative, System Initiative, Runtime Frameworks

### Tactics vs Patterns
- **Tactics:** Fine-grained building blocks, single quality attribute, no tradeoff consideration
- **Patterns:** Coarse-grained packages of tactics, multiple QAs, tradeoffs built in

### Validation Approaches
1. Quality Attribute Checklists (Ch. 14, p. 260)
2. Thought Experiments / Back-of-Envelope Analysis (Ch. 14, p. 262)
3. Experiments, Simulations, Prototypes (Ch. 14, p. 264)
4. ATAM — Architecture Tradeoff Analysis Method (Ch. 21, p. 400)
5. Lightweight Architecture Evaluation (Ch. 21, p. 415)

### Key Takeaway
The 15 modifiability tactics (5 cohesion + 4 coupling + 6 binding) form the direct input catalog for the thesis LLM pipeline. Each tactic has a clear description that can be translated into LLM prompts.
