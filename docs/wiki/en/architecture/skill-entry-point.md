---
title: Skill Entry Point
sources:
  - .claude-plugin/marketplace.json
  - .claude-plugin/plugin.json
  - skills/fpf/SKILL.md
last_updated: 2026-06-16T07:21:51Z
tags:
  - architecture
  - skill
  - entry-point
---

# Skill Entry Point

## Components

The FPF skill entry point is the handshake between the host (Claude Code or Codex CLI) and the agent team. The same skill ships as a plugin for **two** runtimes.

| Component | File | Role |
|-----------|------|------|
| Skill descriptor | `skills/fpf/SKILL.md` | YAML frontmatter with trigger description + body with routing logic |
| Plugin manifest | `.claude-plugin/plugin.json` | Plugin name, `version` (`0.6.3`), keywords — consumed by Claude Code's plugin loader |
| Marketplace manifest | `.claude-plugin/marketplace.json` | Declares the `fpf` plugin (source `./`, repository `pokrovskiyv/FPF-agent`) so users can `/plugin marketplace add pokrovskiyv/FPF-agent` |
| Codex plugin manifest | `.codex-plugin/plugin.json` | Mirror manifest for the Codex CLI edition; version kept in lockstep with `.claude-plugin/plugin.json` |
| Codex installer | `scripts/install_codex_plugin.py` | Installs the FPF plugin into Codex CLI via a home-local marketplace |

The plugin advertises itself as *"Coordination patterns for specialists, teams, and AI agents"* with `category: workflow` and keywords like `coordination`, `structured-thinking`, `decision-making`, `comparison`, `audit`.

## Data Flow

1. User sends a message matching the skill's frontmatter description (coordination / decision / audit / comparison language, or an explicit FPF term).
2. The host (Claude Code or Codex CLI) reads `skills/fpf/SKILL.md` and dispatches [fpf-classifier](../agents/fpf-classifier.md).
3. Classifier returns a structured routing decision (burden, tier, route).
4. Skill dispatches [fpf-retriever](../agents/fpf-retriever.md) with the decision.
5. Retriever loads the narrowest relevant sections; Skill dispatches [fpf-reasoner](../agents/fpf-reasoner.md).
6. For Tier 2/3 (semantic fallback or cross-cutting), Skill dispatches [fpf-reviewer](../agents/fpf-reviewer.md) for grounding + jargon guard.
7. Final output shown to user — no FPF terminology visible.

The skill body contains the burden table, pipeline depth table, and confidence gate logic. All file paths inside are relative to `${CLAUDE_PLUGIN_ROOT}`.

## Decisions

- **Trigger description is broad.** The YAML frontmatter intentionally covers coordination, decision-making, audit, comparison, and solo analysis — not just team coordination. This avoids missing legitimate use-cases while a hard negative list (no standard coding, no simple bug fixes, no syntax questions) prevents false triggers.
- **Confidence gate.** High confidence (≥70%) auto-dispatches; low confidence prompts *"This looks like a coordination problem. Want me to help structure it?"* before doing work. Explicit FPF term mentions (holon, UTS, DRR) bypass the gate.
- **Dual-runtime packaging.** The project is packaged as a plugin for **both** Claude Code (`.claude-plugin/`) and Codex CLI (`.codex-plugin/` + `scripts/install_codex_plugin.py` + a home-local marketplace). It is not a Claude-Code-only artifact. Both manifests carry the same version (`0.6.3`); see [Versioning](#versioning) for how they stay in sync.
- **Plain-language contract.** FPF is invisible infrastructure: the skill body forbids any FPF terminology in output. Patterns are applied internally by the Reasoner and guarded by the Reviewer. See [plain-language-contract](plain-language-contract.md).

## Versioning

The `version` field lives in two manifests and must move together:

- The PreToolUse changelog hook (`scripts/update_changelog.py`) runs before every `git commit` and auto-bumps **only** `.claude-plugin/plugin.json` (`feat` → minor, `fix` → patch, `feat!` → major).
- The [fpf-sync](../agents/fpf-sync.md) routine (Step 7) manually bumps **both** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` so the two editions stay in lockstep.

The single update path for the spec and generated artifacts is the **Claude Code Remote Routine** (trigger `trig_01P7UzjrjgsgzLpMHn84bMoo`, cron 1st & 15th of each month at 07:00 UTC = 09:00 Europe/Belgrade). The former GitHub Action `.github/workflows/rebuild-sections.yml` no longer exists; there is no second sync mechanism. See [fpf-sync](../agents/fpf-sync.md) for the eight-step pipeline.

## Related

- [agent-team](agent-team.md)
- [plain-language-contract](plain-language-contract.md)
- [three-tier-retrieval](three-tier-retrieval.md)
- [fpf-classifier](../agents/fpf-classifier.md)
- [fpf-sync](../agents/fpf-sync.md)
