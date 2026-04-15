---
title: fpf-sync
sources:
  - agents/fpf-sync.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - agent
  - sync
  - scheduled
  - maintenance
---

# fpf-sync

> Source: `agents/fpf-sync.md`

## Purpose

Scheduled maintenance agent (runs every 2 weeks via Claude Code's remote trigger system on the 1st and 15th of each month). Syncs the local fork with upstream `ailev/FPF`, runs the full Python rebuild pipeline, then performs AI enhancement passes on `_index.md` files and `glossary-quick.md` to add plain-language summaries. Commits and pushes all changes.

Unlike the other agents, fpf-sync never interacts with an end user — it's pure project maintenance.

## Interface

**Input:** none (scheduled trigger).

**Output:** git commits on the main branch (`chore: sync upstream + AI-enhanced indexes`) plus a log of what was enhanced.

## The six steps

1. **Check upstream.** `git fetch upstream main`, compare `FPF-Spec.md` hashes. If identical → log "No upstream changes" and stop (saves compute).
2. **Merge.** `git merge upstream/main --no-edit`. Conflicts → stop and report, never force-resolve.
3. **Rebuild.** `bash scripts/rebuild_all.sh` — regenerates `sections/`, `metadata.json`, `glossary-quick.md`, `lexical-rules.md`, routes, xrefs, and the FAISS embeddings index. The embeddings step requires `uv`.
4. **AI-enhance `_index.md`.** For each directory with an `_index.md`, read the first 30 lines of each listed section file and rewrite the index with one-sentence plain-language summaries — focused on what problem each section helps solve, max 120 chars, no FPF terminology.
5. **AI-enhance `glossary-quick.md`.** For each of 50 terms, read the first 20 lines of its source section and add a plain-definition column (max 80 chars). Final table shape: `| Term | Primary Pattern | Plain Definition |`.
6. **Commit + push.** `git add sections/ && git commit -m "chore: sync upstream + AI-enhanced indexes" && git push`.

## Explicit "do not"

The source lists invariants the agent must never violate:

- No modifications to `FPF-Spec.md` (upstream source of truth)
- No modifications to `scripts/`, `agents/`, or `skills/` (maintained manually)
- No force-push, no rebase — always merge
- No FPF terminology in any enhanced summary
- Do not run when upstream has no changes

## Triggering

Two layers documented in CLAUDE.md:

- **GitHub Action** (`.github/workflows/rebuild-sections.yml`) on pushes to main and cron on the 1st and 15th. Runs the Python rebuild only.
- **Claude Code Remote Trigger** every 2 weeks. Runs the full sync + rebuild + AI-enhance flow described above.

## See also

- [sync-and-rebuild](../architecture/sync-and-rebuild.md)
- [build-pipeline](../architecture/build-pipeline.md)
- [agent-team](../architecture/agent-team.md)
- `.github/workflows/rebuild-sections.yml`
