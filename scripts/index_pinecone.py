#!/usr/bin/env python3
"""Prepare FPF sections for Pinecone upsert.

Reads all section files and metadata.json, produces a JSONL file
(sections/pinecone_records.jsonl) that can be upserted to Pinecone
via MCP or API. Each record = one section file with metadata.

For use with Pinecone integrated indexes (built-in embeddings like
multilingual-e5-large) — we send raw text, Pinecone handles embeddings.

Usage:
    python scripts/index_pinecone.py [--sections sections/] [--metadata sections/metadata.json] [--output sections/pinecone_records.jsonl]

After running, upsert to Pinecone via MCP:
    Use mcp__plugin_pinecone_pinecone__upsert-records with the generated records.
"""

import argparse
import json
from pathlib import Path


def build_records(sections_dir: Path, metadata: dict) -> list[dict]:
    """Build Pinecone records from section files."""
    records = []

    for pattern_id, entry in metadata.items():
        file_path = entry.get('file', '')
        if not file_path:
            continue

        full_path = Path(file_path)
        if not full_path.exists():
            continue

        content = full_path.read_text(encoding='utf-8')
        if len(content.strip()) < 50:
            continue

        # Truncate to ~8000 chars (~2000 tokens) for embedding quality
        text = content[:8000]

        title = entry.get('title', '')
        keywords = entry.get('keywords', [])
        status = entry.get('status', '')

        deps = entry.get('dependencies', {})
        builds_on = deps.get('builds_on', [])
        prerequisite_for = deps.get('prerequisite_for', [])

        record = {
            'id': pattern_id.replace('.', '_').lower(),
            'text': f"Pattern {pattern_id}: {title}\n\n{text}",
            'metadata': {
                'pattern_id': pattern_id,
                'title': title,
                'status': status,
                'keywords': ', '.join(keywords[:10]),
                'file_path': file_path,
                'builds_on': ', '.join(builds_on[:5]),
                'prerequisite_for': ', '.join(prerequisite_for[:5]),
            },
        }
        records.append(record)

    return records


def main():
    parser = argparse.ArgumentParser(description='Prepare sections for Pinecone indexing')
    parser.add_argument('--sections', default='sections')
    parser.add_argument('--metadata', default='sections/metadata.json')
    parser.add_argument('--output', default='sections/pinecone_records.jsonl')
    args = parser.parse_args()

    metadata = json.loads(Path(args.metadata).read_text(encoding='utf-8'))
    print(f"Loaded {len(metadata)} metadata entries")

    records = build_records(Path(args.sections), metadata)
    print(f"Built {len(records)} records for Pinecone")

    output_path = Path(args.output)
    with output_path.open('w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"Written to {output_path}")
    print(f"\nTo upsert to Pinecone, use the Pinecone MCP tools:")
    print(f"  1. Create an integrated index: create-index-for-model (name: 'fpf-sections', model: 'multilingual-e5-large')")
    print(f"  2. Upsert records from this file using upsert-records")
    print(f"  3. Search with: search-records (query: 'your question')")


if __name__ == '__main__':
    main()
