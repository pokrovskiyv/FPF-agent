# FPF repository working agreements

This repository maintains the FPF specification and its analysis plugins. Course authoring, the MIPT program, management proposal and personal MIM course live in the sibling repository `engineering-work-with-ai`. For educational work use that repository and its instructions; see [EDUCATION-MOVED.md](EDUCATION-MOVED.md). Do not recreate educational `work/course-*` or `outputs/course-*` trees here.

## Sources and retrieval

- `FPF-Spec.md` is the upstream source of truth. Do not edit it directly or read the entire monolith for an ordinary task.
- `sections/` is generated. Locate relevant material through `sections/metadata.json`, `sections/glossary-quick.md`, route guides, or a narrow keyword search. Use semantic search only if these leave a material gap.
- `.agents/skills/fpf/SKILL.md` is the Codex entrypoint; `skills/fpf/SKILL.md` is the Claude edition. Keep their triggers and shared behavior consistent. `agents/fpf-*.md` contains optional role guidance.
- `.codex-plugin/` and `scripts/install_codex_plugin.py` own Codex packaging. Change canonical repository sources, not installed/cache mirrors.
- Consult [Readme.md](Readme.md) for architecture, route tables, commands and repository layout only when the task needs them. Maintenance details are not a required pre-read.

## Language

For applied problem solving, use the user's language and keep FPF terminology and internal processing out of the answer. For explicit questions about FPF, its terms, specification, teaching, or agent design, use and explain the necessary terms and references.

When editing specification content only, follow `sections/lexical-rules.md`: use Characteristic rather than axis/dimension, U.Measure or Score rather than metric, and the defined scope names. Do not impose this vocabulary on ordinary user-facing text.

## Maintenance and verification

- After an authorized upstream specification update, `./scripts/rebuild_all.sh` rebuilds generated material. Read `agents/fpf-sync.md` for the scheduled sync workflow; its commit/push steps do not authorize unrelated publication.
- For a source, packaging or retrieval change, run the relevant checks: `python3 scripts/test_smoke.py` for generated metadata/routes and `python3 scripts/smoke_codex.py` for Codex packaging. `--all` adds semantic-search dependencies; use it only when that behavior changed or remains uncertain.
- Do not rebuild the specification, embeddings or wiki for an unrelated question or instruction-only edit. After checks pass, repeat only for new changes, failures or unresolved evidence.
- Preserve unrelated dirty files; stage explicit paths. Follow existing user authorization for commits, pushes and external actions.

## Changelog and generated documentation

For `feat:` or `fix:` commits, update CHANGELOG's “What's New” in plain language. Repository hook behavior is described in `scripts/update_changelog.py` and `scripts/check_wiki_gate.py`; do not assume a hook configured for another client runs in Codex.

`docs/wiki/` is generated bilingual plugin documentation, not a copy of the specification. Do not edit generated wiki articles manually. Regenerate RU and EN together only when wiki maintenance is part of the task. Use the wiki skill at `~/.claude/skills/wiki/SKILL.md` and its scanner at `~/.claude/skills/wiki/scanner.py`. Do not claim a wiki refresh unless it was performed and verified. A missing wiki dependency does not block unrelated work.

Auto-generated statistics are maintained by `scripts/sync_doc_stats.py`; do not create additional hard-coded count tables in these instructions.
