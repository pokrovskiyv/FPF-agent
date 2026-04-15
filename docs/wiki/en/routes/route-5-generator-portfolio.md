---
title: "Route 5: Generator Portfolio"
sources:
  - sections/routes/route-5-generator-portfolio.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - generator-portfolio
---

# Route 5: Generator Portfolio

> Source: `sections/routes/route-5-generator-portfolio.md`

## Summary

Triggered when the user asks "what's the state of the art in X?", "what approaches exist for Y?", or "I need a reusable scaffold to survey a field". Output is an overview of schools/approaches, a comparison table, a reusable template for future surveys, and a shortlist.

## Key Decisions

- **Chain length:** 7 sections in full load, 3 core.
- **Core sections:** `A.0` (onboarding glossary), `G.0` (comparability governance), `G.1` (CG-frame-ready generator).
- **Full chain:** adds `G.2` (SoTA harvester & synthesis), `G.5` (multi-method dispatcher), `B.5.2.1` (creative abduction with NQD), `C.17` (creativity-CHR).
- **Highest token budget** with Route 3 (1500 tokens) — surveys require broader context.

## Status

Active. Used for the `generator_portfolio` burden. Reasoner template: "Approaches list → Comparison table → Reusable scaffold → Shortlist".

## Related

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
