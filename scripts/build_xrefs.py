#!/usr/bin/env python3
"""Build cross-reference index files (_xref.md) for each section directory.

Parses metadata.json dependency graph to find incoming references
from other Parts. Each directory gets a _xref.md listing which
patterns in OTHER directories reference patterns in THIS directory.

Usage:
    python scripts/build_xrefs.py [--metadata sections/metadata.json] [--sections sections/]
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


def normalize_pattern_id(raw: str) -> str:
    """Normalize a dependency reference to a clean pattern ID."""
    raw = raw.strip().rstrip('.')
    raw = re.sub(r'\*\*', '', raw)
    raw = re.sub(r'\s+.*$', '', raw)
    match = re.match(r'([A-K]\.[\d.]+[A-Z]*)', raw)
    if match:
        return match.group(1)
    match = re.match(r'([A-K]\.\d+)', raw)
    if match:
        return match.group(1)
    match = re.match(r'(P-\d+)', raw)
    if match:
        return match.group(1)
    return ''


def find_directory_for_pattern(pattern_id: str, metadata: dict, sections_dir: Path) -> str:
    """Find which directory a pattern belongs to."""
    entry = metadata.get(pattern_id, {})
    file_path = entry.get('file', '')
    if file_path:
        rel = Path(file_path).relative_to(sections_dir) if file_path.startswith(str(sections_dir)) else Path(file_path)
        parts = rel.parts
        if len(parts) >= 2:
            return parts[0] if not str(parts[0]).startswith('sections') else parts[1]
    return ''


def build_xref_graph(metadata: dict, sections_dir: Path) -> dict:
    """Build a mapping: target_dir -> list of {source_pattern, target_pattern, relation_type}."""
    xrefs = defaultdict(list)

    dep_fields = [
        'builds_on', 'refines', 'prerequisite_for', 'coordinates_with',
        'constrains', 'informs', 'used_by', 'specialised_by',
    ]

    for source_pid, entry in metadata.items():
        if source_pid.startswith('preface_'):
            continue

        source_dir = find_directory_for_pattern(source_pid, metadata, sections_dir)
        if not source_dir:
            continue

        deps = entry.get('dependencies', {})
        for field in dep_fields:
            for raw_ref in deps.get(field, []):
                target_pid = normalize_pattern_id(raw_ref)
                if not target_pid:
                    continue

                target_dir = find_directory_for_pattern(target_pid, metadata, sections_dir)
                if not target_dir or target_dir == source_dir:
                    continue

                xrefs[target_dir].append({
                    'source_pattern': source_pid,
                    'source_dir': source_dir,
                    'target_pattern': target_pid,
                    'relation': field,
                })

    return dict(xrefs)


def write_xref_files(xrefs: dict, sections_dir: Path) -> int:
    """Write _xref.md files for each directory that has incoming cross-references."""
    count = 0
    for target_dir, refs in sorted(xrefs.items()):
        dir_path = sections_dir / target_dir
        if not dir_path.is_dir():
            continue

        by_source_dir = defaultdict(list)
        for ref in refs:
            by_source_dir[ref['source_dir']].append(ref)

        lines = [f"# Cross-References into {target_dir}", ""]
        lines.append(f"Patterns in other Parts that reference patterns in this directory ({len(refs)} refs).")
        lines.append("")

        for src_dir in sorted(by_source_dir.keys()):
            src_refs = by_source_dir[src_dir]
            lines.append(f"## From {src_dir}")
            lines.append("")
            lines.append("| Source | Relation | Target |")
            lines.append("|--------|----------|--------|")
            seen = set()
            for ref in sorted(src_refs, key=lambda r: r['source_pattern']):
                key = (ref['source_pattern'], ref['relation'], ref['target_pattern'])
                if key in seen:
                    continue
                seen.add(key)
                lines.append(f"| {ref['source_pattern']} | {ref['relation']} | {ref['target_pattern']} |")
            lines.append("")

        xref_path = dir_path / '_xref.md'
        xref_path.write_text('\n'.join(lines), encoding='utf-8')
        count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description='Build cross-reference index files')
    parser.add_argument('--metadata', default='sections/metadata.json')
    parser.add_argument('--sections', default='sections')
    args = parser.parse_args()

    metadata = json.loads(Path(args.metadata).read_text(encoding='utf-8'))
    sections_dir = Path(args.sections)

    print(f"Building cross-reference graph from {len(metadata)} entries...")
    xrefs = build_xref_graph(metadata, sections_dir)

    total_refs = sum(len(refs) for refs in xrefs.values())
    print(f"Found {total_refs} cross-references across {len(xrefs)} directories")

    count = write_xref_files(xrefs, sections_dir)
    print(f"Written {count} _xref.md files")


if __name__ == '__main__':
    main()
