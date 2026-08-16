import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "beamer-live-draft" / "SKILL.md"


class SkillWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_requires_full_deck_review_before_conversion(self):
        self.assertIn("Full-deck intake", self.text)
        self.assertIn("inspect every source slide", self.text)
        self.assertIn("source manifest", self.text)

    def test_forbids_silent_degradation_and_page_screenshots(self):
        self.assertIn("Never silently degrade", self.text)
        self.assertIn("full-page raster", self.text)
        self.assertIn("Do not wait for the user to identify mismatches", self.text)

    def test_requires_completion_audit_and_restore_test(self):
        self.assertIn("audit_draft.py", self.text)
        self.assertIn("save, reload, and restore", self.text)
        self.assertIn("count, order, titles, and component types", self.text)


if __name__ == "__main__":
    unittest.main()
