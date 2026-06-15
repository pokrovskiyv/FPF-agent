---
title: FPF-agent Wiki (English)
last_updated: 2026-06-15T00:00:00Z
tags:
  - index
---

# FPF-agent Wiki

Auto-generated documentation for the **FPF-agent** plugin — a thinking amplifier that applies First Principles Framework patterns to user coordination problems without ever exposing FPF terminology. The plugin is dual-packaged (`.claude-plugin/` + `.codex-plugin/`) and installs into both **Claude Code** and **Codex CLI** (version 0.6.0).

## Project shape

The repo is a fork of `ailev/FPF` plus a skill and five agents that turn the 8.3 MB FPF specification into something queryable by ordinary users. Four moving parts: the spec monolith, ~279 generated section files, the skill entry point, and the agent team.

Key architectural reads:

- [Overview](architecture/overview.md) — components, data flow, and decisions
- [Skill Entry Point](architecture/skill-entry-point.md) — how the host dispatches the agents
- [Agent Team](architecture/agent-team.md) — the five agents and their contract
- [Three-Tier Retrieval](architecture/three-tier-retrieval.md) — routes as cache, semantic as fallback
- [Plain Language Contract](architecture/plain-language-contract.md) — the non-negotiable
- [Build Pipeline](architecture/build-pipeline.md) — the rebuild steps
- [Sync and Rebuild](architecture/sync-and-rebuild.md) — scheduled upstream merge

## Sections

| Section | Articles | Description |
|---------|----------|-------------|
| [Modules](modules/) | 13 | Python scripts that rebuild every generated artifact, plus the Codex plugin installer |
| [Agents](agents/) | 5 | Agent prompts (classifier, retriever, reasoner, reviewer, sync) |
| [Routes](routes/) | 10 | User-facing burden-to-pattern entry routes |
| [Architecture](architecture/) | 7 | System-level views |
| [Concepts](concepts/) | 5 | Project-internal vocabulary (not FPF domain terms) |

## Modules

Thirteen Python scripts orchestrating the rebuild pipeline, runtime semantic search, and the Codex plugin installer.

- [split_spec](modules/split_spec.md) — decompose the 8.3 MB monolith into ~279 section files
- [build_metadata](modules/build_metadata.md) — parse ToC into queryable `metadata.json` (292 entries)
- [enrich_metadata](modules/enrich_metadata.md) — add user-facing queries (EN+RU)
- [build_glossary](modules/build_glossary.md) — extract top-50 terms for reasoner orientation
- [build_lexical](modules/build_lexical.md) — Part K substitution rules
- [build_routes](modules/build_routes.md) — generate the 10 route files
- [build_xrefs](modules/build_xrefs.md) — inverted cross-reference graph per directory
- [build_embeddings](modules/build_embeddings.md) — FAISS index with bge-m3
- [semantic_search](modules/semantic_search.md) — runtime query CLI
- [install_codex_plugin](modules/install_codex_plugin.md) — installs/updates FPF as a Codex CLI plugin into a home-local marketplace (`~/plugins/fpf`)
- [test_smoke](modules/test_smoke.md) — pipeline integrity tests
- [smoke_codex](modules/smoke_codex.md) — Codex skill edition tests
- [update_changelog](modules/update_changelog.md) — PreToolUse commit hook

## Agents

- [fpf-classifier](agents/fpf-classifier.md) — burden detection and tier selection
- [fpf-retriever](agents/fpf-retriever.md) — section loading (route or semantic)
- [fpf-reasoner](agents/fpf-reasoner.md) — plain-language output
- [fpf-reviewer](agents/fpf-reviewer.md) — jargon guard + grounding + actionability
- [fpf-sync](agents/fpf-sync.md) — scheduled upstream sync

## Routes

Ten routes, each a curated section chain for one user burden.

- [Route 1: Project Alignment](routes/route-1-project-alignment.md)
- [Route 2: Language Discovery](routes/route-2-language-discovery.md)
- [Route 3: Boundary Unpacking](routes/route-3-boundary-unpacking.md)
- [Route 4: Comparison Selection](routes/route-4-comparison-selection.md)
- [Route 5: Generator Portfolio](routes/route-5-generator-portfolio.md)
- [Route 6: Rewrite Explanation](routes/route-6-rewrite-explanation.md)
- [Route 7: Ethical Assurance](routes/route-7-ethical-assurance.md)
- [Route 8: Trust Assurance](routes/route-8-trust-assurance.md)
- [Route 9: Composition Aggregation](routes/route-9-composition-aggregation.md)
- [Route 10: Evolution Learning](routes/route-10-evolution-learning.md)

## Concepts

Project-internal vocabulary. These are not FPF domain terms — they're how we talk about the skill's own internals.

- [Burden](concepts/burden.md)
- [Route Chain](concepts/route-chain.md)
- [Tier](concepts/tier.md)
- [Pipeline Depth](concepts/pipeline-depth.md)
- [Changelog Workflow](concepts/changelog-workflow.md)

## Glossary

See [Glossary](glossary.md) for a single-page reference of all terms used across these articles.

## Other language

[Russian wiki](../ru/index.md) — primary user-facing documentation.
