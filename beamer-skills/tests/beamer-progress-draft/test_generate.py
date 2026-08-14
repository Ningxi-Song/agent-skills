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

    def test_builds_structured_article_frames(self):
        data = {
            "mode": "article",
            "slides": [
                {"type": "claim", "frametitle": "The claim", "claim": "AI changes participation.", "evidence": ["Spreads rise"], "takeaway": "Market viability matters.", "speakerNotes": "Explain the mechanism."},
                {"type": "equation", "frametitle": "The fixed point", "equation": "s = Phi(s; alpha)", "definitions": ["s is the spread"], "meaning": "Exit feeds back into pricing."},
                {"type": "theorem", "frametitle": "Collapse threshold", "statement": "If alpha exceeds the threshold, no active equilibrium exists.", "intuition": "The minimum spread exceeds participation value."},
                {"type": "takeaway", "frametitle": "Bottom line", "takeaway": "Efficiency can undermine survival."},
            ],
        }
        output = MODULE.build(data, str(ROOT / "beamer-progress-draft" / "templates"))
        self.assertIn("AI changes participation.", output)
        self.assertIn("s = Phi(s; alpha)", output)
        self.assertIn("Collapse threshold", output)
        self.assertIn("Efficiency can undermine survival.", output)

    def test_article_quality_warning_flags_bullet_only_deck(self):
        data = {"mode": "article", "slides": [{"type": "itemize", "frametitle": "Only bullets", "items": ["One"]}]}
        stream = io.StringIO()
        with redirect_stdout(stream):
            MODULE.build(data, str(ROOT / "beamer-progress-draft" / "templates"))
        self.assertIn("article deck", stream.getvalue())

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
