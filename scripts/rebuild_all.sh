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

echo "[1/5] Splitting FPF-Spec.md into sections..."
rm -rf sections/
python3 scripts/split_spec.py
echo ""

echo "[2/5] Building metadata.json..."
python3 scripts/build_metadata.py
echo ""

echo "[3/5] Building glossary-quick.md..."
python3 scripts/build_glossary.py
echo ""

echo "[4/5] Building lexical-rules.md..."
python3 scripts/build_lexical.py
echo ""

echo "[5/6] Building route chain files..."
python3 scripts/build_routes.py
echo ""

echo "[6/6] Building cross-reference indexes..."
python3 scripts/build_xrefs.py
echo ""

echo "=== Rebuild Complete ==="
echo ""
echo "Stats:"
echo "  Directories:  $(find sections/ -type d | wc -l | tr -d ' ')"
echo "  Section files: $(find sections/ -name '*.md' | wc -l | tr -d ' ')"
echo "  metadata.json: $(python3 -c 'import json; print(len(json.load(open("sections/metadata.json"))))') entries"
echo "  Routes:        $(ls sections/routes/route-*.md 2>/dev/null | wc -l | tr -d ' ') files"
