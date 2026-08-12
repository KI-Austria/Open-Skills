from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("bild-entwickeln", "text-entwickeln")


class PortableSkillTest(unittest.TestCase):
    def test_skill_packages_have_required_files(self) -> None:
        for slug in SKILLS:
            with self.subTest(skill=slug):
                skill_dir = ROOT / "skills" / slug
                self.assertTrue((skill_dir / "SKILL.md").is_file())
                self.assertTrue((skill_dir / "agents" / "openai.yaml").is_file())
                self.assertTrue(any((skill_dir / "references").glob("*.md")))

    def test_frontmatter_name_matches_folder(self) -> None:
        for slug in SKILLS:
            with self.subTest(skill=slug):
                text = (ROOT / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(text, rf"(?m)^name:\s*{re.escape(slug)}\s*$")

    def test_referenced_markdown_files_exist(self) -> None:
        pattern = re.compile(r"(?:\[.*?\]\()?((?:references/)[A-Za-z0-9._/-]+\.md)\)?")
        for slug in SKILLS:
            with self.subTest(skill=slug):
                skill_dir = ROOT / "skills" / slug
                text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                references = set(pattern.findall(text))
                self.assertTrue(references)
                for relative in references:
                    self.assertTrue((skill_dir / relative).is_file(), relative)

    def test_public_packages_contain_no_local_absolute_paths(self) -> None:
        for slug in SKILLS:
            for path in (ROOT / "skills" / slug).rglob("*"):
                if not path.is_file():
                    continue
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("/Users/", text, str(path))
                self.assertNotIn("Dropbox/", text, str(path))


if __name__ == "__main__":
    unittest.main()
