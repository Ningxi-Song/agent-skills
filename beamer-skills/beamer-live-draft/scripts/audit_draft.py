#!/usr/bin/env python3
"""Audit a live Beamer draft against a source-deck manifest."""

import argparse
import json
import sys


LAYOUT_CODES = {
    "titleWrap": "title-wrap",
    "overflow": "overflow",
    "missingAsset": "missing-asset",
    "emptyBody": "empty-body",
}


def issue(code, slide_id=None, detail=""):
    result = {"code": code, "detail": detail}
    if slide_id is not None:
        result["slideId"] = slide_id
    return result


def audit(manifest, draft):
    expected = manifest.get("slides", [])
    actual = draft.get("slides", [])
    issues = []
    if len(expected) != len(actual):
        issues.append(issue("slide-count", detail=f"expected {len(expected)}, found {len(actual)}"))

    for index, expected_slide in enumerate(expected):
        if index >= len(actual):
            issues.append(issue("missing-slide", expected_slide.get("id"), f"missing at position {index + 1}"))
            continue
        slide = actual[index]
        slide_id = slide.get("id", f"position-{index + 1}")
        if slide_id != expected_slide.get("id"):
            issues.append(issue("slide-order", slide_id, f"expected {expected_slide.get('id')} at position {index + 1}"))
        actual_title = slide.get("frametitle") or slide.get("title") or ""
        if actual_title != expected_slide.get("title", ""):
            issues.append(issue("slide-title", slide_id, f"expected {expected_slide.get('title')!r}, found {actual_title!r}"))
        actual_types = [component.get("type") for component in slide.get("components", [])]
        expected_types = expected_slide.get("components", [])
        if actual_types != expected_types:
            issues.append(issue("component-type", slide_id, f"expected {expected_types}, found {actual_types}"))
        for component in slide.get("components", []):
            if component.get("type") == "figure" and component.get("fullPageRaster"):
                issues.append(issue("full-page-raster", slide_id, f"component {component.get('id', '<missing>')} is a page raster"))
        for field, code in LAYOUT_CODES.items():
            if slide.get("layoutChecks", {}).get(field):
                issues.append(issue(code, slide_id, f"layout check {field} failed"))

    return {"ok": not issues, "slideCount": len(actual), "issues": issues}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit a Beamer live draft against a source manifest.")
    parser.add_argument("manifest")
    parser.add_argument("draft")
    args = parser.parse_args(argv)
    with open(args.manifest, encoding="utf-8") as handle:
        manifest = json.load(handle)
    with open(args.draft, encoding="utf-8") as handle:
        draft = json.load(handle)
    report = audit(manifest, draft)
    failed = {item.get("slideId") for item in report["issues"] if item.get("slideId")}
    for slide in manifest.get("slides", []):
        status = "FAIL" if slide.get("id") in failed else "PASS"
        print(f"{status} {slide.get('id')}: {slide.get('title')}")
    for item in report["issues"]:
        print(f"ISSUE {item['code']} {item.get('slideId', 'deck')}: {item['detail']}")
    print(f"SUMMARY {report['slideCount']}/{len(manifest.get('slides', []))} slides; {len(report['issues'])} issues")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
