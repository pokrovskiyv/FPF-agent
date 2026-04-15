---
title: "Route 4: Comparison Selection"
sources:
  - sections/routes/route-4-comparison-selection.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - comparison-selection
---

# Route 4: Comparison Selection

> Source: `sections/routes/route-4-comparison-selection.md`

## Summary

Triggered when the user needs to choose between alternatives — "buy vs build vs fine-tune?", "framework A or B?", "trade-offs are opaque". Output is a decision criteria table, a comparison frame with explicit scale types, a checklist of evidence gaps, and a recommendation (or an explicit "do not pick a winner yet — these cells are empty" if data is missing).

## Key Decisions

- **Chain length:** 7 sections in full load, 3 core.
- **Core sections:** `A.19` (characteristic space), `G.0` (comparability governance), `A.19.CPM` (unified comparison mechanism).
- **Full chain:** adds `A.17` (characteristic rename), `A.18` (minimal CSLC in kernel), `A.19.SelectorMechanism` (selection kernel), `G.5` (multi-method dispatcher).

## Status

Active. Used for the `comparison_selection` burden. Reasoner template: "Decision criteria table → Evidence gaps → Recommendation". Key design constraint: empty cells stay empty until data is collected — no false ranking.

## Related

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
