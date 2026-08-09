import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "documents" / "markitdown-local"
SCRIPT = SKILL / "scripts" / "convert_document.py"
FIXTURE = ROOT / "tests" / "markitdown-local" / "fixtures" / "sample.html"


class SkillStructureTests(unittest.TestCase):
    def test_required_files_and_trigger_terms(self):
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(body.startswith("---\nname: markitdown-local\n"))
        for term in ("PDF", "DOCX", "PPTX", "XLSX", "HTML", "MarkItDown"):
            self.assertIn(term, body)
        self.assertIn("explicit authorization", body)
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file())
        self.assertTrue(SCRIPT.is_file())

    def test_readme_lists_skill(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("documents/", readme)
        self.assertIn("markitdown-local", readme)

    def test_helper_disables_plugins_and_external_services(self):
        helper = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("enable_plugins=False", helper)
        for forbidden in ("api_key", "azure_endpoint", "docintel_endpoint", "cu_endpoint"):
            self.assertNotIn(forbidden, helper)


class ConversionTests(unittest.TestCase):
    def run_helper(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            capture_output=True,
            text=True,
        )

    def test_source_preserved_and_markdown_written(self):
        before = FIXTURE.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sample.md"
            result = self.run_helper(str(FIXTURE), "-o", str(output), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(FIXTURE.read_bytes(), before)
            markdown = output.read_text(encoding="utf-8")
            self.assertIn("Quarterly Note", markdown)
            self.assertIn("Users", markdown)
            metadata = json.loads(result.stdout)
            self.assertEqual(metadata["source"], str(FIXTURE.resolve()))
            self.assertEqual(metadata["output"], str(output.resolve()))
            self.assertGreater(metadata["characters"], 0)

    def test_missing_source_fails_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "missing.md"
            result = self.run_helper("missing.html", "-o", str(output))
            self.assertEqual(result.returncode, 2)
            self.assertIn("does not exist", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
