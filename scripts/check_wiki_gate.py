#!/usr/bin/env python3
"""Deterministic gate: block a commit that CLAIMS a wiki refresh while the wiki
is actually stale.

The fpf-sync routine commits "… + wiki refresh". The real failure mode we hit
was: that commit landed even though `/wiki compile` had silently done nothing
(manifest never advanced). This PreToolUse hook makes that impossible — if the
commit subject says it refreshed the wiki but `scanner.py check` reports stale,
the commit is denied (exit 2) with an explanation. Commits that do not claim a
wiki refresh are never affected.

Wired as a PreToolUse hook on `git commit` in .claude/settings.json.
Reads the hook JSON from stdin. Fail-open on any infrastructure error.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCANNER = Path.home() / ".claude" / "skills" / "wiki" / "scanner.py"

# Only gate commits that explicitly claim the wiki was (re)built.
CLAIM_RE = re.compile(r"wiki\s+(refresh|compile|rebuild)", re.IGNORECASE)


def extract_commit_message(bash_command: str) -> str | None:
    heredoc = re.search(r"<<\s*['\"]?EOF['\"]?\s*\n(.+?)(?:\nEOF)", bash_command, re.DOTALL)
    if heredoc:
        return heredoc.group(1).strip()
    m = re.search(r"""-m\s+["'](.+?)["']""", bash_command, re.DOTALL)
    return m.group(1).strip() if m else None


def wiki_is_stale() -> bool | None:
    """True=stale, False=fresh, None=could not determine (fail-open)."""
    if not SCANNER.exists():
        return None
    try:
        r = subprocess.run(
            [sys.executable, str(SCANNER), "check", str(PROJECT_ROOT)],
            capture_output=True, text=True, timeout=20,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    if r.returncode == 0:
        return False
    if r.returncode == 1:
        return True
    return None  # unexpected exit → don't block


def main() -> None:
    try:
        hook = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return  # allow
    cmd = hook.get("tool_input", {}).get("command", "")
    if "git commit" not in cmd:
        return
    msg = extract_commit_message(cmd) or ""
    if not CLAIM_RE.search(msg):
        return  # commit does not claim a wiki refresh → not our business

    if wiki_is_stale() is True:
        sys.stderr.write(
            "BLOCKED: commit message claims a wiki refresh "
            "(\"wiki refresh/compile/rebuild\") but the wiki is STALE.\n"
            "Run `/wiki compile`, make sure docs/wiki/.state/manifest.json was "
            "updated (last_compiled + source hashes), and verify with\n"
            "  python3 ~/.claude/skills/wiki/scanner.py check .\n"
            "Then commit again — or drop the wiki-refresh claim from the message.\n"
        )
        sys.exit(2)  # deny the tool call


if __name__ == "__main__":
    main()
