---
title: smoke_codex
sources:
  - scripts/smoke_codex.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - module
  - testing
  - codex
  - smoke-tests
  - plugin
---

# smoke_codex

> Source: `scripts/smoke_codex.py`

## Purpose

Dedicated smoke suite for the Codex edition of the FPF skill (`.agents/skills/fpf/SKILL.md`) and the Codex CLI plugin packaging. Validates skill frontmatter, checks that every file path mentioned in the skill body resolves, confirms the Codex skill description matches the Claude Code edition (so both environments trigger on identical user phrasing), and verifies that the repo root is a well-formed Codex plugin with a working installer and marketplace metadata.

Runs offline — no Codex CLI required, and it does not verify LLM behavior. It also guards against Codex-specific hazards: the skill body must not instruct Codex to "Dispatch fpf-..." or use the "Task tool", since Codex has no Task-dispatch primitive and must orchestrate the agent team inline.

## Interface

`unittest`-based module. Auto-discovered test classes:

| Class | What it checks |
|-------|---------------|
| `TestCodexSkillStructure` | Frontmatter present, `name: fpf`, description substantive (>50 chars) and identical to the Claude Code edition (`skills/fpf/SKILL.md`) |
| `TestCodexSkillReferences` | ≥4 `agents/fpf-*.md` references resolve; concrete `sections/...` paths exist; all `scripts/*.py` references exist; no forbidden tokens (`Dispatch fpf-`, `Task tool`) |
| `TestSemanticSearchCLI` | Only when `--all` given: subprocess `uv run scripts/semantic_search.py` succeeds and returns the expected JSON shape (`rank`, `score`, `pattern_id`, `title`, `file`, `keywords`) |
| `TestRootCodexPlugin` | The repo root is the source-controlled Codex plugin: `.codex-plugin/plugin.json` declares `name: fpf`, `skills: ./.agents/skills/`, `license: MIT`, and an `interface` with `displayName: FPF` + `defaultPrompt`; all runtime files exist at plugin root; no duplicated `plugins/fpf` tree; the skill uses the `<FPF_PLUGIN_ROOT>` contract and its references resolve under that root |
| `TestCodexPluginInstaller` | `scripts/install_codex_plugin.py --home <tmp>` syncs the packaged plugin into a home-local Codex marketplace, copies all runtime files, writes the marketplace entry, and does not nest a `plugins/fpf` tree |
| `TestRepoLocalMarketplace` | `.agents/plugins/marketplace.json` exposes a single `fpf` entry whose `source` is `local`, `path` is `./.`, with `AVAILABLE`/`ON_INSTALL` policy and `Productivity` category |

Helpers: `split_frontmatter(text: str) -> tuple[str, str]` returns `(frontmatter_block, body)` (empty frontmatter if missing), and `parse_minimal_yaml(fm: str) -> dict` is a stdlib-only YAML-ish parser sufficient for `name:` and `description:` fields, including `>`/`|` block scalars.

Module-level constants pin the paths under test: `CODEX_SKILL` (`.agents/skills/fpf/SKILL.md`), `CC_SKILL` (`skills/fpf/SKILL.md`), `PLUGIN_MANIFEST` (`.codex-plugin/plugin.json`), `DUPLICATED_PLUGIN_ROOT` (`plugins/fpf`, expected absent), and `REPO_MARKETPLACE` (`.agents/plugins/marketplace.json`). `RUN_ALL` is `True` when `--all` is in `sys.argv`.

## Algorithm

Per-class `setUp` reads and splits the Codex SKILL.md where needed. Each test runs independently:

1. **Structure** — parse frontmatter via `split_frontmatter` + `parse_minimal_yaml`, assert `name == 'fpf'` and a substantive description, then read the Claude Code skill and assert exact description equality (drift in description means different trigger behavior across environments).
2. **References** — `_extract_paths(pattern)` dedupes regex matches; the suite verifies `(PROJECT_ROOT / path).exists()` for every extracted agent/section/script path, and uses a plain `assertNotIn` on the body for the Task-dispatch guard.
3. **Plugin root** — load `.codex-plugin/plugin.json`, assert its fields; check the required runtime files exist; assert `plugins/fpf` does NOT exist; assert the skill body contains `<FPF_PLUGIN_ROOT>`, the phrase "plugin root", and `--index-dir <FPF_PLUGIN_ROOT>/sections/embeddings`, and does NOT contain the stale `launched from the FPF-agent repo root` wording.
4. **Installer** — run `install_codex_plugin.py` against a `tempfile.TemporaryDirectory()` home, assert exit 0, then verify the installed manifest, runtime files, absence of a nested `plugins/fpf`, and the marketplace entry (`source.path == './plugins/fpf'`, `AVAILABLE`/`ON_INSTALL`, `Productivity`).
5. **Repo marketplace** — load `.agents/plugins/marketplace.json` and assert the single `fpf` entry points at the repo root (`source.source == 'local'`, `source.path == './.'`).

Like `test_smoke.py`, `--all` is filtered out of `argv` before being passed to `unittest.main` so the runner doesn't complain about an unknown flag.

## Dependencies

**Imports:** `json`, `re`, `subprocess`, `sys`, `tempfile`, `unittest`, `pathlib.Path` — stdlib only.

**Imported by:** Run standalone after edits to `.agents/skills/fpf/SKILL.md`, `skills/fpf/SKILL.md`, `.codex-plugin/plugin.json`, `scripts/install_codex_plugin.py`, or `.agents/plugins/marketplace.json`.

## See also

- [test_smoke](test_smoke.md) — equivalent suite for the Claude Code edition
- [skill-entry-point](../architecture/skill-entry-point.md)
- [semantic_search](semantic_search.md)
