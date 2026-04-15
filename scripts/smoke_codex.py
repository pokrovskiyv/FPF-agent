#!/usr/bin/env python3
"""Smoke tests for the Codex edition of the FPF skill.

Validates that .agents/skills/fpf/SKILL.md is well-formed, all file references
inside resolve, and the semantic_search.py CLI returns the expected JSON shape.
Runs offline — no Codex CLI required. Does not verify LLM behavior.

Usage:
    python3 scripts/smoke_codex.py           # structural checks only
    python3 scripts/smoke_codex.py --all     # + semantic_search subprocess (requires uv)
"""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CODEX_SKILL = PROJECT_ROOT / '.agents' / 'skills' / 'fpf' / 'SKILL.md'
CC_SKILL = PROJECT_ROOT / 'skills' / 'fpf' / 'SKILL.md'

RUN_ALL = '--all' in sys.argv


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_block, body). Empty frontmatter if missing."""
    if not text.startswith('---\n'):
        return '', text
    end = text.find('\n---\n', 4)
    if end == -1:
        return '', text
    return text[4:end], text[end + 5:]


def parse_minimal_yaml(fm: str) -> dict:
    """Stdlib-only YAML-ish parser sufficient for `name:` and `description:` fields."""
    result: dict[str, str] = {}
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r'^(\w+):\s*(.*)$', line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            if value == '>' or value == '|':
                block: list[str] = []
                i += 1
                while i < len(lines) and (lines[i].startswith('  ') or lines[i] == ''):
                    if lines[i].strip():
                        block.append(lines[i].strip())
                    i += 1
                result[key] = ' '.join(block)
                continue
            result[key] = value
        i += 1
    return result


class TestCodexSkillStructure(unittest.TestCase):
    """SKILL.md file exists and has valid frontmatter."""

    def setUp(self):
        self.assertTrue(CODEX_SKILL.exists(),
                        f'Codex SKILL.md not found at {CODEX_SKILL}')
        self.text = CODEX_SKILL.read_text(encoding='utf-8')
        self.fm, self.body = split_frontmatter(self.text)
        self.fields = parse_minimal_yaml(self.fm)

    def test_frontmatter_present(self):
        self.assertTrue(self.fm, 'Frontmatter block missing or malformed')

    def test_name_is_fpf(self):
        self.assertEqual(self.fields.get('name'), 'fpf',
                         f'Expected name=fpf, got {self.fields.get("name")!r}')

    def test_description_non_empty(self):
        desc = self.fields.get('description', '')
        self.assertGreater(len(desc), 50,
                           'Description must be substantive (>50 chars)')

    def test_description_matches_cc_edition(self):
        """Trigger consistency: Codex and CC skills must share the same description."""
        cc_text = CC_SKILL.read_text(encoding='utf-8')
        cc_fm, _ = split_frontmatter(cc_text)
        cc_fields = parse_minimal_yaml(cc_fm)
        self.assertEqual(self.fields.get('description'),
                         cc_fields.get('description'),
                         'Codex and CC skill descriptions drifted — '
                         'triggers will behave differently')


class TestCodexSkillReferences(unittest.TestCase):
    """Every file path mentioned in SKILL.md body must resolve."""

    def setUp(self):
        text = CODEX_SKILL.read_text(encoding='utf-8')
        _, self.body = split_frontmatter(text)

    def _extract_paths(self, pattern: str) -> list[str]:
        return list(dict.fromkeys(re.findall(pattern, self.body)))

    def test_agent_references_resolve(self):
        paths = self._extract_paths(r'`?(agents/fpf-[a-z]+\.md)`?')
        self.assertGreaterEqual(len(paths), 4,
                                f'Expected 4+ agent references, found {paths}')
        missing = [p for p in paths if not (PROJECT_ROOT / p).exists()]
        self.assertEqual(missing, [],
                         f'Agent file references do not resolve: {missing}')

    def test_section_references_resolve(self):
        paths = self._extract_paths(r'`(sections/[a-zA-Z0-9_./\-]+\.(?:md|json))`')
        concrete = [p for p in paths if '{' not in p and '*' not in p]
        self.assertGreater(len(concrete), 0, 'No concrete section paths found')
        missing = [p for p in concrete if not (PROJECT_ROOT / p).exists()]
        self.assertEqual(missing, [],
                         f'Section file references do not resolve: {missing}')

    def test_script_references_resolve(self):
        paths = self._extract_paths(r'`?(scripts/[a-zA-Z0-9_\-]+\.py)`?')
        concrete = list(set(paths))
        for path in concrete:
            self.assertTrue((PROJECT_ROOT / path).exists(),
                            f'Script reference does not resolve: {path}')

    def test_no_task_dispatch_instructions(self):
        """Codex has no Task-dispatch primitive — orchestration must be inline.

        Guards against instructions that would tell Codex to dispatch isolated
        subagents. Descriptive mentions (e.g., "Unlike the CC edition which
        uses subagents...") are allowed because they explain the difference.
        """
        forbidden = ['Dispatch fpf-', 'Task tool']
        for token in forbidden:
            self.assertNotIn(token, self.body,
                             f'Codex SKILL.md must not instruct "{token}" — '
                             'Codex has no equivalent primitive')


class TestSemanticSearchCLI(unittest.TestCase):
    """semantic_search.py contract that the Codex skill depends on."""

    @unittest.skipUnless(RUN_ALL, 'Skipping subprocess test (pass --all to enable)')
    def test_json_output_shape(self):
        result = subprocess.run(
            ['uv', 'run', 'scripts/semantic_search.py',
             'team handoff responsibility confusion',
             '--top-k', '3', '--json'],
            cwd=PROJECT_ROOT,
            capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0,
                         f'semantic_search.py failed: {result.stderr}')
        data = json.loads(result.stdout)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        required_keys = {'rank', 'score', 'pattern_id', 'title', 'file', 'keywords'}
        for item in data:
            missing = required_keys - set(item.keys())
            self.assertFalse(missing,
                             f'Result missing keys {missing}: {item}')


if __name__ == '__main__':
    argv = [a for a in sys.argv if a != '--all']
    unittest.main(argv=argv, verbosity=2)
