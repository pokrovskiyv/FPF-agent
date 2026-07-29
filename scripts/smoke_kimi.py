#!/usr/bin/env python3
"""Smoke tests for the Kimi Code CLI edition of the FPF skill.

Validates that .kimi-plugin/plugin.json is well-formed against the documented
Kimi Code plugin manifest schema, that the shared universal skill edition
resolves every file reference inside the plugin root, and that the
semantic_search.py CLI returns the expected JSON shape.
Runs offline — no Kimi Code CLI required. Does not verify LLM behavior.

Usage:
    python3 scripts/smoke_kimi.py           # structural checks only
    python3 scripts/smoke_kimi.py --all     # + semantic_search subprocess (requires uv)
"""

import json
import re
import subprocess
import sys
import unittest

from smoke_codex import (
    CC_SKILL,
    CODEX_SKILL,
    PROJECT_ROOT,
    parse_minimal_yaml,
    split_frontmatter,
)

KIMI_MANIFEST = PROJECT_ROOT / '.kimi-plugin' / 'plugin.json'
ROOT_KIMI_MANIFEST = PROJECT_ROOT / 'kimi.plugin.json'

RUN_ALL = '--all' in sys.argv

# Fields documented in the Kimi Code plugin manifest reference.
DOCUMENTED_TOP_LEVEL = {
    'name', 'version', 'description', 'keywords', 'author', 'homepage',
    'license', 'interface', 'skills', 'sessionStart', 'skillInstructions',
    'mcpServers', 'hooks', 'commands',
}
DOCUMENTED_INTERFACE = {
    'displayName', 'shortDescription', 'longDescription', 'developerName',
    'websiteURL',
}
# Documented as ignored-with-diagnostics; shipping them is pointless.
UNSUPPORTED_RUNTIME = {'tools', 'apps', 'inject', 'configFile'}


class TestKimiManifest(unittest.TestCase):
    """The Kimi plugin manifest is well-formed and self-consistent."""

    def setUp(self):
        self.assertTrue(KIMI_MANIFEST.exists(),
                        f'Kimi plugin manifest not found at {KIMI_MANIFEST}')
        self.manifest = json.loads(KIMI_MANIFEST.read_text(encoding='utf-8'))

    def test_name_is_valid_plugin_id(self):
        name = self.manifest.get('name', '')
        self.assertRegex(name, r'^[a-z0-9][a-z0-9_-]{0,63}$',
                         f'name must match the Kimi plugin id pattern: {name!r}')

    def test_required_metadata_present(self):
        for field in ('version', 'description'):
            self.assertTrue(self.manifest.get(field),
                            f'Manifest field {field!r} missing or empty')

    def test_top_level_fields_documented(self):
        unknown = set(self.manifest) - DOCUMENTED_TOP_LEVEL
        self.assertEqual(unknown, set(),
                         f'Undocumented top-level fields (typo risk): {unknown}')

    def test_no_unsupported_runtime_fields(self):
        present = set(self.manifest) & UNSUPPORTED_RUNTIME
        self.assertEqual(present, set(),
                         f'Runtime fields Kimi ignores with diagnostics: {present}')

    def test_interface_fields_documented(self):
        interface = self.manifest.get('interface', {})
        unknown = set(interface) - DOCUMENTED_INTERFACE
        self.assertEqual(unknown, set(),
                         f'Undocumented interface fields: {unknown}')
        self.assertTrue(interface.get('displayName'),
                        'interface.displayName missing')

    def test_skills_path_within_plugin_root(self):
        skills = self.manifest.get('skills', '')
        self.assertTrue(skills.startswith('./'),
                        f'skills must be a ./ path inside the plugin root: {skills!r}')
        resolved = (PROJECT_ROOT / skills).resolve()
        self.assertTrue(resolved.is_relative_to(PROJECT_ROOT.resolve()),
                        f'skills path escapes the plugin root: {skills!r}')
        self.assertTrue(resolved.is_dir(),
                        f'skills path does not resolve to a directory: {skills!r}')

    def test_no_root_manifest_conflict(self):
        self.assertFalse(ROOT_KIMI_MANIFEST.exists(),
                         'kimi.plugin.json at the root takes precedence over '
                         '.kimi-plugin/plugin.json — ship only one manifest')


class TestKimiSkillPackaging(unittest.TestCase):
    """The shared universal skill works when loaded through the Kimi manifest."""

    def setUp(self):
        manifest = json.loads(KIMI_MANIFEST.read_text(encoding='utf-8'))
        skills_dir = PROJECT_ROOT / manifest['skills']
        self.skill = skills_dir / 'fpf' / 'SKILL.md'

    def test_skill_file_exists_under_declared_skills_dir(self):
        self.assertTrue(self.skill.exists(),
                        f'SKILL.md not found at {self.skill}')
        self.assertEqual(self.skill.resolve(), CODEX_SKILL.resolve(),
                         'Kimi and Codex editions must load the same universal skill')

    def test_frontmatter_valid(self):
        text = self.skill.read_text(encoding='utf-8')
        fm, _ = split_frontmatter(text)
        self.assertTrue(fm, 'Frontmatter block missing or malformed')
        fields = parse_minimal_yaml(fm)
        self.assertEqual(fields.get('name'), 'fpf')
        self.assertGreater(len(fields.get('description', '')), 50,
                           'Description must be substantive (>50 chars)')

    def test_description_matches_cc_edition(self):
        """Trigger consistency: Kimi and CC skills must share the same description."""
        text = self.skill.read_text(encoding='utf-8')
        fm, _ = split_frontmatter(text)
        cc_text = CC_SKILL.read_text(encoding='utf-8')
        cc_fm, _ = split_frontmatter(cc_text)
        self.assertEqual(parse_minimal_yaml(fm).get('description'),
                         parse_minimal_yaml(cc_fm).get('description'),
                         'Kimi and CC skill descriptions drifted — '
                         'triggers will behave differently')

    def test_path_convention_covers_kimi_manifest(self):
        text = self.skill.read_text(encoding='utf-8')
        self.assertIn('<FPF_PLUGIN_ROOT>', text)
        self.assertIn('.kimi-plugin/plugin.json', text,
                      'Universal skill must name the Kimi manifest as a valid '
                      '<FPF_PLUGIN_ROOT> anchor')

    def test_runtime_files_exist_at_plugin_root(self):
        required = [
            '.agents/skills/fpf/SKILL.md',
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
        missing = [path for path in required if not (PROJECT_ROOT / path).exists()]
        self.assertEqual(missing, [],
                         f'Kimi plugin is missing runtime files: {missing}')

    def test_skill_references_resolve_inside_plugin_root(self):
        text = self.skill.read_text(encoding='utf-8')
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
        missing = [path for path in concrete if not (PROJECT_ROOT / path).exists()]
        self.assertEqual(missing, [],
                         f'Skill references missing files: {missing}')


class TestSemanticSearchCLI(unittest.TestCase):
    """semantic_search.py contract that the universal skill depends on."""

    @unittest.skipUnless(RUN_ALL, 'Skipping subprocess test (pass --all to enable)')
    def test_json_output_shape(self):
        if not (PROJECT_ROOT / 'sections' / 'embeddings' / 'faiss.index').exists():
            self.skipTest('embeddings index missing — build it first: '
                          'uv run scripts/build_embeddings.py')
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
