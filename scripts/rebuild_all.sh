#!/bin/bash
# Rebuild all generated sections from FPF-Spec.md monolith.
# Run this after syncing the fork with upstream.
#
# Usage: ./scripts/rebuild_all.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

echo "=== FPF Skill-Agent: Full Rebuild ==="
echo ""

echo "[1/9] Splitting FPF-Spec.md into sections..."
rm -rf sections/
python3 scripts/split_spec.py
echo ""

echo "[2/9] Building metadata.json..."
python3 scripts/build_metadata.py
echo ""

echo "[3/9] Enriching metadata with user-facing queries..."
python3 scripts/enrich_metadata.py
echo ""

echo "[4/9] Building glossary-quick.md..."
python3 scripts/build_glossary.py
echo ""

echo "[5/9] Building lexical-rules.md..."
python3 scripts/build_lexical.py
echo ""

echo "[6/9] Building route chain files..."
python3 scripts/build_routes.py
echo ""

echo "[7/9] Building cross-reference indexes..."
python3 scripts/build_xrefs.py
echo ""

echo "[8/9] Syncing hard-coded stats in CLAUDE.md / Readme.md..."
python3 scripts/sync_doc_stats.py
echo ""

# Requires `uv` (https://docs.astral.sh/uv/). Downloads BAAI/bge-m3 on first run.
# Non-fatal: the local FAISS index is gitignored and not available everywhere
# (e.g. the cloud sync routine has no `uv`). The doc stats above do NOT depend on
# it — the vector count is derived from metadata.json, not from the index.
echo "[9/9] Building FAISS embeddings index (optional, needs uv)..."
uv run scripts/build_embeddings.py \
  || echo "  skipped: 'uv' unavailable or build failed (semantic-search index left as-is)"
echo ""

echo "=== Rebuild Complete ==="
echo ""
echo "Stats:"
echo "  Directories:   $(find sections/ -type d | wc -l | tr -d ' ')"
echo "  Section files: $(find sections/ -name '*.md' | wc -l | tr -d ' ')"
echo "  metadata.json: $(python3 -c 'import json; print(len(json.load(open("sections/metadata.json"))))') entries"
echo "  Routes:        $(ls sections/routes/route-*.md 2>/dev/null | wc -l | tr -d ' ') files"
echo ""
echo "Docs synced (CLAUDE.md / Readme.md). Next: /wiki compile, then commit."
