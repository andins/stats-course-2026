"""Installer tests: every tool, project scope, update, dry run, odd paths and clear errors. Uses temporary folders only."""

import contextlib
import io
import pathlib
import shutil
import tempfile
import unittest

import install_skill
import package_skill


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = pathlib.Path(self.tmp.name) / "home"
        self.home.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_tool_gets_the_skill_in_its_own_folder(self):
        expected = {
            "copilot": ".copilot/skills", "claude": ".claude/skills", "agents": ".agents/skills",
            "gemini": ".gemini/skills", "cursor": ".cursor/skills",
        }
        self.assertEqual({t: v[0] for t, v in install_skill.TOOLS.items()}, expected)
        for tool, folder in expected.items():
            with self.subTest(tool=tool):
                destination = install_skill.install(tool, home=self.home)
                self.assertEqual(destination, self.home / folder / "statistics-advisor")
                self.assertTrue((destination / "SKILL.md").is_file())
                self.assertTrue((destination / "references" / "course-topics.md").is_file())
                self.assertTrue((destination / "scripts" / "eda_template.py").is_file())

    def test_project_scope_uses_the_project_folders(self):
        project = pathlib.Path(self.tmp.name) / "my project"      # a space in the path on purpose
        project.mkdir()
        expected = {"copilot": ".github/skills", "claude": ".claude/skills", "agents": ".agents/skills",
                    "gemini": ".gemini/skills", "cursor": ".cursor/skills"}
        for tool, folder in expected.items():
            with self.subTest(tool=tool):
                destination = install_skill.install(tool, project=project, home=self.home)
                self.assertEqual(destination, project / folder / "statistics-advisor")
                self.assertTrue((destination / "SKILL.md").is_file())
        self.assertEqual(list(self.home.iterdir()), [])             # nothing written to the home folder

    def test_installed_folder_name_matches_the_skill_name(self):
        destination = install_skill.install("claude", home=self.home)
        fields, _ = package_skill.read_frontmatter(destination / "SKILL.md")
        self.assertEqual(destination.name, fields["name"])

    def test_update_replaces_the_old_copy_and_removes_stale_files(self):
        destination = install_skill.install("claude", home=self.home)
        (destination / "stale-file.txt").write_text("left over from an old version")
        (destination / "SKILL.md").write_text("broken edit")
        install_skill.install("claude", home=self.home)
        self.assertFalse((destination / "stale-file.txt").exists())
        self.assertNotEqual((destination / "SKILL.md").read_text(), "broken edit")

    def test_dry_run_changes_nothing(self):
        destination = install_skill.install("copilot", home=self.home, dry_run=True)
        self.assertFalse(destination.exists())
        self.assertEqual(list(self.home.iterdir()), [])

    def test_caches_and_ds_store_are_not_copied(self):
        source = pathlib.Path(self.tmp.name) / "src" / "statistics-advisor"
        shutil.copytree(package_skill.SKILL_ROOT, source)
        (source / "scripts" / "__pycache__").mkdir()
        (source / "scripts" / "__pycache__" / "x.cpython-312.pyc").write_bytes(b"x")
        (source / ".DS_Store").write_bytes(b"x")
        destination = install_skill.install("agents", home=self.home, source=source)
        self.assertFalse((destination / ".DS_Store").exists())
        self.assertFalse((destination / "scripts" / "__pycache__").exists())

    def test_source_folder_name_does_not_matter(self):
        renamed = pathlib.Path(self.tmp.name) / "stats-course-2026-main" / "statistics-advisor"
        shutil.copytree(package_skill.SKILL_ROOT, renamed)
        destination = install_skill.install("claude", home=self.home, source=renamed)
        self.assertEqual(destination.name, "statistics-advisor")

    def test_clear_errors(self):
        with self.assertRaises(ValueError):
            install_skill.install("notepad", home=self.home)
        with self.assertRaises(FileNotFoundError):
            install_skill.install("claude", home=self.home, source=pathlib.Path(self.tmp.name) / "empty")
        with self.assertRaises(FileNotFoundError):
            install_skill.install("claude", project=pathlib.Path(self.tmp.name) / "missing", home=self.home)

    def test_installing_over_the_source_is_refused(self):
        project = pathlib.Path(self.tmp.name) / "proj"
        project.mkdir()
        installed = install_skill.install("claude", project=project, home=self.home)
        with self.assertRaises(ValueError):
            install_skill.install("claude", project=project, home=self.home, source=installed)
        self.assertTrue((installed / "SKILL.md").is_file())          # the refusal must not delete anything

    def test_main_reports_success_and_failure(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(install_skill.main(["--tool", "claude", "--dry-run"]), 0)
            self.assertEqual(install_skill.main(["--tool", "claude", "--project", str(self.home / "nope")]), 1)
        self.assertIn("Would install the skill to:", out.getvalue())
        self.assertIn("does not exist", err.getvalue())


if __name__ == "__main__":
    unittest.main()
