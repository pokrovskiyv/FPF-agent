---
title: Agent Team
sources:
  - agents/fpf-classifier.md
  - agents/fpf-retriever.md
  - agents/fpf-reasoner.md
  - agents/fpf-reviewer.md
  - agents/fpf-sync.md
  - skills/fpf/SKILL.md
last_updated: 2026-07-01T07:00:00Z
tags:
  - architecture
  - agents
---

# Agent Team

## Components

Five agents, each a markdown prompt file under `agents/`. Four run inline on
user queries; the fifth runs out-of-band on a schedule.

| Agent | Module | Role |
|-------|--------|------|
| **Classifier** | [fpf-classifier](../agents/fpf-classifier.md) | Decide if there's an FPF signal worth processing, pick a tier and route, set the token budget |
| **Retriever** | [fpf-retriever](../agents/fpf-retriever.md) | Load the minimum sections — route chain (Mode A) or keyword + FAISS semantic search (Mode B) |
| **Reasoner** | [fpf-reasoner](../agents/fpf-reasoner.md) | Apply the pattern structure to the user's problem, output in plain language (zero FPF jargon) |
| **Reviewer** | [fpf-reviewer](../agents/fpf-reviewer.md) | Quality gate: jargon guard, grounding check, actionability check (Tier 2/3 + Tier 1 cross-cutting only) |
| **Sync** | [fpf-sync](../agents/fpf-sync.md) | Scheduled maintenance: upstream sync + rebuild + AI-enhanced indexes + bilingual wiki refresh |

## Data Flow

The four query-time agents compose into an adaptive pipeline. The Classifier
decides depth; not every query reaches the Reviewer.

```
user message
     │
     ▼
┌──────────────┐
│ Classifier   │──► SIGNAL? TIER? BURDEN? ROUTE? BUDGET? SEARCH_QUERY?
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


(separate, scheduled, no user interaction — Claude Code Remote Routine)
┌──────────────┐
│ Sync         │──► 8-step cycle: sync upstream + rebuild_all.sh
└──────────────┘     + AI-enhance indexes + /wiki compile + commit
```

The agents communicate by passing structured text. The Classifier emits a
`SIGNAL / TIER / BURDEN / ROUTE / BUDGET / SECTIONS / SEARCH_QUERY` block; the
Retriever returns loaded section content with citations; the Reasoner emits
plain-language output; the Reviewer returns `STATUS: PASS | CORRECTED`. See
[three-tier-retrieval](three-tier-retrieval.md) for how the Retriever's two
modes map to the tiers.

### Sync: the 8-step maintenance cycle

The Sync agent is not part of the query pipeline. It is driven by the **Claude
Code Remote Routine** (trigger `trig_01P7UzjrjgsgzLpMHn84bMoo`) on cron — the
1st and 15th of each month at 07:00 UTC (= 09:00 Europe/Belgrade), managed at
<https://claude.ai/code/routines/trig_01P7UzjrjgsgzLpMHn84bMoo>. There is a
single update path: the routine reads `agents/fpf-sync.md` each run and follows
its eight steps.

1. **Check upstream** — `git fetch upstream main`, compare `FPF-Spec.md` hashes.
   If unchanged, skip Steps 2–5 but still check wiki freshness (Step 6).
2. **Merge upstream** — `git merge upstream/main --no-edit`. A `Readme.md`
   conflict is expected (our fork's README is plugin-focused) and is
   auto-resolved with `git checkout --ours Readme.md && git add Readme.md`.
   ANY other conflict stops the run and reports.
3. **Rebuild** — `bash scripts/rebuild_all.sh` regenerates `sections/`,
   `metadata.json`, glossary, lexical rules, routes, and the FAISS embeddings
   index.
4. **AI-enhance `_index.md`** — write a one-sentence plain-language summary for
   each section in every directory's `_index.md`.
5. **AI-enhance `glossary-quick.md`** — add a plain-language definition column
   for each of the 50 terms.
6. **Compile the bilingual wiki** — `python3 ~/.claude/skills/wiki/scanner.py
   check .`, then `/wiki compile` if stale. Regenerates both `docs/wiki/ru/`
   and `docs/wiki/en/` and updates `docs/wiki/.state/manifest.json`.
7. **Changelog + version** — append a "What's New" section to `CHANGELOG.md`
   and bump the version in BOTH `.claude-plugin/plugin.json` and
   `.codex-plugin/plugin.json` (kept in lockstep).
8. **Commit and push** — `git add sections/ docs/wiki/ CHANGELOG.md
   .claude-plugin/plugin.json .codex-plugin/plugin.json`, then commit with
   message `chore: sync upstream + rebuild + AI-enhanced indexes + wiki refresh`
   and `git push`.

## Decisions

- **Separate concerns, compose by pipeline.** Each query-time agent has one
  responsibility with explicit input/output — Classifier only decides,
  Retriever only loads, Reasoner only writes user-facing prose, Reviewer only
  validates. This keeps prompts short and independently testable.
- **Adaptive pipeline depth.** Tier 1 simple queries use Retriever → Reasoner
  (~800 tokens). Tier 1 route queries use ~1200–1500 tokens. Tier 2 semantic
  queries add Reviewer (~2000 tokens). Tier 3 combined adds all three
  (~2500 tokens). See [pipeline-depth](../concepts/pipeline-depth.md).
- **Plain language is a contract, not a preference.** The Reasoner's
  Principle #0 and the Reviewer's Check 1 together enforce zero FPF terminology
  in user output. See [plain-language-contract](plain-language-contract.md).
- **Sync is out-of-band and single-path.** It runs only on the scheduled
  remote routine, never on user queries. A previous GitHub Action
  (`.github/workflows/rebuild-sections.yml`) covered the same flow but
  consistently failed and was removed — the remote routine is now the only sync
  mechanism.
- **Dual-plugin packaging stays in lockstep.** The project ships as a plugin for
  BOTH Claude Code (`.claude-plugin/`) and Codex CLI (`.codex-plugin/` plus
  `scripts/install_codex_plugin.py` and a home-local marketplace). The
  PreToolUse changelog hook (`scripts/update_changelog.py`) auto-bumps only
  `.claude-plugin/plugin.json`, so Sync Step 7 manually bumps both `plugin.json`
  files to keep their versions aligned. Current version: 0.6.3.

## Related

- [skill-entry-point](skill-entry-point.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [plain-language-contract](plain-language-contract.md)
- [burden](../concepts/burden.md)
- [tier](../concepts/tier.md)
- [pipeline-depth](../concepts/pipeline-depth.md)
