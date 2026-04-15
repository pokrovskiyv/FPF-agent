---
title: Agent Team
sources:
  - agents/fpf-classifier.md
  - agents/fpf-retriever.md
  - agents/fpf-reasoner.md
  - agents/fpf-reviewer.md
  - agents/fpf-sync.md
  - skills/fpf/SKILL.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - agents
---

# Agent Team

## Components

Five agents, each a markdown prompt file under `agents/`:

| Agent | Module | Role |
|-------|--------|------|
| **Classifier** | [fpf-classifier](../agents/fpf-classifier.md) | Decide if there's a signal worth processing, pick a tier and route, set budget |
| **Retriever** | [fpf-retriever](../agents/fpf-retriever.md) | Load the minimum sections — route chain (Mode A) or semantic search (Mode B) |
| **Reasoner** | [fpf-reasoner](../agents/fpf-reasoner.md) | Apply the pattern structure to the user's problem, output in plain language |
| **Reviewer** | [fpf-reviewer](../agents/fpf-reviewer.md) | Quality gate: jargon check, grounding check, actionability check (Tier 2/3 only) |
| **Sync** | [fpf-sync](../agents/fpf-sync.md) | Scheduled maintenance: upstream sync + rebuild + AI-enhanced indexes |

## Data Flow

```
user message
     │
     ▼
┌──────────────┐
│ Classifier   │──► SIGNAL? TIER? BURDEN? ROUTE? BUDGET?
└──────────────┘
     │
     ▼
┌──────────────┐        reads: routes/*.md, metadata.json,
│ Retriever    │───────►         _xref.md, semantic_search.py
└──────────────┘
     │
     ▼  loaded section content
┌──────────────┐        reads (internal only): glossary-quick.md,
│ Reasoner     │───────►                          lexical-rules.md
└──────────────┘
     │                    plain-language output
     │
     ├──► user  (Tier 1 — simple route)
     │
     ▼  (Tier 2/3 or Tier 1 cross-cutting)
┌──────────────┐
│ Reviewer     │──► STATUS: PASS | CORRECTED
└──────────────┘
     │
     ▼
user


(separate, scheduled, no user interaction)
┌──────────────┐
│ Sync         │──► git pull upstream + rebuild_all.sh + AI-enhance indexes
└──────────────┘
```

## Decisions

- **Separate concerns, compose by pipeline.** Each agent has one responsibility with explicit input/output — Classifier only decides, Retriever only loads, Reasoner only writes user-facing prose, Reviewer only validates. This keeps prompts short and independently testable.
- **Adaptive pipeline depth.** Tier 1 simple queries use Retriever → Reasoner (~800 tokens). Tier 1 route queries use ~1200–1500 tokens. Tier 2 semantic queries add Reviewer (~2000 tokens). Tier 3 combined adds all three (~2500 tokens). See [pipeline-depth](../concepts/pipeline-depth.md).
- **Plain language is a contract, not a preference.** The Reasoner's Principle #0 and the Reviewer's Check 1 together enforce zero FPF terminology in user output. See [plain-language-contract](plain-language-contract.md).
- **Sync is out-of-band.** It runs on a schedule, never on user queries. Its commits pass through the same changelog hook ([update_changelog](../modules/update_changelog.md)) as regular commits.

## Related

- [skill-entry-point](skill-entry-point.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [plain-language-contract](plain-language-contract.md)
- [burden](../concepts/burden.md)
- [tier](../concepts/tier.md)
- [pipeline-depth](../concepts/pipeline-depth.md)
