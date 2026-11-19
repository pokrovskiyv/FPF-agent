---
title: Route Chain
sources:
  - scripts/build_routes.py
  - sections/routes/route-1-project-alignment.md
last_updated: 2026-09-01T00:00:00Z
tags:
  - concept
  - retrieval
  - routes
---

# Route Chain

## Definition

A **route chain** is the ordered list of section files that the Retriever loads for a given burden. Each of the 10 routes in `sections/routes/` encodes one chain: first the core sections (marked `YES` in the Core column — typically 3 of them, loaded for simple queries), then supplementary sections loaded only when deeper context is needed.

Route chains are curated — written by hand rather than inferred — so they represent a known-good starting point for each burden.

## How it works in the system

Chains are defined as Python dicts at the top of [build_routes](../modules/build_routes.md):

```python
{
    "id": 1,
    "slug": "project-alignment",
    "user_says": "Teams don't understand each other...",
    "user_gets": "Map of who owns what...",
    "chain": ["A.1.1", "A.15", "A.15.2", "A.15.3", "B.5.1", "F.11", "F.9", "F.17"],
    "core": ["A.1.1", "A.15", "B.5.1"],
}
```

`build_routes.py` converts each dict into a `sections/routes/route-{id}-{slug}.md` file via `build_route_file()`. The generated file holds a table (`| # | Pattern | Title | File | Core? |`) that resolves each pattern ID to its title and file path from `sections/metadata.json`, marking the core subset with `YES`. A trailing **Loading Strategy** block states the minimum load (the core sections) and the full load (all sections in the chain).

For example, [Route 1: Project Alignment](../routes/route-1-project-alignment.md) resolves to:

- **Core (minimum load):** `A.1.1` (U.BoundedContext Semantic Frame), `A.15` (Role-Method-Work Alignment), `B.5.1` (Explore → Shape → Evidence → Operate).
- **Full chain (8 sections):** the three core sections plus `A.15.2` (U.WorkPlan), `A.15.3` (SlotFillingsPlanItem), `F.11` (Method Quartet Harmonisation), `F.9` (Alignment & Bridge across Contexts), and `F.17` (Unified Term Sheet).

At runtime, the Retriever (Mode A, Tier 1):
1. Reads the route file.
2. Loads the core sections first.
3. If the question needs more context, walks the full chain in order.
4. Stops when the budget is exhausted or the question is covered.

For cross-cutting queries (Tier 3), the Retriever also consumes the chain but supplements it with Mode B semantic results.

## Why ordered

The chain order is semantically meaningful: core patterns come first, general patterns before specific, boundary patterns before operational ones. Hierarchical pattern IDs (`A.6` before `A.6.B`) reinforce this — after deduplication the Retriever sorts final results by pattern ID, giving the Reasoner a natural general-to-specific reading flow.

## See also

- [fpf-retriever](../agents/fpf-retriever.md)
- [build_routes](../modules/build_routes.md)
- [burden](burden.md)
- [tier](tier.md)
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
- Route articles under `routes/`
