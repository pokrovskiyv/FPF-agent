---
title: build_xrefs
sources:
  - scripts/build_xrefs.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - cross-references
---

# build_xrefs

> Source: `scripts/build_xrefs.py`

## Purpose

Builds an `_xref.md` file for each `sections/` directory that lists incoming cross-references from patterns in **other** Parts. Traverses the dependency graph in `metadata.json` — the `builds_on`, `refines`, `coordinates_with`, `prerequisite_for`, `constrains`, `informs`, `used_by`, and `specialised_by` relations — and inverts it so each directory can answer "who depends on me?".

Used by the Retriever agent when a route chain doesn't fully cover a query: it checks `_xref.md` for patterns in other Parts that reference the loaded section.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `normalize_pattern_id` | `(raw: str) -> str` | Trim formatting, strip trailing text, and regex-match a valid hierarchical ID (`A.6.3`, `F.17`, `P-123`) |
| `find_directory_for_pattern` | `(pattern_id, metadata, sections_dir) -> str` | Given a pattern ID, return the top-level directory name under `sections/` |
| `build_xref_graph` | `(metadata, sections_dir) -> dict` | Invert the dependency graph into `{target_dir: [{source_pattern, source_dir, target_pattern, relation}]}` |
| `write_xref_files` | `(xrefs, sections_dir) -> int` | Write `_xref.md` per directory, grouped by source directory, with a deduplicated reference table |
| `main` | `() -> None` | Argparse entry (`--metadata`, `--sections`) |

## Algorithm

1. Read `metadata.json`.
2. For each source pattern, find its directory.
3. For every dependency relation, normalize the target pattern ID and find its directory.
4. Skip same-directory relations (only **cross-directory** references matter here).
5. Accumulate `{target_dir: list of refs}` in a defaultdict.
6. For each target directory, group references by source directory, dedupe by `(source, relation, target)` tuple, and render a markdown table per source.
7. Write `_xref.md` in the target directory.

## Dependencies

**Imports:** `argparse`, `json`, `re`, `collections.defaultdict`, `pathlib.Path` — stdlib only.

**Imported by:** Called from `scripts/rebuild_all.sh` (step 7). Reads [build_metadata](build_metadata.md) output; output is read at runtime by the Retriever agent during Tier 3 cross-reference expansion.

## See also

- [build_metadata](build_metadata.md) — dependency graph source
- [fpf-retriever](../agents/fpf-retriever.md) — uses `_xref.md` for Tier 3 expansion
- [three-tier-retrieval](../architecture/three-tier-retrieval.md)
