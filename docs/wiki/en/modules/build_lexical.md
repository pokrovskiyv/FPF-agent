---
title: build_lexical
sources:
  - scripts/build_lexical.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - module
  - pipeline
  - lexical-rules
---

# build_lexical

> Source: `scripts/build_lexical.py`

## Purpose

Extracts mandatory term-substitution rules from Part K of `FPF-Spec.md` and writes them to `sections/lexical-rules.md`. These rules tell the Reasoner agent which legacy terms (e.g., "axis", "metric" as a noun, "applicability") must be replaced with canonical ones internally — users never see either form, but internal consistency depends on this substitution map.

## Interface

| Function | Signature | Description |
|----------|-----------|-------------|
| `extract_part_k` | `(spec_path: Path) -> str` | Scan the spec for the H1 starting with "Part K" and return its content up to the next top-level H1 |
| `parse_replacement_table` | `(content: str) -> list[dict]` | Find the "Legacy Term" table and return rows as `{legacy, replace_with, plain_allowance, reference}` |
| `parse_deprecations` | `(content: str) -> list[str]` | Extract deprecated scope terms from the "MUST NOT use" block |
| `write_lexical_rules` | `(rules, deprecated, output_path: Path) -> None` | Emit the final rules markdown (replacement table + deprecated list) |
| `main` | `() -> None` | Argparse entry (`--spec`, `--output`) |

## Algorithm

1. Stream `FPF-Spec.md`, toggle an `in_part_k` flag on the Part K heading and off when the next top-level heading appears.
2. Inside Part K, look for the replacement table header containing "Legacy Term" and collect rows into dicts.
3. Parse the deprecations block using a regex scan for `*emphasised*` terms inside the "MUST NOT use" paragraph.
4. Write `sections/lexical-rules.md` with two sections: mandatory replacements (table) and deprecated scope terms (bulleted list with strikethrough).

## Dependencies

**Imports:** `argparse`, `re`, `pathlib.Path` — stdlib only.

**Imported by:** Called from `scripts/rebuild_all.sh` (step 5). Output is read by the Reasoner agent on every invocation.

## See also

- [split_spec](split_spec.md)
- [fpf-reasoner](../agents/fpf-reasoner.md) — enforces these rules internally
- [plain-language-contract](../architecture/plain-language-contract.md)
- [build-pipeline](../architecture/build-pipeline.md)
