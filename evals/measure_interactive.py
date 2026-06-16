#!/usr/bin/env python3
"""Measure the fpf skill's real Layer-1 auto-trigger rate from an INTERACTIVE
Claude Code transcript.

Why this exists: the official `skill-creator` eval harness drives `claude -p`
(headless), where skills do NOT auto-trigger (they resolve only via explicit
`/name`; CLI 2.1.142, anthropics/claude-code#32184). So a headless run reports
0 fires regardless of description quality and tells us nothing. The only faithful
way to measure auto-triggering is to run the golden queries by hand in a real
interactive session, then parse the session transcript — which is what this does.

Usage:
  1. Open a fresh INTERACTIVE Claude Code session in this repo.
  2. Paste the queries from evals/trigger-eval.json one at a time (positives and
     negatives both — order does not matter). Let each answer complete.
  3. Run:
       python3 evals/measure_interactive.py
     (auto-picks the newest transcript for this project), or point it explicitly:
       python3 evals/measure_interactive.py --transcript /path/to/session.jsonl

It matches each pasted query to a user turn, checks whether the `fpf` skill fired
before the next user turn, and prints recall (positives) + false-fire (negatives).
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def project_transcript_dir() -> Path:
    slug = str(REPO).replace("/", "-")
    return Path.home() / ".claude" / "projects" / slug


def newest_transcript() -> Path | None:
    d = project_transcript_dir()
    if not d.is_dir():
        return None
    jsonls = sorted(d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return jsonls[0] if jsonls else None


def extract_user_text(msg: dict) -> str | None:
    """Return the human text of a user turn, or None for tool_result / empty turns."""
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return None
    parts = []
    for c in content:
        if isinstance(c, dict) and c.get("type") == "text":
            parts.append(c.get("text", ""))
        elif isinstance(c, dict) and c.get("type") == "tool_result":
            return None  # tool result, not a human turn
    text = " ".join(parts).strip()
    return text or None


def is_fpf_fire(tool_use: dict) -> bool:
    name = tool_use.get("name", "")
    inp = tool_use.get("input", {}) or {}
    blob = json.dumps(inp).lower()
    if name == "Skill" and "fpf" in str(inp.get("skill", "")).lower():
        return True
    if name in ("Task", "Agent") and "fpf" in (
        str(inp.get("subagent_type", "")) + str(inp.get("agentType", ""))
    ).lower():
        return True
    if name == "Read" and re.search(r"skills/fpf|/fpf/", str(inp.get("file_path", "")).lower()):
        return True
    return False


def parse_events(transcript: Path) -> list[tuple[str, object]]:
    """Flatten transcript into ordered ('user', text) and ('fire', tool_use) markers."""
    events: list[tuple[str, object]] = []
    for line in transcript.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = ev.get("type")
        msg = ev.get("message", {}) if isinstance(ev.get("message"), dict) else {}
        if t == "user":
            text = extract_user_text(msg)
            if text:
                events.append(("user", text))
        elif t == "assistant":
            for c in msg.get("content", []) or []:
                if isinstance(c, dict) and c.get("type") == "tool_use" and is_fpf_fire(c):
                    events.append(("fire", c))
    return events


def measure(eval_set: list[dict], events: list[tuple[str, object]]) -> list[dict]:
    # Index user turns with the slice of fires that follow them (until next user turn).
    turns = []  # (norm_text, fired_bool)
    i = 0
    while i < len(events):
        kind, payload = events[i]
        if kind == "user":
            fired = False
            j = i + 1
            while j < len(events) and events[j][0] != "user":
                if events[j][0] == "fire":
                    fired = True
                j += 1
            turns.append((norm(payload), fired))
            i = j
        else:
            i += 1

    rows = []
    for item in eval_set:
        q = norm(item["query"])
        matched = [fired for (tn, fired) in turns if q in tn or tn in q]
        rows.append({
            "query": item["query"],
            "should_trigger": item["should_trigger"],
            "found": bool(matched),
            "fired": any(matched),
            "note": item.get("note", ""),
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eval-set", default=str(REPO / "evals" / "trigger-eval.json"))
    ap.add_argument("--transcript", default=None, help="Transcript .jsonl (default: newest for this project)")
    args = ap.parse_args()

    transcript = Path(args.transcript) if args.transcript else newest_transcript()
    if not transcript or not transcript.exists():
        print(f"ERROR: no transcript found (looked in {project_transcript_dir()}).", file=sys.stderr)
        sys.exit(1)

    eval_set = json.loads(Path(args.eval_set).read_text())
    rows = measure(eval_set, parse_events(transcript))

    pos = [r for r in rows if r["should_trigger"]]
    neg = [r for r in rows if not r["should_trigger"]]
    pos_found = [r for r in pos if r["found"]]
    neg_found = [r for r in neg if r["found"]]
    pos_fired = sum(r["fired"] for r in pos_found)
    neg_fired = sum(r["fired"] for r in neg_found)

    print(f"Transcript: {transcript}\n")
    for r in rows:
        if not r["found"]:
            mark = "·· not run"
        elif r["fired"]:
            mark = "🔥 FIRED   "
        else:
            mark = "—  no-fire "
        print(f"  [{mark}] want={'yes' if r['should_trigger'] else 'no '}  {r['query'][:74]}")

    print("\n── Layer-1 results (only queries actually found in the transcript) ──")
    if pos_found:
        print(f"  Recall (should-fire that fired):   {pos_fired}/{len(pos_found)} = {pos_fired/len(pos_found):.0%}")
    else:
        print("  Recall: no positive queries found in transcript — paste them and re-run.")
    if neg_found:
        print(f"  False-fire (should-NOT that fired): {neg_fired}/{len(neg_found)} = {neg_fired/len(neg_found):.0%}")
    missing = [r for r in rows if not r["found"]]
    if missing:
        print(f"  ({len(missing)} eval queries not yet run in this session)")


if __name__ == "__main__":
    main()
