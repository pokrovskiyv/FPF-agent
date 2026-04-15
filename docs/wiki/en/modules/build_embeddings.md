---
title: build_embeddings
sources:
  - scripts/build_embeddings.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - embeddings
  - faiss
---

# build_embeddings

> Source: `scripts/build_embeddings.py`

## Purpose

Computes a FAISS flat-IP index over every section in `metadata.json` using the `BAAI/bge-m3` multilingual embedding model (1024-dim). The resulting index powers Tier 2 (semantic fallback) retrieval — when a user's burden doesn't match any of the 10 curated routes, the Retriever queries this index for semantically closest sections.

Unlike the other pipeline scripts, this one requires external dependencies (`sentence-transformers`, `faiss-cpu`, `numpy`) managed via an inline `# /// script` PEP 723 header; run it with `uv run scripts/build_embeddings.py` so `uv` installs the dependencies on demand.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `load_sections` | `(metadata_path: Path) -> list[dict]` | Walk metadata, read each resolved section file, build a combined text string (`Pattern P: title \n Keywords: ... \n Questions: ... \n content[:2000]`), skip sections shorter than 50 chars |
| `build_index` | `(sections: list[dict], model_name: str) -> tuple[IndexFlatIP, ndarray]` | Load the sentence-transformers model, encode in batches of 8 with L2-normalization, build a FAISS inner-product index (equivalent to cosine similarity given normalized vectors) |
| `main` | `() -> None` | Argparse entry (`--metadata`, `--model`, `--output`); write `faiss.index`, `metadata.json` (id→section mapping), and `config.json` (model name, dim, query prefix) |

## Algorithm

1. Load `sections/metadata.json`.
2. For each entry with a resolved `file`, read the section file; skip if < 50 chars of content.
3. Build a compound text: pattern ID + title + up to 10 keywords + up to 5 user queries + up to 2000 chars of body. This gives the embedder multiple anchors — titles for keyword matches, queries for natural-language matches, body for topical matches.
4. Encode all texts in a single batched call with `normalize_embeddings=True`. Store as float32.
5. Build a `faiss.IndexFlatIP` (inner-product index, cosine-equivalent with normalized vectors) and add all embeddings.
6. Serialize three files: `faiss.index`, a parallel `metadata.json` keyed by list index, and a small `config.json` with the model name (used at query time) and `query_prefix: "query: "`.

## Dependencies

**Imports:** `argparse`, `json`, `sys`, `pathlib.Path`, `faiss`, `numpy`, `sentence_transformers.SentenceTransformer`.

**Runtime requirement:** `uv` (auto-installs sentence-transformers, faiss-cpu, numpy via inline deps). Model download (~2 GB) happens on first run.

**Imported by:** Called from `scripts/rebuild_all.sh` (step 8). Output is read by [semantic_search](semantic_search.md) at query time.

## See also

- [semantic_search](semantic_search.md) — query-side counterpart
- [build_metadata](build_metadata.md) / [enrich_metadata](enrich_metadata.md) — produce the input
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
- [fpf-retriever](../agents/fpf-retriever.md) — calls semantic_search as a subprocess
