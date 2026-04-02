---
name: fpf
description: >
  Use when work involves multiple specialists, teams, or AI agents
  that need coordination. Triggers on: teams misunderstanding each
  other, terminology disagreements, choosing between alternatives
  with explicit trade-offs, unpacking mixed contract/spec/SLA
  language, structuring decision-making, handing off work between
  teams, needing different reports for different audiences from
  the same work, organizing state-of-the-art knowledge, or when
  someone has a forming idea they cannot yet articulate clearly.
  Also triggers on explicit FPF terms (holon, UTS, DRR, bounded
  context). Do NOT trigger for standard coding, simple bug fixes,
  or single-person tasks.
---

# FPF Thinking Amplifier

Structured coordination analysis powered by the First Principles Framework.
FPF is invisible infrastructure — output is ALWAYS in plain language.
NEVER use FPF terminology in responses to the user.

## How It Works

1. Classify the user's problem into a burden type (see table below)
2. Dispatch the fpf-classifier agent to determine route and pipeline depth
3. Load only the sections needed (not the full 59K-line spec)
4. Apply FPF structure internally, deliver results in plain language

## Burden Classification

Detect from user's natural language — no FPF terms needed.

| Burden | User signals | Action |
|--------|-------------|--------|
| project_alignment | teams confused, responsibilities unclear, work handoff | Route 1 → sections/routes/route-1-project-alignment.md |
| language_discovery | terminology disagreement, vague idea, can't articulate | Route 2 → sections/routes/route-2-language-discovery.md |
| boundary_unpacking | contract/SLA/API mixes rules and obligations | Route 3 → sections/routes/route-3-boundary-unpacking.md |
| comparison_selection | choosing between options, opaque decision-making | Route 4 → sections/routes/route-4-comparison-selection.md |
| generator_portfolio | state-of-the-art survey, reusable scaffold needed | Route 5 → sections/routes/route-5-generator-portfolio.md |
| rewrite_explanation | rewrite preserving meaning, different audience | Route 6 → sections/routes/route-6-rewrite-explanation.md |
| term_lookup | explicit FPF term question | sections/metadata.json → direct file load |
| cross_cutting | multiple burdens match | Load multiple routes + sections/glossary-quick.md |

## Pipeline Depth (adaptive compute)

| Burden | Agents | Budget |
|--------|--------|--------|
| term_lookup | Retriever only | ~400 tokens |
| route-based | Retriever → Reasoner | ~1200 tokens |
| cross_cutting | Retriever → Reasoner → Reviewer | ~2000 tokens |

## Confidence Gate

- High confidence (≥70%): auto-dispatch pipeline
- Low confidence (<70%): ask user "This looks like a coordination problem. Want me to help structure it?"
- Explicit FPF term: bypass confidence, auto-dispatch

## Key Files

- `sections/metadata.json` — instant pattern lookup (235 entries)
- `sections/routes/route-*.md` — ordered section chains per burden
- `sections/glossary-quick.md` — 50 core terms mapped to patterns
- `sections/lexical-rules.md` — mandatory terminology rules (internal only)

## Agents

- `.claude/agents/fpf-classifier.md` — burden detection + strategy
- `.claude/agents/fpf-retriever.md` — section loading + stagnation detection
- `.claude/agents/fpf-reasoner.md` — applies structure, outputs plain language
- `.claude/agents/fpf-reviewer.md` — grounding + jargon guard
