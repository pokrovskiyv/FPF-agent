---
title: Sync and Rebuild
sources:
  - CLAUDE.md
  - agents/fpf-sync.md
  - scripts/update_changelog.py
last_updated: 2026-07-15T17:17:20Z
tags:
  - architecture
  - sync
  - rebuild
  - scheduled
---

# Sync and Rebuild

## Components

Keeping the fork in sync with upstream `ailev/FPF` runs through a single scheduled path. There is no GitHub Action — the project is packaged as a plugin for **both** Claude Code (`.claude-plugin/`) and Codex CLI (`.codex-plugin/`), and the whole sync cycle is driven by one Claude Code remote routine.

| Component | Where | Role |
|-----------|-------|------|
| Claude Code remote routine | `trig_01P7UzjrjgsgzLpMHn84bMoo` — managed at [claude.ai/code/routines/trig_01P7UzjrjgsgzLpMHn84bMoo](https://claude.ai/code/routines/trig_01P7UzjrjgsgzLpMHn84bMoo) | Cron: 1st and 15th of each month at 07:00 UTC (= 09:00 Europe/Belgrade). Drives the full 8-step cycle below by reading [fpf-sync](../agents/fpf-sync.md) each run. |
| fpf-sync agent | [agents/fpf-sync.md](../agents/fpf-sync.md) | The runbook the routine executes: check upstream, merge, rebuild, AI-enhance, compile wiki, changelog, commit. Source of truth for every step. |
| PreToolUse changelog hook | `.claude/settings.json` → [scripts/update_changelog.py](../modules/update_changelog.md) | Fires on every `git commit`. Parses the Conventional Commit, appends a changelog entry, and auto-bumps **only** `.claude-plugin/plugin.json`. |

The routine fully replaces the old GitHub Action (`.github/workflows/rebuild-sections.yml`), which consistently failed and was removed. It no longer exists, and no Action is active — there is a single update path.

## Data Flow

The fpf-sync runbook has **eight** steps. Steps 2–5 are skipped when upstream is unchanged (Step 1 short-circuits), but Step 6 onward still run so local edits to wiki sources do not leave the wiki stale.

```
 (1st & 15th of each month, 07:00 UTC = 09:00 Europe/Belgrade)
 Claude Code remote routine  →  reads agents/fpf-sync.md
           │
           ▼
    fpf-sync runbook
           │
  Step 1 ──► git fetch upstream; compare FPF-Spec.md hash
           │     (hashes match → skip Steps 2–5, jump to Step 6)
           │
  Step 2 ──► git merge upstream/main --no-edit
           │     Readme.md conflict is EXPECTED → git checkout --ours Readme.md && git add Readme.md
           │     ANY other conflict → stop and report (no force-resolve)
           │
  Step 3 ──► bash scripts/rebuild_all.sh
           │     (regenerates sections/, metadata.json, glossary, lexical rules,
           │      routes, xrefs, and the FAISS embeddings index via uv)
           │
  Step 4 ──► AI-enhance sections/**/_index.md
           │     (one-sentence plain-language summary per section, no FPF jargon)
           │
  Step 5 ──► AI-enhance sections/glossary-quick.md
           │     (add a plain-definition column for the 50 terms)
           │
  Step 6 ──► scanner.py check . → /wiki compile
           │     (bilingual: regenerates BOTH docs/wiki/ru/ and docs/wiki/en/,
           │      updates docs/wiki/.state/manifest.json; verify check exits 0)
           │
  Step 7 ──► CHANGELOG.md "What's New" (plain-language, user-facing)
           │     + manual version bump in BOTH .claude-plugin/plugin.json
           │       AND .codex-plugin/plugin.json (kept in lockstep)
           │
  Step 8 ──► git add sections/ docs/wiki/ CHANGELOG.md \
           │         .claude-plugin/plugin.json .codex-plugin/plugin.json
           └─► git commit -m "chore: sync upstream + rebuild + AI-enhanced indexes + wiki refresh"
               git push
```

The commit in Step 8 also triggers the PreToolUse hook, which appends a Conventional-Commit changelog entry and bumps `.claude-plugin/plugin.json` on its own. The current plugin version is **0.6.3**.

## Decisions

- **Single scheduled path.** The Claude Code remote routine owns the entire sync cycle. The previous GitHub Action duplicated this flow, consistently failed, and was removed — there is no Action fallback and no second update path.
- **Dual-plugin lockstep.** The project ships as a plugin for both Claude Code and Codex CLI, so two manifests carry a version. The PreToolUse hook only knows about `.claude-plugin/plugin.json`; therefore Step 7 of fpf-sync manually bumps **both** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` so they never drift apart.
- **AI enhancement is separate from the mechanical rebuild.** `rebuild_all.sh` produces raw structures with stdlib only; the fpf-sync runbook then rewrites `_index.md` summaries and glossary definitions in plain language. This keeps the Python pipeline dependency-free while still getting LLM-quality, jargon-free summaries.
- **Automatic single-manifest bump on commit.** The PreToolUse hook runs `update_changelog.py`, which parses Conventional Commits and bumps `.claude-plugin/plugin.json`: `feat:` → minor, `fix:` → patch, `feat!:` → major; `docs`/`test`/`chore`/`perf`/`ci`/`style`/`refactor` get a changelog entry with no bump. The Codex manifest is intentionally left to the routine.
- **Expected conflict, scripted resolution.** The fork's plugin-focused `Readme.md` always conflicts with upstream's spec-focused one. That single conflict is auto-resolved with `git checkout --ours Readme.md`; any other conflict halts the run rather than risking a bad force-resolve.
- **Merge, never rebase.** The runbook explicitly forbids force-push and rebase, preserving upstream-downstream provenance.

## Related

- [fpf-sync](../agents/fpf-sync.md)
- [build-pipeline](build-pipeline.md)
- [update_changelog](../modules/update_changelog.md)
- [changelog-workflow](../concepts/changelog-workflow.md)
