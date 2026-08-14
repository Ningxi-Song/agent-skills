import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
HTML = ROOT / "beamer-progress-draft" / "assets" / "progress-draft.html"
SKILL = ROOT / "beamer-progress-draft" / "SKILL.md"


class ArticleSlideContractTests(unittest.TestCase):
    def test_skill_documents_structured_article_mode(self):
        text = SKILL.read_text(encoding="utf-8")
        for marker in ("article mode", "claim", "equation", "theorem", "takeaway"):
            self.assertIn(marker, text.lower())

    def test_html_declares_structured_article_slide_types(self):
        text = HTML.read_text(encoding="utf-8")
        for slide_type in ("claim", "equation", "theorem", "figure", "takeaway"):
            self.assertRegex(text, rf'["\']{slide_type}["\']')

    def test_html_has_article_quality_checks_without_notes_panel(self):
        text = HTML.read_text(encoding="utf-8")
        self.assertIn("articleQuality", text)
        self.assertNotIn("notesEditor", text)

    def test_article_fixture_has_narrative_components(self):
        fixture = ROOT / "examples" / "ai-lemons-article-progress.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        types = {slide["type"] for slide in data["slides"]}
        self.assertTrue({"claim", "figure", "equation", "theorem", "takeaway"}.issubset(types))
        self.assertFalse(any("speakerNotes" in slide for slide in data["slides"]))


if __name__ == "__main__":
    unittest.main()
