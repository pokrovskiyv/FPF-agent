---
title: Skill Entry Point
sources:
  - skills/fpf/SKILL.md
  - .claude-plugin/plugin.json
  - .claude-plugin/marketplace.json
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - skill
  - entry-point
---

# Skill Entry Point

## Components

The FPF skill entry point is the handshake between Claude Code and the agent team.

| Component | File | Role |
|-----------|------|------|
| Skill descriptor | `skills/fpf/SKILL.md` | YAML frontmatter with trigger description + body with routing logic |
| Plugin manifest | `.claude-plugin/plugin.json` | Plugin name, version, keywords — consumed by Claude Code's plugin loader |
| Marketplace manifest | `.claude-plugin/marketplace.json` | Declares the plugin to Claude Code's marketplace so users can `/plugin marketplace add pokrovskiyv/FPF-agent` |

## Data Flow

1. User sends a message matching the skill's frontmatter description (coordination / decision / audit / comparison language).
2. Claude Code reads `skills/fpf/SKILL.md` and dispatches [fpf-classifier](../agents/fpf-classifier.md) via the Task tool.
3. Classifier returns a structured routing decision.
4. Skill dispatches [fpf-retriever](../agents/fpf-retriever.md) with the decision.
5. Retriever loads sections; Skill dispatches [fpf-reasoner](../agents/fpf-reasoner.md).
6. For Tier 2/3 (semantic or cross-cutting), Skill dispatches [fpf-reviewer](../agents/fpf-reviewer.md).
7. Final output shown to user — no FPF terminology visible.

The skill body contains the burden table, pipeline depth table, and confidence gate logic. All file paths inside are relative to `${CLAUDE_PLUGIN_ROOT}`.

## Decisions

- **Trigger description is broad.** The YAML frontmatter intentionally covers coordination, decision-making, audit, comparison, and solo analysis — not just team coordination. This avoids missing legitimate use-cases while a hard negative list (no syntax questions, no file ops) prevents false triggers.
- **Confidence gate.** High confidence (≥70%) auto-dispatches; low confidence prompts "This looks like a coordination problem. Want me to help structure it?" before doing work. Explicit FPF term mentions (A.6, UTS, DRR) bypass the gate.
- **Two parallel editions.** `skills/fpf/SKILL.md` (Claude Code) and `.agents/skills/fpf/SKILL.md` (Codex). Their descriptions must remain bit-for-bit identical — see [smoke_codex](../modules/smoke_codex.md) for the parity test. Codex lacks `Task` dispatch, so the Codex skill inlines the orchestration.

## Related

- [agent-team](agent-team.md)
- [plain-language-contract](plain-language-contract.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [fpf-classifier](../agents/fpf-classifier.md)
- [smoke_codex](../modules/smoke_codex.md)
