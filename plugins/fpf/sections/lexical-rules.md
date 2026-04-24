# FPF Lexical Rules (Part K — Mandatory)

These substitutions are MANDATORY in all normative content.
The Reasoner agent must enforce these internally; output uses plain language.

## Measurement Terms — Mandatory Replacements

| DO NOT use | Use instead | Notes |
|------------|-------------|-------|
| axis (of measurement); dimension (of a system or quality) | **(disallowed in Core prose)** → use **Characteristic** | No parenthetical allowance in Core; use **Characteristic / Measure / Coordinate** only |
| point (on an axis); data point | **Coordinate** (on a Scale) | “point” _(in explanations only, e.g. “a point on the scale”)_ |
| metric value; raw score | **Coordinate** (or **Value**) | “value” _(acceptable in plain usage when context is clear, but formally it’s a Coordinate tied to a Characteristic)_ |
| score (composite or normalized) | **Score** (produced via a **ScoringMethod**) | “score” _(if needed in narrative, ensure it’s explained as a result of a defined ScoringMethod)_ |
| unit dimension; unit axis | **Unit** (of a Scale) | “unit” _(plain usage okay)_ |
| metric (as a noun) | **Avoid in Tech and as primitive** → use **`U.DHCMethodRef` / `U.Measure` / Score** | “metric” _(Plain only on first use, with pointer to canonical terms)_ |

## Scope Terms — Deprecated (MUST NOT use in normative text)

- ~~applicability~~ → use `U.ClaimScope` (G), `U.WorkScope`, or `U.Scope`
- ~~envelope~~ → use `U.ClaimScope` (G), `U.WorkScope`, or `U.Scope`
- ~~generality~~ → use `U.ClaimScope` (G), `U.WorkScope`, or `U.Scope`
- ~~capability envelope~~ → use `U.ClaimScope` (G), `U.WorkScope`, or `U.Scope`
- ~~validity~~ → use `U.ClaimScope` (G), `U.WorkScope`, or `U.Scope`
