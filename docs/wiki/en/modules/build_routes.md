---
title: build_routes
sources:
  - scripts/build_routes.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - routes
---

# build_routes

> Source: `scripts/build_routes.py`

## Purpose

Generates the 10 route files under `sections/routes/` from a hardcoded `ROUTES` constant. Each route encodes a curated section chain for one user burden — e.g., "teams don't understand each other" → Route 1 → `[A.1.1, A.15, A.15.2, ...]`. Routes act as a cache over the semantic search: when a user's burden matches a known burden, the Classifier picks the matching route directly instead of running a full search.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `build_route_file` | `(route: dict, metadata: dict) -> str` | Render a single route markdown: header with "When user says" / "What user gets", a chain table (pattern ID, title, file path, core flag), and a loading-strategy footer |
| `main` | `() -> None` | Argparse entry (`--metadata`, `--output`); iterate `ROUTES`, write one file per route |

At module level, the `ROUTES` constant is a hand-curated list of 10 dicts. Each dict carries `id`, `slug`, `user_says`, `user_gets`, `chain` (ordered pattern IDs), and `core` (subset used for minimum load).

## Algorithm

1. Load `sections/metadata.json` to resolve pattern IDs → titles and file paths.
2. For each of the 10 routes, build a markdown table where the Core column is marked `YES` only for patterns listed in `route['core']`.
3. Write files named `route-{id}-{slug}.md` into `sections/routes/`.
4. Print one confirmation per file written.

Route files are the primary Tier 1 asset — they let the Retriever agent skip semantic search entirely for common burdens.

## Dependencies

**Imports:** `argparse`, `json`, `pathlib.Path` — stdlib only.

**Imported by:** Called from `scripts/rebuild_all.sh` (step 6). Reads output of [build_metadata](build_metadata.md); written files are read at runtime by the Retriever.

## See also

- [fpf-classifier](../agents/fpf-classifier.md) — picks a route
- [fpf-retriever](../agents/fpf-retriever.md) — loads the route chain
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
- [route-chain](../concepts/route-chain.md)
