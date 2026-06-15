---
title: Plain Language Contract
sources:
  - CLAUDE.md
  - agents/fpf-reasoner.md
  - agents/fpf-reviewer.md
  - scripts/build_lexical.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - architecture
  - plain-language
  - contract
  - non-negotiable
---

# Plain Language Contract

The plain language contract is the project's non-negotiable rule: FPF is **invisible infrastructure**. Users speak their own language, and output comes back in their language — with no `holon`, `bounded context`, `episteme`, `transformer quartet`, `CharacteristicSpace`, pattern IDs, or any other FPF terminology. Patterns are applied internally by the Reasoner and never exposed.

## Components

The contract is enforced at three layers: the Reasoner's Principle #0, the Reviewer's Check 1 (jargon guard), and the lexical rules produced by `build_lexical`.

| Component | Source | Role in this context |
|-----------|--------|----------------------|
| Reasoner Principle #0 | [fpf-reasoner](../agents/fpf-reasoner.md) | "You apply FPF. You never explain FPF." Every response is in the user's language with zero FPF terminology by design |
| Reviewer Check 1 | [fpf-reviewer](../agents/fpf-reviewer.md) | Highest-priority check: scans the Reasoner's output for banned tokens and rewrites any offending passage in plain language |
| `sections/lexical-rules.md` | [build_lexical](../modules/build_lexical.md) | Mandatory term substitutions (e.g., "axis"/"dimension" → Characteristic, "metric" as noun → Measure/Score) that the Reasoner enforces internally |

## Data Flow

```
user message (plain words)
      │
      ▼
Classifier (internal FPF labels, not shown)
      │
      ▼
Retriever loads FPF sections (full terminology visible to agents)
      │
      ▼
Reasoner:
  - reads glossary-quick.md + lexical-rules.md internally
  - applies pattern structure to the user's problem
  - produces output in the user's language
  - zero FPF terms in output
      │
      ▼  (for Tier 2 / Tier 3 queries)
Reviewer:
  - Check 1: scans output for banned tokens, rewrites offenders
  - Check 2: grounding (claims traceable to loaded sections)
  - Check 3: actionability
  - returns STATUS: PASS | CORRECTED
      │
      ▼
user (plain words)
```

The Reasoner always reads `sections/glossary-quick.md` (for internal orientation only) and `sections/lexical-rules.md` before generating output. The Reviewer only runs on the deeper pipeline tiers; for the lightest term-lookup queries the contract rests entirely on the Reasoner's Principle #0.

## Decisions

- **Invisible infrastructure.** The Reasoner's analogy (in `agents/fpf-reasoner.md`): "You are a GPS. You use Dijkstra's algorithm internally. You tell the user 'turn right in 200 meters.' You never say 'applying shortest-path algorithm to weighted graph.'"
- **The banned-term list is non-exhaustive.** The Reviewer is instructed to flag anything that *sounds* like framework jargon — not just the tokens on the explicit list. This handles future spec extensions without requiring list updates.
- **Example rewrites are baked into the Reviewer prompt.** "Using U.Commitment deontic objects..." → "Here are the obligations this creates...". These calibrate what "plain language" means in this project.
- **Lexical rules come from Part K of the spec.** The substitution map is baked into `FPF-Spec.md` and extracted by `build_lexical.py` (function `parse_replacement_table`) into `sections/lexical-rules.md` — there is no separately maintained banned-terms list to drift.
- **Non-negotiable, per CLAUDE.md.** Every commit and code change is expected to preserve the contract. Violations surface immediately in the Reviewer's output or in smoke tests.

## Example (from CLAUDE.md and the agent prompts)

Terms that must NEVER appear in user-facing output: `holon`, `bounded context`, `episteme`, `transformer quartet`, `CharacteristicSpace`, `SenseCells`, `MVPK`, `Claim Register`, pattern IDs (`A.6`, `E.17`, `F.17`, `B.3`), `U.anything` (`U.System`, `U.Method`, `U.Work`, ...), framework abbreviations (`F-G-R`, `NQD`, `E/E-LOG`, `DRR`, `UTS`, `CSLC`, `USM`, `USCM`), meta-references ("according to FPF", "the framework", "the specification"), and the lexical-debt terms `axis`/`dimension`/`metric` (as a noun).

## Related

- [agent-team](agent-team.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [fpf-reasoner](../agents/fpf-reasoner.md)
- [fpf-reviewer](../agents/fpf-reviewer.md)
- [build_lexical](../modules/build_lexical.md)
