---
title: "Route 8: Trust Assurance"
sources:
  - sections/routes/route-8-trust-assurance.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - trust-assurance
---

# Route 8: Trust Assurance

> Source: `sections/routes/route-8-trust-assurance.md`

## Summary

Triggered when the user asks "can we trust this metric?", "how do I aggregate confidence without overclaiming?", or "what's the evidence grounding for this system?" Output is an assurance profile per component (formality, scope, reliability, evidence), a dependency map, and an explicit list of evidence gaps — so weakest links are visible.

## Key Decisions

- **Chain length:** 5 sections in full load, 3 core.
- **Core sections:** `B.3` (trust & assurance calculus F-G-R with congruence), `B.3.5` (working-model relations & grounding), `B.1` (universal algebra of aggregation).
- **Full chain:** adds `B.1.1` (dependency graph & proofs) and `A.6.B` (boundary norm square).

## Status

Active. Used for the `trust_assurance` burden. Reasoner template: "Confidence per component table → Evidence gaps (where confidence is weakest) → Recommendations".

## Related

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
