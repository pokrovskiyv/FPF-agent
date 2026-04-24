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
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CODEX_SKILL = PROJECT_ROOT / '.agents' / 'skills' / 'fpf' / 'SKILL.md'
CC_SKILL = PROJECT_ROOT / 'skills' / 'fpf' / 'SKILL.md'
PLUGIN_ROOT = PROJECT_ROOT / 'plugins' / 'fpf'
PLUGIN_SKILL = PLUGIN_ROOT / 'skills' / 'fpf' / 'SKILL.md'
PLUGIN_MANIFEST = PLUGIN_ROOT / '.codex-plugin' / 'plugin.json'
REPO_MARKETPLACE = PROJECT_ROOT / '.agents' / 'plugins' / 'marketplace.json'

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


class TestPackagedCodexPlugin(unittest.TestCase):
    """Source-controlled Codex plugin package is self-contained."""

    def test_manifest_exists_and_declares_skills(self):
        self.assertTrue(PLUGIN_MANIFEST.exists(),
                        f'Plugin manifest not found at {PLUGIN_MANIFEST}')
        manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(manifest.get('name'), 'fpf')
        self.assertEqual(manifest.get('skills'), './skills/')
        self.assertEqual(manifest.get('license'), 'MIT')
        interface = manifest.get('interface', {})
        self.assertEqual(interface.get('displayName'), 'FPF')
        self.assertIn('defaultPrompt', interface)

    def test_runtime_files_exist_in_plugin(self):
        required = [
            'skills/fpf/SKILL.md',
            'agents/fpf-classifier.md',
            'agents/fpf-retriever.md',
            'agents/fpf-reasoner.md',
            'agents/fpf-reviewer.md',
            'sections/metadata.json',
            'sections/glossary-quick.md',
            'sections/lexical-rules.md',
            'sections/routes/route-1-project-alignment.md',
            'scripts/semantic_search.py',
            'scripts/build_embeddings.py',
        ]
        missing = [path for path in required if not (PLUGIN_ROOT / path).exists()]
        self.assertEqual(missing, [],
                         f'Packaged plugin is missing runtime files: {missing}')

    def test_packaged_skill_uses_plugin_root_contract(self):
        self.assertTrue(PLUGIN_SKILL.exists(),
                        f'Packaged skill not found at {PLUGIN_SKILL}')
        text = PLUGIN_SKILL.read_text(encoding='utf-8')
        self.assertIn('plugin root', text.lower())
        self.assertNotIn('launched from the FPF-agent repo root', text)

    def test_packaged_skill_references_resolve_inside_plugin(self):
        self.assertTrue(PLUGIN_SKILL.exists(),
                        f'Packaged skill not found at {PLUGIN_SKILL}')
        text = PLUGIN_SKILL.read_text(encoding='utf-8')
        _, body = split_frontmatter(text)
        patterns = [
            r'`?(agents/fpf-[a-z]+\.md)`?',
            r'`(sections/[a-zA-Z0-9_./\-]+\.(?:md|json))`',
            r'`?(scripts/[a-zA-Z0-9_\-]+\.py)`?',
        ]
        paths = []
        for pattern in patterns:
            paths.extend(re.findall(pattern, body))
        concrete = sorted({
            path for path in paths
            if '{' not in path and '*' not in path and 'route-' not in path
        })
        missing = [path for path in concrete if not (PLUGIN_ROOT / path).exists()]
        self.assertEqual(missing, [],
                         f'Packaged skill references missing files: {missing}')


class TestCodexPluginInstaller(unittest.TestCase):
    """Installer syncs packaged plugin into a home-local Codex marketplace."""

    def test_installer_syncs_plugin_and_marketplace_to_temp_home(self):
        installer = PROJECT_ROOT / 'scripts' / 'install_codex_plugin.py'
        self.assertTrue(installer.exists(), f'Installer not found: {installer}')

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = subprocess.run(
                [sys.executable, str(installer), '--home', str(home)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            installed_manifest = home / 'plugins' / 'fpf' / '.codex-plugin' / 'plugin.json'
            self.assertTrue(installed_manifest.exists(),
                            f'Installed manifest missing: {installed_manifest}')
            manifest = json.loads(installed_manifest.read_text(encoding='utf-8'))
            self.assertEqual(manifest.get('name'), 'fpf')

            marketplace_path = home / '.agents' / 'plugins' / 'marketplace.json'
            self.assertTrue(marketplace_path.exists(),
                            f'Marketplace missing: {marketplace_path}')
            marketplace = json.loads(marketplace_path.read_text(encoding='utf-8'))
            entries = marketplace.get('plugins', [])
            matching = [entry for entry in entries if entry.get('name') == 'fpf']
            self.assertEqual(len(matching), 1)
            self.assertEqual(matching[0]['source']['path'], './plugins/fpf')
            self.assertEqual(matching[0]['policy']['installation'], 'AVAILABLE')
            self.assertEqual(matching[0]['policy']['authentication'], 'ON_INSTALL')
            self.assertEqual(matching[0]['category'], 'Productivity')


class TestRepoLocalMarketplace(unittest.TestCase):
    """Repo exposes the packaged plugin through Codex marketplace metadata."""

    def test_repo_marketplace_points_to_packaged_plugin(self):
        self.assertTrue(REPO_MARKETPLACE.exists(),
                        f'Repo marketplace not found: {REPO_MARKETPLACE}')
        marketplace = json.loads(REPO_MARKETPLACE.read_text(encoding='utf-8'))
        entries = marketplace.get('plugins', [])
        matching = [entry for entry in entries if entry.get('name') == 'fpf']
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]['source']['source'], 'local')
        self.assertEqual(matching[0]['source']['path'], './plugins/fpf')
        self.assertEqual(matching[0]['policy']['installation'], 'AVAILABLE')
        self.assertEqual(matching[0]['policy']['authentication'], 'ON_INSTALL')
        self.assertEqual(matching[0]['category'], 'Productivity')


if __name__ == '__main__':
    argv = [a for a in sys.argv if a != '--all']
    unittest.main(argv=argv, verbosity=2)
