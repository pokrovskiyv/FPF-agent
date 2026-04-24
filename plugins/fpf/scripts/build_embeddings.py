#!/usr/bin/env python3
# /// script
# dependencies = [
#   "sentence-transformers>=3.0.0",
#   "faiss-cpu>=1.8.0",
#   "numpy>=1.26.0",
# ]
# ///
"""Build a FAISS index from FPF section files for semantic search.

Reads all section .md files, generates embeddings with a multilingual
model, and saves a FAISS index + metadata mapping.

Usage:
    uv run scripts/build_embeddings.py [--model MODEL] [--output DIR]

Output:
    sections/embeddings/faiss.index   — FAISS flat L2 index
    sections/embeddings/metadata.json — id→{pattern_id, title, file} mapping
"""

import argparse
import json
import sys
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "BAAI/bge-m3"
DEFAULT_OUTPUT = "sections/embeddings"
PASSAGE_PREFIX = ""


def load_sections(metadata_path: Path) -> list[dict]:
    """Load section content and metadata for embedding."""
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    sections = []

    for pattern_id, entry in metadata.items():
        file_path = entry.get("file", "")
        if not file_path:
            continue

        full_path = Path(file_path)
        if not full_path.exists():
            continue

        content = full_path.read_text(encoding="utf-8").strip()
        if len(content) < 50:
            continue

        title = entry.get("title", "")
        keywords = entry.get("keywords", [])
        queries = entry.get("queries", [])

        # Build text for embedding: title + keywords + queries + content (truncated)
        text_parts = [f"Pattern {pattern_id}: {title}"]
        if keywords:
            text_parts.append(f"Keywords: {', '.join(keywords[:10])}")
        if queries:
            text_parts.append(f"Questions: {' | '.join(queries[:5])}")
        text_parts.append(content[:2000])
        text = "\n".join(text_parts)

        sections.append({
            "pattern_id": pattern_id,
            "title": title,
            "file": file_path,
            "text": text,
            "keywords": keywords,
        })

    return sections


def build_index(sections: list[dict], model_name: str) -> tuple[faiss.IndexFlatIP, np.ndarray]:
    """Generate embeddings and build FAISS index."""
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    texts = [PASSAGE_PREFIX + s["text"] for s in sections]

    print(f"Encoding {len(texts)} sections...")
    embeddings = model.encode(
        texts,
        batch_size=8,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    embeddings = np.array(embeddings, dtype=np.float32)

    dim = embeddings.shape[1]
    print(f"Building FAISS index (dim={dim})...")
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    return index, embeddings


def main():
    parser = argparse.ArgumentParser(description="Build FAISS index for FPF sections")
    parser.add_argument("--metadata", default="sections/metadata.json")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    if not metadata_path.exists():
        print(f"Error: {metadata_path} not found", file=sys.stderr)
        sys.exit(1)

    sections = load_sections(metadata_path)
    print(f"Loaded {len(sections)} sections")

    if not sections:
        print("No sections to index", file=sys.stderr)
        sys.exit(1)

    index, embeddings = build_index(sections, args.model)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    index_path = output_dir / "faiss.index"
    faiss.write_index(index, str(index_path))
    print(f"Saved FAISS index: {index_path}")

    mapping = [
        {
            "id": i,
            "pattern_id": s["pattern_id"],
            "title": s["title"],
            "file": s["file"],
            "keywords": s["keywords"],
        }
        for i, s in enumerate(sections)
    ]
    mapping_path = output_dir / "metadata.json"
    mapping_path.write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Saved metadata mapping: {mapping_path} ({len(mapping)} entries)")

    config_path = output_dir / "config.json"
    config_path.write_text(
        json.dumps({
            "model": args.model,
            "dim": int(embeddings.shape[1]),
            "num_sections": len(sections),
            "passage_prefix": PASSAGE_PREFIX,
            "query_prefix": "query: ",
        }, indent=2),
        encoding="utf-8",
    )
    print(f"Saved config: {config_path}")


if __name__ == "__main__":
    main()
