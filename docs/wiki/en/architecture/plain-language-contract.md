---
title: Plain Language Contract
sources:
  - CLAUDE.md
  - agents/fpf-reasoner.md
  - agents/fpf-reviewer.md
  - skills/fpf/SKILL.md
  - scripts/build_lexical.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - plain-language
  - contract
  - non-negotiable
---

# Plain Language Contract

## Components

The plain language contract is enforced at three layers: the Reasoner's Principle #0, the Reviewer's Check 1 (jargon guard), and the lexical rules produced by `build_lexical`.

| Layer | What it does |
|-------|--------------|
| Reasoner Principle #0 | Every response in the user's own words; zero FPF terminology by design |
| Reviewer Check 1 | Scans the Reasoner's output for banned terms and rewrites any found |
| `sections/lexical-rules.md` | Mandatory term substitutions (e.g., "axis" → Characteristic, "metric" as noun → Measure/Score) enforced internally by the Reasoner |

## Data Flow

```
user message (plain words)
      │
      ▼
Classifier (internal FPF labels, not shown)
      │
      ▼
Retriever loads FPF patterns (full terminology visible to agents)
      │
      ▼
Reasoner:
  - reads lexical-rules.md internally
  - applies pattern structure to user's problem
  - produces output in user's language
  - zero FPF terms in output
      │
      ▼  (for Tier 2/3)
Reviewer:
  - scans output for banned tokens
  - rewrites offenders in plain language
  - returns STATUS: PASS | CORRECTED
      │
      ▼
user (plain words)
```

## Decisions

- **Invisible infrastructure.** The Reasoner's analogy (in `agents/fpf-reasoner.md`): "You are a GPS. You use Dijkstra's algorithm internally. You tell the user 'turn right in 200 meters.' You never say 'applying shortest-path algorithm to weighted graph.'"
- **Banned-term list is non-exhaustive.** The Reviewer is instructed to flag anything that *sounds* like framework jargon — not just tokens on the explicit list. This handles future extensions without requiring list updates.
- **Example rewrites are written into the Reviewer prompt.** "Using U.Commitment deontic objects..." → "Here are the obligations this creates...". Calibration for what "plain language" means in this project.
- **Lexical rules are Part K of the spec.** The substitution map is baked into `FPF-Spec.md` and extracted by `build_lexical.py` — no independent maintenance of the banned terms.
- **Non-negotiable, per CLAUDE.md.** Every commit and code change in this project is expected to preserve the contract. Violations show up immediately in the Reviewer's output or in smoke tests.

## Example (from CLAUDE.md)

Terms that must NEVER appear in user-facing output: `holon`, `bounded context`, `episteme`, `transformer quartet`, `CharacteristicSpace`, pattern IDs (`A.6`, `E.17`), `U.anything`, framework abbreviations (`F-G-R`, `NQD`, `DRR`, `UTS`, ...), meta-references ("according to FPF", "the framework"), and the lexical-debt terms `axis`/`dimension`/`metric` (as noun).

## Related

- [agent-team](agent-team.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [fpf-reviewer](../agents/fpf-reviewer.md)
- [build_lexical](../modules/build_lexical.md)
