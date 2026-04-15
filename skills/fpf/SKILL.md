---
name: fpf
description: >
  Structure complex thinking: compare options, analyze specs/contracts,
  resolve team misunderstandings, audit trust/bias/ethics, debug misleading
  metrics, survey approaches in a field, structure handoffs, or make sense
  of messy multi-stakeholder situations. Triggers on any problem needing
  structured decomposition — not just teams, also solo analysis of complex
  systems. Also on explicit FPF terms (holon, UTS, DRR). Do NOT trigger
  for standard coding, simple bug fixes, or syntax questions.
---

# FPF Thinking Amplifier

Structured coordination analysis powered by the First Principles Framework.
FPF is invisible infrastructure — output is ALWAYS in plain language.
NEVER use FPF terminology in responses to the user.

## Base Path

All file paths in this skill and its agents are relative to `${CLAUDE_PLUGIN_ROOT}`.
When reading files, always prefix paths with `${CLAUDE_PLUGIN_ROOT}/`.

## How It Works

Three-tier architecture: routes as cache, semantic search as foundation.

1. Detect FPF signal in user's message (broader than burden matching)
2. Dispatch fpf-classifier to determine tier and route
3. **Tier 1 (route match):** Load curated section chain — fast, cheap, high quality
4. **Tier 2 (semantic fallback):** No route matches — retriever uses keyword + FAISS search to assemble dynamic chain
5. **Tier 3 (combined):** Multiple concerns — route core + semantic supplement
6. Apply FPF structure internally, deliver results in plain language

## Burden Classification

Detect from user's natural language — no FPF terms needed.

| Burden | User signals | Tier | Action |
|--------|-------------|------|--------|
| project_alignment | teams confused, responsibilities unclear | 1 | Route 1 → route-1-project-alignment.md |
| language_discovery | terminology disagreement, vague idea | 1 | Route 2 → route-2-language-discovery.md |
| boundary_unpacking | contract/SLA/API mixes rules and obligations | 1 | Route 3 → route-3-boundary-unpacking.md |
| comparison_selection | choosing between options, opaque decisions | 1 | Route 4 → route-4-comparison-selection.md |
| generator_portfolio | state-of-the-art survey, reusable scaffold | 1 | Route 5 → route-5-generator-portfolio.md |
| rewrite_explanation | rewrite preserving meaning, different audience | 1 | Route 6 → route-6-rewrite-explanation.md |
| ethical_assurance | bias audit, ethical assumptions, value conflicts | 1 | Route 7 → route-7-ethical-assurance.md |
| trust_assurance | trust metrics, overclaim, evidence aggregation | 1 | Route 8 → route-8-trust-assurance.md |
| composition_aggregation | KPIs lie, aggregation mismatch, sum != whole | 1 | Route 9 → route-9-composition-aggregation.md |
| evolution_learning | design drift, lessons learned, feedback loops | 1 | Route 10 → route-10-evolution-learning.md |
| term_lookup | explicit FPF term question | 1 | metadata.json → direct file load |
| semantic | FPF signal but no route match | 2 | Keyword + FAISS → dynamic chain |
| cross_cutting | multiple burdens match | 3 | Primary route + semantic supplement |

## Pipeline Depth (adaptive compute)

| Tier | Agents | Budget |
|------|--------|--------|
| 1: term_lookup | Retriever → Reasoner | ~800 tokens |
| 1: route-based | Retriever → Reasoner | ~1200-1500 tokens |
| 2: semantic | Retriever → Reasoner → Reviewer | ~2000 tokens |
| 3: combined | Retriever → Reasoner → Reviewer | ~2500 tokens |

## Confidence Gate

- High confidence (≥70%): auto-dispatch pipeline
- Low confidence (<70%): ask user "This looks like a coordination problem. Want me to help structure it?"
- Explicit FPF term: bypass confidence, auto-dispatch

## Key Files

- `sections/metadata.json` — instant pattern lookup (235 entries)
- `sections/routes/route-{1..10}.md` — ordered section chains per burden (10 routes)
- `sections/glossary-quick.md` — 50 core terms mapped to patterns
- `sections/lexical-rules.md` — mandatory terminology rules (internal only)
- `sections/embeddings/` — FAISS index for semantic search (rebuilt locally)

## Agents

- `agents/fpf-classifier.md` — burden detection + strategy
- `agents/fpf-retriever.md` — section loading + stagnation detection + semantic search
- `agents/fpf-reasoner.md` — applies structure, outputs plain language
- `agents/fpf-reviewer.md` — grounding + jargon guard
- `agents/fpf-sync.md` — scheduled upstream sync + rebuild pipeline
