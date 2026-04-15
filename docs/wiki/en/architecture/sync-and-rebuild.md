---
title: Sync and Rebuild
sources:
  - agents/fpf-sync.md
  - scripts/rebuild_all.sh
  - scripts/update_changelog.py
  - CLAUDE.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - sync
  - rebuild
  - scheduled
---

# Sync and Rebuild

## Components

Keeping the repo in sync with upstream `ailev/FPF` uses a two-layer automation stack:

| Layer | Where | What it does |
|-------|-------|--------------|
| GitHub Action | `.github/workflows/rebuild-sections.yml` | Runs `scripts/rebuild_all.sh` on push to main when `FPF-Spec.md` changes. Also runs on cron (1st and 15th of each month, 09:00 UTC) to auto-sync the fork. |
| Claude Code remote trigger | Managed at claude.ai/code/scheduled | Every 2 weeks runs [fpf-sync](../agents/fpf-sync.md). Same rebuild plus AI-enhancement passes on `_index.md` and `glossary-quick.md`. |
| PreToolUse hook | `.claude/settings.json` → `scripts/update_changelog.py` | Fires on every `git commit`. Bumps version in `plugin.json` and appends a changelog entry. |

## Data Flow

```
 (every 2 weeks)
 Claude Code scheduled trigger
           │
           ▼
    fpf-sync agent
           │
           ├──► 1. git fetch upstream; compare FPF-Spec.md hash
           │       (bail out if identical)
           │
           ├──► 2. git merge upstream/main --no-edit
           │       (bail on conflict)
           │
           ├──► 3. bash scripts/rebuild_all.sh
           │       (8 steps → sections/, metadata, routes, xrefs, embeddings)
           │
           ├──► 4. AI-enhance sections/**/_index.md
           │       (one-sentence plain-language summary per section)
           │
           ├──► 5. AI-enhance sections/glossary-quick.md
           │       (add plain-definition column)
           │
           └──► 6. git add sections/ && git commit && git push
                   (PreToolUse hook: bump version, append CHANGELOG entry)


 (orthogonal, on every push)
 GitHub Action
           │
           ├──► rebuild-sections.yml runs rebuild_all.sh
           │       (steps 1-7; step 8 skipped in CI — no uv)
           │
           └──► commits regenerated sections/ back to main if changed
```

## Decisions

- **Two independent update paths.** GitHub Action handles anything triggered by a push; Claude Code agent handles the scheduled upstream sync. They don't step on each other because both commit on main and the sync agent is idempotent.
- **AI enhancement is separate from mechanical rebuild.** `rebuild_all.sh` produces raw structures; the Sync agent rewrites `_index.md` summaries in plain language. Keeps the Python pipeline dependency-free while allowing LLM-quality summaries.
- **Version bumping is automatic.** The PreToolUse hook on `git commit` runs `update_changelog.py` which parses Conventional Commits and bumps `plugin.json` accordingly — `feat:` → minor, `fix:` → patch, `feat!:` → major, other types → changelog entry without bump.
- **Merge, never rebase.** The Sync agent's "what not to do" list explicitly forbids force-push or rebase. History stays linear-enough while preserving upstream-downstream provenance.

## Related

- [fpf-sync](../agents/fpf-sync.md)
- [build-pipeline](build-pipeline.md)
- [update_changelog](../modules/update_changelog.md)
- [changelog-workflow](../concepts/changelog-workflow.md)
