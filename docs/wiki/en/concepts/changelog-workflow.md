---
title: Changelog Workflow
sources:
  - scripts/update_changelog.py
  - CHANGELOG.md
  - CLAUDE.md
  - .claude/settings.json
  - .claude-plugin/plugin.json
last_updated: 2026-04-15T00:00:00Z
tags:
  - concept
  - workflow
  - changelog
  - versioning
---

# Changelog Workflow

## Definition

The **changelog workflow** is the automatic hook-plus-manual process that keeps `CHANGELOG.md` and `plugin.json`'s `version` field in sync with every commit. Uses Conventional Commits parsing: `feat:` → minor bump, `fix:` → patch bump, `feat!:` → major bump, other types (`docs`, `test`, `chore`, `perf`, `ci`, `style`, `refactor`) → changelog entry without version bump.

Consists of an automatic half (the PreToolUse hook) and a manual half (writing the human-readable "What's New" section).

## How it works in the system

### Automatic half

Defined in `.claude/settings.json` as a PreToolUse hook on `Bash` when the command matches `git commit*`. The hook runs [update_changelog](../modules/update_changelog.md) which:

1. Reads the hook JSON from stdin.
2. Extracts the commit subject line (heredoc or `-m`).
3. Parses as Conventional Commit — bails silently if it doesn't match.
4. Bumps `plugin.json` version if type is `feat` / `fix` / has `!`.
5. Appends a bullet to `CHANGELOG.md` under today's date / "### All Changes".
6. `git add`s the modified files so they land in the same commit.

Idempotent — re-commits with the same subject don't duplicate entries.

### Manual half

For user-facing changes (`feat:` or significant `fix:`), Claude or the developer also writes a line in the "### What's New" subsection of `CHANGELOG.md` under today's date. This uses plain language from the user's perspective — not the commit message.

CLAUDE.md explicitly notes: "Write in plain language from the user's perspective, not commit messages. Group related changes into one bullet point."

## Why split automatic and manual

- Automatic records WHAT (commit history) — deterministic, complete.
- Manual records WHY at the user level (product voice) — the thing users actually read.

Mixing them would either produce "### What's New — `chore(agents): bump description`" lines (meaningless to users) or require the hook to call an LLM (slow, flaky).

## See also

- [update_changelog](../modules/update_changelog.md)
- [sync-and-rebuild](../architecture/sync-and-rebuild.md)
- CLAUDE.md "Changelog & Versioning" section
- `CHANGELOG.md` — the file under governance
