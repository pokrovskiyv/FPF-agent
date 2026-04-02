#!/usr/bin/env python3
"""Smoke tests for FPF-agent pipeline integrity.

Validates metadata, routes, glossary, cross-references, and semantic search
without external dependencies (stdlib only, except semantic search tests
which require uv + sentence-transformers).

Usage:
    python3 scripts/test_smoke.py           # metadata, routes, glossary, xrefs
    python3 scripts/test_smoke.py --all     # + semantic search (requires uv)
"""

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECTIONS = PROJECT_ROOT / 'sections'
METADATA = SECTIONS / 'metadata.json'
GLOSSARY = SECTIONS / 'glossary-quick.md'
ROUTES_DIR = SECTIONS / 'routes'
EMBEDDINGS_DIR = SECTIONS / 'embeddings'

RUN_ALL = '--all' in sys.argv


def load_metadata() -> dict:
    with open(METADATA, encoding='utf-8') as f:
        return json.load(f)


class TestMetadataIntegrity(unittest.TestCase):
    """Validate metadata.json structure and file references."""

    def setUp(self):
        self.metadata = load_metadata()

    def test_metadata_exists_and_parses(self):
        self.assertTrue(METADATA.exists(), 'metadata.json not found')
        self.assertIsInstance(self.metadata, dict)

    def test_minimum_entry_count(self):
        self.assertGreaterEqual(len(self.metadata), 230,
                                f'Expected >=230 entries, got {len(self.metadata)}')

    def test_no_bold_markers_in_keys(self):
        bold_keys = [k for k in self.metadata if '**' in k]
        self.assertEqual(bold_keys, [],
                         f'Keys with bold markers: {bold_keys}')

    def test_all_entries_have_title(self):
        missing = [k for k, v in self.metadata.items() if not v.get('title')]
        self.assertEqual(missing, [],
                         f'Entries without title: {missing}')

    def test_file_paths_resolve(self):
        missing = []
        for key, entry in self.metadata.items():
            file_path = entry.get('file', '')
            if file_path and not Path(file_path).exists():
                missing.append((key, file_path))
        self.assertEqual(missing, [],
                         f'File paths that do not exist: {missing}')

    def test_resolved_file_count(self):
        resolved = sum(1 for v in self.metadata.values() if v.get('file'))
        self.assertGreaterEqual(resolved, 200,
                                f'Expected >=200 resolved files, got {resolved}')


class TestRouteFiles(unittest.TestCase):
    """Validate route files and their section chains."""

    ROUTE_NAMES = [
        'route-1-project-alignment.md',
        'route-2-language-discovery.md',
        'route-3-boundary-unpacking.md',
        'route-4-comparison-selection.md',
        'route-5-generator-portfolio.md',
        'route-6-rewrite-explanation.md',
        'route-7-ethical-assurance.md',
        'route-8-trust-assurance.md',
        'route-9-composition-aggregation.md',
        'route-10-evolution-learning.md',
    ]

    def test_all_routes_exist(self):
        for name in self.ROUTE_NAMES:
            path = ROUTES_DIR / name
            self.assertTrue(path.exists(), f'Route file missing: {name}')

    def test_route_sections_exist(self):
        for name in self.ROUTE_NAMES:
            path = ROUTES_DIR / name
            if not path.exists():
                continue
            content = path.read_text(encoding='utf-8')
            file_refs = re.findall(r'sections/[^\s|]+\.md', content)
            missing = [f for f in file_refs if not Path(f).exists()]
            self.assertEqual(missing, [],
                             f'{name}: referenced files missing: {missing}')

    def test_routes_have_core_sections(self):
        for name in self.ROUTE_NAMES:
            path = ROUTES_DIR / name
            if not path.exists():
                continue
            content = path.read_text(encoding='utf-8')
            core_count = content.count('YES')
            self.assertGreaterEqual(core_count, 1,
                                    f'{name}: no core sections (YES) found')

    def test_routes_have_minimum_chain_length(self):
        for name in self.ROUTE_NAMES:
            path = ROUTES_DIR / name
            if not path.exists():
                continue
            content = path.read_text(encoding='utf-8')
            file_refs = re.findall(r'sections/[^\s|]+\.md', content)
            self.assertGreaterEqual(len(file_refs), 3,
                                    f'{name}: chain too short ({len(file_refs)} sections)')


class TestGlossary(unittest.TestCase):
    """Validate glossary-quick.md structure."""

    def setUp(self):
        self.content = GLOSSARY.read_text(encoding='utf-8') if GLOSSARY.exists() else ''

    def test_glossary_exists(self):
        self.assertTrue(GLOSSARY.exists(), 'glossary-quick.md not found')

    def test_has_table_header(self):
        self.assertIn('| Term |', self.content,
                       'Glossary missing table header')

    def test_minimum_entries(self):
        data_rows = [
            line for line in self.content.splitlines()
            if line.startswith('|') and not line.startswith('| Term')
            and not line.startswith('|---') and not line.startswith('| :---')
        ]
        self.assertGreaterEqual(len(data_rows), 40,
                                f'Expected >=40 glossary entries, got {len(data_rows)}')


class TestCrossReferences(unittest.TestCase):
    """Validate _xref.md files reference existing patterns."""

    def setUp(self):
        self.metadata = load_metadata()
        self.valid_pids = set()
        for key in self.metadata:
            self.valid_pids.add(key)
            clean = key.replace('**', '').strip()
            if clean:
                self.valid_pids.add(clean)

    def test_xref_files_exist(self):
        xref_files = list(SECTIONS.rglob('_xref.md'))
        self.assertGreaterEqual(len(xref_files), 5,
                                f'Expected >=5 _xref.md files, got {len(xref_files)}')

    def test_xref_patterns_valid(self):
        dangling = []
        for xref_file in SECTIONS.rglob('_xref.md'):
            content = xref_file.read_text(encoding='utf-8')
            pids = re.findall(r'\b([A-K]\.\d+(?:\.[A-Za-z0-9]+)*)\b', content)
            for pid in pids:
                if pid not in self.valid_pids:
                    dangling.append((xref_file.name, pid))
        # Allow some dangling refs (subsections without metadata entries)
        # but flag if more than 20% are unresolved
        if dangling:
            total_refs = sum(
                len(re.findall(r'\b([A-K]\.\d+(?:\.[A-Za-z0-9]+)*)\b',
                               f.read_text(encoding='utf-8')))
                for f in SECTIONS.rglob('_xref.md')
            )
            ratio = len(dangling) / max(total_refs, 1)
            self.assertLess(ratio, 0.2,
                            f'{len(dangling)}/{total_refs} xref PIDs unresolved (>{20}%)')


@unittest.skipUnless(RUN_ALL, 'Semantic search tests require --all flag')
class TestSemanticSearch(unittest.TestCase):
    """Validate semantic search returns reasonable results."""

    # Queries for score/result-count checks (all 6)
    ALL_QUERIES = [
        'teams cannot agree on responsibilities',
        'what is a bounded context',
        'how to compare two approaches',
        'contract mixes rules and obligations',
        'как определить зоны ответственности',
        'definition of done for quality',
    ]

    # Queries with stable expected PIDs (only the most predictable ones)
    QUERIES_WITH_EXPECTED = [
        ('teams cannot agree on responsibilities', ['A.1.1', 'A.15', 'C.3', 'F.9']),
        ('what is a bounded context', ['A.1.1']),
    ]

    def _run_search(self, query: str) -> list[dict]:
        result = subprocess.run(
            ['uv', 'run', str(PROJECT_ROOT / 'scripts' / 'semantic_search.py'),
             query, '--top-k', '3', '--json'],
            capture_output=True, text=True, timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        self.assertEqual(result.returncode, 0,
                         f'semantic_search.py failed: {result.stderr}')
        return json.loads(result.stdout)

    def test_search_returns_results(self):
        for query in self.ALL_QUERIES:
            results = self._run_search(query)
            self.assertGreater(len(results), 0,
                               f'No results for query: {query}')

    def test_scores_above_minimum(self):
        for query in self.ALL_QUERIES:
            results = self._run_search(query)
            if results:
                top_score = results[0]['score']
                self.assertGreaterEqual(top_score, 0.35,
                                        f'Top score {top_score} too low for: {query}')

    def test_relevant_patterns_in_top3(self):
        for query, expected_pids in self.QUERIES_WITH_EXPECTED:
            results = self._run_search(query)
            result_pids = [r['pattern_id'] for r in results]
            overlap = set(result_pids) & set(expected_pids)
            self.assertGreater(len(overlap), 0,
                               f'Query "{query}": expected one of {expected_pids}, '
                               f'got {result_pids}')


if __name__ == '__main__':
    # Remove --all from argv before passing to unittest
    test_argv = [a for a in sys.argv if a != '--all']
    unittest.main(argv=test_argv, verbosity=2)
