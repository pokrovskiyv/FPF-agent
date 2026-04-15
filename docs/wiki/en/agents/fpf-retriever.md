---
title: fpf-retriever
sources:
  - agents/fpf-retriever.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - agent
  - retriever
  - retrieval
---

# fpf-retriever

> Source: `agents/fpf-retriever.md`

## Purpose

Second agent. Given the Classifier's routing decision, loads the minimum set of sections needed to answer the user's question. Operates in two modes:

- **Mode A (Tier 1 route-based):** loads a curated chain from a `sections/routes/route-*.md` file. Cheapest and highest quality.
- **Mode B (Tier 2 semantic / Tier 3 combined):** runs keyword search over `metadata.json` plus FAISS semantic search via [semantic_search](../modules/semantic_search.md), merges results, deduplicates by pattern ID.

## Interface

**Input:** Classifier output (TIER, BURDEN, ROUTE, SEARCH_QUERY, BUDGET, SECTIONS).

**Output:** concatenated section content with source citations:

```
SECTIONS_LOADED: [count]
TOTAL_LINES: [approximate]

--- Section: [pattern_id] ([file_path]) ---
[section content]

--- Section: [pattern_id] ([file_path]) ---
[section content]
```

## Retrieval strategies

Mode A (Tier 1) walks three sub-tiers in order, stopping when it has enough:

1. **Direct pattern ID lookup** — when the user mentions a specific ID (A.6, E.17), read `metadata.json` and load that single file.
2. **Route chain loading** — read the route file, load core sections first (marked `YES` in the Core column), then remaining chain sections in order until the question is covered.
3. **Cross-reference expansion** — if coverage is incomplete, follow `builds_on`/`prerequisite_for`/`coordinates_with` dependencies via `_xref.md` files into other Parts.

Mode B (Tier 2/3) is a 5-step dynamic pipeline:

1. Keyword search `metadata.json` `keywords` and `queries` fields, collect top 10.
2. Run `uv run scripts/semantic_search.py "<SEARCH_QUERY>" --top-k 5 --json`, keep score ≥ 0.45.
3. Merge keyword and semantic results, dedupe by pattern ID, cap at 5 sections.
4. For the top 3, consult their directory's `_xref.md` and add up to 2 cross-referenced sections.
5. Sort final list by pattern ID (hierarchical IDs give natural general-to-specific ordering).

Tier 3 combines both modes: load route core first, then supplement with Mode B steps 1–5 for the `SEARCH_QUERY`.

## Stagnation detection

If the retriever notices it's loading the same sections repeatedly or circling, it escalates to Tier 3 (cross-refs), then if still stuck reports back to the user: "This question spans multiple areas. Let me broaden the search." It may also load `glossary-quick.md` as orientation aid.

## Position in the pipeline

```
classifier → [fpf-retriever] → reasoner
```

The retriever passes full section content to the reasoner — it never summarizes. Respects the budget from the Classifier's strategy table (800–2500 tokens depending on tier).

## See also

- [fpf-classifier](fpf-classifier.md) — produces the routing decision
- [fpf-reasoner](fpf-reasoner.md) — consumes the loaded sections
- [semantic_search](../modules/semantic_search.md) — backend for Mode B
- [build_xrefs](../modules/build_xrefs.md) — produces `_xref.md` files used for stagnation recovery
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
- [route-chain](../concepts/route-chain.md)
