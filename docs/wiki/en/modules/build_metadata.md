---
title: build_metadata
sources:
  - scripts/build_metadata.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - metadata
---

# build_metadata

> Source: `scripts/build_metadata.py`

## Purpose

Parses the Table of Contents tables embedded at the top of `FPF-Spec.md` (lines 7-337) into a queryable `sections/metadata.json`. For every entry the script captures pattern ID, title, status, keywords, queries (user-facing phrasings), and dependency graph (`builds_on`, `coordinates_with`, etc.), then resolves each pattern ID to its section file by scanning `_index.md` files produced by [split_spec](split_spec.md).

This pre-computed index lets the Retriever agent find sections by pattern ID, keyword, or plain-language query without streaming the full spec.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `find_section_file` | `(pattern_id: str, sections_dir: Path) -> str` | Locate the file for a pattern using three-step matching: exact link-text match, word-boundary substring match, and parent fallback (B.2.1 → B.2) |
| `parse_keywords` | `(text: str) -> list[str]` | Extract comma-separated keywords from `*Keywords:* ...` cell |
| `parse_queries` | `(text: str) -> list[str]` | Extract quoted user queries from `*Queries:* "..."` cell |
| `parse_dependencies` | `(text: str) -> dict` | Parse relation types (`Builds on:`, `Refines:`, `Used by:`, etc.) into a dict of lists |
| `_split_table_row` | `(line: str) -> list[str]` | Markdown table row splitter that ignores pipes inside backticks |
| `parse_toc` | `(spec_path: Path) -> list[dict]` | Scan the ToC section, emit one dict per entry |
| `resolve_files` | `(entries: list[dict], sections_dir: Path) -> list[dict]` | Add a `file` field to each entry using `find_section_file` |
| `build_metadata_dict` | `(entries: list[dict]) -> dict` | Convert to `{pattern_id: entry}` dictionary, generating keys like `preface_1` for unnamed entries |
| `main` | `() -> None` | Argparse entry (`--spec`, `--sections`, `--output`) |

## Algorithm

1. Scan `FPF-Spec.md` until `# Table of Content`, then read rows until the next H1.
2. For each table row with ≥3 cells, classify as short form (3 cells) or full form (5 cells including pattern ID and dependencies).
3. Parse keywords, queries, and dependency text from the relevant cells.
4. After all rows are parsed, pass through `resolve_files` to attach the section file path. Falls back to parent pattern (B.2.1 → B.2) when direct lookup fails.
5. Serialize the final dict to `sections/metadata.json` using `ensure_ascii=False` (preserves Russian queries).

## Dependencies

**Imports:** `argparse`, `json`, `re`, `pathlib.Path` — stdlib only.

**Imported by:** Called from `scripts/rebuild_all.sh` (step 2). Consumed downstream by [build_glossary](build_glossary.md), [build_routes](build_routes.md), [build_xrefs](build_xrefs.md), [build_embeddings](build_embeddings.md), and [enrich_metadata](enrich_metadata.md).

## See also

- [split_spec](split_spec.md) — produces the directory structure this script scans
- [enrich_metadata](enrich_metadata.md) — runs after this to add user-facing keywords
- [build-pipeline](../architecture/build-pipeline.md)
