# Changelog

## 2026-06-16

### What's New
- The structured-analysis assistant now decides when to engage from concrete real-world situations — ownership disputes between teams, opaque decisions, tangled contracts/SLAs, misleading KPIs, bias audits, terminology disagreements, audience rewrites, and design-vs-reality drift — rather than an abstract "structure your thinking" pitch, and is explicit about staying out of plain coding, refactors, and syntax. This makes it activate more reliably on the problems it's actually meant for.

### All Changes
- **fix**: rewrite fpf skill description for reliable Layer-1 triggering
- **chore**: add trigger-eval harness + interactive fire-rate tool; harden sync routine
- **docs**: refresh wiki after fpf description rewrite + sync-routine invariant

## 2026-06-15

### What's New
- Across-the-board precision upgrade: the spec now explicitly distinguishes between what exists in a system and what is being claimed about it. This means fewer "description drift" errors — where a report or spec quietly shifts from describing reality to asserting interpretation without signaling the shift
- New authoring rule (E.24): when writing about systems, transformations, or decisions, you are now required to be explicit about what's being claimed to exist vs. what's an observation or inference. Reduces hidden ambiguity in requirements and design docs
- New transformation pattern (A.3.4): a dedicated section for describing how transformations work, with greater precision about what the transformation takes as input vs. what it produces vs. what it assumes
- Anti-Goodhart protection extended to quality improvement loops (E.13 upgrade): now explicitly detects "teaching to the test" patterns in improvement initiatives, not just in metrics design. Helps teams notice when an improvement campaign is optimizing the measurement rather than the underlying thing
- Promise-to-Work tracking improvements (E.18.1): cleaner structure for tracing how a commitment becomes actual work, with explicit handling of gaps between what was promised and what was planned
- Refreshed search index: 279 section files (+12 vs. previous sync), 292 metadata entries (+17)

### All Changes
- **chore**: sync upstream FPF (ontic precision migration + E.24 + A.3.4 + E.13 anti-Goodhart upgrade + E.18.1 P2W + 51 upstream commits)
- **chore**: rebuild sections after upstream sync
- **chore**: AI-enhance all _index.md files with plain-language summaries
- **chore**: AI-enhance glossary-quick.md plain-definition column
- **chore**: wiki compile — update timestamps, fix sync-and-rebuild architecture article
- **chore**: sync upstream + rebuild + AI-enhanced indexes + wiki refresh
- **docs**: refresh wiki, correct doc metrics, fix sync routine wiki-compile step
- **docs**: rebuild local FAISS index (239 → 251 vectors) and correct embeddings figures in Readme
- **chore**: auto-generate doc metrics and add a commit gate for a stale wiki
- **chore**: ignore Python bytecode (__pycache__, *.pyc)

## 2026-06-01

### What's New
- Major quality improvement campaign across 217 pattern sections: descriptions are cleaner, more precise, and easier to navigate — the same patterns you know, now significantly more readable
- New tool for vague language: when a knowledge claim's source, interpretation, or precision level is unclear, the new precision-restoration pattern (C.2.P) tells you exactly how to repair it
- New problem-framing record (C.22.2): before a messy situation is formal enough to type, you can now capture it in a structured first-framing card — useful when you know something is wrong but can't yet articulate what
- New tool for mathematical adequacy (C.29): check whether a formal or mathematical model is actually appropriate to use here, not just technically available
- New wording-repair architecture (E.10.ARCH): when a word is doing hidden work in a description, a routing system now tells you which precision-restoration tool applies — for relations, architecture terms, quality claims, functions, or general wording
- Improved discipline-health assessment (C.21): more structured, typed ways to evaluate whether a field of practice is mature enough to be used as a source of evidence
- Refreshed search index: 251 section files (+14 vs previous sync), 275 metadata entries (+17)

### All Changes
- **chore**: sync upstream FPF + rebuild sections (quality campaign + C.2.P + C.21 + C.22.2 + C.29 + E.10.ARCH)
- **chore**: AI-enhance all _index.md files with plain-language summaries
- **chore**: AI-enhance glossary-quick.md with plain-language definitions column
- **chore**: refresh wiki route articles (timestamps updated)

## 2026-05-15

### What's New
- FPF теперь упакован как полноценный плагин для Codex CLI: можно установить через marketplace командой `codex plugin marketplace add pokrovskiyv/FPF-agent` или локальным скриптом `python3 scripts/install_codex_plugin.py`. После установки навык работает из любой рабочей директории, а не только из корня репо FPF-agent
- Новая команда установки: установщик копирует плагин в `~/plugins/fpf/` и регистрирует его в `~/.agents/plugins/marketplace.json` — обновления делаются через `git pull && python3 scripts/install_codex_plugin.py`
- Свежая синхронизация с upstream FPF: добавлена ontology семиотической эпистемы (E.10.SEMIO), допустимые действия в проблемных ситуациях, функциональные описания и новый паттерн A.15.4 work-relevant source restoration, ужесточена терминология в кластере A.6.P и узле F-G-R

### All Changes
- **chore**: sync upstream FPF — E.10.SEMIO + functional descriptions + A.15.4 + admissible action + A.6.P/F-G-R terminology cleanup
- **chore**: rebuild sections after upstream sync
- **feat**: package FPF as Codex CLI plugin with marketplace and installer

## 2026-05-01

### What's New
- New analysis lens for situations where the act of asking changes the answer: Quantum-Like Modeling (C.26) — covers probe-coupled boundary interaction, enacted distributed-state evidence, and viability-envelope regulation. Useful when answers depend on who is measuring or what they are optimizing for
- Explicit handling of "is this claim still true?" — Temporal Claim Adequacy (C.27) distinguishes state readings, temporal trends, and intervention-sensitive change, so stale or context-shifted statements can be detected instead of silently propagating
- New technique for reaching consensus by deliberately reducing precision: Controlled Semantic Coarsening (A.6.3.CSC) — vs. accidentally vague language nobody noticed got loose
- New patterns for "can the people who need this find it, and recognize it as itself across contexts": Recognition Signatures (A.6.RSIG) + First-Practical Entry & Discoverability Discipline (E.11)
- Major rework of how the spec records its own design rationale: Design-Rationale Record method (E.9 DRR) overhaul — improves how decisions, alternatives, and constraints are captured for future review
- Formal math substrate for the Characteristic concept (A.19.SURF-SPACE, A.19.SUPPORT-VIEW) — the term that replaced "axis"/"dimension" everywhere now has an explicit cross-surface layer
- New navigation aids: Detailed Walk-throughs (I.2) and First-Practical Entry Neighborhood Index (J.4)
- Refreshed search index: +10 indexed sections (236 vs. 226), 267 section files (+27), 253 metadata entries (+11)

### All Changes
- **chore**: sync upstream FPF-Spec (temporal claim adequacy + quantum-like cluster + E.9 DRR + A.19.* + recognizability)
- **chore**: rebuild sections after upstream sync
- **docs**: add 'What's New' for upstream sync — describe user-facing additions
- **fix**: complete truncated changelog entry from previous commit

## 2026-04-15

### What's New
- FPF skill теперь доступен и в OpenAI Codex CLI — одна команда `git clone && uv sync`, и тот же триггер по описанию задачи работает рядом с существующей установкой в Claude Code
- New analysis path for choosing between options under uncertainty: expected utility, value of information, and robustness to bad-case outcomes (Decision Theory)
- Cleaner terminology for process-effectiveness questions — how to notice and close "non-quality-driven" gaps in how work actually happens
- Broader skill triggers: `/fpf` now also fires for solo analysis work (spec review, trade-offs, survey of approaches), not just team-coordination problems
- Specification preamble rewritten for clarity about what FPF is and why it matters
- Refreshed search index: +37 indexed sections (226 vs. 189), coverage 93% vs. 78%, new dependency edges connect Decision Theory to comparison/selection routes

### All Changes
- **chore**: broaden skill triggers to solo analysis + expand marketplace keywords
- **chore**: sync upstream FPF-Spec (C.11 Decision Theory + NQD cleanup) and rebuild sections
- **feat**: add Codex CLI edition of FPF skill
- **docs**: initialize bilingual (RU+EN) wiki for FPF-agent

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
