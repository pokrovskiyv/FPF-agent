---
title: Burden
sources:
  - skills/fpf/SKILL.md
  - agents/fpf-classifier.md
  - scripts/build_routes.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - concept
  - classification
---

# Burden

## Definition

In this project, **burden** is the name of the user's coordination problem. It's a label the Classifier attaches after reading the user's message — one of eleven values: 10 recognized types plus `semantic` (no route matches). Once assigned, the burden determines which route file the Retriever loads and which output template the Reasoner uses.

"Burden" is deliberately a neutral domain-internal term. It does **not** appear in the user-facing output — see [plain-language-contract](../architecture/plain-language-contract.md).

## How it works in the system

Burden classification happens in stage 2 of the Classifier. The classifier prompt contains a trigger table:

| Burden | Example user signals | Route |
|--------|--------------------|-------|
| `project_alignment` | "teams don't understand each other", "who owns what" | route-1 |
| `language_discovery` | "can't agree on terms", "vague idea" | route-2 |
| `boundary_unpacking` | "contract mixes everything", "SLA unclear" | route-3 |
| `comparison_selection` | "choose between options", "how to decide" | route-4 |
| `generator_portfolio` | "state of the art", "survey the field" | route-5 |
| `rewrite_explanation` | "rewrite for different audience" | route-6 |
| `ethical_assurance` | "hidden bias", "value conflicts" | route-7 |
| `trust_assurance` | "can we trust this metric", "overclaim" | route-8 |
| `composition_aggregation` | "KPIs lie", "sum of parts != whole" | route-9 |
| `evolution_learning` | "design is outdated", "feedback loop" | route-10 |
| `term_lookup` | explicit pattern ID (A.6, E.17, UTS) | metadata.json lookup |
| `semantic` | signal present, no route match | semantic fallback |
| `cross_cutting` | multiple burdens match | combined (Tier 3) |

The Reasoner has one output template per burden — see [fpf-reasoner](../agents/fpf-reasoner.md).

## Why these 10

The burden list was derived from observed usage of FPF patterns. Each burden maps onto a cluster of related patterns in the spec that, taken together, produce a complete answer to that kind of question. New burdens would require a new route file and a new Reasoner template.

## See also

- [fpf-classifier](../agents/fpf-classifier.md)
- [route-chain](route-chain.md)
- [tier](tier.md)
- [build_routes](../modules/build_routes.md)
- Route articles under `routes/`
