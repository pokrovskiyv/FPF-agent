---
title: enrich_metadata
sources:
  - scripts/enrich_metadata.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - metadata
  - bilingual
---

# enrich_metadata

> Source: `scripts/enrich_metadata.py`

## Purpose

Adds user-facing keywords and plain-language queries (English + Russian) to metadata entries whose automatic extraction produced weak results. The raw ToC often gives you jargon-only keywords; this script supplements them with phrasings an actual user would type — questions like "How to choose between competing alternatives for a project?" or "Как сравнить два подхода?".

Runs as a post-processing step on `sections/metadata.json` and is **idempotent** — re-running it does not duplicate entries.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `main` | `() -> None` | Load `metadata.json`, iterate over the hardcoded `ENRICHMENTS` list, and merge new keywords/queries into matching entries |

The file also defines a module-level `ENRICHMENTS` list — a hand-curated set of dicts with `pattern_id`, `add_keywords`, and `add_queries` (bilingual). Extending the enrichment set means editing this list directly.

## Algorithm

1. Read `sections/metadata.json`.
2. For each enrichment dict, look up the target entry by `pattern_id`; skip if not found.
3. Compute the set difference between proposed keywords/queries and existing ones (idempotency guard).
4. Append only the new items to the entry's `keywords` and `queries` lists.
5. Write the enriched metadata back to `sections/metadata.json` with `ensure_ascii=False`.

The script prints a summary line per enriched entry (`A.19.CPM: +5 keywords, +6 queries`) so you can confirm which patterns were touched.

## Dependencies

**Imports:** `json`, `pathlib.Path` — stdlib only.

**Imported by:** Called from `scripts/rebuild_all.sh` (step 3). Runs after [build_metadata](build_metadata.md) produces the baseline file.

## See also

- [build_metadata](build_metadata.md) — produces the input file
- [build_embeddings](build_embeddings.md) — consumes the enriched queries to improve semantic search recall
- [build-pipeline](../architecture/build-pipeline.md)
