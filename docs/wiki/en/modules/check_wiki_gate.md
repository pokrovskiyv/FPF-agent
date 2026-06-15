---
title: check_wiki_gate
sources:
  - scripts/check_wiki_gate.py
last_updated: 2026-06-15T00:00:00Z
tags:
  - module
  - hook
  - wiki
  - gate
---

# check_wiki_gate

> Source: `scripts/check_wiki_gate.py`

## Purpose

A deterministic PreToolUse hook (wired on `git commit` in `.claude/settings.json`) that blocks a commit which *claims* a wiki refresh while the wiki is actually stale. The real failure mode this prevents: the `fpf-sync` routine commits "… + wiki refresh", but `/wiki compile` had silently done nothing (the manifest never advanced), so the claim landed with no actual change. The hook reads the commit message; if its subject says it refreshed the wiki but `scanner.py check` reports the wiki is stale, the commit is denied (exit 2) with an explanation. Commits that do not claim a wiki refresh are never affected, and any infrastructure error fails open (the commit proceeds).

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `extract_commit_message` | `(bash_command: str) -> str \| None` | Pull the commit message out of the bash command; handles both the heredoc (`<<EOF … EOF`) and `-m "…"` / `-m '…'` forms; returns `None` if neither matches |
| `wiki_is_stale` | `() -> bool \| None` | Run `scanner.py check <project root>`; `True` = stale (exit 1), `False` = fresh (exit 0), `None` = could not determine (scanner missing, subprocess error, or unexpected exit → fail open) |
| `main` | `() -> None` | Read hook JSON from stdin, decide whether to gate, and `sys.exit(2)` to deny if the claim is unbacked |

Module constants: `PROJECT_ROOT` (repo root, two levels up from the script), `SCANNER` (`~/.claude/skills/wiki/scanner.py`), and `CLAIM_RE` (`wiki\s+(refresh|compile|rebuild)`, case-insensitive).

## Algorithm

1. Read the hook payload as JSON from stdin. On `JSONDecodeError` / `EOFError`, return silently (allow the commit).
2. Read `tool_input.command`. If it does not contain `git commit`, return (not our concern).
3. Extract the commit message via `extract_commit_message`. If the message does not match `CLAIM_RE` — i.e. it does not claim a wiki refresh/compile/rebuild — return (allow).
4. Call `wiki_is_stale()`. Only when it returns exactly `True` does the hook deny: it writes a remediation message to stderr (run `/wiki compile`, confirm `docs/wiki/.state/manifest.json` advanced, re-check with `scanner.py check .`) and `sys.exit(2)` to block the tool call.
5. Every other path — no claim, fresh wiki, or an indeterminate scanner result (`None`) — falls through and the commit proceeds. The gate is deliberately fail-open: it only ever blocks on a *positive* staleness signal against a *positive* claim.

## Dependencies

**Imports:** `json`, `re`, `subprocess`, `sys`, `pathlib.Path` — stdlib only.

**External tool:** `~/.claude/skills/wiki/scanner.py` (the wiki staleness checker), invoked with `sys.executable`.

**Invoked by:** `.claude/settings.json` as a PreToolUse hook on `Bash` matching `git commit`.

## See also

- [update_changelog](update_changelog.md) — the other PreToolUse `git commit` hook
- [sync-and-rebuild](../architecture/sync-and-rebuild.md) — the `fpf-sync` routine whose wiki-refresh claim this gate guards
- CLAUDE.md "Wiki" section — `/wiki compile`, `scanner.py check`, and the manifest
