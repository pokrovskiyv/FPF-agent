#!/usr/bin/env python3
"""Extract top 50 core FPF terms from metadata.json keywords into glossary-quick.md.

Counts keyword frequency across all ToC entries, picks top 50,
and maps each to its primary pattern ID and one-line description.

Usage:
    python scripts/build_glossary.py [--metadata sections/metadata.json] [--output sections/glossary-quick.md]
"""

import argparse
import json
from collections import Counter
from pathlib import Path


def build_glossary(metadata: dict, top_n: int = 50) -> list[dict]:
    """Extract top-N keywords with their primary source pattern."""
    keyword_counts = Counter()
    keyword_source = {}

    for pid, entry in metadata.items():
        for kw in entry.get('keywords', []):
            kw_lower = kw.lower().strip()
            if len(kw_lower) < 3 or len(kw_lower) > 60:
                continue
            keyword_counts[kw_lower] += 1
            if kw_lower not in keyword_source:
                keyword_source[kw_lower] = {
                    'pattern_id': pid,
                    'title': entry.get('title', ''),
                    'original_form': kw,
                }

    top_keywords = keyword_counts.most_common(top_n)

    glossary = []
    for kw, count in top_keywords:
        src = keyword_source[kw]
        glossary.append({
            'term': src['original_form'],
            'pattern_id': src['pattern_id'],
            'pattern_title': src['title'],
            'frequency': count,
        })

    return glossary


def write_glossary(glossary: list[dict], output_path: Path) -> None:
    """Write glossary-quick.md."""
    lines = [
        "# FPF Quick Glossary (Top 50 Terms)",
        "",
        "Auto-generated from metadata.json. Maps core terms to their primary pattern.",
        "",
        "| Term | Primary Pattern | Pattern Title |",
        "|------|----------------|---------------|",
    ]
    for entry in glossary:
        pid = entry['pattern_id']
        title = entry['pattern_title'][:60]
        term = entry['term']
        lines.append(f"| {term} | {pid} | {title} |")

    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Build glossary-quick.md from metadata')
    parser.add_argument('--metadata', default='sections/metadata.json')
    parser.add_argument('--output', default='sections/glossary-quick.md')
    args = parser.parse_args()

    metadata = json.loads(Path(args.metadata).read_text(encoding='utf-8'))
    print(f"Loaded {len(metadata)} entries from metadata.json")

    glossary = build_glossary(metadata, top_n=50)
    print(f"Extracted {len(glossary)} glossary terms")

    write_glossary(glossary, Path(args.output))
    print(f"Written to {args.output}")


if __name__ == '__main__':
    main()
