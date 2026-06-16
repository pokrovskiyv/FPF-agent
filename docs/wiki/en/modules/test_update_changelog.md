---
title: test_update_changelog
sources:
  - scripts/test_update_changelog.py
last_updated: 2026-06-16T07:21:51Z
tags:
  - module
  - testing
  - changelog
---

# test_update_changelog

> Source: `scripts/test_update_changelog.py`

## Purpose

Regression tests for [update_changelog](update_changelog.md), the PreToolUse changelog hook. They lock in the fix for a bug where a commit subject containing an apostrophe inside a double-quoted `-m` message (e.g. `"docs: add What's New"`) was truncated at the apostrophe, producing a half-written changelog bullet (`- **docs**: What`). The tests assert the extractor preserves the full description and that the bullet written to `CHANGELOG.md` is complete.

Run standalone before changing the hook: `python3 scripts/test_update_changelog.py`.

## Interface

Uses Python's `unittest`. Two suites:

| Class | What it checks |
|-------|---------------|
| `TestExtractCommitMessage` | `extract_commit_message` on: an apostrophe inside a double-quoted message, escaped double-quotes (`\"X\"`), plain double / single quotes, heredoc subject extraction, a multi-line message (subject only), multiple `-m` flags (first wins), and no message present |
| `TestAppendedBullet` | End-to-end: parse → `format_entry` → `update_changelog` into a throwaway temp file, asserting the full description appears and the old truncated form does not |

## Dependencies

**Imports:** `sys`, `tempfile`, `unittest`, `datetime.date`, `pathlib.Path`, plus the functions under test from `update_changelog` — stdlib only.

**Imported by:** Run standalone; like the other smoke suites it is executed manually before commit, not wired into an automated runner.

## See also

- [update_changelog](update_changelog.md) — the module under test
- [test_smoke](test_smoke.md) — pipeline integrity smoke tests
- [changelog-workflow](../concepts/changelog-workflow.md)
