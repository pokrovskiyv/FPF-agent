# Changelog

## 2026-04-15

### What's New
- New analysis path for choosing between options under uncertainty: expected utility, value of information, and robustness to bad-case outcomes (Decision Theory)
- Cleaner terminology for process-effectiveness questions — how to notice and close "non-quality-driven" gaps in how work actually happens
- Broader skill triggers: `/fpf` now also fires for solo analysis work (spec review, trade-offs, survey of approaches), not just team-coordination problems
- Specification preamble rewritten for clarity about what FPF is and why it matters
- Refreshed search index: +37 indexed sections (226 vs. 189), coverage 93% vs. 78%, new dependency edges connect Decision Theory to comparison/selection routes

### All Changes
- **chore**: broaden skill triggers to solo analysis + expand marketplace keywords
- **chore**: sync upstream FPF-Spec (C.11 Decision Theory + NQD cleanup) and rebuild sections

## 2026-04-04

### All Changes
- **docs**: rewrite README intro for clarity — explain what FPF is and why it matters

## 2026-04-03

### All Changes
- **feat**: automated changelog + auto-versioning via PreToolUse hook
- **chore**: sync schedule monthly → every 2 weeks (1st and 15th)

## 2026-04-02

### What's New
- FPF Thinking Amplifier: skill + five-agent team with 10 entry routes, three-tier retrieval, and semantic search fallback
- Local FAISS semantic search (BAAI/bge-m3 multilingual) replaces cloud dependency
- Cross-reference index (493 xrefs) connects patterns across all Parts
- Four new analysis routes: ethical audits, trust metrics, system composition, and feedback loops
- Three-tier routing: fast cached routes, semantic fallback, combined mode for cross-cutting questions
- Russian README with deep model comparison (Haiku/Sonnet/Opus)

### All Changes
- **feat**: FPF skill-agent with plain language contract
- **feat**: cross-references (493 xrefs) + Pinecone semantic search prep
- **feat**: local FAISS semantic search (BAAI/bge-m3) replaces Pinecone
- **feat**: Russian README + deep model comparison (Haiku/Sonnet/Opus)
- **feat(routes)**: add routes 7-10 (ethics, trust, composition, evolution)
- **feat(classifier)**: classifier v2 with three-tier signal detection
- **feat(retriever)**: retriever v2 with Mode B semantic fallback
- **feat(reasoner)**: reasoner v2 with 4 new templates + universal template
- **feat(reviewer)**: reviewer v2 with tier-aware grounding validation
- **feat(skill)**: SKILL.md v2 with three-tier architecture
- **fix**: correct Opus S1 stress test result (PARTIAL, not PASS)
- **fix**: parse 7 missing ToC entries (pipe inside backticks) + rewrite README intro
- **fix**: semantic threshold 0.83→0.45, term_lookup jargon guard, metadata resolution
- **docs**: update agent team, pipeline docs, and plugin structure
- **docs**: add technical pipeline details to README
- **docs**: reposition README — FPF improves your work, not teaches you FPF
- **docs**: simplify install instructions, sync schedule monthly
- **docs**: move installation to top of README
- **docs**: update CLAUDE.md for three-tier routing architecture
- **docs**: update README for three-tier routing architecture (10 routes + semantic fallback)
- **test**: update smoke tests for 10 routes
- **style**: remove AI-sounding patterns from README
- **style**: replace em dashes with periods and commas for natural flow
- **chore**: remove dead files for cleaner public repo
