---
name: fpf
description: >
  Structure complex thinking: compare options, analyze specs/contracts,
  resolve team misunderstandings, audit trust/bias/ethics, debug misleading
  metrics, survey approaches in a field, structure handoffs, or make sense
  of messy multi-stakeholder situations. Triggers on any problem needing
  structured decomposition — not just teams, also solo analysis of complex
  systems. Also on explicit FPF terms (holon, UTS, DRR). Do NOT trigger
  for standard coding, simple bug fixes, or syntax questions.
---

# FPF Thinking Amplifier (Codex edition)

Structured coordination analysis powered by the First Principles Framework.
FPF is invisible infrastructure — output is ALWAYS in plain language.
NEVER use FPF terminology in responses to the user.

## Path convention

This skill assumes Codex is launched from the FPF-agent repo root. All file
paths below are relative to that root. When reading referenced agent files
under `agents/`, you will encounter the token `${CLAUDE_PLUGIN_ROOT}/` — treat
it as an empty string. A path like `${CLAUDE_PLUGIN_ROOT}/sections/metadata.json`
means exactly `sections/metadata.json` from the repo root. Never try to
resolve the env var.

## Pipeline (single context, four roles sequential)

Unlike the Claude Code edition which dispatches isolated subagents, you run
all four roles in this same context. To prevent drift between steps, you MUST
quote each step's output verbatim before starting the next step. The quoted
block is your anti-drift anchor.

### Step 1 — Classifier

Read `agents/fpf-classifier.md` in full. Apply its instructions to the
user's message. Emit a structured block with these fields:

```
SIGNAL: yes | no
TIER: 1 | 2 | 3
BURDEN: <burden name from the table in the classifier prompt>
ROUTE: <route number or "semantic" or "cross_cutting">
SEARCH_QUERY: <plain-language query for semantic fallback, or "n/a">
CONFIDENCE: <high | low>
```

Quote this block verbatim as your Step 1 output, then proceed.

If `SIGNAL=no` → stop the pipeline. Respond to the user as you normally would
(no FPF processing). If `CONFIDENCE=low` and no explicit FPF term appears in
the user's message → ask the user "This looks like a coordination problem —
want me to structure it?" before continuing.

### Step 2 — Retriever

Read `agents/fpf-retriever.md` in full. Using the Step 1 structured block:

- **Tier 1 (route-based):** Open `sections/routes/route-{N}.md` where N is
  from `ROUTE`. Follow its ordered chain — read each section file the route
  lists. Also consult `sections/metadata.json` for any pattern ID references.
- **Tier 2 (semantic fallback):** Run:
  ```
  uv run scripts/semantic_search.py "<SEARCH_QUERY>" --top-k 5 --json
  ```
  Parse the returned JSON array. Read each result's `file` field — those are
  your sections. Expect objects of shape:
  `{rank, score, pattern_id, title, file, keywords}`.
- **Tier 3 (combined):** Do Tier 1 first (primary route), then supplement
  with Tier 2 semantic search to cover the second burden.

For term lookups (explicit FPF term like "UTS" or "DRR"), skip routes and
read `sections/glossary-quick.md` plus the pattern file referenced there.

Before Step 3, quote the list of loaded section pattern IDs (e.g., "Loaded:
A.6, A.6.P, E.17, G.3") as your Step 2 anchor.

### Step 3 — Reasoner

Read `agents/fpf-reasoner.md` in full. Apply FPF structure to the user's
problem internally. Produce a draft answer that:

- Is in the user's language (Russian if they wrote Russian, English if
  English — match the input)
- Never contains FPF terminology: no "holon", "UTS", "DRR",
  "CharacteristicSpace", "episteme", "transformer quartet",
  "bounded context", no pattern IDs (A.6.P, E.17, etc.), no
  "route 1/2/3..." mentions, no mention of this pipeline
- Uses the structural artifacts the reasoner prompt specifies for the
  burden type (comparison table, responsibility map, term sheet, etc.)

Quote the full draft as your Step 3 anchor before moving to Step 4.

### Step 4 — Reviewer (mandatory for Tier 2 and Tier 3; optional for Tier 1)

This is a **cold review**. Explicit framing: ignore everything you produced
in Steps 1–3. Treat the Step 3 draft as text written by someone else. You
have never seen the reasoning, the retrieved sections, or the classification.
Your only job is to validate the draft against four criteria:

**(a) Jargon check.** The draft must not contain any of these tokens:
`holon`, `UTS`, `DRR`, `CharacteristicSpace`, `episteme`, `SenseCell`,
`transformer quartet`, `bounded context`, `U.Measure`, `U.ClaimScope`,
`U.WorkScope`, `MVPK`, pattern IDs matching regex `[A-K]\.\d+(\.[A-Z])?`.
Also not in translation ("холон", "эпистема", "транспортёрный квартет").

**(b) Concept leakage.** Even without jargon tokens, the draft must not
paraphrase FPF structural patterns by rote. Red flags:
- "A four-step transformation: X → Y → Z → W" (that's the transformer quartet
  described without naming it)
- "Divide responsibility across four quadrants: description / capability /
  execution / plan" (that's a specific FPF pattern in disguise)
- "Apply the four-part language maturity diagnostic" (same issue)

Paraphrasing the *shape* of an FPF pattern while omitting the name is still
terminology leakage. The user should receive analysis-as-output, not
pattern-as-output.

**(c) Grounding.** Every substantive claim in the draft should be traceable
to a section loaded in Step 2. Check the Step 2 anchor (the pattern ID list).
Any claim with no visible grounding → flag.

**(d) Plain-language contract.** Cross-check against `sections/lexical-rules.md`
for domain-specific rules (e.g., "axis" / "dimension" forbidden → must say
"characteristic"; "metric" as noun forbidden → must say "measure" or "score").

If any check fails → revise the draft to fix the specific problem, then
re-review. Maximum 2 revision passes. If still failing after 2 passes,
surface the issue plainly to the user rather than publishing broken output.

## Burden Classification Reference

Detect from user's natural language — no FPF terms needed.

| Burden | User signals | Tier | Route file |
|--------|-------------|------|------------|
| project_alignment | teams confused, responsibilities unclear | 1 | `sections/routes/route-1-project-alignment.md` |
| language_discovery | terminology disagreement, vague idea | 1 | `sections/routes/route-2-language-discovery.md` |
| boundary_unpacking | contract/SLA/API mixes rules and obligations | 1 | `sections/routes/route-3-boundary-unpacking.md` |
| comparison_selection | choosing between options, opaque decisions | 1 | `sections/routes/route-4-comparison-selection.md` |
| generator_portfolio | state-of-the-art survey, reusable scaffold | 1 | `sections/routes/route-5-generator-portfolio.md` |
| rewrite_explanation | rewrite preserving meaning, different audience | 1 | `sections/routes/route-6-rewrite-explanation.md` |
| ethical_assurance | bias audit, ethical assumptions, value conflicts | 1 | `sections/routes/route-7-ethical-assurance.md` |
| trust_assurance | trust metrics, overclaim, evidence aggregation | 1 | `sections/routes/route-8-trust-assurance.md` |
| composition_aggregation | KPIs lie, aggregation mismatch, sum != whole | 1 | `sections/routes/route-9-composition-aggregation.md` |
| evolution_learning | design drift, lessons learned, feedback loops | 1 | `sections/routes/route-10-evolution-learning.md` |
| term_lookup | explicit FPF term question | 1 | `sections/metadata.json` → direct file load |
| semantic | FPF signal but no route match | 2 | Keyword + FAISS → dynamic chain |
| cross_cutting | multiple burdens match | 3 | Primary route + semantic supplement |

## Key Files

- `sections/metadata.json` — instant pattern lookup (~235 entries)
- `sections/routes/route-{1..10}.md` — ordered section chains per burden
- `sections/glossary-quick.md` — 50 core terms mapped to patterns
- `sections/lexical-rules.md` — mandatory terminology rules (internal only, for Reviewer step)
- `sections/embeddings/` — FAISS index for semantic search (rebuilt locally via `uv run scripts/build_embeddings.py`)

## Shared Agent Prompts

These files contain the full instructions for each pipeline role. They are
shared with the Claude Code edition of this skill, so you will see the token
`${CLAUDE_PLUGIN_ROOT}/` inside them — ignore that token (see Path convention
section above).

- `agents/fpf-classifier.md` — Step 1 instructions
- `agents/fpf-retriever.md` — Step 2 instructions
- `agents/fpf-reasoner.md` — Step 3 instructions
- `agents/fpf-reviewer.md` — Step 4 instructions

The file `agents/fpf-sync.md` is dev-side infrastructure (scheduled upstream
sync + rebuild pipeline) and is NOT used during skill execution.

## Output

One plain-language answer to the user. Never mention:
- FPF, the framework, or any FPF term
- Agents, pipeline, steps, tiers, routes, burdens
- Pattern IDs or section file names
- The classifier / retriever / reasoner / reviewer roles

The user should see a direct, structured analysis of their problem — nothing
else.
