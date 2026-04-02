#!/usr/bin/env python3
# /// script
# dependencies = [
#   "sentence-transformers>=3.0.0",
#   "faiss-cpu>=1.8.0",
#   "numpy>=1.26.0",
# ]
# ///
"""Semantic search over FPF sections using pre-built FAISS index.

Usage:
    uv run scripts/semantic_search.py "teams can't agree on responsibilities"
    uv run scripts/semantic_search.py "как сравнить два подхода" --top-k 5
    uv run scripts/semantic_search.py "definition of done" --json

Output (default):
    Ranked list of matching sections with scores.

Output (--json):
    JSON array of {pattern_id, title, file, score, keywords}.
"""

import argparse
import json
import sys
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_INDEX_DIR = "sections/embeddings"

_model_cache = {}


def load_model(model_name: str) -> SentenceTransformer:
    """Load model with caching for repeated calls."""
    if model_name not in _model_cache:
        _model_cache[model_name] = SentenceTransformer(model_name)
    return _model_cache[model_name]


def search(
    query: str,
    index_dir: str = DEFAULT_INDEX_DIR,
    top_k: int = 5,
) -> list[dict]:
    """Search FAISS index and return top-k results with scores."""
    index_path = Path(index_dir)

    config = json.loads((index_path / "config.json").read_text(encoding="utf-8"))
    mapping = json.loads((index_path / "metadata.json").read_text(encoding="utf-8"))
    index = faiss.read_index(str(index_path / "faiss.index"))

    model = load_model(config["model"])
    query_prefix = config.get("query_prefix", "query: ")

    query_embedding = model.encode(
        [query_prefix + query],
        normalize_embeddings=True,
    )
    query_vec = np.array(query_embedding, dtype=np.float32)

    scores, indices = index.search(query_vec, min(top_k, index.ntotal))

    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < 0:
            continue
        entry = mapping[int(idx)]
        results.append({
            "rank": rank + 1,
            "score": round(float(score), 4),
            "pattern_id": entry["pattern_id"],
            "title": entry["title"],
            "file": entry["file"],
            "keywords": entry.get("keywords", []),
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Semantic search over FPF sections")
    parser.add_argument("query", help="Search query (any language)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--index-dir", default=DEFAULT_INDEX_DIR, help="Path to embeddings directory")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    parser.add_argument("--threshold", type=float, default=0.0, help="Minimum score threshold")
    args = parser.parse_args()

    results = search(args.query, args.index_dir, args.top_k)

    if args.threshold > 0:
        results = [r for r in results if r["score"] >= args.threshold]

    if args.json_output:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("No results found.")
            sys.exit(0)

        print(f"\nQuery: {args.query}")
        print(f"{'─' * 60}")
        for r in results:
            kw = ", ".join(r["keywords"][:5]) if r["keywords"] else "—"
            print(f"  #{r['rank']}  [{r['score']:.4f}]  {r['pattern_id']}: {r['title']}")
            print(f"       File: {r['file']}")
            print(f"       Keywords: {kw}")
            print()


if __name__ == "__main__":
    main()
