---
title: build_glossary
sources:
  - scripts/build_glossary.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - glossary
---

# build_glossary

> Source: `scripts/build_glossary.py`

## Purpose

Extracts the 50 most frequently occurring terms from `sections/metadata.json` keywords and writes them to `sections/glossary-quick.md` as a table mapping each term to its primary source pattern. The glossary is loaded by the Reasoner agent as an internal orientation aid (never exposed to the user).

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `build_glossary` | `(metadata: dict, top_n: int = 50) -> list[dict]` | Count keyword frequency across all entries, record the first pattern to mention each keyword, return top-N with `{term, pattern_id, pattern_title, frequency}` |
| `write_glossary` | `(glossary: list[dict], output_path: Path) -> None` | Emit a markdown table `\| Term \| Primary Pattern \| Pattern Title \|` |
| `main` | `() -> None` | Argparse entry (`--metadata`, `--output`) |

## Algorithm

1. Load `sections/metadata.json`.
2. Walk every entry's `keywords` list, lowercase-trim each keyword, filter by length (3–60 chars).
3. Increment a `Counter` and record the first pattern ID to introduce each keyword (first-occurrence wins).
4. Take `Counter.most_common(50)`.
5. Write a 3-column markdown table to `sections/glossary-quick.md`.

Later, the [fpf-sync](../agents/fpf-sync.md) agent runs an AI-enhancement pass on this file that adds a fourth "plain definition" column — that enrichment is out of scope for this module.

## Dependencies

**Imports:** `argparse`, `json`, `collections.Counter`, `pathlib.Path` — stdlib only.

**Imported by:** Called from `scripts/rebuild_all.sh` (step 4). Reads output of [build_metadata](build_metadata.md)/[enrich_metadata](enrich_metadata.md).

## See also

- [build_metadata](build_metadata.md)
- [enrich_metadata](enrich_metadata.md)
- [fpf-sync](../agents/fpf-sync.md) — AI-enhances the glossary with plain-language definitions
- [build-pipeline](../architecture/build-pipeline.md)
