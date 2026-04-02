# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

The **First Principles Framework (FPF)** specification (~59,000 lines) plus a **Claude Code Skill** that applies FPF to users' coordination problems — without exposing FPF terminology.

- `FPF-Spec.md` — upstream monolith (source of truth, do not edit directly)
- `sections/` — decomposed spec (~240 files), generated from the monolith
- `.claude/skills/fpf/SKILL.md` — skill entry point (burden-based routing)
- `.claude/agents/fpf-*.md` — agent team (Classifier → Retriever → Reasoner → Reviewer → Sync)
- `scripts/` — Python rebuild pipeline (no external deps)

## Plain Language Contract (non-negotiable)

FPF is **invisible infrastructure**. When the skill is active:
- Users speak their own language ("teams don't understand each other", "how to choose between options")
- Output is in their language — no "holon", "bounded context", "episteme", "transformer quartet", "CharacteristicSpace", pattern IDs, or any FPF terminology
- FPF patterns are applied internally by the Reasoner, never exposed

## Commands

```bash
# Full rebuild (after FPF-Spec.md changes)
./scripts/rebuild_all.sh

# Individual scripts
python3 scripts/split_spec.py          # FPF-Spec.md → sections/ (~240 files)
python3 scripts/build_metadata.py      # ToC → sections/metadata.json (235 entries)
python3 scripts/build_glossary.py      # → sections/glossary-quick.md (50 terms)
python3 scripts/build_lexical.py       # → sections/lexical-rules.md (Part K rules)
python3 scripts/build_routes.py        # → sections/routes/route-{1..6}.md
```

No external Python dependencies. All scripts use stdlib only.

## Navigating the Spec

**Do not read FPF-Spec.md directly** — it's 59K lines. Instead:

1. **By pattern ID** (e.g., A.6, E.17): look up in `sections/metadata.json` → `file` field → read that file
2. **By burden/route**: read `sections/routes/route-{1..6}.md` → follow the section chain
3. **By keyword**: search `sections/metadata.json` `keywords` and `queries` fields
4. **By Part**: read `sections/{directory}/_index.md` for a listing of all sections in that Part

Pattern IDs are hierarchical: `A.6.P` is a child of `A.6`, which belongs to Part A (dir `04-part-a-kernel-architecture-cluster`).

## Agent Team Architecture

| Agent | Role |
|-------|------|
| **fpf-classifier** | Detects coordination burden from user's natural language, selects route and pipeline depth via strategy table |
| **fpf-retriever** | Loads narrowest relevant sections using tiered retrieval (pattern ID → route chain → cross-refs → keyword fallback) |
| **fpf-reasoner** | Applies FPF structure to user's problem, outputs plain language. "Apply, don't explain." Generates structured artifacts (comparison tables, responsibility maps, term sheets, structured breakdowns) |
| **fpf-reviewer** | Validates grounding (claims traceable to sections) + jargon guard (catches FPF terminology leaking into output) |
| **fpf-sync** | Scheduled remote agent: syncs upstream fork, rebuilds sections, AI-enhances _index.md summaries |

Pipeline depth is adaptive: simple term lookups use Retriever only (~400 tokens), route-based queries add Reasoner (~1200), cross-cutting queries add Reviewer (~2000).

## Sync & Rebuild

Two-layer automatic update:

**GitHub Action** (`.github/workflows/rebuild-sections.yml`):
- Hook: push to main with FPF-Spec.md change → Python rebuild
- Cron: 1st and 15th, 7:00 UTC → auto-sync fork + rebuild

**Claude Code Remote Trigger** (bi-weekly):
- Same schedule → syncs upstream → Python rebuild → AI-enhances `_index.md` and `glossary-quick.md` with plain-language summaries
- Manage at: https://claude.ai/code/scheduled

## Lexical Rules (enforce when editing the spec)

- **NEVER** "axis" / "dimension" for measurable aspects → **Characteristic**
- **NEVER** "metric" as noun → `U.Measure` / Score
- **NEVER** "applicability" / "envelope" / "generality" as scope names → `U.ClaimScope`, `U.WorkScope`
- Full rules: `sections/lexical-rules.md`

## Six Entry Routes (burden-based)

| # | User's burden | Route file |
|---|--------------|------------|
| 1 | Teams confused about responsibilities / handoffs | `sections/routes/route-1-project-alignment.md` |
| 2 | Terminology disagreements / vague emerging ideas | `sections/routes/route-2-language-discovery.md` |
| 3 | Contract/SLA/API mixes rules, conditions, obligations | `sections/routes/route-3-boundary-unpacking.md` |
| 4 | Choosing between alternatives / opaque decisions | `sections/routes/route-4-comparison-selection.md` |
| 5 | State-of-the-art survey / portfolio scaffold needed | `sections/routes/route-5-generator-portfolio.md` |
| 6 | Rewrite for different audience / compare text versions | `sections/routes/route-6-rewrite-explanation.md` |

## Spec Structure (Parts A-K)

| Part | Content |
|------|---------|
| **A** | Kernel: ontology (holons, contexts, roles), transformation quartet, boundary discipline (A.6.*), constitutional principles |
| **B** | Trans-disciplinary reasoning: aggregation, trust calculus (F-G-R), evolution loop, abduction |
| **C** | Extensions: domain calculi, creativity/NQD, measurement, explore/exploit |
| **D** | Multi-scale ethics, conflict optimization |
| **E** | FPF constitution: pillars, authoring protocol, lexical law, multi-view publication (MVPK), DRR governance |
| **F** | Unification suite: concept-sets, SenseCells, bridges, UTS |
| **G** | SoTA patterns kit: harvesting, selector/dispatcher, portfolio governance |
| **H-K** | Glossary, annexes, indexes, lexical debt |
