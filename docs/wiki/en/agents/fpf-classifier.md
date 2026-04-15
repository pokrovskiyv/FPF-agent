---
title: fpf-classifier
sources:
  - agents/fpf-classifier.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - agent
  - classifier
  - entry-point
---

# fpf-classifier

> Source: `agents/fpf-classifier.md`

## Purpose

First agent in the pipeline. Takes the user's raw message and decides five things: is there a signal worth structuring at all, which tier to use (route / semantic / combined), which specific burden it matches, how much compute to spend, and what search query to hand downstream. Its output is a structured routing decision — the Retriever and Reasoner never see the raw message, only the Classifier's verdict.

The Classifier is intentionally conservative: if the signal is weak, it returns `SIGNAL: no` and the pipeline stops. This guards against false positives on ordinary coding questions.

## Interface

**Input:** user's natural-language message.

**Output:**

```
SIGNAL: [yes/no]
TIER: [1/2/3]
BURDEN: [burden_type]
CONFIDENCE: [HIGH/LOW/BYPASS]
ROUTE: [route file path | "metadata.json" | null]
PIPELINE: [retriever→reasoner | retriever→reasoner→reviewer]
BUDGET: [token budget]
SECTIONS: [list of section files to preload]
SEARCH_QUERY: [natural language query for Tier 2/3 semantic search]
```

## Classification logic

Three stages:

1. **Signal detection** — scan for any coordination, systems engineering, or transdisciplinary cue. Broader than direct burden matching: catches "help me structure this", "this is a mess", "what am I missing?" The classifier also rejects signals: pure coding tasks, library/syntax questions, file ops.
2. **Route matching** — match the user's words against a burden-trigger table with 10 known burdens (`project_alignment`, `language_discovery`, `boundary_unpacking`, `comparison_selection`, `generator_portfolio`, `rewrite_explanation`, `ethical_assurance`, `trust_assurance`, `composition_aggregation`, `evolution_learning`) plus a `term_lookup` special case.
3. **Tier assignment** — one strong match → Tier 1 (auto-dispatch). Multiple matches → Tier 3 (combined). Signal but no match → Tier 2 (semantic fallback). Explicit pattern ID (A.6, UTS, DRR) → bypass confidence and auto-dispatch Tier 1 `term_lookup`.

The strategy table in the source maps each burden to a concrete route file, pipeline depth, and token budget.

## Position in the pipeline

```
USER → [fpf-classifier] → retriever → reasoner → (reviewer) → output
```

All downstream agents depend on the Classifier's decision. If it says `SIGNAL: no`, the pipeline stops immediately.

## See also

- [fpf-retriever](fpf-retriever.md) — receives the routing decision
- [fpf-reasoner](fpf-reasoner.md) — receives retrieved sections plus the original question
- [agent-team](../architecture/agent-team.md)
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
- [burden](../concepts/burden.md)
- [tier](../concepts/tier.md)
