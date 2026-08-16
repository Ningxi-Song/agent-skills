import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "beamer-live-draft" / "scripts" / "generate.py"
SPEC = importlib.util.spec_from_file_location("beamer_live_generate", MODULE_PATH)
generate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generate)


class ComponentGenerationTests(unittest.TestCase):
    def test_unknown_component_fails_with_ids(self):
        slide = {"id": "slide-2", "frametitle": "Bad", "components": [{"id": "c1", "type": "mystery"}]}
        with self.assertRaisesRegex(ValueError, "slide-2.*c1.*mystery"):
            generate.slide_to_frame(slide)

    def test_supported_components_emit_native_beamer(self):
        slide = {
            "id": "slide-2",
            "frametitle": "Native components",
            "components": [
                {"id": "r", "type": "rich-text", "items": ["Point"]},
                {"id": "m", "type": "formula", "tex": r"x=\beta z"},
                {"id": "t", "type": "table", "headers": ["A", "B"], "rows": [["1", "2"]]},
                {"id": "d", "type": "diagram", "nodes": [{"id": "z", "label": "Z", "x": 10, "y": 20}, {"id": "y", "label": "Y", "x": 70, "y": 20}], "edges": [{"from": "z", "to": "y"}]},
            ],
        }
        tex = generate.slide_to_frame(slide)
        self.assertIn(r"\begin{itemize}", tex)
        self.assertIn(r"\[", tex)
        self.assertIn(r"\begin{tabular}", tex)
        self.assertIn(r"\begin{tikzpicture}", tex)

    def test_full_page_raster_is_rejected(self):
        slide = {"id": "slide-3", "frametitle": "Raster", "components": [{"id": "f", "type": "figure", "src": "page.png", "fullPageRaster": True}]}
        with self.assertRaisesRegex(ValueError, "Full-page raster"):
            generate.slide_to_frame(slide)


if __name__ == "__main__":
    unittest.main()
