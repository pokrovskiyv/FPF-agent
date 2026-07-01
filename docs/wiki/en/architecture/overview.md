---
title: Overview
sources:
  - .claude-plugin/marketplace.json
  - .claude-plugin/plugin.json
  - CLAUDE.md
  - Readme.md
last_updated: 2026-07-01T07:00:00Z
tags:
  - architecture
  - overview
  - packaging
---

# Overview

## What this repository is

The **First Principles Framework (FPF)** specification (~94 000 lines) plus a **skill** that applies FPF patterns to user coordination problems — while keeping all FPF terminology invisible.

The project is **dual-packaged**: the same repository is a plugin for **Claude Code** (via `.claude-plugin/`) and for **Codex CLI** (via `.codex-plugin/` + a home-local marketplace). Current version: **0.6.3** (kept in lockstep across both manifests).

The moving parts on disk:

| Layer | Location | What it holds |
|-------|----------|---------------|
| **Spec monolith** | `FPF-Spec.md` | Upstream source of truth; never edited directly |
| **Decomposed sections** | `sections/` | ~307 generated files + metadata.json + routes + xrefs + FAISS index |
| **Skill entry (Claude Code)** | `skills/fpf/SKILL.md` | Burden-based routing logic read by Claude Code |
| **Skill entry (Codex CLI)** | `.agents/skills/fpf/SKILL.md` | Same skill, surfaced to Codex |
| **Agent team** | `agents/fpf-*.md` | Five agents: classifier, retriever, reasoner, reviewer, sync |
| **Claude Code manifest** | `.claude-plugin/` | `plugin.json` + `marketplace.json` |
| **Codex CLI manifest** | `.codex-plugin/` | `plugin.json` pointing the skill at `.agents/skills/` |
| **Codex installer** | `scripts/install_codex_plugin.py` | Builds a home-local package in `~/plugins/fpf` and registers it in `~/.agents/plugins/marketplace.json` |

## Components

| Component | Module | Role |
|-----------|--------|------|
| Pipeline driver | [rebuild_all.sh](build-pipeline.md) | Orchestrates the 8-step rebuild |
| Spec decomposer | [split_spec](../modules/split_spec.md) | Splits the monolith into section files |
| Index builder | [build_metadata](../modules/build_metadata.md) | Parses ToC into metadata.json |
| Metadata enricher | [enrich_metadata](../modules/enrich_metadata.md) | Adds user-facing queries (EN+RU) |
| Glossary | [build_glossary](../modules/build_glossary.md) | Top-50 term frequency table |
| Lexical rules | [build_lexical](../modules/build_lexical.md) | Mandatory term substitutions |
| Routes | [build_routes](../modules/build_routes.md) | 10 curated burden chains |
| Cross-references | [build_xrefs](../modules/build_xrefs.md) | Inverted dependency graph per directory |
| Embeddings | [build_embeddings](../modules/build_embeddings.md) | FAISS + bge-m3 |
| Query CLI | [semantic_search](../modules/semantic_search.md) | Runtime semantic search |
| Codex installer | [install_codex_plugin](../modules/install_codex_plugin.md) | Home-local Codex package + marketplace entry |
| Classifier | [fpf-classifier](../agents/fpf-classifier.md) | Burden detection |
| Retriever | [fpf-retriever](../agents/fpf-retriever.md) | Section loading |
| Reasoner | [fpf-reasoner](../agents/fpf-reasoner.md) | Plain-language output |
| Reviewer | [fpf-reviewer](../agents/fpf-reviewer.md) | Quality gate (Tier 2/3) |
| Sync | [fpf-sync](../agents/fpf-sync.md) | Scheduled upstream sync |
| Changelog hook | [update_changelog](../modules/update_changelog.md) | PreToolUse version + changelog bump |

## Data Flow

```
FPF-Spec.md  ──split_spec──►  sections/*/**.md
                                     │
                                     ├──build_metadata──►  metadata.json
                                     │                          │
                                     │                    enrich_metadata
                                     │                          │
                                     ├──build_glossary──►  glossary-quick.md
                                     ├──build_lexical──►   lexical-rules.md
                                     ├──build_routes──►    routes/route-*.md
                                     ├──build_xrefs──►     */_xref.md
                                     └──build_embeddings──► embeddings/{faiss,meta,config}

User message ──► fpf-classifier ──► fpf-retriever ──► fpf-reasoner ──► user
                                         │                │
                                         ▼                ▼
                        (reads) routes / metadata / xrefs / semantic_search
                                                          │
                                                          ▼ (optional, Tier 2/3)
                                                      fpf-reviewer
```

### Two install paths

Both runtimes consume the same repository; only the entry manifest differs.

```
Claude Code:  /plugin marketplace add pokrovskiyv/FPF-agent
              └─ reads .claude-plugin/marketplace.json → installs plugin "fpf"
              └─ updates pulled automatically on pushes to main

Codex CLI:    codex plugin marketplace add pokrovskiyv/FPF-agent
              └─ repo root is the Codex plugin: .codex-plugin/plugin.json
              └─ skill served from .agents/skills/fpf/

Codex (local, no marketplace UI):
              python3 scripts/install_codex_plugin.py
              └─ builds ~/plugins/fpf from repo root
              └─ registers it in ~/.agents/plugins/marketplace.json
              └─ refresh: git pull && python3 scripts/install_codex_plugin.py
```

## Decisions

- **Dual packaging.** A single repository ships as both a Claude Code plugin (`.claude-plugin/`) and a Codex CLI plugin (`.codex-plugin/` + `scripts/install_codex_plugin.py`). There is no fork: the Codex skill is served from `.agents/skills/fpf/`, and the two `plugin.json` files carry the same version.
- **Plain language contract.** FPF terminology never leaks to the user. See [plain-language-contract](plain-language-contract.md).
- **Three-tier retrieval.** Routes as cache, semantic search as fallback, combined for cross-cutting. See [three-tier-retrieval](three-tier-retrieval.md).
- **Stdlib-only rebuild.** All scripts except the two embedding-related ones use only Python stdlib; embeddings declare deps inline via PEP 723 and run under `uv`.
- **Version lockstep.** The PreToolUse changelog hook (`scripts/update_changelog.py`) auto-bumps only `.claude-plugin/plugin.json`. The scheduled sync routine manually bumps **both** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` so they never drift.
- **Single update path.** Upstream sync runs through one mechanism only — the Claude Code Remote Routine (`trig_01P7UzjrjgsgzLpMHn84bMoo`, cron on the 1st and 15th at 07:00 UTC). The earlier GitHub Action no longer exists. See [sync-and-rebuild](sync-and-rebuild.md).

## See also

- [skill-entry-point](skill-entry-point.md)
- [build-pipeline](build-pipeline.md)
- [agent-team](agent-team.md)
- [sync-and-rebuild](sync-and-rebuild.md)
