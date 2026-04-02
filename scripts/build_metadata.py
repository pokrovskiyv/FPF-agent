#!/usr/bin/env python3
"""Parse FPF-Spec.md Table of Contents into sections/metadata.json.

Extracts pattern_id, title, status, keywords, queries, and dependency
graph from the structured ToC tables (lines 7-337 of the spec).

Pattern from RAGLegalChallenge build_article_index.py: pre-computed
index for instant lookup without reading section files.

Usage:
    python scripts/build_metadata.py [--spec FPF-Spec.md] [--sections sections/] [--output sections/metadata.json]
"""

import argparse
import json
import re
from pathlib import Path


def find_section_file(pattern_id: str, sections_dir: Path) -> str:
    """Find the file path for a given pattern ID by scanning _index.md files.

    Strategy:
    1. Exact match on PID extracted from link text, e.g. [Title (A.6.P)](file.md)
    2. Substring match with word-boundary check to avoid false positives
       (e.g. D.1 must not match E.10.D1 filename)
    3. Parent fallback: B.2.1 -> B.2's file
    """
    pid = pattern_id.replace('*', '').strip()
    if not pid:
        return ''

    pid_lower = pid.lower().replace('.', '')

    for index_file in sorted(sections_dir.rglob('_index.md')):
        content = index_file.read_text(encoding='utf-8')
        for line in content.splitlines():
            link_match = re.search(r'\[.*?\]\((.+?\.md)\)', line)
            if not link_match:
                continue
            filename = link_match.group(1)
            fn_norm = filename.lower().replace('-', '').replace('.', '')

            idx = fn_norm.find(pid_lower)
            if idx < 0:
                continue
            # Word-boundary check: character before match must not be a letter
            if idx > 0 and fn_norm[idx - 1].isalpha():
                continue
            return str(index_file.parent / filename)

    # Parent fallback: B.2.1 -> B.2, D.2.1 -> D.2
    parts = pid.rsplit('.', 1)
    if len(parts) == 2 and len(parts[0]) > 1:
        return find_section_file(parts[0], sections_dir)

    return ''


def parse_keywords(text: str) -> list[str]:
    """Extract keywords from '*Keywords:* ...' text."""
    match = re.search(r'\*Keywords:\*\s*(.+?)(?:\.\s*\*Queries|\.$|$)', text, re.DOTALL)
    if not match:
        return []
    raw = match.group(1)
    keywords = [k.strip().strip('.,') for k in re.split(r',\s*', raw) if k.strip()]
    return [k for k in keywords if k and len(k) < 100]


def parse_queries(text: str) -> list[str]:
    """Extract queries from '*Queries:* "..." text."""
    match = re.search(r'\*Queries:\*\s*(.+?)$', text, re.DOTALL)
    if not match:
        return []
    raw = match.group(1)
    queries = re.findall(r'"([^"]+)"', raw)
    return queries


def parse_dependencies(text: str) -> dict:
    """Parse dependency text into structured dict."""
    deps = {}
    patterns = [
        ('builds_on', r'\*\*Builds on:\*\*\s*(.+?)(?:\.\s*\*\*|\.\s*$|\|)'),
        ('refines', r'\*\*Refines:\*\*\s*(.+?)(?:\.\s*\*\*|\.\s*$|\|)'),
        ('prerequisite_for', r'\*\*Prerequisite for:\*\*\s*(.+?)(?:\.\s*\*\*|\.\s*$|\|)'),
        ('coordinates_with', r'\*\*Coordinates with:\*\*\s*(.+?)(?:\.\s*\*\*|\.\s*$|\|)'),
        ('constrains', r'\*\*Constrains:\*\*\s*(.+?)(?:\.\s*\*\*|\.\s*$|\|)'),
        ('informs', r'\*\*Informs:\*\*\s*(.+?)(?:\.\s*\*\*|\.\s*$|\|)'),
        ('used_by', r'\*\*Used by:\*\*\s*(.+?)(?:\.\s*\*\*|\.\s*$|\|)'),
        ('specialised_by', r'\*\*Specialised by:\*\*\s*(.+?)(?:\.\s*\*\*|\.\s*$|\|)'),
    ]
    for key, pattern in patterns:
        match = re.search(pattern, text)
        if match:
            raw = match.group(1).strip().rstrip('.')
            refs = [r.strip() for r in re.split(r'[,;]\s*', raw) if r.strip()]
            if refs:
                deps[key] = refs
    return deps


def _split_table_row(line: str) -> list[str]:
    """Split a markdown table row on | delimiters, ignoring | inside backticks."""
    placeholder = '\x00PIPE\x00'
    result = []
    in_backtick = False
    chars = list(line)
    for i, ch in enumerate(chars):
        if ch == '`':
            in_backtick = not in_backtick
            result.append(ch)
        elif ch == '|' and in_backtick:
            result.append(placeholder)
        else:
            result.append(ch)
    protected = ''.join(result)
    cells = [c.strip().replace(placeholder, '|') for c in protected.split('|')[1:-1]]
    return cells


def parse_toc(spec_path: Path) -> list[dict]:
    """Parse the Table of Contents tables from the spec."""
    lines = spec_path.read_text(encoding='utf-8').splitlines()
    entries = []

    in_toc = False
    for i, line in enumerate(lines):
        if line.strip() == '# Table of Content':
            in_toc = True
            continue

        if in_toc and line.startswith('# ') and 'Table of Content' not in line:
            break

        if not in_toc:
            continue

        if not line.startswith('|'):
            continue

        if line.startswith('| :---') or line.startswith('| §') or line.startswith('| ---'):
            continue

        cells = _split_table_row(line)
        if len(cells) < 3:
            continue

        if cells[0].startswith('***') or cells[0].startswith('*Cluster'):
            continue

        if len(cells) == 3:
            entry_id = ''
            title_raw = cells[0]
            status = cells[1]
            keywords_text = cells[2]
            deps_text = ''
        elif len(cells) == 5:
            entry_id = cells[0].strip()
            title_raw = cells[1].strip()
            status = cells[2].strip()
            keywords_text = cells[3].strip()
            deps_text = cells[4].strip()
        else:
            continue

        if not entry_id and not title_raw:
            continue

        title = re.sub(r'\*\*|`', '', title_raw).strip()
        if not title:
            continue

        if not entry_id:
            pattern_id = ''
        else:
            pattern_id = re.sub(r'\*\*', '', entry_id).strip()

        entry = {
            'pattern_id': pattern_id,
            'title': title,
            'status': status if status else 'unknown',
            'keywords': parse_keywords(keywords_text),
            'queries': parse_queries(keywords_text),
        }

        deps = parse_dependencies(deps_text)
        if deps:
            entry['dependencies'] = deps

        if pattern_id or title:
            entries.append(entry)

    return entries


def resolve_files(entries: list[dict], sections_dir: Path) -> list[dict]:
    """Add file paths to entries by matching against _index.md files."""
    preface_index = str(sections_dir / '03-preface-non-normative' / '_index.md')
    preface_exists = Path(preface_index).exists()

    for entry in entries:
        if entry['pattern_id']:
            entry['file'] = find_section_file(entry['pattern_id'], sections_dir)
        else:
            entry['file'] = preface_index if preface_exists else ''
    return entries


def build_metadata_dict(entries: list[dict]) -> dict:
    """Convert list to dict keyed by pattern_id (or title slug for Preface entries)."""
    result = {}
    unnamed_counter = 0
    for entry in entries:
        key = entry['pattern_id']
        if not key:
            unnamed_counter += 1
            key = f"preface_{unnamed_counter}"
        result[key] = {k: v for k, v in entry.items() if k != 'pattern_id'}
    return result


def main():
    parser = argparse.ArgumentParser(description='Build metadata.json from FPF-Spec ToC')
    parser.add_argument('--spec', default='FPF-Spec.md', help='Path to FPF-Spec.md')
    parser.add_argument('--sections', default='sections', help='Sections directory')
    parser.add_argument('--output', default='sections/metadata.json', help='Output path')
    args = parser.parse_args()

    spec_path = Path(args.spec)
    sections_dir = Path(args.sections)
    output_path = Path(args.output)

    print(f"Parsing ToC from {spec_path}...")
    entries = parse_toc(spec_path)
    print(f"Found {len(entries)} ToC entries")

    print(f"Resolving file paths from {sections_dir}/...")
    entries = resolve_files(entries, sections_dir)
    resolved = sum(1 for e in entries if e.get('file'))
    print(f"Resolved {resolved}/{len(entries)} entries to files")

    metadata = build_metadata_dict(entries)
    output_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Written to {output_path} ({len(metadata)} entries)")


if __name__ == '__main__':
    main()
