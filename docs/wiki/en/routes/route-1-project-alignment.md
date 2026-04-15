---
title: "Route 1: Project Alignment"
sources:
  - sections/routes/route-1-project-alignment.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - project-alignment
---

# Route 1: Project Alignment

> Source: `sections/routes/route-1-project-alignment.md`

## Summary

Triggered when the user says things like: "teams don't understand each other", "responsibilities are unclear", "who owns what?", or "we need to hand off work but the boundary is fuzzy". Returns a map of who owns what, how work flows between teams, and where the gaps are.

## Key Decisions

- **Chain length:** 8 sections in full load, 3 marked core for minimum load.
- **Core sections:** `A.1.1` (semantic frame), `A.15` (role-method-work alignment), `B.5.1` (explore → shape → evidence → operate).
- **Full chain:** adds work plan and slot filling details (`A.15.2`, `A.15.3`), method harmonisation (`F.11`), cross-context alignment (`F.9`), and the unified term sheet (`F.17`).

## Status

Active. Used for the `project_alignment` burden detected by the Classifier. Output template (from the Reasoner) is "Responsibility areas → Work flow between teams → Gaps with owner".

## Related

- [fpf-classifier](../agents/fpf-classifier.md) — selects this route
- [fpf-retriever](../agents/fpf-retriever.md) — loads the chain
- [fpf-reasoner](../agents/fpf-reasoner.md) — applies the project_alignment template
- [route-chain](../concepts/route-chain.md)
