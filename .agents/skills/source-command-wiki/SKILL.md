---
name: "source-command-wiki"
description: "Check, query, or regenerate the FPF plugin wiki when the user requests wiki work."
---

# source-command-wiki

Use this skill when the user asks to run the migrated source command `wiki`.

## Plugin root

Resolve `<FPF_PLUGIN_ROOT>` as the nearest ancestor of this Skill containing `.codex-plugin/plugin.json`. Run scanner and wiki work from that root, including when installed, rather than from the user's project.

## Command Template

Invoke the wiki skill at ~/.claude/skills/wiki/SKILL.md.
Wiki state: docs/wiki/.state/config.json
Scanner: python3 ~/.claude/skills/wiki/scanner.py

Pass the user's argument to determine the subcommand:
- No args or "status": run `python3 ~/.claude/skills/wiki/scanner.py check <FPF_PLUGIN_ROOT>` and report
- "init": full initialization
- "compile": incremental update
- "rebuild": full recompilation
- "lint": integrity check
- "query <question>": Q&A mode

Project specifics:
- The wiki is bilingual (RU + EN) with parallel trees under docs/wiki/ru/ and docs/wiki/en/.
- When regenerating articles, always produce BOTH language variants.
- Code identifiers, pattern IDs, filenames stay English in both languages.
- Generated section files under `sections/` (not routes/) are excluded from the wiki — they're derived from FPF-Spec.md, not source code.
