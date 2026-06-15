---
title: fpf-sync
sources:
  - agents/fpf-sync.md
last_updated: 2026-06-15T00:00:00Z
tags:
  - agent
  - sync
  - scheduled
  - maintenance
---

# fpf-sync

> Source: `agents/fpf-sync.md`

## Purpose

Scheduled maintenance agent. Syncs the local fork with upstream `ailev/FPF`, runs the full Python rebuild pipeline, performs AI enhancement passes on `_index.md` files and `glossary-quick.md`, recompiles the bilingual wiki, updates the changelog, and bumps both plugin manifests. Commits and pushes all changes.

Unlike the other agents, fpf-sync never interacts with an end user — it's pure project maintenance.

## Interface

**Input:** none (scheduled trigger).

**Output:** a single git commit on the main branch with the message `chore: sync upstream + rebuild + AI-enhanced indexes + wiki refresh`, plus a pushed `main`. The staged set is exactly:

```bash
git add sections/ docs/wiki/ CHANGELOG.md .claude-plugin/plugin.json .codex-plugin/plugin.json
```

## The eight steps

1. **Check upstream.** Add the `upstream` remote if missing, `git fetch upstream main`, then compare `FPF-Spec.md` hashes (`git rev-parse upstream/main:FPF-Spec.md` vs `HEAD:FPF-Spec.md`). If identical → skip the merge and rebuild (Steps 2–5) to save compute, but do **not** stop: local edits to wiki sources (`CLAUDE.md`, `Readme.md`, `agents/*`, `sections/routes/*`, `skills/*`) can still leave the wiki stale, so jump to Step 6.
2. **Merge.** `git merge upstream/main --no-edit`. A `Readme.md` conflict is **expected** — the fork carries a plugin-focused README, upstream a spec-focused one — and is auto-resolved by keeping ours: `git checkout --ours Readme.md && git add Readme.md`. For ANY other conflict the agent stops and reports; it never force-resolves.
3. **Rebuild.** `bash scripts/rebuild_all.sh` — regenerates `sections/`, `metadata.json`, `glossary-quick.md`, `lexical-rules.md`, routes, xrefs, and the FAISS embeddings index. The embeddings step requires `uv` (sentence-transformers + faiss-cpu via inline script dependencies).
4. **AI-enhance `_index.md`.** For each directory with an `_index.md`, read the first 30 lines of each listed section file and rewrite the index with one-sentence plain-language summaries — focused on what problem each section helps solve, max 120 chars, no FPF terminology. Link format: `- [Title](filename.md) — one-sentence summary`.
5. **AI-enhance `glossary-quick.md`.** For each of 50 terms, read the first 20 lines of its source section and add a plain-definition column (max 80 chars). Final table shape: `| Term | Primary Pattern | Plain Definition |`.
6. **Compile the bilingual wiki.** First run `python3 ~/.claude/skills/wiki/scanner.py check .`. If it reports stale, run `/wiki compile` (LLM-driven, incremental) — it regenerates every affected article in BOTH `docs/wiki/ru/` and `docs/wiki/en/` and updates `docs/wiki/.state/manifest.json`. There is no command-line fallback: if the `/wiki` skill is unavailable, STOP and report. Verify by re-running `scanner.py check .`, which must now exit 0 before any commit.
7. **Update the changelog + version.** Append a plain-language "What's New" section to `CHANGELOG.md` under today's date, written from the user's perspective (not copied commit messages). When the sync adds new user-facing patterns, bump the version in **both** `.claude-plugin/plugin.json` **and** `.codex-plugin/plugin.json` (minor bump) so they stay in lockstep; otherwise leave them as is.
8. **Commit + push.** Stage the set above, commit with `chore: sync upstream + rebuild + AI-enhanced indexes + wiki refresh`, then `git push`.

## Why both plugin.json files are bumped manually

The project ships as a plugin for two hosts — Claude Code (`.claude-plugin/`) and Codex CLI (`.codex-plugin/`, installed via `scripts/install_codex_plugin.py`). The PreToolUse changelog hook (`scripts/update_changelog.py`) auto-bumps **only** `.claude-plugin/plugin.json`. So the fpf-sync routine bumps **both** manifests by hand to keep their versions in lockstep. Both are currently at `0.6.0`.

## Explicit "do not"

The source lists invariants the agent must never violate:

- No modifications to `FPF-Spec.md` (upstream source of truth)
- No modifications to `scripts/`, `agents/`, or `skills/` (maintained manually)
- No editing `docs/wiki/` by hand — regenerate it via `/wiki compile`
- No force-push, no rebase — always merge
- No FPF terminology in any enhanced summary
- Do not stop early if the wiki is stale from local edits — Step 6 must still run and the refresh must be committed

## Triggering

A single mechanism now drives the sync: the **Claude Code Remote Routine** (trigger `trig_01P7UzjrjgsgzLpMHn84bMoo`), cron on the 1st and 15th of each month at 07:00 UTC (= 09:00 Europe/Belgrade), managed at <https://claude.ai/code/routines/trig_01P7UzjrjgsgzLpMHn84bMoo>. It reads `agents/fpf-sync.md` on each run and executes the eight steps above.

A previous GitHub Action (`.github/workflows/rebuild-sections.yml`) covered the same flow but consistently failed and has been **removed** — the remote routine fully replaces it. There is no longer any active GitHub Action, and no second update path.

## See also

- [sync-and-rebuild](../architecture/sync-and-rebuild.md)
- [build-pipeline](../architecture/build-pipeline.md)
- [agent-team](../architecture/agent-team.md)
