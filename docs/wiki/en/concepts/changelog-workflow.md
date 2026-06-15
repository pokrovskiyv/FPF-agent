---
title: Changelog Workflow
sources:
  - .claude-plugin/plugin.json
  - CHANGELOG.md
  - CLAUDE.md
  - scripts/update_changelog.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - concept
  - workflow
  - changelog
  - versioning
---

# Changelog Workflow

## Definition

The **changelog workflow** is the automatic-plus-manual process that keeps `CHANGELOG.md` and the `version` field of `plugin.json` in sync with every commit. It parses Conventional Commits: `feat:` → minor bump, `fix:` → patch bump, `feat!:` (or any type with `!`) → major bump, and other types (`docs`, `test`, `chore`, `perf`, `ci`, `style`, `refactor`) → a changelog entry without a version bump.

It has two halves: an automatic half (a PreToolUse hook that runs on every commit) and a manual half (a human-written "What's New" section). The current published version is **0.6.0**.

## How it works in the system

### Automatic half — the commit hook

Defined in `.claude/settings.json` as a PreToolUse hook on `Bash` with the condition `if: Bash(git commit*)`. Before every commit, it runs `scripts/update_changelog.py` (see [update_changelog](../modules/update_changelog.md)), which:

1. Reads the hook JSON from stdin.
2. Extracts the commit subject line — handles both the `-m "..."` form and Claude Code's heredoc form (`-m "$(cat <<'EOF' ... EOF)"`).
3. Parses it as a Conventional Commit via `CC_PATTERN` — bails silently if it doesn't match.
4. Determines the bump (`determine_bump` / `bump_version`) and, if it's `feat` / `fix` / breaking, updates the `version` field **only in `.claude-plugin/plugin.json`** (the `PLUGIN_JSON` constant points there).
5. Appends a bullet to `CHANGELOG.md` under today's date heading, inside the `### All Changes` subsection.
6. `git add`s the modified files (`CHANGELOG.md`, plus `.claude-plugin/plugin.json` when a bump happened) so they land in the same commit.

The changelog insertion is idempotent: a re-commit with the same subject does not duplicate the entry (`update_changelog` does a whole-line match before inserting).

### Manual half — the "What's New" section

For user-facing changes (a `feat:` or a significant `fix:`), Claude or the developer also writes a line in the `### What's New` subsection of `CHANGELOG.md` under today's date. As CLAUDE.md puts it: "Write in plain language from the user's perspective, not commit messages. Group related changes into one bullet point." This is the part users actually read — see the bilingual, product-voice entries in `CHANGELOG.md` itself.

### Two plugin manifests, kept in lockstep

The project ships as a plugin for **both** Claude Code (`.claude-plugin/plugin.json`) and the Codex CLI (`.codex-plugin/plugin.json`, installed via `scripts/install_codex_plugin.py` into a home-local marketplace). Both manifests carry the same `version`.

The hook only ever touches `.claude-plugin/plugin.json`. The second manifest is brought into sync by the scheduled [fpf-sync](../agents/fpf-sync.md) routine, whose Step 7 bumps the version in **both** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` and whose Step 8 stages both. So routine-driven syncs keep the two manifests in lockstep, while ad-hoc commits only move the Claude-Code one — the Codex manifest catches up on the next sync.

### Where the bi-weekly "What's New" comes from

The recurring upstream-sync commits that fill the `### What's New` section are produced by the [sync-and-rebuild](../architecture/sync-and-rebuild.md) flow — the Claude Code Remote Routine, the single sync mechanism (there is no GitHub Action anymore). Its Step 7 writes the user-facing "What's New" entry and bumps both manifests; its commit message is `chore: sync upstream + rebuild + AI-enhanced indexes + wiki refresh`, which the hook then records under `### All Changes`.

## Why split automatic and manual

- The automatic half records **what** changed (commit history) — deterministic and complete.
- The manual half records **why** at the product level (the voice users read) — the curated story.

Mixing them would either produce `### What's New — chore(agents): bump description` lines (meaningless to users) or require the hook to call an LLM on every commit (slow and flaky). Keeping them separate lets a sub-second deterministic hook own the ledger while a human (or the sync routine) owns the narrative.

## See also

- [update_changelog](../modules/update_changelog.md) — the hook script
- [sync-and-rebuild](../architecture/sync-and-rebuild.md) — where bi-weekly "What's New" entries originate
- [fpf-sync](../agents/fpf-sync.md) — the routine that bumps both manifests
- CLAUDE.md "Changelog & Versioning" section
- `CHANGELOG.md` — the file under governance
