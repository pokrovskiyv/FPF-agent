---
title: smoke_codex
sources:
  - scripts/smoke_codex.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - testing
  - codex
  - smoke-tests
---

# smoke_codex

> Source: `scripts/smoke_codex.py`

## Purpose

Dedicated smoke suite for the Codex edition of the FPF skill (`.agents/skills/fpf/SKILL.md`). Validates frontmatter, checks that every file path mentioned in the skill body resolves, and confirms the Codex skill description matches the Claude Code edition so both environments trigger on identical user phrasing.

Also guards against Codex-specific hazards — e.g., the skill body must not instruct Codex to "Dispatch fpf-..." since Codex has no Task-dispatch primitive.

## Interface

`unittest`-based module. Auto-discovered test classes:

| Class | What it checks |
|-------|---------------|
| `TestCodexSkillStructure` | Frontmatter present, `name: fpf`, description substantive (>50 chars) and identical to the Claude Code edition |
| `TestCodexSkillReferences` | ≥4 `agents/fpf-*.md` references resolve; concrete `sections/...` paths exist; all `scripts/*.py` references exist; no forbidden tokens (`Dispatch fpf-`, `Task tool`) |
| `TestSemanticSearchCLI` | Only when `--all` given: subprocess `uv run scripts/semantic_search.py` succeeds and returns the expected JSON shape |

Helpers: `split_frontmatter(text) -> (fm, body)` and `parse_minimal_yaml(fm) -> dict` — stdlib-only YAML-ish parsing sufficient for `name:` and `description:` fields.

## Algorithm

Per-class setUp reads and splits the Codex SKILL.md. Each test runs independently:
- Reference tests use `_extract_paths(pattern)` to dedupe regex matches and verify `(PROJECT_ROOT / path).exists()` for every extracted path.
- The description-parity test reads the Claude Code skill too and asserts exact string equality — drift in description means different trigger behavior across environments.
- The Task-dispatch guard is a plain `assertNotIn` on the body text.

Like `test_smoke.py`, `--all` is filtered from `argv` before passing to `unittest.main` so the test runner doesn't complain.

## Dependencies

**Imports:** `json`, `re`, `subprocess`, `sys`, `unittest`, `pathlib.Path` — stdlib only.

**Imported by:** Run standalone after edits to `.agents/skills/fpf/SKILL.md` or `skills/fpf/SKILL.md`.

## See also

- [test_smoke](test_smoke.md) — equivalent suite for the Claude Code edition
- [skill-entry-point](../architecture/skill-entry-point.md)
- [semantic_search](semantic_search.md)
