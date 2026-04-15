---
title: "Route 2: Language Discovery"
sources:
  - sections/routes/route-2-language-discovery.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - route
  - tier-1
  - language-discovery
---

# Route 2: Language Discovery

> Source: `sections/routes/route-2-language-discovery.md`

## Summary

Triggered when the user says things like: "we can't agree on terminology", "everyone means something different", "I have a vague idea and can't articulate it yet", or "this word keeps causing confusion". Returns a per-team meaning table, flagged danger zones, and a preservation note so early-stage ideas aren't lost while the vocabulary stabilizes.

## Key Decisions

- **Chain length:** 7 sections in full load, 3 core.
- **Core sections:** `C.2.2a` (language-state chart), `A.16` (language-state transduction), `A.16.1` (pre-articulation cue pack).
- **Full chain:** adds thin-owner profile (`C.2.LS`), reopen/backoff handling (`A.16.2`), observe→notice→stabilize→route (`B.4.1`), and abductive prompt (`B.5.2.0`).

## Status

Active. Used for the `language_discovery` burden. Reasoner template: "Term meanings per team → Recommended action (which terms to agree on first)".

## Related

- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-retriever](../agents/fpf-retriever.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [route-chain](../concepts/route-chain.md)
