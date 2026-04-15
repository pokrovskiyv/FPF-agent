---
title: fpf-reasoner
sources:
  - agents/fpf-reasoner.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - agent
  - reasoner
  - plain-language
---

# fpf-reasoner

> Source: `agents/fpf-reasoner.md`

## Purpose

Third agent and the one that speaks to the user. Reads the FPF patterns loaded by the Retriever, applies their internal structure to the user's specific situation, and returns a practical, actionable result in the user's language. **The Reasoner never exposes FPF terminology** — no pattern IDs, no "holon", no "bounded context", no "U.anything". The source file calls this "Principle #0: Plain Language Contract".

The analogy in the source: the Reasoner is a GPS. It uses Dijkstra's algorithm internally. It tells the user "turn right in 200 meters." It never says "applying shortest-path algorithm to weighted graph."

## Interface

**Input:** loaded sections from the Retriever + the user's original question + the Classifier's burden label.

**Output:** a structured response matching one of ten burden-specific templates (one per route), or the `semantic` universal template when no route applies.

## Output templates

Eleven templates in total, one per burden plus the universal semantic fallback. Each has a fixed skeleton the Reasoner fills with content specific to the user's situation:

| Burden | Skeleton (header level) |
|--------|------------------------|
| `project_alignment` | Responsibility areas → Work flow → Gaps |
| `language_discovery` | Term table → Recommended action |
| `boundary_unpacking` | Rules → Access conditions → Obligations → Evidence required |
| `comparison_selection` | Criteria table → Evidence gaps → Recommendation |
| `generator_portfolio` | Approaches list → Comparison table → Reusable scaffold |
| `rewrite_explanation` | Rewritten text → What preserved / changed |
| `ethical_assurance` | Conflict map → Bias register → Audit checklist |
| `trust_assurance` | Confidence per component → Evidence gaps → Recommendations |
| `composition_aggregation` | Diagnosis → Dependency map → Fix recommendations |
| `evolution_learning` | Cycle map → Break point → Loop closure plan → Health indicators |
| `semantic` (universal) | Situation → Key insights → Recommendations → Watch points |

## Always load

Before generating, the Reasoner always reads two internal helpers:

- `sections/glossary-quick.md` — for internal orientation
- `sections/lexical-rules.md` — to enforce term substitutions silently (never exposed)

## Guided route mode

For route-based queries the Reasoner is instructed to walk the analysis step by step rather than dumping everything at once. Start with the most relevant insight from the first core section, build on it with the next section's structure, end with actionable next steps.

## Position in the pipeline

```
retriever → [fpf-reasoner] → (optional: reviewer) → output
```

For Tier 1, the Reasoner's output goes directly to the user. For Tier 2/3 the Reviewer runs afterwards as a jargon-guard and grounding check.

## See also

- [fpf-retriever](fpf-retriever.md) — feeds sections
- [fpf-reviewer](fpf-reviewer.md) — downstream quality gate
- [plain-language-contract](../architecture/plain-language-contract.md)
- [build_lexical](../modules/build_lexical.md) — produces the lexical rules file the Reasoner enforces
