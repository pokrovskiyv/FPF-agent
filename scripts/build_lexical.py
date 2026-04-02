#!/usr/bin/env python3
"""Extract Part K lexical rules (mandatory term substitutions) into lexical-rules.md.

Parses the replacement tables from Part K of FPF-Spec.md.

Usage:
    python scripts/build_lexical.py [--spec FPF-Spec.md] [--output sections/lexical-rules.md]
"""

import argparse
import re
from pathlib import Path


def extract_part_k(spec_path: Path) -> str:
    """Extract Part K content from the spec."""
    lines = spec_path.read_text(encoding='utf-8').splitlines()
    in_part_k = False
    part_k_lines = []

    for line in lines:
        if re.match(r'^#\s+\*?\*?Part K', line):
            in_part_k = True
        elif in_part_k and line.startswith('# ') and 'Part K' not in line:
            break

        if in_part_k:
            part_k_lines.append(line)

    return '\n'.join(part_k_lines)


def parse_replacement_table(content: str) -> list[dict]:
    """Parse the mandatory replacement map table."""
    rules = []
    in_table = False

    for line in content.splitlines():
        if '| Legacy Term' in line or '| legacy' in line.lower():
            in_table = True
            continue
        if in_table and line.startswith('| ---'):
            continue
        if in_table and line.startswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if len(cells) >= 3:
                rules.append({
                    'legacy': cells[0],
                    'replace_with': cells[1],
                    'plain_allowance': cells[2] if len(cells) > 2 else '',
                    'reference': cells[3] if len(cells) > 3 else '',
                })
        elif in_table and not line.strip():
            in_table = False

    return rules


def parse_deprecations(content: str) -> list[str]:
    """Extract deprecated terms from the deprecations section."""
    deprecated = []
    match = re.search(
        r'following terms \*\*MUST NOT\*\*.*?Use instead:',
        content,
        re.DOTALL,
    )
    if match:
        block = match.group(0)
        terms = re.findall(r'\*([^*]+)\*', block)
        deprecated = [
            t.strip() for t in terms
            if len(t.strip()) > 2
            and not t.strip().startswith('MUST')
            and not any(w in t.lower() for w in ['name ', 'scope ', 'following'])
        ]
    return deprecated


def write_lexical_rules(rules: list[dict], deprecated: list[str], output_path: Path) -> None:
    """Write lexical-rules.md."""
    lines = [
        "# FPF Lexical Rules (Part K — Mandatory)",
        "",
        "These substitutions are MANDATORY in all normative content.",
        "The Reasoner agent must enforce these internally; output uses plain language.",
        "",
        "## Measurement Terms — Mandatory Replacements",
        "",
        "| DO NOT use | Use instead | Notes |",
        "|------------|-------------|-------|",
    ]

    for rule in rules:
        legacy = rule['legacy']
        replacement = rule['replace_with']
        notes = rule.get('plain_allowance', '')
        lines.append(f"| {legacy} | {replacement} | {notes} |")

    if deprecated:
        lines.extend([
            "",
            "## Scope Terms — Deprecated (MUST NOT use in normative text)",
            "",
        ])
        for term in deprecated:
            lines.append(f"- ~~{term}~~ → use `U.ClaimScope` (G), `U.WorkScope`, or `U.Scope`")

    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Extract Part K lexical rules')
    parser.add_argument('--spec', default='FPF-Spec.md')
    parser.add_argument('--output', default='sections/lexical-rules.md')
    args = parser.parse_args()

    spec_path = Path(args.spec)
    print(f"Extracting Part K from {spec_path}...")
    content = extract_part_k(spec_path)
    print(f"Part K content: {len(content)} chars")

    rules = parse_replacement_table(content)
    print(f"Found {len(rules)} replacement rules")

    deprecated = parse_deprecations(content)
    print(f"Found {len(deprecated)} deprecated terms")

    write_lexical_rules(rules, deprecated, Path(args.output))
    print(f"Written to {args.output}")


if __name__ == '__main__':
    main()
