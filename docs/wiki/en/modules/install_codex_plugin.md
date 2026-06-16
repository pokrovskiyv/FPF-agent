---
title: install_codex_plugin
sources:
  - scripts/install_codex_plugin.py
last_updated: 2026-06-16T03:34:37Z
tags:
  - module
  - codex
  - installer
  - marketplace
  - plugin
---

# install_codex_plugin

> Source: `scripts/install_codex_plugin.py`

## Purpose

Installs FPF as a Codex CLI plugin into a **home-local marketplace**, so the skill works from any working directory rather than only inside the FPF-agent repo. The installer does not copy a source-controlled duplicate package — it assembles a minimal plugin from the repository root by copying the runtime files the skill actually needs into `~/plugins/fpf` and registering an entry in `~/.agents/plugins/marketplace.json`.

The same script handles updates: after `git pull`, re-running it rebuilds `~/plugins/fpf` from the current repo state (the old target directory is removed first) and refreshes the marketplace entry idempotently. A `--home` flag redirects the install root, which is what the smoke tests use to install into a temporary directory.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `plugin_entry` | `() -> dict` | Builds the marketplace record for `fpf`: `source` is `local` pointing at `./plugins/fpf`, policy `installation: AVAILABLE` / `authentication: ON_INSTALL`, category `Productivity` |
| `load_marketplace` | `(path: Path) -> dict` | Reads `marketplace.json` or returns a fresh `local` skeleton; raises `ValueError` on invalid JSON or a non-object root, and backfills missing `plugins` / `name` / `interface.displayName` keys |
| `update_marketplace` | `(path: Path) -> None` | Drops any existing `fpf` entry, appends a fresh one from `plugin_entry()`, creates the parent dir, and writes pretty-printed JSON (`ensure_ascii=False`, indent 2) |
| `sync_plugin` | `(source: Path, target: Path) -> None` | Validates the source, removes the old target, then copies the runtime directories and files into it (skipping `__pycache__`, `*.pyc`, `.DS_Store`) |
| `parse_args` | `(argv: list[str]) -> argparse.Namespace` | Parses `--home` (default current user's home) and `--source` (default project root) |
| `main` | `(argv: list[str] \| None = None) -> int` | Resolves home and source, runs `sync_plugin` then `update_marketplace`, prints the install + marketplace paths, returns `0` |

Module constants define what gets copied. `COPY_DIRECTORIES` copies `.codex-plugin`, `.agents/skills/fpf`, `agents`, and `sections`; `COPY_FILES` copies `scripts/semantic_search.py` and `scripts/build_embeddings.py`. `PLUGIN_NAME` is `fpf`; `DEFAULT_PLUGIN_SOURCE` is the repository root resolved from `__file__`.

## Algorithm

1. `main` resolves `--home` and `--source` (expanding `~` and resolving to absolute paths), then derives `target = home/plugins/fpf` and `marketplace_path = home/.agents/plugins/marketplace.json`.
2. `sync_plugin(source, target)` runs its guard checks: the source must exist, must contain `.codex-plugin/plugin.json`, and must not equal the target. It then asserts every path in `COPY_DIRECTORIES` and `COPY_FILES` exists, collecting any missing ones into a single `FileNotFoundError`.
3. If `target` already exists it is removed with `shutil.rmtree`, then recreated fresh. Each directory is copied with `shutil.copytree` (using the ignore filter); each file is copied with `shutil.copy2` after ensuring its parent exists. This is what makes re-running the installer a clean update rather than a merge.
4. `update_marketplace(marketplace_path)` loads (or initializes) the marketplace, removes any prior `fpf` entry so re-runs don't duplicate it, appends the current `plugin_entry()`, and writes the file back.
5. `main` prints `Installed plugin: <target>` and `Updated marketplace: <marketplace_path>` and returns `0`.

The update path is therefore: `git pull` to refresh the repo, then `python3 scripts/install_codex_plugin.py` to re-sync the home-local copy. No separate uninstall step is needed — the target directory is rebuilt and the marketplace entry is replaced in place.

## Usage

```bash
# First install (from the repo root)
python3 scripts/install_codex_plugin.py

# Update after pulling new spec/sections
git pull && python3 scripts/install_codex_plugin.py

# Install into an alternate home (used by tests)
python3 scripts/install_codex_plugin.py --home /tmp/codex-home
```

After install, the semantic fallback needs its FAISS index built once from the installed copy: `cd ~/plugins/fpf && uv run scripts/build_embeddings.py`.

## Dependencies

**Imports:** `argparse`, `json`, `shutil`, `sys`, `pathlib.Path` — standard library only.

**Imported by:** invoked as a script. Referenced from `Readme.md` and `CLAUDE.md` as the local-install command, and listed in `CHANGELOG.md` as the Codex installer. The `.codex-plugin/` manifest it packages is the Codex twin of `.claude-plugin/` — both `plugin.json` files are kept in lockstep at version `0.6.1`.

## See also

- [smoke_codex](smoke_codex.md) — validates the Codex edition of the skill that this installer ships
- [build_embeddings](build_embeddings.md) — builds the FAISS index the installed plugin needs for semantic fallback
- [sync-and-rebuild](../architecture/sync-and-rebuild.md) — the routine that bumps both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
- [changelog-workflow](../concepts/changelog-workflow.md)
