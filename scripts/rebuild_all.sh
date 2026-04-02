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

echo "[1/8] Splitting FPF-Spec.md into sections..."
rm -rf sections/
python3 scripts/split_spec.py
echo ""

echo "[2/8] Building metadata.json..."
python3 scripts/build_metadata.py
echo ""

echo "[3/8] Enriching metadata with user-facing queries..."
python3 scripts/enrich_metadata.py
echo ""

echo "[4/8] Building glossary-quick.md..."
python3 scripts/build_glossary.py
echo ""

echo "[5/8] Building lexical-rules.md..."
python3 scripts/build_lexical.py
echo ""

echo "[6/8] Building route chain files..."
python3 scripts/build_routes.py
echo ""

echo "[7/8] Building cross-reference indexes..."
python3 scripts/build_xrefs.py
echo ""

# Requires `uv` (https://docs.astral.sh/uv/).
# Will auto-download the BAAI/bge-m3 model on first run.
echo "[8/8] Building FAISS embeddings index..."
uv run scripts/build_embeddings.py
echo ""

echo "=== Rebuild Complete ==="
echo ""
echo "Stats:"
echo "  Directories:  $(find sections/ -type d | wc -l | tr -d ' ')"
echo "  Section files: $(find sections/ -name '*.md' | wc -l | tr -d ' ')"
echo "  metadata.json: $(python3 -c 'import json; print(len(json.load(open("sections/metadata.json"))))') entries"
echo "  Routes:        $(ls sections/routes/route-*.md 2>/dev/null | wc -l | tr -d ' ') files"
