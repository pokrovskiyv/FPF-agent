---
title: "Route 2: Language Discovery"
sources:
  - sections/routes/route-2-language-discovery.md
  - scripts/build_routes.py
last_updated: 2026-06-15T00:00:00Z
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
- **Core sections:** `C.2.2a` (U.LanguageStateSpace — language-state chart over U.Character), `A.16` (Language-State Move Coordination), `A.16.1` (U.PreArticulationCuePack).
- **Full chain adds:** `C.2.LS` (U.LanguageStateFacetProfile — compact owner profile), `A.16.2` (Reopen / SketchBackoff / Respecify), `B.4.1` (Observe → Notice → Stabilize → Route), `B.5.2.0` (U.AbductivePrompt).
- **Loading strategy:** minimum load uses the first 3 core sections for simple queries; full load uses all 7 for complex queries. If stagnation is detected, the Retriever consults `_xref.md` for cross-references.

The route file is generated mechanically by `build_route_file()` from `scripts/build_routes.py`: pattern IDs are resolved against `sections/metadata.json` to fill in each section's title and file path, and titles are truncated to 60 characters. Regenerating the route is part of `scripts/rebuild_all.sh` — never hand-edit `sections/routes/route-2-language-discovery.md`.

## Section Chain

| # | Pattern | Title | Core? |
|---|---------|-------|-------|
| 1 | C.2.2a | U.LanguageStateSpace — language-state chart over U.Character | YES |
| 2 | C.2.LS | U.LanguageStateFacetProfile — compact owner profile | |
| 3 | A.16 | Language-State Move Coordination | YES |
| 4 | A.16.1 | U.PreArticulationCuePack | YES |
| 5 | A.16.2 | Reopen / SketchBackoff / Respecify | |
| 6 | B.4.1 | Observe → Notice → Stabilize → Route | |
| 7 | B.5.2.0 | U.AbductivePrompt | |

## Status

Active. Used for the `language_discovery` burden. Reasoner output template: "Term meanings per team → flagged danger zones → recommended action (which terms to agree on first)", with a preservation note for ideas that are still pre-articulation.

## Related

- [fpf-classifier](../agents/fpf-classifier.md) — detects the `language_discovery` burden and selects this route
- [fpf-retriever](../agents/fpf-retriever.md) — loads the section chain by `id` (Tier 1 cache)
- [fpf-reasoner](../agents/fpf-reasoner.md) — applies the chain and emits the per-team meaning table
- [route-chain](../concepts/route-chain.md) — how route chains are built and loaded
