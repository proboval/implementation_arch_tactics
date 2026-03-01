# Can LLMs Implement Architectural Tactics? Early Results

Software maintainability is a critical quality attribute that directly affects system evolution cost and reliability. Improving maintainability often requires architectural-level modifications demanding specialized expertise and significant manual effort. While Large Language Models (LLMs) have shown strong capabilities in code understanding and generation, their potential for systematic architecture-level software quality improvement remains largely unexplored.

This paper presents an automated pipeline that leverages an LLM to improve software maintainability through architectural tactic implementation. The pipeline operates in three stages: (1) architecture detection, where the LLM analyzes repository structure and identifies the dominant architectural pattern; (2) architectural tactic selection, where the LLM chooses an appropriate tactic from a predefined catalog based on the detected architecture and expected maintainability impact; and (3) tactic implementation using a Test-Driven Development approach to ensure correctness. The pipeline follows a Pipes and Filters architecture and operates without manual intervention.

We applied the pipeline to 158 open-source Python backend repositories collected and filtered from GitHub. Preliminary results show that the LLM successfully detected architectural patterns (e.g., modular monolith, layered, script-based) in 106 repositories and selected contextually appropriate tactics for 77 repositories, with Reduced Coupling being the most frequently chosen tactic. Baseline maintainability was measured using the Radon static analysis tool, with the Maintainability Index as the primary metric.

This work contributes a reproducible methodology for LLM-driven architectural improvement and provides early empirical evidence on the feasibility of using LLMs for architecture-level analysis and tactic reasoning.

**Keywords:** software maintainability, architectural tactics, large language models, automated software improvement, static analysis, software architecture
