---
title: test_smoke
sources:
  - scripts/test_smoke.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - testing
  - smoke-tests
---

# test_smoke

> Source: `scripts/test_smoke.py`

## Purpose

Pipeline integrity smoke tests runnable without external dependencies. Validates that `metadata.json` parsed cleanly, every resolved file path exists, all 10 route files exist with a minimum chain length, the glossary table has at least 40 entries, and cross-reference files resolve to real pattern IDs. A separate `--all` flag enables a stricter set that subprocess-runs semantic search via `uv`.

Run after every rebuild to catch regressions before commit.

## Interface

This module uses Python's `unittest` framework. Each public class is discovered automatically by `unittest.main`:

| Class | What it checks |
|-------|---------------|
| `TestMetadataIntegrity` | metadata.json exists, parses, has ≥230 entries, no bold markers in keys, every entry has a title, every resolved file path exists (≥200 resolved) |
| `TestRouteFiles` | All 10 route files exist, referenced section files exist, each route has ≥1 core section and ≥3 chain entries |
| `TestGlossary` | `glossary-quick.md` exists, has `| Term |` header, ≥40 data rows |
| `TestCrossReferences` | At least 5 `_xref.md` files, unresolved pattern IDs stay under 20% of total refs |
| `TestSemanticSearch` | Only when `--all` given: top score ≥ 0.35, relevant PIDs appear in top 3 for calibration queries |

Helper: `load_metadata() -> dict` — single JSON read shared by all suites.

## Algorithm

`unittest.main` auto-discovers and runs the test classes above. The `RUN_ALL = '--all' in sys.argv` flag gates the semantic-search suite via `@unittest.skipUnless(RUN_ALL, ...)`. At the bottom, `argv` is filtered to remove the custom flag before passing to unittest so it doesn't complain about unknown arguments.

## Dependencies

**Imports:** `json`, `os`, `re`, `subprocess`, `sys`, `unittest`, `pathlib.Path` — stdlib only for the basic suite; semantic-search suite shells out to `uv`.

**Imported by:** Run standalone (`python3 scripts/test_smoke.py`); documented as the verification step in CLAUDE.md and in `rebuild_all.sh` (though the shell script does not invoke it — tests are run manually).

## See also

- [smoke_codex](smoke_codex.md) — parallel suite targeting the Codex edition
- [build-pipeline](../architecture/build-pipeline.md)
- [semantic_search](semantic_search.md) — tested via `--all`
