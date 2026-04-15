---
title: Overview
sources:
  - CLAUDE.md
  - Readme.md
  - .claude-plugin/plugin.json
  - .claude-plugin/marketplace.json
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - overview
---

# Overview

## What this repository is

The **First Principles Framework (FPF)** specification (~61 000 lines, 5.5 MB, ~1.3 M tokens) plus a **Claude Code Skill** that applies FPF patterns to user coordination problems — while keeping all FPF terminology invisible.

The project has four moving parts on disk:

| Layer | Location | What it holds |
|-------|----------|---------------|
| **Spec monolith** | `FPF-Spec.md` | Upstream source of truth; never edited directly |
| **Decomposed sections** | `sections/` | ~240 generated files + metadata.json + routes + xrefs + FAISS index |
| **Skill entry** | `skills/fpf/SKILL.md` | Burden-based routing logic read by Claude Code |
| **Agent team** | `agents/fpf-*.md` | Five agents: classifier, retriever, reasoner, reviewer, sync |

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

## Decisions

- **Plain language contract.** FPF terminology never leaks to the user. See [plain-language-contract](plain-language-contract.md).
- **Three-tier retrieval.** Routes as cache, semantic search as fallback, combined for cross-cutting. See [three-tier-retrieval](three-tier-retrieval.md).
- **Stdlib-only rebuild.** All scripts except the two embedding-related ones use only Python stdlib; embeddings declare deps inline via PEP 723 and run under `uv`.
- **Upstream-friendly fork.** The spec stays in sync with `ailev/FPF` upstream via a scheduled sync agent. See [sync-and-rebuild](sync-and-rebuild.md).

## See also

- [skill-entry-point](skill-entry-point.md)
- [build-pipeline](build-pipeline.md)
- [agent-team](agent-team.md)
