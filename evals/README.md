# Trigger evals — does the `fpf` skill actually auto-fire?

This folder measures **Layer-1 triggering**: whether the host model decides to
invoke the `fpf` skill at all, from its `name` + `description` alone — *instead of
just answering directly*. None of the in-skill machinery (classifier, routes,
FAISS, confidence gate) runs until Layer 1 fires, so this is the decisive gate.

## Files

- `trigger-eval.json` — 20 curated golden queries (bilingual): 10 should-fire FPF
  sweet-spot problems + 10 tricky near-miss negatives that share keywords
  (`compare`, `structure`, `decompose`, `audit`, `metric`, `trust`) but are plain
  coding / lookup tasks. This is the reusable asset; keep it in sync with the routes.
- `measure_interactive.py` — parses an interactive session transcript and reports
  the real fire-rate (recall on positives, false-fire on negatives).

## ⚠️ Why you can't use `skill-creator`'s `run_eval.py` here

The official harness drives `claude -p` (headless). In headless mode (verified
2026-06-15, CLI 2.1.142) **skills do not auto-trigger at all** — they resolve only
via an explicit `/name` (`--bare` help: "Skills still resolve via /skill-name";
[anthropics/claude-code#32184](https://github.com/anthropics/claude-code/issues/32184)).
Proven by controls: the current description, a maximally "pushy" ALWAYS/MUST
description, a slam-dunk `docx` request, and an explicit "use the fpf skill" prompt
**all** produced zero auto-fires. So a headless run reports 0 regardless of
description quality — it measures the bug, not the skill.

## How to get the real number (interactive protocol)

1. Open a **fresh interactive** Claude Code session in this repo (not `claude -p`).
2. Paste each query from `trigger-eval.json`, one per turn; let each answer finish.
   (Order/mix of positives and negatives doesn't matter.)
3. Run:

   ```bash
   python3 evals/measure_interactive.py
   ```

   It auto-picks the newest transcript for this project, matches your pasted
   queries, and prints recall + false-fire. Point at a specific file with
   `--transcript <path.jsonl>` if needed.

A clean run uses a session that did nothing else, so the only `fpf` firings are
the ones triggered by these queries.
