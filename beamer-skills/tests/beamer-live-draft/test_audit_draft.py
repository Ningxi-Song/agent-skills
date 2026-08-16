import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "beamer-live-draft" / "scripts" / "audit_draft.py"
MANIFEST_PATH = Path(__file__).parent / "fixtures" / "full-deck-manifest.json"


def load_module():
    spec = importlib.util.spec_from_file_location("beamer_live_audit", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matching_draft(manifest):
    slides = []
    for expected in manifest["slides"]:
        components = []
        for index, kind in enumerate(expected["components"]):
            component = {"id": f"{expected['id']}-c{index+1}", "type": kind}
            if kind in {"diagram", "flow"}:
                component.update(nodes=[], edges=[])
            elif kind == "table":
                component.update(headers=["A"], rows=[["1"]])
            elif kind == "figure":
                component.update(src="figure.png", fullPageRaster=False)
            elif kind == "formula":
                component.update(tex="x=1")
            else:
                component.update(items=["Point"])
            components.append(component)
        slides.append({"id": expected["id"], "frametitle": expected["title"], "components": components})
    return {"schemaVersion": 2, "slides": slides}


class FullDeckAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit_module = load_module()
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_matching_35_slide_deck_passes(self):
        report = self.audit_module.audit(self.manifest, matching_draft(self.manifest))
        self.assertTrue(report["ok"])
        self.assertEqual(report["slideCount"], 35)

    def test_detects_missing_slide_wrong_type_and_raster(self):
        draft = matching_draft(self.manifest)
        draft["slides"].pop()
        draft["slides"][1]["components"][0]["type"] = "rich-text"
        draft["slides"][5]["components"][0]["fullPageRaster"] = True
        report = self.audit_module.audit(self.manifest, draft)
        codes = {issue["code"] for issue in report["issues"]}
        self.assertTrue({"slide-count", "component-type", "full-page-raster"}.issubset(codes))

    def test_detects_renderer_layout_failures(self):
        draft = matching_draft(self.manifest)
        draft["slides"][3]["layoutChecks"] = {"titleWrap": True, "overflow": True}
        report = self.audit_module.audit(self.manifest, draft)
        self.assertEqual({"title-wrap", "overflow"}, {issue["code"] for issue in report["issues"]})


if __name__ == "__main__":
    unittest.main()
