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

    def test_declares_complex_component_renderers(self):
        for name in ("diagram", "formula", "table", "figure", "flow", "rich-text"):
            self.assertIn(f"'{name}'", self.text)
        self.assertIn("componentRenderers", self.text)

    def test_preserves_last_good_and_exports_backup(self):
        self.assertIn("last-good", self.text)
        self.assertIn("导出备份", self.text)

    def test_rejects_full_page_raster_substitution(self):
        self.assertIn("fullPageRaster", self.text)
        self.assertIn("Full-page raster slides are prohibited", self.text)

    def test_exposes_undo_history_and_keyboard_command(self):
        self.assertIn('id="undoDraft"', self.text)
        self.assertIn("function undoDraft()", self.text)
        self.assertIn("historyKey", self.text)
        self.assertIn("event.key.toLowerCase()==='z'", self.text)


if __name__ == "__main__":
    unittest.main()
