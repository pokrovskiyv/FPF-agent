---
title: Build Pipeline
sources:
  - scripts/rebuild_all.sh
  - scripts/split_spec.py
  - scripts/build_metadata.py
  - scripts/enrich_metadata.py
  - scripts/build_glossary.py
  - scripts/build_lexical.py
  - scripts/build_routes.py
  - scripts/build_xrefs.py
  - scripts/build_embeddings.py
last_updated: 2026-04-15T00:00:00Z
tags:
  - architecture
  - pipeline
  - rebuild
---

# Build Pipeline

## Components

The build pipeline is orchestrated by `scripts/rebuild_all.sh` — an 8-step shell script that rebuilds every generated artifact from `FPF-Spec.md`. Steps 1–7 are stdlib-only Python; step 8 needs `uv` plus the `bge-m3` model.

| Step | Script | Produces |
|------|--------|----------|
| 1 | [split_spec](../modules/split_spec.md) | `sections/**/*.md` (~240 files + `_index.md` per directory) |
| 2 | [build_metadata](../modules/build_metadata.md) | `sections/metadata.json` |
| 3 | [enrich_metadata](../modules/enrich_metadata.md) | `sections/metadata.json` (in place) |
| 4 | [build_glossary](../modules/build_glossary.md) | `sections/glossary-quick.md` |
| 5 | [build_lexical](../modules/build_lexical.md) | `sections/lexical-rules.md` |
| 6 | [build_routes](../modules/build_routes.md) | `sections/routes/route-*.md` |
| 7 | [build_xrefs](../modules/build_xrefs.md) | `sections/*/_xref.md` |
| 8 | [build_embeddings](../modules/build_embeddings.md) | `sections/embeddings/{faiss.index, metadata.json, config.json}` |

## Data Flow

```
FPF-Spec.md  (5.5 MB, ~1.3 M tokens)
     │
     ▼  step 1  rm -rf sections/; python3 scripts/split_spec.py
sections/**/*.md  +  sections/*/_index.md
     │
     ▼  step 2  python3 scripts/build_metadata.py
sections/metadata.json           (≈242 entries, file paths resolved)
     │
     ▼  step 3  python3 scripts/enrich_metadata.py
sections/metadata.json           (enriched with user-facing queries, idempotent)
     │
     ├──► step 4  build_glossary   → glossary-quick.md
     ├──► step 5  build_lexical     → lexical-rules.md      (reads FPF-Spec Part K)
     ├──► step 6  build_routes      → routes/route-*.md
     ├──► step 7  build_xrefs       → */_xref.md
     └──► step 8  uv run build_embeddings → embeddings/
```

Each step is idempotent: rerunning emits the same outputs modulo changes in the source spec. Step 1 deletes `sections/` first so stale files don't accumulate.

## Decisions

- **Stdlib-only for 7 of 8 steps.** Keeps the rebuild runnable anywhere Python 3 exists. The one step that needs heavy ML deps (`build_embeddings`) uses the PEP 723 inline-metadata pattern with `uv`, which auto-installs on first run.
- **`set -euo pipefail` at the top of the script.** Any failing step stops the rebuild; the shell aborts rather than producing partial artifacts.
- **Stats printed at end.** The script counts directories, section files, metadata entries, and routes — a quick sanity check after each rebuild.
- **Embeddings step is rebuild-only.** It takes ≈90 seconds and re-downloads nothing after the first run, but it's the step most likely to fail on a fresh machine (model download). Run `./scripts/rebuild_all.sh` locally after syncing the spec; the CI path skips step 8.

## Related

- [overview](overview.md)
- [sync-and-rebuild](sync-and-rebuild.md)
- Individual module articles (linked in the steps table above)
