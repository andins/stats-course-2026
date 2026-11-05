"""Guard the skill's portability: spec-compliant frontmatter, and packages that contain everything SKILL.md links to."""

import pathlib
import re
import tempfile
import unittest
import zipfile

import package_skill


class SkillFrontmatterTests(unittest.TestCase):
    def test_frontmatter_follows_the_agent_skills_limits(self):
        fields, body = package_skill.read_frontmatter(package_skill.SKILL_ROOT / "SKILL.md")
        self.assertEqual(fields["name"], "statistics-advisor")   # must match the folder name the skill is installed under
        self.assertLessEqual(len(fields["description"]), 1024)
        self.assertIn("statistics", fields["description"])
        self.assertTrue(body.strip().startswith("# Statistics Advisor"))

    def test_invalid_frontmatter_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = pathlib.Path(tmp) / "SKILL.md"
            for text in (
                "no frontmatter",
                "---\nname: Bad_Name\ndescription: x\n---\nbody",
                "---\nname: good-name\ndescription: " + "x" * 1025 + "\n---\nbody",
                "---\nname: good-name\n---\nbody",
            ):
                skill.write_text(text)
                with self.subTest(text=text[:40]):
                    with self.assertRaises(ValueError):
                        package_skill.read_frontmatter(skill)


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = pathlib.Path(cls.tmp.name)
        cls.zip_path = package_skill.build_zip(cls.out)
        cls.single_path = package_skill.build_single_file(cls.out)
        with zipfile.ZipFile(cls.zip_path) as archive:
            cls.names = set(archive.namelist())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_zip_has_the_skill_folder_at_its_root(self):
        self.assertIn("statistics-advisor/SKILL.md", self.names)
        self.assertTrue(all(name.startswith("statistics-advisor/") for name in self.names))

    def test_zip_contains_only_skill_content(self):
        top_level = {name.split("/")[1] for name in self.names}
        self.assertEqual(top_level, {"SKILL.md", "references", "scripts"})
        for name in self.names:
            for fragment in ("explainers", "statistics-course", "__pycache__", ".pyc", ".DS_Store",
                             "dist/", "course_teacher_notes", "package_skill", "install_skill", "/test_"):
                self.assertNotIn(fragment, name)

    def test_skill_folder_has_no_course_or_tooling_files(self):
        on_disk = {p.name for p in package_skill.SKILL_ROOT.iterdir() if p.name not in package_skill.EXCLUDED_NAMES}
        self.assertEqual(on_disk, {"SKILL.md", "references", "scripts"})

    def test_skill_text_does_not_link_outside_the_skill_folder(self):
        for path in package_skill.SKILL_ROOT.rglob("*.md"):
            text = path.read_text()
            for target in re.findall(r"\]\(([^)#\s]+)", text):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (path.parent / target).resolve()
                with self.subTest(file=path.name, link=target):
                    self.assertTrue(resolved.is_relative_to(package_skill.SKILL_ROOT.resolve()),
                                    f"{path.name} links outside the skill: {target}")
                    self.assertTrue(resolved.exists(), f"{path.name} has a dead link: {target}")

    def test_every_relative_link_in_skill_md_is_in_the_zip(self):
        text = (package_skill.SKILL_ROOT / "SKILL.md").read_text()
        targets = {t.split("#")[0] for t in re.findall(r"\]\((\./[^)]+)\)", text)}
        self.assertTrue(targets)
        for target in targets:
            with self.subTest(link=target):
                self.assertIn(f"statistics-advisor/{target[2:]}", self.names)

    def test_zip_is_reproducible(self):
        with tempfile.TemporaryDirectory() as other:
            again = package_skill.build_zip(pathlib.Path(other))
            self.assertEqual(again.read_bytes(), self.zip_path.read_bytes())

    def test_single_file_contains_the_instructions_and_every_reference(self):
        text = self.single_path.read_text()
        self.assertIn("## Instructions (SKILL.md)", text)
        self.assertIn("# Statistics Advisor", text)
        self.assertNotIn("name: statistics-advisor\ndescription:", text)   # frontmatter is not repeated
        for name in package_skill.SINGLE_FILE_REFERENCES:
            self.assertIn(f"## Reference file: references/{name}", text)
        self.assertIn("Analysis triage", text)

    def test_main_writes_both_files(self):
        with tempfile.TemporaryDirectory() as out:
            self.assertEqual(package_skill.main(["--out", out]), 0)
            self.assertEqual(sorted(p.name for p in pathlib.Path(out).iterdir()),
                             ["statistics-advisor-single-file.md", "statistics-advisor.zip"])


if __name__ == "__main__":
    unittest.main()
