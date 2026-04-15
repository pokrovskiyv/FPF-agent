---
title: split_spec
sources:
  - scripts/split_spec.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - entry-point
---

# split_spec

> Source: `scripts/split_spec.py`

## Purpose

First stage of the rebuild pipeline. Reads the 5.5 MB `FPF-Spec.md` monolith and decomposes it into ~240 individual section files organized by Part and Cluster. H1 headings become directory boundaries; H2 headings become individual section files. Each directory receives a generated `_index.md` listing its sections.

This module exists because the full spec never fits in a single context window — all downstream processing (metadata, routes, embeddings) operates on these decomposed files instead.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `slugify` | `(text: str, max_len: int = 60) -> str` | Convert heading text to filesystem-safe ASCII slug (strips formatting, normalizes Unicode) |
| `extract_pattern_id` | `(heading: str) -> str` | Pull a hierarchical pattern ID like `A.6.P` or `B.3.3` from a heading line |
| `is_real_h1` | `(line: str) -> bool` | Guard against false H1 matches (excludes markdown table rows starting with `#`) |
| `is_h2` | `(line: str) -> bool` | True when the line starts with `## ` |
| `parse_spec` | `(spec_path: Path) -> list[dict]` | Stream the spec line-by-line, yielding nested H1 → H2 structure with captured content |
| `write_sections` | `(sections: list[dict], output_dir: Path) -> dict` | Create directories, write section files, generate `_index.md` per directory |
| `main` | `() -> None` | Argparse entry point (`--spec`, `--output`) |

## Algorithm

1. Stream `FPF-Spec.md` line by line.
2. On each H1, flush the previous section and open a new directory slug. Increment a directory counter used for numeric prefix (`04-part-a-...`).
3. On each H2, flush the previous H2 content and open a new file slug. Extract the pattern ID (if any) for the filename prefix.
4. All other lines accumulate into the current H2's content buffer (or the current H1's preamble if no H2 has opened yet).
5. After the last line, flush the final H2 and write all files.
6. For each directory, emit `_index.md` with a bulleted list linking to every section file with its pattern ID in parentheses.

Tricky edge cases handled explicitly: `is_real_h1` rejects table rows beginning with `|`, and headings shorter than 3 characters are ignored to avoid false positives.

## Dependencies

**Imports:** `argparse`, `re`, `unicodedata`, `pathlib.Path` — stdlib only.

**Imported by:** Called as a subprocess from `scripts/rebuild_all.sh` (step 1 of 8). Not imported by other Python modules.

## See also

- [build-pipeline](../architecture/build-pipeline.md)
- [build_metadata](build_metadata.md) — consumes the directory structure created here
- [rebuild_all.sh](../architecture/build-pipeline.md) — orchestrates the full rebuild chain
