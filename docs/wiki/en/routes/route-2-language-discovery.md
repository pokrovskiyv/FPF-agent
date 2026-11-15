---
title: "Route 2: Language Discovery"
sources:
  - sections/routes/route-2-language-discovery.md
  - scripts/build_routes.py
last_updated: 2026-11-15T07:00:00Z
tags:
  - route
  - tier-1
  - language-discovery
---

# Route 2: Language Discovery

> Source: `sections/routes/route-2-language-discovery.md`

## Summary

Triggered when the user says things like: "we can't agree on terminology", "everyone means something different by this word", "I have a vague idea and can't articulate it yet", or "there's an emerging concern I can't pin down". The route returns a per-team meaning table for the contested terms, flagged danger zones where the same word carries divergent meanings, and a preservation note so early-stage ideas aren't discarded while the vocabulary stabilizes.

This is a Tier 1 route: the section chain acts as a cache, so the Retriever can load it directly by `id` without falling back to semantic search.

## Key Decisions

- **Chain length:** 7 sections in full load, 3 marked core. Defined in `scripts/build_routes.py` (`ROUTES`, entry `id: 2`, `slug: "language-discovery"`).
- **Core sections:** `C.2.2a` (Language-State Chart over CharacteristicSpace — where a term sits on a spectrum from vague to defined), `A.16` (Language-State Moves: how to advance a term toward a stable definition), `A.16.1` (PreArticulationCuePack: preserving early intuitions before committing to a definition).
- **Full chain adds:** `C.2.LS` (Language-State Facet Profile: publish readings and use conditions), `A.16.2` (Reopen, SketchBackoff, Respecify, or Retire a language state), `B.4.1` (Publish Candidate Routes for a Stabilized Cue), `B.5.2.0` (Question Form for Entering Abduction).
- **Loading strategy:** minimum load uses the first 3 core sections for simple queries; full load uses all 7 for complex queries. If stagnation is detected, the Retriever consults `_xref.md` for cross-references.

The route file is generated mechanically by `build_route_file()` from `scripts/build_routes.py`: pattern IDs are resolved against `sections/metadata.json` to fill in each section's title and file path, and titles are truncated to 60 characters. Regenerating the route is part of `scripts/rebuild_all.sh` — never hand-edit `sections/routes/route-2-language-discovery.md`.

## Section Chain

| # | Pattern | Title | Core? |
|---|---------|-------|-------|
| 1 | C.2.2a | Language-State Chart over CharacteristicSpace | YES |
| 2 | C.2.LS | Language-State Facet Profile: Publish Readings and Use Conditions | |
| 3 | A.16 | Language-State Moves: Choose the Next Publication and Use of a Term | YES |
| 4 | A.16.1 | PreArticulationCuePack: Preserve an Early Cue Before Choosing a Route | YES |
| 5 | A.16.2 | Reopen, SketchBackoff, Respecify, or Retire a Language-State | |
| 6 | B.4.1 | Publish Candidate Routes for a Stabilized Cue (RoutedCueSet) | |
| 7 | B.5.2.0 | Question Form for Entering Abduction | |

## Status

Active. Used for the `language_discovery` burden. Reasoner output template: "Term meanings per team → flagged danger zones → recommended action (which terms to agree on first)", with a preservation note for ideas that are still pre-articulation.

## Related

- [fpf-classifier](../agents/fpf-classifier.md) — detects the `language_discovery` burden and selects this route
- [fpf-retriever](../agents/fpf-retriever.md) — loads the section chain by `id` (Tier 1 cache)
- [fpf-reasoner](../agents/fpf-reasoner.md) — applies the chain and emits the per-team meaning table
- [route-chain](../concepts/route-chain.md) — how route chains are built and loaded
