#!/usr/bin/env python3
"""Split FPF-Spec.md monolith into ~230 section files organized by Part/Cluster.

H1 headings (# ) define directory boundaries (Parts, Clusters).
H2 headings (## ) define individual section files.
Each directory gets an _index.md listing its sections.

Usage:
    python scripts/split_spec.py [--spec FPF-Spec.md] [--output sections/]
"""

import argparse
import re
import unicodedata
from pathlib import Path


def slugify(text: str, max_len: int = 60) -> str:
    """Convert heading text to filesystem-safe slug."""
    text = re.sub(r'\*\*|`|[*]', '', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = re.sub(r'[-\s]+', '-', text).strip('-').lower()
    return text[:max_len]


def extract_pattern_id(heading: str) -> str:
    """Extract pattern ID like 'A.6.P' or 'B.3.3' from heading text."""
    match = re.match(r'[*\s]*([A-K]\.\d+(?:\.\d+)*(?:\.[A-Z]+)?)', heading)
    if match:
        return match.group(1)
    match = re.match(r'[*\s]*(A\.0|[A-K]\.\d+)', heading)
    if match:
        return match.group(1)
    return ''


def is_real_h1(line: str) -> bool:
    """Check if a line is a real H1 heading (not a table row starting with #)."""
    if not line.startswith('# '):
        return False
    stripped = line[2:].strip()
    if stripped.startswith('|'):
        return False
    if len(stripped) < 3:
        return False
    return True


def is_h2(line: str) -> bool:
    """Check if a line is an H2 heading."""
    return line.startswith('## ')


def parse_spec(spec_path: Path) -> list[dict]:
    """Parse the spec into a list of sections with metadata."""
    lines = spec_path.read_text(encoding='utf-8').splitlines()

    h1_sections = []
    current_h1 = {'title': 'preamble', 'slug': '00-preamble', 'h2s': [], 'start': 0}
    current_h2 = None
    h2_lines = []
    dir_counter = 0

    for i, line in enumerate(lines):
        if is_real_h1(line):
            if current_h2 is not None:
                current_h2['content'] = '\n'.join(h2_lines)
                current_h1['h2s'].append(current_h2)
                current_h2 = None
                h2_lines = []
            elif h2_lines and current_h1['h2s'] == []:
                current_h1['preamble_content'] = '\n'.join(h2_lines)
                h2_lines = []

            if current_h1['h2s'] or h2_lines:
                if not current_h1['h2s'] and h2_lines:
                    current_h1['preamble_content'] = '\n'.join(h2_lines)
                h1_sections.append(current_h1)
            elif dir_counter > 0:
                h1_sections.append(current_h1)

            dir_counter += 1
            title = line[2:].strip().strip('*').strip()
            current_h1 = {
                'title': title,
                'slug': f'{dir_counter:02d}-{slugify(title)}',
                'h2s': [],
                'start': i,
            }
            h2_lines = []

        elif is_h2(line):
            if current_h2 is not None:
                current_h2['content'] = '\n'.join(h2_lines)
                current_h1['h2s'].append(current_h2)

            title = line[3:].strip()
            pattern_id = extract_pattern_id(title)
            h2_counter = len(current_h1['h2s']) + 1
            slug_prefix = f'{h2_counter:02d}'
            if pattern_id:
                slug_prefix += f'-{slugify(pattern_id)}'
            slug = f'{slug_prefix}-{slugify(title)}'

            current_h2 = {
                'title': title,
                'pattern_id': pattern_id,
                'slug': slug,
                'line_num': i + 1,
            }
            h2_lines = [line]

        else:
            h2_lines.append(line)

    if current_h2 is not None:
        current_h2['content'] = '\n'.join(h2_lines)
        current_h1['h2s'].append(current_h2)
    elif h2_lines:
        current_h1['preamble_content'] = '\n'.join(h2_lines)

    h1_sections.append(current_h1)

    return h1_sections


def write_sections(sections: list[dict], output_dir: Path) -> dict:
    """Write section files and _index.md files. Returns stats."""
    output_dir.mkdir(parents=True, exist_ok=True)

    total_dirs = 0
    total_files = 0

    for section in sections:
        dir_path = output_dir / section['slug']
        dir_path.mkdir(parents=True, exist_ok=True)
        total_dirs += 1

        preamble = section.get('preamble_content', '')
        if preamble.strip():
            preamble_file = dir_path / '00-preamble.md'
            preamble_file.write_text(preamble, encoding='utf-8')
            total_files += 1

        index_lines = [f"# {section['title']}\n"]

        for h2 in section['h2s']:
            filename = f"{h2['slug']}.md"
            filepath = dir_path / filename
            filepath.write_text(h2['content'], encoding='utf-8')
            total_files += 1

            pid = f" ({h2['pattern_id']})" if h2['pattern_id'] else ''
            title_clean = re.sub(r'[`*]', '', h2['title'])
            index_lines.append(f"- [{title_clean}{pid}]({filename})")

        index_path = dir_path / '_index.md'
        index_path.write_text('\n'.join(index_lines) + '\n', encoding='utf-8')

    return {'directories': total_dirs, 'files': total_files}


def main():
    parser = argparse.ArgumentParser(description='Split FPF-Spec.md into section files')
    parser.add_argument('--spec', default='FPF-Spec.md', help='Path to FPF-Spec.md')
    parser.add_argument('--output', default='sections', help='Output directory')
    args = parser.parse_args()

    spec_path = Path(args.spec)
    output_dir = Path(args.output)

    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    print(f"Parsing {spec_path}...")
    sections = parse_spec(spec_path)

    print(f"Found {len(sections)} top-level sections")
    for s in sections:
        print(f"  {s['slug']}: {len(s['h2s'])} subsections")

    print(f"\nWriting to {output_dir}/...")
    stats = write_sections(sections, output_dir)

    print(f"\nDone: {stats['directories']} directories, {stats['files']} files")


if __name__ == '__main__':
    main()
