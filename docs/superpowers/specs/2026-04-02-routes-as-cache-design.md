# Routes as Cache: Three-Tier FPF Routing Architecture

**Date:** 2026-04-02
**Status:** Draft
**Problem:** 6 hardcoded routes cover ~16% of FPF spec (37/242 patterns), creating a ceiling on what users can access. Part D (ethics) has 0% coverage. The fixed-route model doesn't scale with spec growth.

## Design Principle

Routes are an **optimization (cache), not the architecture**. The foundation is retrieval over all 242 patterns. Routes are pre-computed, curated section chains for frequent queries.

## Three-Tier Architecture

```
User query → Classifier v2
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
    Tier 1     Tier 2     Tier 3
   Route      Semantic   Combined
   match      fallback   (route + semantic)
        │         │          │
        ▼         ▼          ▼
   route file  FAISS      route core +
   → chain     top-k →    FAISS supplement
   (800-1500)  dynamic    (2000-2500)
               chain
               (1200-2000)
```

**Tier 1 — Route match.** Classifier maps query to one of ~10 routes with HIGH confidence (>=70%). Retriever loads route file and core sections. Cheapest and highest-quality path.

**Tier 2 — Semantic fallback.** No route matches. Retriever uses keyword search (metadata.json) + FAISS embeddings to assemble a dynamic section chain. Slightly more expensive, but covers all 242 patterns.

**Tier 3 — Combined.** Query touches a route + additional areas. Retriever loads route core + supplements with semantic search. Most expensive, for cross-cutting queries.

### Token Budget

| Tier | Retriever | Reasoner | Total | Frequency |
|------|-----------|----------|-------|-----------|
| 1    | ~500      | ~1200    | ~1700 | ~60%      |
| 2    | ~800      | ~1800    | ~2600 | ~30%      |
| 3    | ~1000     | ~2200    | ~3200 | ~10%      |
| **Weighted avg** | | | **~2100** | vs ~1700 now (+24%) |

## Classifier v2

### Logic Change

Current: "Which of 6 burdens?" → `NONE` if no match.
New: "Is there an FPF signal? If yes — which tier is optimal?"

```
User query
    │
    ▼
Is there an FPF signal? ── no ──► NONE (don't trigger)
    │ yes
    ▼
Matches a route? ── HIGH (>=70%) ──► Tier 1
    │ no/LOW
    ▼
Multiple routes? ── yes ──► Tier 3
    │ no
    ▼
Tier 2 (semantic)
```

### FPF Signal Detection (broader than burden matching)

The classifier detects ANY coordination, systems engineering, or transdisciplinary signal — not just the 10 route-specific burdens. Examples of Tier 2 signals:

- "How to formalize norms in our domain?"
- "Need a framework for architectural decisions"
- "How to combine approaches from different disciplines?"
- "Need a methodology for systematic research"

### Expanded Signal Table

| Signal Group | Example Phrases | Tier |
|---|---|---|
| Project alignment | "teams don't understand each other", "who owns what" | 1 (route-1) |
| Language discovery | "can't agree on terms", "vague idea" | 1 (route-2) |
| Boundary unpacking | "contract mixes everything", "rules vs obligations" | 1 (route-3) |
| Comparison selection | "choose between options", "trade-offs" | 1 (route-4) |
| Generator portfolio | "state of the art", "survey the field" | 1 (route-5) |
| Rewrite explanation | "rewrite for different audience", "simplify this" | 1 (route-6) |
| **Ethical assurance** | "hidden bias", "ethical audit", "value conflicts" | 1 (route-7) |
| **Trust & assurance** | "can we trust this metric", "overclaim", "evidence" | 1 (route-8) |
| **Composition** | "KPIs lie", "sum of parts != whole", "aggregation" | 1 (route-9) |
| **Evolution** | "design is outdated", "lessons learned", "feedback loop" | 1 (route-10) |
| **General FPF signal** | coordination, systems engineering, transdisciplinary | 2 (semantic) |

### Output Format v2

```
SIGNAL: [yes/no]
TIER: [1/2/3]
BURDEN: [burden_type]           # for Tier 1
CONFIDENCE: [HIGH/LOW/BYPASS]
ROUTE: [route file | null]      # null for Tier 2
PIPELINE: [retriever→reasoner | retriever→reasoner→reviewer]
BUDGET: [token budget]
SECTIONS: [...]                 # for Tier 1 (from route); empty for Tier 2
SEARCH_QUERY: [...]             # for Tier 2/3 (hint for retriever)
```

### Soft-trigger

For Tier 2 with LOW confidence:

> "This looks like a coordination / systems engineering problem. Want me to help structure it?"

## New Routes (7-10)

### Route 7: Ethical Assurance

- **Burden:** "How to audit for hidden bias? What ethical assumptions are we making?"
- **Why route:** Part D forms a closed cycle: principles → conflict topology → mapping → audit → register. Semantic search finds pieces, not the cycle.
- **Chain:** D.1 → D.2 → D.3 → D.4 → D.5
- **Core:** D.2, D.3, D.5
- **Artifact:** Bias register, conflict map by scale, audit checklist

### Route 8: Trust & Assurance

- **Burden:** "Can we trust this metric? How to aggregate confidence without overclaim?"
- **Why route:** Trust calculus (F-G-R) is a formal system with three components + aggregation rules. Needs strict order: definitions → aggregation → grounding.
- **Chain:** B.3 → B.3.5 → B.1 → B.1.1 → A.6.B
- **Core:** B.3, B.3.5, B.1
- **Artifact:** Assurance profile (F/G/R per component), dependency map, evidence gaps

### Route 9: Composition & Aggregation

- **Burden:** "Why do KPI dashboards lie? Why does Tool A aggregate differently from Tool B?"
- **Why route:** Aggregation (Gamma) has 5 invariants (Invariant Quintet) and 4 specializations (sys/epist/ctx/time). Without curated chain, user gets fragments.
- **Chain:** B.1 → B.1.1 → B.1.2 → B.1.3 → B.1.4 → B.1.5
- **Core:** B.1, B.1.1, B.1.4
- **Artifact:** Violated invariant diagnosis, aggregation dependency map, fix recommendations

### Route 10: Evolution & Learning Loops

- **Burden:** "Design is outdated and nobody noticed. How to close the loop between operations and design?"
- **Why route:** Evolution Loop is a 4-phase cycle (Operate → Observe → Refine → Deploy), each phase depends on previous + B.5.1 state machine. Order is critical.
- **Chain:** B.4 → B.4.1 → B.5.1 → A.4 → G.11
- **Core:** B.4, B.4.1, B.5.1
- **Artifact:** Current cycle map (where the break is), loop closure plan, cycle health metrics

### Route Coverage After Expansion

| Metric | Before | After |
|--------|--------|-------|
| Routes | 6 | 10 |
| Patterns in routes | ~37 (16%) | ~58 (24%) |
| Part D coverage | 0% | ~33% |
| Part B coverage | 13% | ~35% |
| **+ Tier 2 semantic** | — | **100%** |

## Retriever v2

### Two Modes

**Mode A (Tier 1 — route):** Unchanged. Receives route file, loads core sections.

**Mode B (Tier 2 — semantic):** Receives `SEARCH_QUERY` from classifier. Assembles dynamic chain:

```
SEARCH_QUERY
    │
    ▼
Tier 4: keyword search metadata.json (keywords + queries fields)
    │ top-10 candidates
    ▼
Tier 5: FAISS semantic search (top-5 results)
    │ merge + deduplicate
    ▼
Rank & cut (max 5 sections by relevance score)
    │
    ▼
Load _xref.md for top-3 sections (add if relevant)
    │ final chain: 3-7 sections
    ▼
Pass to Reasoner
```

### Section Ordering (Tier 2)

Sort by pattern ID. FPF IDs are hierarchical: `A.6` before `A.6.B`, `B.1` before `B.1.3`. This gives natural general-to-specific ordering at zero token cost.

### Tier 2 Token Budget

| Step | Tokens | Purpose |
|------|--------|---------|
| metadata.json scan | ~200 | Keyword matching |
| FAISS query | ~100 | semantic_search.py call |
| Load 3-5 sections | ~1200-1800 | Main content for reasoner |
| _xref.md check | ~200 | Additional context |
| **Total** | **~1700-2300** | |

## Reasoner v2

### 10 Route Templates + 1 Universal

4 new templates for routes 7-10:

| Route | Output Template |
|-------|----------------|
| 7: Ethical Assurance | Conflict map → Bias register → Audit checklist |
| 8: Trust & Assurance | Assurance profile (F/G/R) → Gaps → Recommendations |
| 9: Composition | Invariant diagnosis → Dependency map → Fixes |
| 10: Evolution | Current cycle → Break point → Closure plan |

Universal template for Tier 2 (semantic, no route):

```markdown
## Structured Analysis

### Situation
[Reformulation of user's problem]

### Key Patterns Found
[Applicable patterns in user's language, no FPF terms]

### Recommendations
[Concrete steps]

### Watch Points
[Risks and things to monitor]
```

## Reviewer v2 Scope

| Tier | Reviewer? | Why |
|------|-----------|-----|
| 1 (any route) | No | Curated chain, reliable enough |
| 2 (semantic) | **Yes** | Dynamic chain needs grounding validation |
| 3 (combined) | **Yes** | Most complex case |

Reviewer checks: grounding (claims traceable to loaded sections) + jargon guard (no FPF terms in output).

## Migration Plan

| Step | What | Risk |
|------|------|------|
| 1 | Add 4 route files (7-10) to `build_routes.py` | Zero — additive |
| 2 | Update classifier: new SIGNAL→TIER logic | Medium — regression test old burdens |
| 3 | Update retriever: add Mode B (semantic) | Low — Tier 4-5 already implemented |
| 4 | Update reasoner: 4 new templates + universal | Low — additive |
| 5 | Update reviewer: expand scope to Tier 2/3 | Zero — same logic, called more often |
| 6 | Update SKILL.md and CLAUDE.md | Zero — documentation |

## Test Plan

### Tier 1 Regression (routes 1-6)
- [ ] "Teams don't understand each other" → route-1
- [ ] "Can't agree on terms" → route-2
- [ ] "Contract mixes rules and obligations" → route-3
- [ ] "Choose between options" → route-4
- [ ] "State of the art survey" → route-5
- [ ] "Rewrite for different audience" → route-6

### Tier 1 New Routes (7-10)
- [ ] "How to audit hidden bias in the system?" → route-7
- [ ] "Can we trust this aggregated metric?" → route-8
- [ ] "Why does the sum of parts != the whole?" → route-9
- [ ] "Design is outdated, nobody updates it" → route-10

### Tier 2 Semantic Fallback
- [ ] "How to formalize norms in our domain?" → semantic → C.10
- [ ] "Need a framework for architectural decisions" → semantic → C.12
- [ ] "How to apply this to a physical system?" → semantic → C.1

### Tier 3 Combined
- [ ] "Teams don't understand each other and we can't trust the metrics" → route-1 + semantic (B.3)

### Non-trigger (must NOT activate)
- [ ] "Fix the bug in auth.ts" → NONE
- [ ] "Write a React component" → NONE
- [ ] "How do I use git rebase?" → NONE
