---
title: update_changelog
sources:
  - scripts/update_changelog.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - hook
  - changelog
  - versioning
---

# update_changelog

> Source: `scripts/update_changelog.py`

## Purpose

PreToolUse hook script that runs before every `git commit`. Reads the hook's JSON payload from stdin, extracts the commit subject line, parses it as a Conventional Commit, auto-bumps the `version` in `.claude-plugin/plugin.json` (feat → minor, fix → patch, breaking → major), and appends a formatted entry to `CHANGELOG.md` under today's date and an "### All Changes" subsection. Finally stages both files so the bump and changelog entry land in the same commit.

Silent skip when the commit message isn't a Conventional Commit or the hook JSON is missing.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `extract_commit_message` | `(bash_command: str) -> str \| None` | Return the first subject line; handles both heredoc (`<<EOF ...`) and `-m "..."`/`-m '...'` forms |
| `parse_conventional_commit` | `(message: str) -> dict \| None` | Regex-parse `type(scope)!: description`; return None on mismatch |
| `determine_bump` | `(parsed: dict) -> str` | Return `major`, `minor`, `patch`, or `none` based on parsed type and breaking flag |
| `bump_version` | `(current: str, bump_type: str) -> str` | Increment a semver string; `none` returns unchanged |
| `update_plugin_json` | `(path: Path, new_version: str) -> None` | Immutable read-then-write of `plugin.json` with updated version |
| `format_entry` | `(parsed: dict) -> str` | Format the bullet line (`- **feat(scope)**: description`) |
| `update_changelog` | `(path: Path, entry_line: str, date_str: str) -> None` | Insert under today's date / "### All Changes"; idempotent (skip if line already present) |
| `stage_files` | `(*paths: Path) -> None` | Run `git add` on the given paths |
| `main` | `() -> None` | Orchestrate the pipeline; prints diagnostic info at each step |

## Algorithm

1. Read JSON from stdin; bail out quietly if missing or malformed.
2. Extract the bash command, then the commit subject line. Bail if either is empty.
3. Parse as Conventional Commit; bail if it doesn't match.
4. Determine bump type. If not `none`, load `plugin.json`, bump the version, and write it back.
5. Format a changelog entry line and call `update_changelog` with today's date.
6. `git add` the modified files so they're part of the current commit.

Idempotency is handled in `update_changelog`: if the exact entry line already exists in the file, skip the append.

## Dependencies

**Imports:** `json`, `re`, `subprocess`, `sys`, `datetime.date`, `pathlib.Path` — stdlib only.

**Imported by:** Wired into `.claude/settings.json` as a PreToolUse hook matcher on `Bash` when the command matches `git commit*`.

## See also

- [changelog-workflow](../concepts/changelog-workflow.md) — the overall versioning policy
- [sync-and-rebuild](../architecture/sync-and-rebuild.md)
- CLAUDE.md "Changelog & Versioning" section
