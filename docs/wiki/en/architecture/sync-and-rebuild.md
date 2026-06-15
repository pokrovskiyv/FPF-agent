---
title: Sync and Rebuild
sources:
  - agents/fpf-sync.md
  - scripts/rebuild_all.sh
  - scripts/update_changelog.py
  - CLAUDE.md
last_updated: 2026-06-15T07:00:00Z
tags:
  - architecture
  - sync
  - rebuild
  - scheduled
---

# Sync and Rebuild

## Components

Keeping the repo in sync with upstream `ailev/FPF` uses a single-layer automation stack:

| Layer | Where | What it does |
|-------|-------|--------------|
| Claude Code remote routine | `trig_01P7UzjrjgsgzLpMHn84bMoo` — managed at claude.ai/code/routines | 1st and 15th of each month at 07:00 UTC. Fetches upstream, compares `FPF-Spec.md` hash, merges if changed, rebuilds sections, AI-enhances indexes and glossary, compiles the wiki, updates changelog, and pushes. |
| PreToolUse hook | `.claude/settings.json` → `scripts/update_changelog.py` | Fires on every `git commit`. Bumps version in `plugin.json` and appends a changelog entry. |

Note: A previous GitHub Action (`.github/workflows/rebuild-sections.yml`) covered the same flow but consistently failed and was removed. The remote routine replaces it.

## Data Flow

```
 (1st and 15th of each month, 07:00 UTC)
 Claude Code scheduled routine
           │
           ▼
    fpf-sync agent
           │
           ├──► 1. git fetch upstream; compare FPF-Spec.md hash
           │       (bail out if identical)
           │
           ├──► 2. git merge upstream/main --no-edit
           │       (resolve expected Readme.md conflict; bail on any other)
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
           ├──► 6. /wiki compile
           │       (incremental update of docs/wiki/ru/ and docs/wiki/en/)
           │
           ├──► 7. Append What's New to CHANGELOG.md; bump version if needed
           │
           └──► 8. git add sections/ docs/wiki/ CHANGELOG.md && git commit && git push
                   (PreToolUse hook: bump version, append CHANGELOG entry)
```

## Decisions

- **Single scheduled path.** The Claude Code remote routine owns the full sync cycle. No GitHub Action duplication — the previous Action consistently failed and was removed.
- **AI enhancement is separate from mechanical rebuild.** `rebuild_all.sh` produces raw structures; the Sync agent rewrites `_index.md` summaries in plain language. Keeps the Python pipeline dependency-free while allowing LLM-quality summaries.
- **Version bumping is automatic.** The PreToolUse hook on `git commit` runs `update_changelog.py` which parses Conventional Commits and bumps `plugin.json` accordingly — `feat:` → minor, `fix:` → patch, `feat!:` → major, other types → changelog entry without bump.
- **Merge, never rebase.** The Sync agent's "what not to do" list explicitly forbids force-push or rebase. History stays linear-enough while preserving upstream-downstream provenance.

## Related

- [fpf-sync](../agents/fpf-sync.md)
- [build-pipeline](build-pipeline.md)
- [update_changelog](../modules/update_changelog.md)
- [changelog-workflow](../concepts/changelog-workflow.md)
