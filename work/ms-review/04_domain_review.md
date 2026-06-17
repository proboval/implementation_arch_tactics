# Domain Examiner Review (R2)

**Reviewer:** Software-architecture specialist (architectural tactics, modularity, technical debt)
**Target:** diploma/v3 — emphasis on Ch.2 (Lit Review), tactic catalog, the code-level vs. architecture-level gap
**Date:** 2026-06-17
**Mode:** post-draft
**Frame:** Innopolis MS defense (+ publishability)

---

## Summary judgment

As a contribution to the architecture community, the thesis's most valuable output is, paradoxically, a *negative* architectural result: current LLM agentic pipelines, given architectural tactic instructions, produce code-level file splitting and not architecture-level restructuring (package count unchanged 42/42; directory depth changed 2/42; Δfiles↔ΔMI ρ=0.74). That is a clean, well-evidenced finding the field should hear, and §5.6 develops it properly. The literature review is competent and current (Horikawa, Martinez, Esposito on the agentic scale-gap; Bass and Márquez for tactics). My concerns are about **conceptual precision** and one **interpretive over-attribution**: the thesis attributes the code-level ceiling to LLM capability, but the implementation harness is *designed* in a way that mechanically forbids architectural restructuring (R2-D2). That caveat must be foregrounded or the central architectural claim is partly circular.

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Lit review coverage | ✅ Present | Foundations (Garlan, Perry, Bass), tactics (Márquez, Bi, Bogner), LLM-refactoring scale gap (Horikawa, Martinez, Shokri). Current and well-synthesized. | — |
| S2 | Tactic catalog grounded | ✅ Present | §2.4/§3.7 grounded in Bass and Márquez; scope rationale (code-level only) is explicit and defensible. | — |
| S3 | Architecture-level evidence for an architecture claim | ⚠️ Partial | §5.6 uses fan-out/package/depth as proxies — good — but the promised coupling/cycle/tangle metrics (§3.10.4) are absent (see R1-T2). For a thesis about *architectural* tactics, the architecture-level measurement is the part the domain reviewer most wants and it is the part that is thinnest. | MUST |

## Persuasive effectiveness / domain soundness

| # | Issue | Status | Detail | Priority |
|---|-------|--------|--------|----------|
| **R2-D1** | Catalog (4 tactics) vs. usage (3) | ⚠️ Weak | §2.4/§3.7 define four tactics including **Deferred Binding Time**, but it never appears in any results table (§5.2.3, §5.5 show Decomposability, Localized Modification, Reduced Coupling, "Other/none"). If the LLM never selected it, say so and explain why (and consider dropping it from the catalog to match the implemented set). A defined-but-never-used tactic invites the question "was it reachable at all?" | SHOULD |
| **R2-D2** | Code-level ceiling is partly harness-designed, not purely LLM-limited | ❌ Open | The Patch Agent returns single whole-file replacements (App §A.3), is *rejected if it targets `__init__.py`*, is capped at 400 lines/file and 5 iterations, and operates one file per step. These constraints **structurally preclude** creating packages or reorganizing module boundaries. So "the pipeline operates at the code level, not the architecture level" (§5.6.6, §5.11.3) is partly a property of the harness, not solely an LLM capability gap. This must be stated explicitly in §5.6 and §5.11.3, otherwise the thesis's headline architectural conclusion is confounded by its own design. (It also opens a strong future-work direction: a planner allowed to create packages.) | MUST |
| **R2-D3** | "architecture-aware" vs. "architectural context" terminology | ⚠️ Weak | Ch.3 repeatedly says "architecture-aware workflow / tactic implementation" (§3 intro, §3.1) while Ch.5/6 retreat to "guided by architectural context." Pick one term and use it consistently; the conclusion's term is the defensible one. (Consistency checker also flags.) | SHOULD |
| **R2-D4** | Tactic↔transformation faithfulness | ⚠️ Weak | §5.6 honestly shows that "Decomposability" sometimes means genuine separation of concerns (Paper2Rebuttal) and sometimes mechanical splitting (webapp-color). Good. But the thesis stops at MI; a domain reviewer wants a brief qualitative judgment per improved repo of whether the *tactic intent* (cohesion along responsibility boundaries) was actually realized. You have the data (you describe both cases) — generalize it into a small "faithful vs. mechanical" tally across the 18 improved repos. | SHOULD |
| **R2-D5** | Taxonomy reduction justified but boundary under-theorized | ✅/⚠️ | Excluding microservice/event-driven because they need deployment-level evidence (§3.2) is sound. The modular-monolith/layered boundary is correctly identified as semantic (domain vs. technical packaging, §5.4.4). This is genuinely the field's hard problem and the thesis frames it well — consider citing it as a *contribution* (LLMs inherit the same ambiguity humans have), not only as an error source. | NICE |

## Standing critical issue coverage
- **CRIT-1** ⚠️ — the reframing is the right architectural call. Completing it requires R2-D2 (own the harness confound) and R1-T2 (deliver the architecture-level metrics).
- **CRIT-2/4** ❌ — from a domain view, the decisive baseline is "random file split with no architectural reasoning"; if it matches the LLM's ΔMI, the architectural framing adds nothing measurable. This is the experiment that would most strengthen the domain contribution.
- **CRIT-3** ❌ — the modular-monolith/layered κ matters *because* §5.4.4 shows that boundary is where both models and humans struggle.
- **CRIT-5** ✅.

## Defensibility vs. publishability
- **Defensible?** Yes — the negative architectural finding is real and well-argued. R2-D2 (own the harness confound) is the one MUST that affects the integrity of the central claim.
- **Publishable?** The architecture community would want R1-T2 (coupling/cycle/tangle deltas) and the random-split baseline before accepting "LLMs don't restructure architecture" as a general claim rather than a property of this harness.

## Decisions required
1. **R2-D2:** Add an explicit paragraph in §5.6/§5.11.3 stating that the harness (no `__init__.py` edits, single-file patches, ≤5 iterations) cannot create packages by construction, so the code-level result is jointly attributable to LLM behavior *and* harness design.
2. **R2-D1:** Confirm whether Deferred Binding Time was ever selected; report or drop it.
