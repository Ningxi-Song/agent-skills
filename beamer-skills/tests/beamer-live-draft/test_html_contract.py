import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "beamer-live-draft" / "assets" / "beamer-draft.html"


class LiveDraftAutosaveContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = HTML.read_text(encoding="utf-8")

    def test_autosaves_and_restores_live_state(self):
        self.assertIn("localStorage.setItem(storageKey", self.text)
        self.assertIn("localStorage.getItem(storageKey", self.text)
        self.assertIn("restore();", self.text)

    def test_omits_manual_json_controls(self):
        self.assertNotIn('id="exportJson"', self.text)
        self.assertNotIn('id="importJson"', self.text)
        self.assertNotIn('id="exportHtml"', self.text)


if __name__ == "__main__":
    unittest.main()
