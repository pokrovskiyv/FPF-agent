---
title: Pipeline Depth
sources:
  - skills/fpf/SKILL.md
  - agents/fpf-classifier.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - concept
  - pipeline
  - adaptive-compute
---

# Pipeline Depth

## Definition

**Pipeline depth** is the number of agents engaged for a given query. Shorter depth = less compute, faster response. Longer depth adds the Reviewer for quality gating. The depth is chosen by the Classifier alongside the tier.

Minimum depth: Retriever → Reasoner. Full depth: Retriever → Reasoner → Reviewer.

## How it works in the system

The Classifier's strategy table (see [fpf-classifier](../agents/fpf-classifier.md)) maps each burden/tier combination to a depth and token budget:

| Tier | Burden examples | Pipeline | Budget |
|------|----------------|----------|--------|
| 1 | `term_lookup` | retriever → reasoner | ~800 tokens |
| 1 | `project_alignment`, `language_discovery` | retriever → reasoner | ~1200 tokens |
| 1 | `boundary_unpacking`, `generator_portfolio`, `ethical_assurance`, `trust_assurance` | retriever → reasoner | ~1500 tokens |
| 2 | `semantic` (any Tier 2) | retriever → reasoner → reviewer | ~2000 tokens |
| 3 | `cross_cutting` | retriever → reasoner → reviewer | ~2500 tokens |

The classifier emits the `PIPELINE` and `BUDGET` fields as part of its structured output; the skill dispatches agents accordingly.

## Why adaptive

Running the Reviewer on every query would roughly double compute for no benefit on simple lookups where the Reasoner's template discipline is enough. Running it on Tier 2/3 is essential because the retrieved sections are assembled dynamically and the Reasoner has more room to drift or hallucinate.

This mirrors a broader pattern in AI orchestration — "pay for compute only where it buys accuracy", familiar from speculative decoding and mixture-of-experts routing.

## See also

- [tier](tier.md)
- [agent-team](../architecture/agent-team.md)
- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-reviewer](../agents/fpf-reviewer.md)
