#!/usr/bin/env python3
"""Tests for scripts/update_changelog.py.

Focus: the commit-message extractor must not truncate a description at an
apostrophe (or any quote) inside a double-quoted -m message, and the bullet
written to CHANGELOG.md must contain the full description.

Run: python3 scripts/test_update_changelog.py
"""

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from update_changelog import (  # noqa: E402
    extract_commit_message,
    format_entry,
    parse_conventional_commit,
    update_changelog,
)


class TestExtractCommitMessage(unittest.TestCase):
    def test_apostrophe_in_double_quoted_message(self):
        # The regression: ' inside "..." used to truncate at the apostrophe.
        cmd = 'git commit -m "docs: add What\'s New for the fix"'
        self.assertEqual(
            extract_commit_message(cmd), "docs: add What's New for the fix"
        )

    def test_escaped_double_quote_in_message(self):
        cmd = 'git commit -m "fix: handle the \\"X\\" case"'
        self.assertEqual(extract_commit_message(cmd), 'fix: handle the "X" case')

    def test_plain_double_quoted(self):
        self.assertEqual(
            extract_commit_message('git commit -m "feat: add thing"'),
            "feat: add thing",
        )

    def test_single_quoted(self):
        self.assertEqual(
            extract_commit_message("git commit -m 'chore: tidy up'"),
            "chore: tidy up",
        )

    def test_heredoc_subject_only(self):
        cmd = (
            "git commit -m \"$(cat <<'EOF'\n"
            "fix: the subject line\n\nbody paragraph\nEOF\n)\""
        )
        self.assertEqual(extract_commit_message(cmd), "fix: the subject line")

    def test_multiline_double_quoted_takes_subject(self):
        self.assertEqual(
            extract_commit_message('git commit -m "feat: subject\n\nbody"'),
            "feat: subject",
        )

    def test_first_of_multiple_m_flags(self):
        self.assertEqual(
            extract_commit_message('git commit -m "fix: subject" -m "body text"'),
            "fix: subject",
        )

    def test_no_message(self):
        self.assertIsNone(extract_commit_message("git status"))


class TestAppendedBullet(unittest.TestCase):
    def test_full_description_preserved_in_bullet(self):
        subject = extract_commit_message(
            'git commit -m "docs: add What\'s New and align manifest"'
        )
        parsed = parse_conventional_commit(subject)
        entry = format_entry(parsed)
        self.assertEqual(entry, "- **docs**: add What's New and align manifest")

        # End-to-end into a throwaway changelog: the bullet must appear in full,
        # and the old truncated form must NOT be present.
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "CHANGELOG.md"
            path.write_text("# Changelog\n\n", encoding="utf-8")
            update_changelog(path, entry, date.today().isoformat())
            content = path.read_text(encoding="utf-8")
            self.assertIn("add What's New and align manifest", content)
            self.assertNotIn("- **docs**: What\n", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
