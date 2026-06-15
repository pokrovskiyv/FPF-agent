---
title: sync_doc_stats
sources:
  - scripts/sync_doc_stats.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - module
  - docs
  - stats
  - gate
  - rebuild
---

# sync_doc_stats

> Source: `scripts/sync_doc_stats.py`

## Purpose

Keeps the hard-coded counts scattered through `CLAUDE.md` and `Readme.md` in sync with reality. The spec grows on every upstream sync, so any number written by hand — spec line count, section count, metadata entries, FAISS vectors, keywords, dependency-graph edges — drifts and silently goes wrong. This script recomputes every such number from `FPF-Spec.md` + `sections/metadata.json` and rewrites the two docs in place so the figures can never go stale past a single rebuild. It runs as step 8 of `scripts/rebuild_all.sh`, and its `--check` mode doubles as a drift gate. Stdlib only — no `uv` or FAISS index required.

The FAISS vector count is **derived**, not measured: it equals the number of metadata entries that carry a `file` field (entries without a section file, e.g. preface/ToC rows, are not indexed). No embedding index needs to exist to compute it.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `compute_stats` | `() -> dict` | Read `FPF-Spec.md` + `sections/metadata.json` and the `sections/` tree; return a dict of every derived figure (spec lines/MB/tokens, section file count, content dirs, entries, keywords, queries, edges, vectors, percentages, FAISS size) |
| `sp` | `(n: int) -> str` | Group digits with a thin space — `12345` → `'12 345'` (Russian convention used in `Readme.md`) |
| `en` | `(n: int) -> str` | Group digits with a comma — English thousands separator |
| `round_to` | `(n: int, base: int) -> int` | Round `n` to the nearest multiple of `base` (used for the `~N` approximate figures) |
| `plural_ru` | `(n: int, one: str, few: str, many: str) -> str` | Pick the correct Russian noun form for a count (handles the 11–14 exception and the `%10` rule) |
| `build_rules` | `(s: dict) -> dict[str, list[tuple[re.Pattern, str]]]` | Build the per-file list of `(regex, replacement)` rules from the stats dict; keyed by `"CLAUDE.md"` and `"Readme.md"` |
| `process` | `(check: bool) -> int` | Apply or check all rules across both files; return exit code (`0` ok / drift fixed, `1` drift found in check mode) |
| `main` | `() -> None` | Parse `--check` and `sys.exit(process(...))` |

## Algorithm

1. **`compute_stats`** reads the spec's byte size and line count (`count(b"\n")`, matching `wc -l`), loads `sections/metadata.json`, and sums `keywords`, `queries`, and dependency `edges` across all entries. It counts section `.md` files (excluding `_index.md`, `_xref.md`, the `routes/` and `embeddings/` dirs, and top-level files), content directories, and total section bytes. `vectors` = entries that have a `file`; `no_file` = the rest; `faiss_kb`, `vec_pct`, and the spec MB/token figures are derived arithmetically.
2. **`build_rules`** turns those numbers into replacement rules. Each rule is a `(regex, fragment)` pair: the regex matches the current line with the number left loose (so it locates the fragment regardless of the stale value), and the fragment is the corrected text. Russian fragments use `plural_ru` helpers (`secs`, `vec_nom`, `files_ru`, …) for correct noun agreement; approximate figures use `round_to`.
3. **`process`** loads each file, runs every rule with `pat.sub(..., count=1)`. If a rule's regex does not match, it records a drift note (the doc was likely hand-edited away from the expected shape). In apply mode it writes the file back and prints what changed; in `--check` mode it records "stale numbers" without writing.
4. If `--check` found any drift, `process` prints the drift report and returns `1` (the gate fails the build); otherwise it prints `up to date ✓`. In apply mode it prints a one-line summary of the synced figures.

## Dependencies

**Imports:** `argparse`, `json`, `re`, `sys`, `pathlib.Path` — stdlib only.

**Reads:** `FPF-Spec.md`, `sections/metadata.json`, the `sections/` tree.
**Writes / checks:** `CLAUDE.md`, `Readme.md`.

**Invoked by:** `scripts/rebuild_all.sh` (step 8, apply mode). The `--check` mode is intended as a CI/pre-commit drift gate.

## See also

- [sync-and-rebuild](../architecture/sync-and-rebuild.md) — where this slots into the rebuild pipeline
- [update_changelog](update_changelog.md) — sibling docs-maintenance hook
- CLAUDE.md "Commands" / "Sync & Rebuild" sections (one of the two files this script keeps current)
