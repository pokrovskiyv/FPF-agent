---
title: "Route 9: Composition Aggregation"
sources:
  - sections/routes/route-9-composition-aggregation.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - composition-aggregation
---

# Route 9: Composition Aggregation

> Source: `sections/routes/route-9-composition-aggregation.md`

## Summary

Triggered when KPIs lie, sum-of-parts doesn't equal the whole, or Tool A aggregates differently from Tool B. Output is a diagnosis of which composition invariants were violated, an aggregation dependency map, and concrete fix recommendations.

## Key Decisions

- **Chain length:** 6 sections in full load, 3 core.
- **Core sections:** `B.1` (universal algebra of aggregation Γ), `B.1.1` (dependency graph & proofs), `B.1.4` (contextual & temporal aggregation).
- **Full chain:** adds `B.1.2` (system-specific aggregation Γ_sys), `B.1.3` (knowledge-specific aggregation Γ_epist), `B.1.5` (order-sensitive method composition Γ_method).

## Status

Active. Used for the `composition_aggregation` burden. Reasoner template: "Diagnosis (violated invariants) → Dependency map → Fix recommendations".

## Related

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
