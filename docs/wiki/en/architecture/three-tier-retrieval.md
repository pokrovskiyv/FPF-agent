---
title: Three-Tier Retrieval
sources:
  - skills/fpf/SKILL.md
  - agents/fpf-classifier.md
  - agents/fpf-retriever.md
  - scripts/build_routes.py
  - scripts/build_embeddings.py
  - scripts/semantic_search.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - retrieval
  - tier
---

# Three-Tier Retrieval

## Components

Retrieval is layered across three tiers that trade accuracy and compute. The Classifier picks the tier; the Retriever executes it.

| Tier | When it fires | What it loads | Typical budget |
|------|---------------|---------------|----------------|
| **Tier 1 — Route / term lookup** | Burden matches one of 10 routes, or user mentions a pattern ID | A curated section chain (route) or a single section (term lookup) | 800–1500 tokens |
| **Tier 2 — Semantic fallback** | Signal present, no route matches | Dynamic chain assembled from keyword search + FAISS semantic search | 2000 tokens (incl. Reviewer) |
| **Tier 3 — Combined** | Multiple routes match (cross-cutting) | Primary route core + semantic supplement | 2500 tokens (incl. Reviewer) |

## Data Flow

```
Classifier decision
     │
     ├──► Tier 1 ─► Retriever Mode A
     │              (read routes/route-N.md  → load core YES sections first,
     │               then remaining chain if needed; fall back to _xref.md
     │               for cross-part expansion if stagnation detected)
     │
     ├──► Tier 2 ─► Retriever Mode B
     │              (keyword search metadata.json  +
     │               uv run scripts/semantic_search.py "<SEARCH_QUERY>" --top-k 5 --json
     │               merge, dedupe by pattern ID, keep score ≥ 0.45,
     │               sort by pattern ID hierarchy)
     │
     └──► Tier 3 ─► Mode A core + Mode B supplement
                    (load route core sections, then Mode B steps 1–5
                     on SEARCH_QUERY, dedupe against already-loaded)
```

## Decisions

- **Routes as cache, semantic as foundation.** Routes give deterministic high-quality retrieval for known burdens; semantic search covers everything else. The ten routes were hand-picked from observed usage and represent a heuristic cache over the 242-pattern spec.
- **Cosine similarity via normalized IP.** `build_embeddings` normalizes vectors and builds a `IndexFlatIP`, so `index.search` returns cosine-equivalent scores. Threshold 0.45 was tuned against the calibration queries in [test_smoke](../modules/test_smoke.md).
- **Hierarchical pattern IDs provide natural ordering.** After merging results, the Retriever sorts by pattern ID (`A.6` before `A.6.B`, `B.1` before `B.1.3`), giving a general-to-specific reading order for the Reasoner.
- **Stagnation detection.** If the Retriever notices loops (same sections loaded repeatedly), it escalates to Tier 3, adds `_xref.md` cross-references, or reports back to the user.
- **Reviewer only for Tier 2/3.** Tier 1 routes are pre-validated; the Reasoner's template discipline is enough. Dynamic retrieval needs the extra grounding check.

## Related

- [overview](overview.md)
- [agent-team](agent-team.md)
- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [route-chain](../concepts/route-chain.md)
- [tier](../concepts/tier.md)
- [build_embeddings](../modules/build_embeddings.md)
- [semantic_search](../modules/semantic_search.md)
