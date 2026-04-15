---
title: "Route 10: Evolution Learning"
sources:
  - sections/routes/route-10-evolution-learning.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - evolution-learning
---

# Route 10: Evolution Learning

> Source: `sections/routes/route-10-evolution-learning.md`

## Summary

Triggered when the design is outdated and nobody noticed, the feedback loop between operations and design is broken, or lessons learned keep recurring. Output is a current cycle map showing where the loop is broken, a loop-closure plan, and cycle-health indicators with target values.

## Key Decisions

- **Chain length:** 5 sections in full load, 3 core.
- **Core sections:** `B.4` (canonical evolution loop), `B.4.1` (observe → notice → stabilize → route), `B.5.1` (explore → shape → evidence → operate).
- **Full chain:** adds `A.4` (temporal duality & open-ended evolution) and `G.11` (telemetry-driven refresh & decay orchestrator).

## Status

Active. Used for the `evolution_learning` burden. Reasoner template: "Current cycle map → Break point → Loop closure plan → Cycle health indicators".

## Related

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
