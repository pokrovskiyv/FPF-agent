---
title: Tier
sources:
  - skills/fpf/SKILL.md
  - agents/fpf-classifier.md
  - agents/fpf-retriever.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - concept
  - retrieval
---

# Tier

## Definition

A **tier** is the Retriever's loading strategy for a given query. Three tiers are defined: Tier 1 (route-based), Tier 2 (semantic fallback), Tier 3 (combined). The Classifier picks the tier based on how well the user's message matches known burdens; the Retriever executes the chosen strategy.

Tiers exist to balance retrieval quality against compute: Tier 1 is cheapest and most precise, Tier 2 is broader but pays for a model inference, Tier 3 uses both.

## How it works in the system

| Tier | Trigger | Loads | Budget |
|------|---------|-------|--------|
| **Tier 1** | Strong burden match OR explicit pattern ID | Curated route chain OR single section | 800–1500 tokens |
| **Tier 2** | FPF signal, no burden match (or weak match) | Dynamic chain from keyword + FAISS search | ~2000 tokens (incl. Reviewer) |
| **Tier 3** | Multiple burdens match (cross-cutting) | Primary route core + semantic supplement | ~2500 tokens (incl. Reviewer) |

The tier choice also controls pipeline depth — see [pipeline-depth](pipeline-depth.md). Tier 1 simple lookups skip the Reviewer; Tier 2 and Tier 3 always add it.

In the Classifier's output format, the `TIER` field is the selected value (1, 2, or 3), and the `PIPELINE` field captures whether the Reviewer runs.

## Note on terminology

The `three-tier` language in this project is about **retrieval strategy**, not ladder of capability. A Tier 2 query isn't "better" than Tier 1 — it's handled differently because no curated route matches. If the semantic search later calibrates well enough that a new burden deserves its own route, that query graduates from Tier 2 to Tier 1 by route creation, not by metric improvement.

## See also

- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
- [pipeline-depth](pipeline-depth.md)
- [burden](burden.md)
- [route-chain](route-chain.md)
- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
