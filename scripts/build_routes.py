#!/usr/bin/env python3
"""Build route chain files for each of the 10 practical FPF entry routes.

Each route file lists the ordered chain of sections to load, with a
plain-language description of what the user will get.

Usage:
    python scripts/build_routes.py [--metadata sections/metadata.json] [--output sections/routes/]
"""

import argparse
import json
from pathlib import Path

ROUTES = [
    {
        "id": 1,
        "slug": "project-alignment",
        "user_says": "Teams don't understand each other / need work structure / confused about responsibilities",
        "user_gets": "Map of who owns what, how work flows between teams, where the gaps are",
        "chain": ["A.1.1", "A.15", "A.15.2", "A.15.3", "B.5.1", "F.11", "F.9", "F.17"],
        "core": ["A.1.1", "A.15", "B.5.1"],
    },
    {
        "id": 2,
        "slug": "language-discovery",
        "user_says": "Can't agree on terminology / have a vague idea that's hard to articulate / emerging concern",
        "user_gets": "Table of what each term means for each team, flagged danger zones, preservation note for early ideas",
        "chain": ["C.2.2a", "C.2.LS", "A.16", "A.16.1", "A.16.2", "B.4.1", "B.5.2.0"],
        "core": ["C.2.2a", "A.16", "A.16.1"],
    },
    {
        "id": 3,
        "slug": "boundary-unpacking",
        "user_says": "Contract/API/SLA/spec mixes rules, conditions, obligations, and evidence",
        "user_gets": "Structured breakdown: what's a rule, what's an access condition, what's an obligation, what needs proof",
        "chain": ["A.6", "A.6.B", "A.6.C", "A.6.P", "A.6.Q", "A.6.A"],
        "core": ["A.6", "A.6.B", "A.6.C"],
    },
    {
        "id": 4,
        "slug": "comparison-selection",
        "user_says": "Need to choose between options / decision-making is opaque / comparing alternatives",
        "user_gets": "Decision criteria table, comparison frame, evidence gaps checklist, recommendation",
        "chain": ["A.17", "A.18", "A.19", "G.0", "A.19.CPM", "A.19.SelectorMechanism", "G.5"],
        "core": ["A.19", "G.0", "A.19.CPM"],
    },
    {
        "id": 5,
        "slug": "generator-portfolio",
        "user_says": "What's the state of the art in X? / need a reusable search scaffold / portfolio of approaches",
        "user_gets": "Overview of schools/approaches, comparison table, reusable scaffold, what to shortlist",
        "chain": ["A.0", "G.0", "G.1", "G.2", "G.5", "B.5.2.1", "C.17"],
        "core": ["A.0", "G.0", "G.1"],
    },
    {
        "id": 6,
        "slug": "rewrite-explanation",
        "user_says": "Rewrite without changing meaning / explain for different audience / compare two versions",
        "user_gets": "Rewritten text with notes on what was preserved and what changed, faithfulness profile",
        "chain": ["A.6.3.CR", "A.6.3.RT", "E.17.EFP", "E.17.ID.CR", "E.17.AUD.LHR"],
        "core": ["A.6.3.CR", "A.6.3.RT", "E.17.EFP"],
    },
    {
        "id": 7,
        "slug": "ethical-assurance",
        "user_says": "How to audit for hidden bias? / ethical assumptions / value conflicts across teams at different scales",
        "user_gets": "Bias register, conflict map by scale, ethical audit checklist",
        "chain": ["D.1", "D.2", "D.3", "D.4", "D.5"],
        "core": ["D.2", "D.3", "D.5"],
    },
    {
        "id": 8,
        "slug": "trust-assurance",
        "user_says": "Can we trust this metric? / how to aggregate confidence without overclaim / evidence grounding",
        "user_gets": "Assurance profile (formality/scope/reliability per component), dependency map, evidence gaps",
        "chain": ["B.3", "B.3.5", "B.1", "B.1.1", "A.6.B"],
        "core": ["B.3", "B.3.5", "B.1"],
    },
    {
        "id": 9,
        "slug": "composition-aggregation",
        "user_says": "Why do KPI dashboards lie? / sum of parts != whole / Tool A aggregates differently from Tool B",
        "user_gets": "Violated invariant diagnosis, aggregation dependency map, fix recommendations",
        "chain": ["B.1", "B.1.1", "B.1.2", "B.1.3", "B.1.4", "B.1.5"],
        "core": ["B.1", "B.1.1", "B.1.4"],
    },
    {
        "id": 10,
        "slug": "evolution-learning",
        "user_says": "Design is outdated and nobody noticed / how to close the loop between operations and design / lessons learned",
        "user_gets": "Current cycle map (where the break is), loop closure plan, cycle health metrics",
        "chain": ["B.4", "B.4.1", "B.5.1", "A.4", "G.11"],
        "core": ["B.4", "B.4.1", "B.5.1"],
    },
]


def build_route_file(route: dict, metadata: dict) -> str:
    """Generate a route file with section chain and file paths."""
    lines = [
        f"# Route {route['id']}: {route['slug'].replace('-', ' ').title()}",
        "",
        f"**When user says:** {route['user_says']}",
        "",
        f"**What user gets:** {route['user_gets']}",
        "",
        "## Section Chain (load in order)",
        "",
        "| # | Pattern | Title | File | Core? |",
        "|---|---------|-------|------|-------|",
    ]

    for i, pid in enumerate(route['chain'], 1):
        entry = metadata.get(pid, {})
        title = entry.get('title', '(not found)')[:60]
        file_path = entry.get('file', '')
        is_core = 'YES' if pid in route['core'] else ''
        lines.append(f"| {i} | {pid} | {title} | {file_path} | {is_core} |")

    lines.extend([
        "",
        "## Loading Strategy",
        "",
        f"- **Minimum load** (simple query): first {len(route['core'])} core sections",
        f"- **Full load** (complex query): all {len(route['chain'])} sections in chain",
        "- If stagnation detected: check _xref.md for cross-references",
    ])

    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description='Build route chain files')
    parser.add_argument('--metadata', default='sections/metadata.json')
    parser.add_argument('--output', default='sections/routes')
    args = parser.parse_args()

    metadata = json.loads(Path(args.metadata).read_text(encoding='utf-8'))
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    for route in ROUTES:
        content = build_route_file(route, metadata)
        filename = f"route-{route['id']}-{route['slug']}.md"
        (output_dir / filename).write_text(content, encoding='utf-8')
        print(f"Written {filename}")

    print(f"\n{len(ROUTES)} route files written to {output_dir}/")


if __name__ == '__main__':
    main()
