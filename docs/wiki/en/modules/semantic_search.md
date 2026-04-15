---
title: semantic_search
sources:
  - scripts/semantic_search.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - query-time
  - embeddings
  - faiss
---

# semantic_search

> Source: `scripts/semantic_search.py`

## Purpose

CLI for querying the FAISS index produced by [build_embeddings](build_embeddings.md). Encodes a natural-language query (any language — English, Russian, etc., thanks to the multilingual `bge-m3` model) with the same model that built the index, runs a top-K inner-product search, and prints or JSON-dumps the matching sections.

The Retriever agent invokes this module as a subprocess (`uv run scripts/semantic_search.py ... --json`) during Tier 2 (semantic fallback) and Tier 3 (combined) retrieval.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `load_model` | `(model_name: str) -> SentenceTransformer` | Lazy-load model with a module-level cache so repeated calls in one process don't re-init |
| `search` | `(query, index_dir=DEFAULT_INDEX_DIR, top_k=5) -> list[dict]` | Read config/index/mapping, encode the query with the configured `query_prefix`, normalize, run `index.search`, return ranked list with `{rank, score, pattern_id, title, file, keywords}` |
| `main` | `() -> None` | Argparse entry (`query`, `--top-k`, `--index-dir`, `--json`, `--threshold`); print results as table or JSON |

## Algorithm

1. Load `sections/embeddings/config.json` to read the model name and query prefix, load `metadata.json` for id→section mapping, and load `faiss.index`.
2. Encode `query_prefix + query` with `normalize_embeddings=True` (matches how the index was built).
3. Call `index.search(vec, top_k)` — FAISS returns scores (inner-products) and integer indices.
4. Zip results with the mapping to produce the final list.
5. Optional threshold filter: drop results with `score < threshold` (default 0.0 = keep all).
6. Output: human-readable table (default) or JSON (`--json`).

The module-level `_model_cache` keeps the model loaded between calls in the same process, which matters when tests or batch queries call `search()` repeatedly.

## Dependencies

**Imports:** `argparse`, `json`, `sys`, `pathlib.Path`, `faiss`, `numpy`, `sentence_transformers.SentenceTransformer`.

**Runtime requirement:** `uv` and the FAISS index from `build_embeddings`. Model download (~2 GB) on first run if not cached.

**Imported by:** Called as a subprocess by [fpf-retriever](../agents/fpf-retriever.md) in semantic mode. Also tested by [test_smoke](test_smoke.md) and [smoke_codex](smoke_codex.md).

## See also

- [build_embeddings](build_embeddings.md) — builds the index this queries
- [fpf-retriever](../agents/fpf-retriever.md) — primary consumer
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
