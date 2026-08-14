import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "beamer-progress-draft" / "scripts" / "generate.py"
SPEC = importlib.util.spec_from_file_location("progress_generate", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ProgressGeneratorTests(unittest.TestCase):
    def test_builds_title_and_itemize_frames(self):
        data = {
            "version": 1,
            "template": "clean",
            "slides": [
                {"type": "title", "title": "Project progress", "subtitle": "Week 1"},
                {"type": "itemize", "frametitle": "Data is ready", "items": ["Cleaned data"]},
            ],
        }
        output = MODULE.build(data, str(ROOT / "beamer-progress-draft" / "templates"))
        self.assertIn(r"\title{Project progress}", output)
        self.assertIn(r"\begin{frame}{Data is ready}", output)
        self.assertIn(r"\item Cleaned data", output)

    def test_escapes_latex_special_characters(self):
        self.assertEqual(MODULE.latex_escape("A&B_50%"), r"A\&B\_50\%")

    def test_rejects_malformed_top_level_data(self):
        with self.assertRaisesRegex(ValueError, "slides"):
            MODULE.validate_data({"template": "clean"})

    def test_warns_for_unknown_types_and_format_risks(self):
        data = {
            "slides": [
                {"type": "itemize", "frametitle": "", "items": ["1", "2", "3", "4", "5", "6"]},
                {"type": "future", "frametitle": "Later"},
            ]
        }
        stream = io.StringIO()
        with redirect_stdout(stream):
            MODULE.build(data, str(ROOT / "beamer-progress-draft" / "templates"))
        warning_text = stream.getvalue()
        self.assertIn("more than five bullets", warning_text)
        self.assertIn("unknown slide type", warning_text)

    def test_missing_template_falls_back_to_clean(self):
        data = {"slides": [{"type": "itemize", "frametitle": "Progress", "items": []}], "template": "missing"}
        stream = io.StringIO()
        with redirect_stdout(stream):
            output = MODULE.build(data, str(ROOT / "beamer-progress-draft" / "templates"))
        self.assertIn(r"\usetheme{Madrid}", output)
        self.assertIn("falling back to clean", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
