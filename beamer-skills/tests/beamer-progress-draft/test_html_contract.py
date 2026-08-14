import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "beamer-progress-draft" / "assets" / "progress-draft.html"


class ProgressDraftHtmlContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = HTML.read_text(encoding="utf-8")

    def test_is_self_contained(self):
        self.assertNotRegex(self.text, r"<(script|link)[^>]+https?://")

    def test_has_required_controls(self):
        for control_id in (
            "addTitle",
            "addItem",
            "deleteSlide",
            "moveUp",
            "moveDown",
            "exportJson",
            "importJson",
            "theme",
        ):
            self.assertIn('id="%s"' % control_id, self.text)

    def test_contains_json_round_trip_and_supported_slide_types(self):
        self.assertIn("JSON.stringify", self.text)
        self.assertIn("JSON.parse", self.text)
        self.assertIn('type:"title"', self.text)
        self.assertIn('type:"itemize"', self.text)
        self.assertIn('type:"image_grid"', self.text)
        self.assertIn("image-grid", self.text)
        self.assertIn("more than five bullets", self.text)


if __name__ == "__main__":
    unittest.main()
