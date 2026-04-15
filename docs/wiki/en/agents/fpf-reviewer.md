---
title: fpf-reviewer
sources:
  - agents/fpf-reviewer.md
last_updated: 2026-04-15T00:00:00Z
tags:
  - agent
  - reviewer
  - quality-gate
---

# fpf-reviewer

> Source: `agents/fpf-reviewer.md`

## Purpose

Optional fourth agent that runs on Tier 2 (semantic) and Tier 3 (combined) outputs, plus any Tier 1 cross-cutting query. Performs three validation checks on the Reasoner's output: jargon guard (highest priority), grounding validation, and actionability. If any check fails, the Reviewer corrects the output in place; if all pass, it forwards the Reasoner's output unchanged.

Skipped for simple Tier 1 term lookups and clean route-based queries — those are cheap and the Reasoner's template discipline is enough.

## Interface

**Input:** Reasoner's output + the source sections the Retriever loaded.

**Output:**

```
STATUS: [PASS | CORRECTED]
FIXES: [list of corrections made, if any]

[final output for user]
```

## The three checks

### Check 1 — Jargon guard (HIGHEST priority)

Scans the output for any FPF-specific terminology that leaked through. The source lists banned terms explicitly: `holon`, `episteme`, `bounded context`, `transformer quartet`, `CharacteristicSpace`, `SenseCells`, `MVPK`, `Claim Register`, any `U.anything`, any pattern ID (A.6, E.17, ...), framework abbreviations (F-G-R, NQD, E/E-LOG, DRR, UTS, CSLC, USM, USCM), plus meta-references like "according to FPF", "the framework", "the specification", and the lexical-debt terms `axis`/`dimension`/`metric` (as a noun). Any match triggers a rewrite of the offending passage in plain language.

Example rewrites (from the source):
- "Using U.Commitment deontic objects..." → "Here are the obligations this creates..."
- "The Boundary Norm Square suggests L/A/D/E routing..." → "This text mixes four different things: rules, conditions, obligations, and evidence requirements..."
- "Applying CharacteristicSpace A.19..." → "Here are the criteria to evaluate each option..."

### Check 2 — Grounding validation

Each substantive claim must be traceable to content in the loaded sections. Claims that introduce concepts absent from any source section get flagged and either removed or qualified.

- **Tier 2 queries** get stricter validation because the section chain was assembled dynamically.
- **Tier 3 queries** mix route-based and semantic sections — route-derived claims get normal validation, semantic-derived claims get Tier 2 scrutiny.
- Bridging claims that connect two sections must be explicitly justified.

### Check 3 — Actionability

The output must be specific (not generic advice), structured (tables/lists, not walls of text), actionable (clear next steps), and concise.

## Position in the pipeline

```
reasoner → [fpf-reviewer] → output    (Tier 2, Tier 3, Tier 1 cross-cutting only)
```

## See also

- [fpf-reasoner](fpf-reasoner.md) — produces the input
- [plain-language-contract](../architecture/plain-language-contract.md)
- [agent-team](../architecture/agent-team.md)
