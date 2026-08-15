import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CATALOG = ROOT / "catalog" / "skills.json"
GENERATOR = ROOT / "scripts" / "update_catalog.py"
README = ROOT.parent / "README.md"


class CatalogContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_catalog_matches_skill_directories(self):
        expected = {
            path.parent.name
            for path in ROOT.glob("*/SKILL.md")
        }
        actual = {entry["id"] for entry in self.entries}
        self.assertEqual(actual, expected)

    def test_catalog_paths_and_links_exist(self):
        for entry in self.entries:
            skill_dir = ROOT / entry["path"]
            self.assertTrue((skill_dir / "SKILL.md").is_file(), entry["id"])
            self.assertEqual(
                entry["link"],
                f"beamer-skills/{entry['id']}/SKILL.md",
            )

    def test_readme_is_generated_and_contains_current_links(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_readme_has_no_renamed_skill_aliases(self):
        readme = README.read_text(encoding="utf-8")
        self.assertNotIn("beamer-presentation", readme)


if __name__ == "__main__":
    unittest.main()
