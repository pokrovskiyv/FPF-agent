---
title: "Route 6: Rewrite Explanation"
sources:
  - sections/routes/route-6-rewrite-explanation.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - rewrite-explanation
---

# Route 6: Rewrite Explanation

> Source: `sections/routes/route-6-rewrite-explanation.md`

## Summary

Triggered when the user says "rewrite without changing the meaning", "explain this for a different audience", or "compare these two versions for faithfulness". Output is the rewritten text plus notes on what was preserved and what was changed, plus a faithfulness profile — so the rewrite isn't a silent translation.

## Key Decisions

- **Chain length:** 5 sections in full load (shortest Tier 1 route), 3 core.
- **Core sections:** `A.6.3.CR` (conservative retextualization), `A.6.3.RT` (representation transduction), `E.17.EFP` (explanation faithfulness profile).
- **Full chain:** adds `E.17.ID.CR` (comparative reading) and `E.17.AUD.LHR` (local head restoration).

## Status

Active. Used for the `rewrite_explanation` burden. Reasoner template: "Rewritten text → What was preserved → What was changed (with rationale)".

## Related

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
