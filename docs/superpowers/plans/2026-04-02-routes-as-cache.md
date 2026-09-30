# Routes as Cache Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the fixed 6-route architecture with a three-tier system (routes as cache + semantic fallback + combined), expanding from 16% to 100% spec coverage.

**Architecture:** 10 curated routes for common burdens (Tier 1), FAISS-based semantic retrieval for everything else (Tier 2), and combined mode for cross-cutting queries (Tier 3). Classifier v2 detects broad "FPF signals" instead of only matching 6 burden types.

**Tech Stack:** Python 3 (stdlib only for build scripts), Markdown (agent definitions), existing FAISS index + semantic_search.py for Tier 2.

**Spec:** `docs/superpowers/specs/2026-04-02-routes-as-cache-design.md`

---

### Task 1: Add 4 new routes to build_routes.py

**Files:**
- Modify: `scripts/build_routes.py:15-64` (ROUTES list)
- Generated: `sections/routes/route-7-ethical-assurance.md`
- Generated: `sections/routes/route-8-trust-assurance.md`
- Generated: `sections/routes/route-9-composition-aggregation.md`
- Generated: `sections/routes/route-10-evolution-learning.md`

**Note on D.3/D.4:** Pattern IDs D.3 and D.4 exist in metadata.json but have no file (empty `file` field). Route 7 chain includes them — `build_route_file()` will show `(not found)` for their file path, and the retriever will skip them at load time. This is acceptable: when files are eventually generated from the spec, the route will automatically pick them up.

- [ ] **Step 1: Add 4 new route definitions to ROUTES list**

In `scripts/build_routes.py`, append these 4 entries after the existing route 6 dict (line 63, before the closing `]`):

```python
    {
        "id": 7,
        "slug": "ethical-assurance",
        "user_says": "How to audit for hidden bias? / ethical assumptions / value conflicts across teams at different scales",
        "user_gets": "Bias register, conflict map by scale, ethical audit checklist",
        "chain": ["D.1", "D.2", "D.3", "D.4", "D.5"],
        "core": ["D.2", "D.3", "D.5"],
    },
    {
        "id": 8,
        "slug": "trust-assurance",
        "user_says": "Can we trust this metric? / how to aggregate confidence without overclaim / evidence grounding",
        "user_gets": "Assurance profile (formality/scope/reliability per component), dependency map, evidence gaps",
        "chain": ["B.3", "B.3.5", "B.1", "B.1.1", "A.6.B"],
        "core": ["B.3", "B.3.5", "B.1"],
    },
    {
        "id": 9,
        "slug": "composition-aggregation",
        "user_says": "Why do KPI dashboards lie? / sum of parts != whole / Tool A aggregates differently from Tool B",
        "user_gets": "Violated invariant diagnosis, aggregation dependency map, fix recommendations",
        "chain": ["B.1", "B.1.1", "B.1.2", "B.1.3", "B.1.4", "B.1.5"],
        "core": ["B.1", "B.1.1", "B.1.4"],
    },
    {
        "id": 10,
        "slug": "evolution-learning",
        "user_says": "Design is outdated and nobody noticed / how to close the loop between operations and design / lessons learned",
        "user_gets": "Current cycle map (where the break is), loop closure plan, cycle health metrics",
        "chain": ["B.4", "B.4.1", "B.5.1", "A.4", "G.11"],
        "core": ["B.4", "B.4.1", "B.5.1"],
    },
```

- [ ] **Step 2: Update module docstring**

Change line 2 from:
```python
"""Build route chain files for each of the 6 practical FPF entry routes.
```
to:
```python
"""Build route chain files for each of the 10 practical FPF entry routes.
```

- [ ] **Step 3: Run the script to generate route files**

Run: `python3 scripts/build_routes.py`

Expected output:
```
Written route-1-project-alignment.md
Written route-2-language-discovery.md
Written route-3-boundary-unpacking.md
Written route-4-comparison-selection.md
Written route-5-generator-portfolio.md
Written route-6-rewrite-explanation.md
Written route-7-ethical-assurance.md
Written route-8-trust-assurance.md
Written route-9-composition-aggregation.md
Written route-10-evolution-learning.md

10 route files written to sections/routes/
```

- [ ] **Step 4: Verify generated route files have correct structure**

Run: `head -20 sections/routes/route-7-ethical-assurance.md`

Expected: markdown file with table showing D.1-D.5 chain, Core column with YES for D.2, D.3, D.5.

Run: `head -20 sections/routes/route-9-composition-aggregation.md`

Expected: markdown file with table showing B.1-B.1.5 chain, Core column with YES for B.1, B.1.1, B.1.4.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_routes.py sections/routes/route-7-*.md sections/routes/route-8-*.md sections/routes/route-9-*.md sections/routes/route-10-*.md
git commit -m "feat: add routes 7-10 (ethics, trust, composition, evolution)"
```

---

### Task 2: Rewrite fpf-classifier.md with v2 logic

**Files:**
- Modify: `agents/fpf-classifier.md` (full rewrite)

- [ ] **Step 1: Replace entire content of fpf-classifier.md**

Write the following to `agents/fpf-classifier.md`:

```markdown
---
description: >
  FPF burden classifier v2. Detects FPF-relevant signals in user's
  message, selects tier (route / semantic / combined), determines
  pipeline depth. Input: user's message. Output: signal, tier,
  burden, route, pipeline, and search query.
---

You are the **Classifier v2** agent for the FPF thinking amplifier.

## Your Role

Given the user's message, determine:
1. **FPF Signal** — is this a problem where FPF can help? (broader than burden matching)
2. **Tier** — route match (1), semantic fallback (2), or combined (3)
3. **Burden type** — for Tier 1: which specific route
4. **Pipeline depth** — how many agents to engage
5. **Search query** — for Tier 2/3: hint for the retriever's semantic search

## Three-Stage Classification

### Stage 1: FPF Signal Detection

Detect ANY coordination, systems engineering, or transdisciplinary signal. This is BROADER than matching a specific burden — it catches any problem where FPF patterns could help.

**FPF signals include** (non-exhaustive):
- Team coordination, responsibility, handoffs
- Terminology disagreements, vague emerging concepts
- Contract/specification/API boundary confusion
- Decision-making between alternatives
- State-of-the-art surveys, portfolio building
- Text rewriting with meaning preservation
- Ethical audits, bias detection, value conflicts
- Trust, assurance, evidence aggregation
- System composition, aggregation inconsistencies
- Design evolution, feedback loops, learning cycles
- Formalization of norms, domain-specific rules
- Cross-disciplinary methodology questions
- Systems engineering, holistic system analysis

**NOT FPF signals** (do NOT trigger):
- Standard coding tasks (bug fixes, feature implementation)
- Simple questions about tools, libraries, syntax
- File management, git operations
- Single-person tasks with no coordination aspect

If no FPF signal detected → return `SIGNAL: no` and stop.

### Stage 2: Route Matching

If FPF signal detected, try to match against known burden types:

| Burden | Trigger patterns (user's words) | Route |
|--------|-------------------------------|-------|
| `project_alignment` | "teams don't understand each other", "who owns what", "responsibilities unclear", "how to hand off work", "alignment" | route-1 |
| `language_discovery` | "can't agree on terms", "everyone means something different", "vague idea", "can't articulate", "terminology" | route-2 |
| `boundary_unpacking` | "contract mixes everything", "SLA unclear", "API boundary", "spec confusing", "rules vs obligations" | route-3 |
| `comparison_selection` | "choose between options", "how to decide", "trade-offs", "comparing alternatives", "decision criteria" | route-4 |
| `generator_portfolio` | "state of the art", "what approaches exist", "survey the field", "build a portfolio", "competing schools" | route-5 |
| `rewrite_explanation` | "rewrite for different audience", "explain without changing meaning", "simplify this", "compare two versions" | route-6 |
| `ethical_assurance` | "hidden bias", "ethical audit", "value conflicts", "ethical assumptions", "bias in the system" | route-7 |
| `trust_assurance` | "can we trust this metric", "overclaim", "aggregated confidence", "evidence grounding", "assurance" | route-8 |
| `composition_aggregation` | "KPIs lie", "sum of parts != whole", "aggregation mismatch", "why do tools disagree", "integration proof" | route-9 |
| `evolution_learning` | "design is outdated", "lessons learned", "feedback loop", "design drift", "operations vs design" | route-10 |
| `term_lookup` | "what is [X] in FPF", "define [X]", mentions specific pattern ID (A.6, E.17, etc.) | metadata.json |

### Stage 3: Tier Assignment

| Signal | Confidence | Tier | Action |
|--------|-----------|------|--------|
| One strong route match | HIGH (>=70%) | **Tier 1** | Auto-dispatch with route |
| Multiple routes match | HIGH | **Tier 3** | Combined: primary route + semantic supplement |
| FPF signal but no route match | — | **Tier 2** | Semantic fallback |
| Weak route match | LOW (<70%) | **Tier 2** | Soft trigger, use semantic search |
| Explicit FPF term (A.6, UTS, DRR, holon) | BYPASS | **Tier 1** | Auto-dispatch, `term_lookup` |
| No FPF signal | NONE | — | Do NOT trigger |

**Soft trigger** (for LOW confidence or Tier 2):
> "This looks like a coordination / systems engineering problem. Want me to help structure it?"

## Strategy Table

| Tier | Burden | Agents | Budget | Route file |
|------|--------|--------|--------|------------|
| 1 | `term_lookup` | retriever → reasoner | 800 | metadata.json lookup |
| 1 | `project_alignment` | retriever → reasoner | 1200 | route-1-project-alignment.md |
| 1 | `language_discovery` | retriever → reasoner | 1200 | route-2-language-discovery.md |
| 1 | `boundary_unpacking` | retriever → reasoner | 1500 | route-3-boundary-unpacking.md |
| 1 | `comparison_selection` | retriever → reasoner | 1200 | route-4-comparison-selection.md |
| 1 | `generator_portfolio` | retriever → reasoner | 1500 | route-5-generator-portfolio.md |
| 1 | `rewrite_explanation` | retriever → reasoner | 1200 | route-6-rewrite-explanation.md |
| 1 | `ethical_assurance` | retriever → reasoner | 1500 | route-7-ethical-assurance.md |
| 1 | `trust_assurance` | retriever → reasoner | 1500 | route-8-trust-assurance.md |
| 1 | `composition_aggregation` | retriever → reasoner | 1200 | route-9-composition-aggregation.md |
| 1 | `evolution_learning` | retriever → reasoner | 1200 | route-10-evolution-learning.md |
| 2 | `semantic` | retriever → reasoner → reviewer | 2000 | (none — semantic search) |
| 3 | `cross_cutting` | retriever → reasoner → reviewer | 2500 | primary route + semantic |

## Output Format

Return a structured classification:

```
SIGNAL: [yes/no]
TIER: [1/2/3]
BURDEN: [burden_type]
CONFIDENCE: [HIGH/LOW/BYPASS]
ROUTE: [route file path | "metadata.json" | null]
PIPELINE: [retriever→reasoner | retriever→reasoner→reviewer]
BUDGET: [token budget]
SECTIONS: [list of section files to load, from route "Core" column first]
SEARCH_QUERY: [natural language query for semantic search, for Tier 2/3]
```

For **Tier 2**, set `ROUTE: null` and `SECTIONS: []`. The retriever will use `SEARCH_QUERY` to find sections via keyword + semantic search.

For **Tier 3**, set both `ROUTE` (primary route file) and `SEARCH_QUERY` (for supplementary semantic search).

## What NOT to Do

- Do NOT use FPF terminology when communicating with the user
- Do NOT classify regular coding tasks as FPF-relevant
- Do NOT force queries into routes — if no route fits well, use Tier 2
- Do NOT default to cross_cutting — use Tier 3 only when genuinely multiple routes apply
- Do NOT skip the FPF signal check — it prevents false positives
```

- [ ] **Step 2: Verify the file was written correctly**

Run: `wc -l agents/fpf-classifier.md`

Expected: approximately 120-130 lines.

- [ ] **Step 3: Commit**

```bash
git add agents/fpf-classifier.md
git commit -m "feat: classifier v2 with three-tier signal detection"
```

---

### Task 3: Update fpf-retriever.md with Mode B

**Files:**
- Modify: `agents/fpf-retriever.md` (add Mode B, update loading budget)

- [ ] **Step 1: Update the description frontmatter**

Replace lines 1-6:
```markdown
---
description: >
  FPF section retriever v2. Supports two modes: Mode A (route-based,
  loads curated section chains) and Mode B (semantic fallback, assembles
  dynamic chains via keyword + FAISS search). Input: classifier output
  (tier, burden, route, search_query). Output: loaded section content.
---
```

- [ ] **Step 2: Replace "Your Role" section**

Replace the existing "Your Role" section (lines 9-10) with:

```markdown
## Your Role

Given the classifier's routing decision, load the minimum sections needed. You operate in two modes based on the classifier's TIER output.

## Mode A: Route-Based Loading (Tier 1)

Used when the classifier returns a specific route file. Load curated section chains — this is the cheapest and highest-quality path.
```

- [ ] **Step 3: Move existing Tiers 1-3 under Mode A**

Keep the existing Tier 1 (Direct Pattern ID Lookup), Tier 2 (Route Chain Loading), and Tier 3 (Cross-Reference Expansion) sections as-is, but indent them under Mode A. These are the retrieval tiers for route-based loading.

- [ ] **Step 4: Add Mode B section after Mode A**

After the existing Tier 3 (Cross-Reference Expansion), and BEFORE the existing Tier 4 (Keyword Search), insert:

```markdown
## Mode B: Semantic Retrieval (Tier 2 and Tier 3)

Used when the classifier returns `ROUTE: null` (Tier 2) or both a route and a `SEARCH_QUERY` (Tier 3). Assembles a dynamic section chain from the full spec.

### Step 1: Keyword Search

Search `sections/metadata.json` fields `keywords` and `queries` for terms from the classifier's `SEARCH_QUERY`. Collect top-10 candidates by match count.

### Step 2: Semantic Search

Run: `uv run scripts/semantic_search.py "<SEARCH_QUERY>" --top-k 5 --json`

The script returns ranked sections with cosine similarity scores. Use results with score >= 0.45 as high-confidence matches.

### Step 3: Merge and Deduplicate

Combine results from Steps 1 and 2. Remove duplicates (same pattern ID). Keep max 5 sections, prioritizing:
1. Sections that appear in BOTH keyword and semantic results
2. Semantic results with score >= 0.5
3. Keyword results with >= 2 matching terms

### Step 4: Cross-Reference Expansion

For the top-3 sections, check their `_xref.md` file (in the same directory). If cross-references point to sections relevant to the SEARCH_QUERY, add them (up to 2 additional sections).

### Step 5: Order by Pattern ID

Sort the final section list by pattern ID. FPF IDs are hierarchical (A.6 before A.6.B, B.1 before B.1.3), giving natural general-to-specific ordering.

### Tier 3 Combined Mode

When the classifier returns BOTH a route file AND a SEARCH_QUERY (Tier 3):
1. Load core sections from the route file (Mode A, Tier 2)
2. Run Mode B Steps 1-5 for the SEARCH_QUERY
3. Merge results, deduplicating sections already loaded from the route
4. Total section count: route core (2-4) + semantic supplement (1-3)
```

- [ ] **Step 5: Move existing Tier 4 and Tier 5 under Mode B reference**

The existing Tier 4 (Keyword Search) and Tier 5 (Semantic Search) sections describe the same tools that Mode B uses. Replace them with a note:

```markdown
## Standalone Fallback Tools

The keyword search (metadata.json) and semantic search (FAISS) tools described in Mode B can also be used as standalone fallbacks in Mode A when the route chain doesn't fully answer the query. See Mode B Steps 1-2 for details.
```

- [ ] **Step 6: Update Loading Budget section**

Replace the existing "Loading Budget" section with:

```markdown
## Loading Budget

Respect the budget from the classifier's strategy table:

| Mode | Scenario | Budget |
|------|----------|--------|
| A | term_lookup | ~800 tokens (1 section) |
| A | route-based (Tier 1) | ~1200-1500 tokens (2-4 core sections) |
| B | semantic (Tier 2) | ~1700-2300 tokens (3-5 sections via search) |
| A+B | combined (Tier 3) | ~2000-2500 tokens (route core + 1-3 semantic) |
```

- [ ] **Step 7: Commit**

```bash
git add agents/fpf-retriever.md
git commit -m "feat: retriever v2 with Mode B semantic fallback"
```

---

### Task 4: Update fpf-reasoner.md with new templates

**Files:**
- Modify: `agents/fpf-reasoner.md:36-131` (add 4 new templates + universal template)

- [ ] **Step 1: Add 4 new burden templates**

After the `rewrite_explanation` template (line 131, after the closing triple backticks), add:

````markdown
### ethical_assurance
```
Here's an ethical audit of your system/process:

1. **Conflict map** (where values clash across scales):
   - [Scale/Level]: [Value A] vs [Value B] — [impact]
   ...

2. **Bias register** (identified biases):
   | Bias type | Where it appears | Risk level | Mitigation |
   |-----------|-----------------|------------|------------|
   ...

3. **Audit checklist**:
   - [ ] [Check item and who should perform it]
   ...
```

### trust_assurance
```
Here's the assurance profile for [system/component]:

1. **Confidence assessment per component**:
   | Component | Formality | Scope | Reliability | Evidence |
   |-----------|-----------|-------|-------------|----------|
   ...

2. **Evidence gaps** (where confidence is weakest):
   - [ ] [Gap description — what evidence is missing]
   ...

3. **Recommendations**:
   - [action to strengthen weakest link]
   ...
```

### composition_aggregation
```
Here's why your aggregation is producing unexpected results:

1. **Diagnosis** (which composition rules are violated):
   - [Rule]: [how it's violated] — [observable symptom]
   ...

2. **Dependency map** (what depends on what):
   [Component A] → [aggregation method] → [Component B]
   ...

3. **Fix recommendations**:
   - [ ] [specific fix and expected result]
   ...
```

### evolution_learning
```
Here's your current improvement cycle and where it breaks:

1. **Current cycle map**:
   Operate → [status] → Observe → [status] → Refine → [status] → Deploy → [status]

2. **Break point**: [where the loop is broken and why]

3. **Loop closure plan**:
   - [ ] [step to close the gap]
   ...

4. **Cycle health indicators**:
   | Indicator | Current state | Target |
   |-----------|--------------|--------|
   ...
```
````

- [ ] **Step 2: Add universal template for Tier 2**

After the `evolution_learning` template, add:

````markdown
### semantic (universal — for Tier 2 queries with no route)
```
Here's a structured analysis of your problem:

## Situation
[Reformulation of the user's problem in their own language]

## Key Patterns Found
[What patterns apply — described in plain language, no FPF terms.
 Each pattern as a numbered insight with practical implication.]

1. **[Insight name]**: [what it means for the user's situation]
   ...

## Recommendations
[Concrete, actionable steps]
- [ ] [step]
...

## Watch Points
[Risks, edge cases, things to monitor]
- [risk and why it matters]
...
```
````

- [ ] **Step 3: Commit**

```bash
git add agents/fpf-reasoner.md
git commit -m "feat: reasoner v2 with 4 new templates + universal template"
```

---

### Task 5: Update fpf-reviewer.md with expanded scope

**Files:**
- Modify: `agents/fpf-reviewer.md:1-6` (update description)
- Modify: `agents/fpf-reviewer.md` (add Tier 2/3 grounding notes)

- [ ] **Step 1: Update frontmatter description**

Replace lines 1-6:
```markdown
---
description: >
  FPF reviewer v2. Validates reasoner output for Tier 2 (semantic)
  and Tier 3 (combined) queries. Checks grounding (claims traceable
  to source sections), plain language compliance (no FPF jargon),
  and actionability. Also validates Tier 1 cross_cutting queries.
  Input: reasoner output + source sections. Output: validated or
  corrected response.
---
```

- [ ] **Step 2: Add Tier 2 grounding note after Check 2**

After the existing "Unacceptable" line in Check 2 (line 42), and after the existing semantic search note (lines 44-45), add:

```markdown
**Tier 2 (semantic) queries**: The section chain was assembled dynamically, not curated. Apply stricter grounding validation:
- Every substantive claim must cite content from at least one loaded section
- If the reasoner makes claims that go beyond the loaded sections, flag and remove
- Pay extra attention to "bridging" claims that connect sections — verify the connection is justified

**Tier 3 (combined) queries**: The section chain mixes curated (route) and dynamic (semantic) sections. Claims based on route sections get normal validation. Claims based on semantic sections get stricter Tier 2 validation.
```

- [ ] **Step 3: Commit**

```bash
git add agents/fpf-reviewer.md
git commit -m "feat: reviewer v2 with tier-aware grounding validation"
```

---

### Task 6: Update SKILL.md with new architecture

**Files:**
- Modify: `skills/fpf/SKILL.md` (update description, burden table, pipeline depth, key files)

- [ ] **Step 1: Update the description in frontmatter**

Replace lines 1-14 of the frontmatter `description` field:
```markdown
---
name: fpf
description: >
  Use when work involves coordination, systems engineering, or
  transdisciplinary problems. Triggers on: teams misunderstanding
  each other, terminology disagreements, choosing between alternatives,
  unpacking mixed contract/spec/SLA language, structuring decisions,
  handing off work, ethical audits, trust/assurance questions,
  aggregation/composition problems, design evolution and learning
  loops, or any systems engineering coordination challenge.
  Also triggers on explicit FPF terms (holon, UTS, DRR, bounded
  context). Supports semantic fallback for queries that don't match
  any predefined route. Do NOT trigger for standard coding, simple
  bug fixes, or single-person tasks.
---
```

- [ ] **Step 2: Update "How It Works" section**

Replace the existing "How It Works" section with:

```markdown
## How It Works

Three-tier architecture: routes as cache, semantic search as foundation.

1. Detect FPF signal in user's message (broader than burden matching)
2. Dispatch fpf-classifier to determine tier and route
3. **Tier 1 (route match):** Load curated section chain — fast, cheap, high quality
4. **Tier 2 (semantic fallback):** No route matches — retriever uses keyword + FAISS search to assemble dynamic chain
5. **Tier 3 (combined):** Multiple concerns — route core + semantic supplement
6. Apply FPF structure internally, deliver results in plain language
```

- [ ] **Step 3: Replace Burden Classification table**

Replace the existing burden table with:

```markdown
## Burden Classification

Detect from user's natural language — no FPF terms needed.

| Burden | User signals | Tier | Action |
|--------|-------------|------|--------|
| project_alignment | teams confused, responsibilities unclear | 1 | Route 1 → route-1-project-alignment.md |
| language_discovery | terminology disagreement, vague idea | 1 | Route 2 → route-2-language-discovery.md |
| boundary_unpacking | contract/SLA/API mixes rules and obligations | 1 | Route 3 → route-3-boundary-unpacking.md |
| comparison_selection | choosing between options, opaque decisions | 1 | Route 4 → route-4-comparison-selection.md |
| generator_portfolio | state-of-the-art survey, reusable scaffold | 1 | Route 5 → route-5-generator-portfolio.md |
| rewrite_explanation | rewrite preserving meaning, different audience | 1 | Route 6 → route-6-rewrite-explanation.md |
| ethical_assurance | bias audit, ethical assumptions, value conflicts | 1 | Route 7 → route-7-ethical-assurance.md |
| trust_assurance | trust metrics, overclaim, evidence aggregation | 1 | Route 8 → route-8-trust-assurance.md |
| composition_aggregation | KPIs lie, aggregation mismatch, sum != whole | 1 | Route 9 → route-9-composition-aggregation.md |
| evolution_learning | design drift, lessons learned, feedback loops | 1 | Route 10 → route-10-evolution-learning.md |
| term_lookup | explicit FPF term question | 1 | metadata.json → direct file load |
| semantic | FPF signal but no route match | 2 | Keyword + FAISS → dynamic chain |
| cross_cutting | multiple burdens match | 3 | Primary route + semantic supplement |
```

- [ ] **Step 4: Replace Pipeline Depth section**

```markdown
## Pipeline Depth (adaptive compute)

| Tier | Agents | Budget |
|------|--------|--------|
| 1: term_lookup | Retriever → Reasoner | ~800 tokens |
| 1: route-based | Retriever → Reasoner | ~1200-1500 tokens |
| 2: semantic | Retriever → Reasoner → Reviewer | ~2000 tokens |
| 3: combined | Retriever → Reasoner → Reviewer | ~2500 tokens |
```

- [ ] **Step 5: Update Key Files section**

Add to the existing Key Files list:
```markdown
- `sections/routes/route-{1..10}.md` — ordered section chains per burden (10 routes)
```

Replace the old line referencing `route-*.md` with the above.

- [ ] **Step 6: Commit**

```bash
git add skills/fpf/SKILL.md
git commit -m "feat: SKILL.md v2 with three-tier architecture"
```

---

### Task 7: Update CLAUDE.md documentation

**Files:**
- Modify: `CLAUDE.md:92-103` (routes table)
- Modify: `CLAUDE.md:67-73` (pipeline depth description)
- Modify: `CLAUDE.md:38` (build_routes.py comment)

- [ ] **Step 1: Update routes table**

Replace the "Six Entry Routes" section (lines 92-103) with:

```markdown
## Ten Entry Routes + Semantic Fallback

| # | User's burden | Route file |
|---|--------------|------------|
| 1 | Teams confused about responsibilities / handoffs | `sections/routes/route-1-project-alignment.md` |
| 2 | Terminology disagreements / vague emerging ideas | `sections/routes/route-2-language-discovery.md` |
| 3 | Contract/SLA/API mixes rules, conditions, obligations | `sections/routes/route-3-boundary-unpacking.md` |
| 4 | Choosing between alternatives / opaque decisions | `sections/routes/route-4-comparison-selection.md` |
| 5 | State-of-the-art survey / portfolio scaffold needed | `sections/routes/route-5-generator-portfolio.md` |
| 6 | Rewrite for different audience / compare text versions | `sections/routes/route-6-rewrite-explanation.md` |
| 7 | Hidden bias / ethical audit / value conflicts | `sections/routes/route-7-ethical-assurance.md` |
| 8 | Trust metrics / overclaim / evidence aggregation | `sections/routes/route-8-trust-assurance.md` |
| 9 | KPIs lie / aggregation mismatch / sum != whole | `sections/routes/route-9-composition-aggregation.md` |
| 10 | Design drift / lessons learned / feedback loops | `sections/routes/route-10-evolution-learning.md` |
| — | Any other FPF-relevant query | Semantic fallback (FAISS + keyword search) |
```

- [ ] **Step 2: Update pipeline depth description**

Replace the pipeline depth paragraph (lines 71-73) with:

```markdown
Pipeline depth is adaptive: simple term lookups use Retriever → Reasoner (~800 tokens), route-based queries use Retriever → Reasoner (~1200-1500), semantic fallback and cross-cutting queries add Reviewer (~2000-2500). Three-tier architecture: routes as cache (Tier 1), semantic search as fallback (Tier 2), combined for cross-cutting (Tier 3).
```

- [ ] **Step 3: Update build_routes.py comment**

Change `route-{1..6}.md` to `route-{1..10}.md` on line 38.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for three-tier routing architecture"
```

---

### Task 8: Update smoke tests

**Files:**
- Modify: `scripts/test_smoke.py:76-85` (update ROUTE_NAMES list)

- [ ] **Step 1: Update ROUTE_NAMES list**

Replace the ROUTE_NAMES list (lines 78-85) with:

```python
    ROUTE_NAMES = [
        'route-1-project-alignment.md',
        'route-2-language-discovery.md',
        'route-3-boundary-unpacking.md',
        'route-4-comparison-selection.md',
        'route-5-generator-portfolio.md',
        'route-6-rewrite-explanation.md',
        'route-7-ethical-assurance.md',
        'route-8-trust-assurance.md',
        'route-9-composition-aggregation.md',
        'route-10-evolution-learning.md',
    ]
```

- [ ] **Step 2: Run smoke tests**

Run: `python3 scripts/test_smoke.py`

Expected: All tests pass, including the 4 new route files.

```
test_all_routes_exist ... ok
test_route_sections_exist ... ok
test_routes_have_core_sections ... ok
test_routes_have_minimum_chain_length ... ok
```

Note: route-7 may have warnings about D.3/D.4 having no file paths. This is expected and acceptable — the test checks that referenced section files exist, and D.3/D.4 have empty file fields (not broken paths).

- [ ] **Step 3: Commit**

```bash
git add scripts/test_smoke.py
git commit -m "test: update smoke tests for 10 routes"
```

---

### Task 9: Final verification

- [ ] **Step 1: Run full smoke test suite**

Run: `python3 scripts/test_smoke.py`

Expected: All tests pass.

- [ ] **Step 2: Run build_routes.py to verify idempotency**

Run: `python3 scripts/build_routes.py`

Expected: All 10 route files written, no errors.

- [ ] **Step 3: Verify route file count**

Run: `ls sections/routes/route-*.md | wc -l`

Expected: `10`

- [ ] **Step 4: Verify no FPF jargon leaked into agent descriptions**

Run: `grep -i "holon\|episteme\|CharacteristicSpace\|SenseCells\|MVPK" agents/fpf-classifier.md agents/fpf-retriever.md agents/fpf-reasoner.md`

Expected: No matches (except in banned-terms lists in reviewer).

- [ ] **Step 5: Spot-check classifier output format**

Read `agents/fpf-classifier.md` and verify:
- Output format includes `SIGNAL`, `TIER`, `SEARCH_QUERY` fields
- Strategy table has all 10 routes + semantic + cross_cutting
- Soft-trigger text is present for LOW confidence

- [ ] **Step 6: Spot-check retriever modes**

Read `agents/fpf-retriever.md` and verify:
- Mode A and Mode B sections exist
- Mode B describes keyword + FAISS + merge + dedup + ordering
- Loading budget table has 4 tiers
- Tier 3 combined mode is documented
