---
title: "Route 3: Boundary Unpacking"
sources:
  - sections/routes/route-3-boundary-unpacking.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - boundary-unpacking
---

# Route 3: Boundary Unpacking

> Source: `sections/routes/route-3-boundary-unpacking.md`

## Summary

Triggered when the user has a contract, API spec, SLA, or technical specification that mixes rules, conditions, obligations, and evidence requirements into one soup. Output is a structured breakdown that separates: what's a rule, what's an access condition, what's an obligation, what needs to be proven.

## Key Decisions

- **Chain length:** 6 sections in full load, 3 core.
- **Core sections:** `A.6` (signature stack & boundary discipline), `A.6.B` (boundary norm square), `A.6.C` (contract unpacking).
- **Full chain:** adds relational precision (`A.6.P`), quality-term precision (`A.6.Q`), and action invitation precision (`A.6.A`).
- **Highest token budget** of the Tier 1 routes (1500 tokens) because contracts tend to require more context.

## Status

Active. Used for the `boundary_unpacking` burden. Reasoner template: "Rules / Access conditions / Obligations / Evidence required" — four fixed quadrants.

## Related

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
