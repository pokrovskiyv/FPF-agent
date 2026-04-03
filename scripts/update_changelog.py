#!/usr/bin/env python3
"""Update CHANGELOG.md and plugin.json version from conventional commit.

Called by PreToolUse hook before git commit. Reads hook JSON from stdin,
parses the commit message, determines version bump, updates plugin.json,
and appends to CHANGELOG.md under "### All Changes".

Usage:
    echo '{"tool_input":{"command":"git commit -m \"feat: add X\""}}' | python3 scripts/update_changelog.py
"""

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = PROJECT_ROOT / ".claude-plugin" / "plugin.json"
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"

COMMIT_TYPES = frozenset(
    {"feat", "fix", "docs", "test", "chore", "perf", "ci", "style", "refactor"}
)
CC_PATTERN = re.compile(
    r"^(?P<type>" + "|".join(COMMIT_TYPES) + r")"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?"
    r":\s*(?P<description>.+)$"
)
BUMP_MAP = {"feat": "minor", "fix": "patch"}


# ── Extract commit message from bash command ──────────────────────────


def extract_commit_message(bash_command: str) -> str | None:
    """Extract the subject line from a git commit bash command.

    Handles two Claude Code formats:
    1. -m "msg" or -m 'msg'
    2. heredoc: -m "$(cat <<'EOF'\\nsubject\\n...\\nEOF\\n)"
    """
    # Strategy 1: heredoc (Claude Code default for multi-line)
    heredoc = re.search(
        r"<<\s*['\"]?EOF['\"]?\s*\n(.+?)(?:\nEOF)", bash_command, re.DOTALL
    )
    if heredoc:
        return heredoc.group(1).strip().splitlines()[0].strip()

    # Strategy 2: -m "..." or -m '...' (DOTALL for multiline messages)
    m_flag = re.search(r"""-m\s+["'](.+?)["']""", bash_command, re.DOTALL)
    if m_flag:
        return m_flag.group(1).strip().splitlines()[0].strip()

    return None


# ── Parse conventional commit ─────────────────────────────────────────


def parse_conventional_commit(message: str) -> dict | None:
    """Parse 'type(scope)!: description' into components."""
    match = CC_PATTERN.match(message)
    if not match:
        return None
    return {
        "type": match.group("type"),
        "scope": match.group("scope"),
        "breaking": match.group("breaking") == "!",
        "description": match.group("description").strip(),
    }


# ── Version bump ──────────────────────────────────────────────────────


def determine_bump(parsed: dict) -> str:
    """Return 'major', 'minor', 'patch', or 'none'."""
    if parsed["breaking"]:
        return "major"
    return BUMP_MAP.get(parsed["type"], "none")


def bump_version(current: str, bump_type: str) -> str:
    """Increment semver string. Returns current unchanged for 'none'."""
    if bump_type == "none":
        return current
    major, minor, patch = map(int, current.split("."))
    if bump_type == "major":
        return f"{major + 1}.0.0"
    if bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


# ── File updates ──────────────────────────────────────────────────────


def update_plugin_json(path: Path, new_version: str) -> None:
    """Update version field in plugin.json (immutable read-then-write)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    updated = {**data, "version": new_version}
    path.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def format_entry(parsed: dict) -> str:
    """Format a single changelog entry line."""
    if parsed["scope"]:
        return f"- **{parsed['type']}({parsed['scope']})**: {parsed['description']}"
    return f"- **{parsed['type']}**: {parsed['description']}"


def update_changelog(path: Path, entry_line: str, date_str: str) -> None:
    """Insert entry into CHANGELOG.md under today's date / All Changes."""
    if not path.exists():
        path.write_text("# Changelog\n\n", encoding="utf-8")

    content = path.read_text(encoding="utf-8")
    date_header = f"## {date_str}"
    all_changes_header = "### All Changes"

    # Idempotency: skip if exact line already present (whole-line match)
    if f"\n{entry_line}\n" in content or content.endswith(f"\n{entry_line}"):
        print(f"  duplicate, skipping: {entry_line}")
        return

    if date_header not in content:
        # Insert new date section after "# Changelog\n\n"
        new_section = f"{date_header}\n\n{all_changes_header}\n{entry_line}\n"
        anchor = "# Changelog\n\n"
        if anchor in content:
            pos = content.index(anchor) + len(anchor)
            content = content[:pos] + new_section + "\n" + content[pos:]
        else:
            content += f"\n{new_section}"
    else:
        # Date section exists — find the All Changes subsection
        date_pos = content.index(date_header)
        # Scope: from date header to next date header (or end)
        rest = content[date_pos:]
        next_date = rest.find("\n## ", 1)
        scope = rest[:next_date] if next_date != -1 else rest

        if all_changes_header not in scope:
            # Add All Changes subsection at end of this date section
            insert_at = date_pos + len(scope.rstrip("\n"))
            content = (
                content[:insert_at]
                + f"\n\n{all_changes_header}\n{entry_line}\n"
                + content[insert_at:]
            )
        else:
            # Append entry after last line under All Changes
            ac_start = date_pos + scope.index(all_changes_header)
            after_ac = scope[scope.index(all_changes_header) + len(all_changes_header):]
            # Find end: next subsection or end of date scope
            next_sub = after_ac.find("\n### ")
            if next_sub != -1:
                insert_at = ac_start + len(all_changes_header) + next_sub
            else:
                insert_at = ac_start + len(all_changes_header) + len(after_ac.rstrip("\n"))
            content = content[:insert_at] + "\n" + entry_line + content[insert_at:]

    path.write_text(content, encoding="utf-8")


def stage_files(*paths: Path) -> None:
    """Git add specified files."""
    subprocess.run(
        ["git", "add", *(str(p) for p in paths)],
        check=True,
        cwd=str(PROJECT_ROOT),
    )


# ── Main ──────────────────────────────────────────────────────────────


def main() -> None:
    # Read hook JSON from stdin
    try:
        hook_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        print("update_changelog: no valid JSON on stdin, skipping")
        return

    bash_command = hook_data.get("tool_input", {}).get("command", "")
    if not bash_command:
        print("update_changelog: no command in tool_input, skipping")
        return

    subject = extract_commit_message(bash_command)
    if not subject:
        print(f"update_changelog: no commit message found, skipping")
        return

    parsed = parse_conventional_commit(subject)
    if not parsed:
        print(f"update_changelog: not conventional commit, skipping: {subject}")
        return

    label = f"{parsed['type']}({parsed['scope']})" if parsed["scope"] else parsed["type"]
    print(f"update_changelog: {label}: {parsed['description']}")

    # Version bump
    bump_type = determine_bump(parsed)
    if bump_type != "none":
        current = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"]
        new_ver = bump_version(current, bump_type)
        update_plugin_json(PLUGIN_JSON, new_ver)
        print(f"  version: {current} -> {new_ver} ({bump_type})")

    # Changelog entry
    today = date.today().isoformat()
    entry_line = format_entry(parsed)
    update_changelog(CHANGELOG, entry_line, today)
    print(f"  changelog: appended under {today}")

    # Stage modified files
    files_to_stage = [CHANGELOG]
    if bump_type != "none":
        files_to_stage.append(PLUGIN_JSON)
    stage_files(*files_to_stage)
    print(f"  staged: {', '.join(p.name for p in files_to_stage)}")


if __name__ == "__main__":
    main()
