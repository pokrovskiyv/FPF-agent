---
title: "Route 7: Ethical Assurance"
sources:
  - sections/routes/route-7-ethical-assurance.md
  - scripts/build_routes.py
last_updated: 2026-07-01T07:00:00Z
tags:
  - route
  - tier-1
  - ethical-assurance
---

# Route 7: Ethical Assurance

> Source: `sections/routes/route-7-ethical-assurance.md`

## Summary

Triggered by questions about hidden bias, ethical assumptions, or value conflicts across teams that operate at different scales ("how do I audit our process for bias?", "values clash between engineers and ops — what's the map?"). The output the user receives is a bias register, a conflict map grouped by scale, and an ethical-audit checklist. The route is one of the ten Tier-1 entry routes; the section chain and its core/full split are defined declaratively in `scripts/build_routes.py` and rendered into the route file by `build_route_file()`.

## Key Decisions

- **Chain length:** 5 sections in the full load, 3 of them marked core.
- **Core sections** (minimum load for a simple query): `D.2` (Multilevel Ethics For System Work), `D.3` (Interlevel Ethical Conflict Structure), `D.5` (Bias Audit and Ethical Assurance).
- **Full chain** (complex query) adds: `D.1` (Ethical Value Plurality and Boundary) and `D.4` (Ethical Mediation and Decision Use).
- **Loading order** is fixed by the chain sequence; if the Retriever detects stagnation it falls back to `_xref.md` cross-references.

## Section Chain

The chain is loaded in order. Core sections are loaded for simple queries; the full chain for complex ones.

| # | Pattern | Title | Core? |
|---|---------|-------|-------|
| 1 | D.1 | Ethical Value Plurality and FPF Boundary | |
| 2 | D.2 | Multilevel Ethics For System-Holon Work | YES |
| 3 | D.3 | Interlevel Ethical Conflict Structure | YES |
| 4 | D.4 | Ethical Mediation and Decision Use | |
| 5 | D.5 | Bias Audit and Ethical Assurance | YES |

Pattern-to-file mapping is resolved against `sections/metadata.json` at build time; sections whose file path is not yet present in metadata render with an empty file column until the spec is re-split.

## Status

Active. Used for the `ethical_assurance` burden detected by the Classifier. The Reasoner template for this route is: conflict map by scale → bias register (type / location / risk / mitigation) → audit checklist. The route definition lives in the `ROUTES` list in `scripts/build_routes.py`; editing the chain or core set there and re-running the script regenerates this file.

## Related

- [fpf-classifier](../agents/fpf-classifier.md) — detects the `ethical_assurance` burden and selects this route
- [fpf-retriever](../agents/fpf-retriever.md) — loads the section chain (core vs. full) and follows `_xref.md` on stagnation
- [fpf-reasoner](../agents/fpf-reasoner.md) — produces the bias register, conflict map, and audit checklist
- [route-chain](../concepts/route-chain.md) — explains how route chains are structured and consumed
