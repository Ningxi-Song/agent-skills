# Verify TikZ Layout Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Build, validate, install, and publish a reusable skill that compiles TikZ sources, renders all relevant outputs, requires actual image inspection, repairs layout defects iteratively, and never equates compilation with visual verification.

**Architecture:** A concise SKILL.md routes agents to shared acceptance criteria and context modules for standalone figures, papers, and Beamer. A Python standard-library helper performs deterministic context detection, compilation, log scanning, rendering, artifact naming, and manifest creation, but it cannot award a visual pass. Unit tests cover deterministic behavior; LaTeX fixtures and actual rendered-image inspection cover the visual workflow.

**Tech Stack:** Agent Skills Markdown/YAML, Python 3 standard library, unittest, LaTeX/TikZ, latexmk or Tectonic or a TeX engine, Poppler pdftoppm or MuPDF mutool, Git, Codex image inspection.

---

## Repository map

The repository stores category folders at its root. The canonical path is latex/verify-tikz-layout, not skills/latex/verify-tikz-layout.

**Create:**

- latex/verify-tikz-layout/SKILL.md — trigger, router, strict states, repair loop, and report contract.
- latex/verify-tikz-layout/agents/openai.yaml — Codex-facing metadata.
- latex/verify-tikz-layout/references/visual-acceptance.md — shared visual pass/fail checklist.
- latex/verify-tikz-layout/references/standalone-figures.md — standalone and bounding-box rules.
- latex/verify-tikz-layout/references/papers.md — isolated plus page-context rules.
- latex/verify-tikz-layout/references/beamer-slides.md — frame and overlay rules.
- latex/verify-tikz-layout/scripts/prepare_tikz_review.py — compile/render/manifest CLI.
- latex/verify-tikz-layout/assets/standalone-harness.tex — fragment wrapper.
- tests/verify-tikz-layout/test_prepare_tikz_review.py — unit and fail-closed tests.
- tests/verify-tikz-layout/fixtures/standalone-overlap.tex — broken standalone layout.
- tests/verify-tikz-layout/fixtures/paper-column-pressure.tex — paper overflow fixture.
- tests/verify-tikz-layout/fixtures/beamer-overlays.tex — overlay collision fixture.
- tests/verify-tikz-layout/VALIDATION.md — evidence-backed validation record.
- .gitignore — temporary render exclusions if absent.

**Modify:**

- README.md — correct the root layout and add the latex category.
- docs/superpowers/specs/2026-07-16-verify-tikz-layout-design.md — already corrected to the root-category convention.

## Task 1: Scaffold the skill and lock the behavioral contract

**Files:**

- Create: latex/verify-tikz-layout/SKILL.md
- Create: latex/verify-tikz-layout/agents/openai.yaml
- Create directories: latex/verify-tikz-layout/references, scripts, assets

- [ ] **Step 1: synchronize the checkout**

Run:

~~~powershell
git pull --ff-only origin main
~~~

Expected: the checkout includes the approved design specification and path correction with no merge commit.

- [ ] **Step 2: generate the standard skeleton**

Run:

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\HKUBS\.codex\skills\.system\skill-creator\scripts\init_skill.py' verify-tikz-layout --path latex --resources scripts,references,assets --interface display_name='Verify TikZ Layout' --interface short_description='Render, inspect, and repair TikZ layouts' --interface default_prompt='Use $verify-tikz-layout to compile, render, inspect, and repair this TikZ diagram.'
~~~

Expected: the skill directory, metadata file, and three resource directories are created.

- [ ] **Step 3: replace SKILL.md**

Write exactly:

~~~markdown
---
name: verify-tikz-layout
description: Verifies and repairs LaTeX TikZ layouts through a strict compile, render, inspect, and iterate loop. Use when creating or editing TikZ diagrams in standalone files, papers, or Beamer slides; when nodes, arrows, labels, panels, or overlays may overlap or clip; or before claiming that a TikZ visual is complete.
---

# Verify TikZ Layout

Compilation is not visual verification. Never claim a layout is verified until every required rendered image has been opened and inspected.

## Route the task

1. Locate the TeX entry point and affected TikZ source.
2. Classify each target as standalone, paper, or Beamer.
3. Read references/visual-acceptance.md.
4. Read every applicable context module:
   - references/standalone-figures.md
   - references/papers.md
   - references/beamer-slides.md

## Prepare rendered evidence

Run:

    python scripts/prepare_tikz_review.py SOURCE.tex --output-dir OUTPUT

Pass --context, --engine, or --pages when automatic discovery is insufficient. Inspect manifest.json and compile.log.

The helper may emit only:

- COMPILE_FAILED
- RENDER_FAILED
- RENDERED_PENDING_REVIEW
- VISUAL_VERIFICATION_UNAVAILABLE

It must never emit VISUALLY_VERIFIED.

## Mandatory visual gate

For every manifest image:

1. Open it with the available image-inspection tool.
2. Apply every check in references/visual-acceptance.md.
3. Record defects by object and location.
4. Edit layout without changing analytical meaning.
5. Recompile, rerender, and inspect again.

Inspect paper figures both in isolation and on the final page. Inspect every distinct Beamer overlay state.

Repeat for at most five repair cycles per target unless the user changes the limit. At the limit, stop and report remaining defects.

## Semantic preservation

You may change coordinates, anchors, node distances, text widths, bends, routes, layers, scaling, and margins. Do not remove or relabel nodes, relationships, arrows, panels, or substantive content merely to obtain a pass.

## Status language

Award VISUALLY VERIFIED only after personally opening and inspecting every required image.

If image inspection is unavailable, say exactly:

COMPILED — VISUAL VERIFICATION UNAVAILABLE

Then state that overlaps, clipping, or other layout defects may remain.

## Final report

Report context and files; pages, frames, and overlays inspected; repair-cycle count; remaining compiler warnings; final status; and unresolved defects with evidence paths.
~~~

- [ ] **Step 4: replace agents/openai.yaml**

~~~yaml
interface:
  display_name: "Verify TikZ Layout"
  short_description: "Render, inspect, and repair TikZ layouts"
  default_prompt: "Use $verify-tikz-layout to compile, render, inspect, and repair this TikZ diagram."

policy:
  allow_implicit_invocation: true
~~~

- [ ] **Step 5: validate and commit**

Run:

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\HKUBS\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'latex\verify-tikz-layout'
git add latex/verify-tikz-layout/SKILL.md latex/verify-tikz-layout/agents/openai.yaml
git commit -m "feat: define strict TikZ visual verification workflow"
~~~

Expected: validation succeeds, then one contract-only commit is created.

## Task 2: Write failing tests for deterministic preparation

**Files:**

- Create: tests/verify-tikz-layout/test_prepare_tikz_review.py
- Test: latex/verify-tikz-layout/scripts/prepare_tikz_review.py

- [ ] **Step 1: create the complete test module**

~~~python
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "latex" / "verify-tikz-layout" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import prepare_tikz_review as review


class ContextTests(unittest.TestCase):
    def test_contexts(self):
        cases = {
            r"\begin{tikzpicture}\node {A};\end{tikzpicture}": "standalone",
            r"\documentclass{standalone}\begin{document}x\end{document}": "standalone",
            r"\documentclass{article}\begin{document}x\end{document}": "paper",
            r"\documentclass[aspectratio=169]{beamer}\begin{document}x\end{document}": "beamer",
        }
        for text, expected in cases.items():
            with self.subTest(expected=expected):
                self.assertEqual(review.detect_context(text), expected)


class PageTests(unittest.TestCase):
    def test_ranges_expand_without_duplicates(self):
        self.assertEqual(review.parse_pages("1,3-5,4"), [1, 3, 4, 5])

    def test_descending_range_fails(self):
        with self.assertRaisesRegex(ValueError, "descending"):
            review.parse_pages("5-3")

    def test_zero_fails(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            review.parse_pages("0")


class CommandTests(unittest.TestCase):
    def test_pdflatex_command(self):
        command = review.build_compile_command(
            "C:/tex/pdflatex.exe", Path("paper.tex"), Path("out")
        )
        self.assertEqual(command[0], "C:/tex/pdflatex.exe")
        self.assertIn("-halt-on-error", command)
        self.assertIn("-output-directory=out", command)
        self.assertEqual(command[-1], "paper.tex")

    def test_selected_pages_create_distinct_commands(self):
        commands, expected = review.build_render_commands(
            "C:/poppler/pdftoppm.exe",
            Path("paper.pdf"),
            Path("render/target"),
            [1, 3],
            200,
        )
        self.assertEqual(len(commands), 2)
        self.assertEqual(
            expected,
            [Path("render/target-page-1.png"), Path("render/target-page-3.png")],
        )

    def test_actionable_log_scan(self):
        log = "Overfull \\hbox (12.0pt too wide)\nMissing character: There is no x\n"
        self.assertEqual(len(review.scan_log(log)), 2)


class FailClosedTests(unittest.TestCase):
    def test_script_cannot_award_visual_verification(self):
        self.assertNotIn("VISUALLY_VERIFIED", review.ALLOWED_PREPARATION_STATUSES)

    def test_missing_compiler_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "paper.tex"
            source.write_text(
                r"\documentclass{article}\begin{document}x\end{document}",
                encoding="utf-8",
            )
            manifest = review.prepare(
                source, root / "out", "auto", "auto", None, 200,
                which=lambda name: None,
            )
            self.assertEqual(manifest["status"], "COMPILE_FAILED")

    def test_missing_renderer_is_unverified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "paper.tex"
            source.write_text(
                r"\documentclass{article}\begin{document}x\end{document}",
                encoding="utf-8",
            )

            def fake_which(name):
                return "pdflatex" if name == "pdflatex" else None

            def fake_runner(command, **kwargs):
                output_arg = next(
                    item for item in command if item.startswith("-output-directory=")
                )
                output_dir = Path(output_arg.split("=", 1)[1])
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "paper.pdf").write_bytes(b"%PDF-1.4\n")
                return subprocess.CompletedProcess(command, 0, "compiled", "")

            manifest = review.prepare(
                source, root / "out", "auto", "auto", None, 200,
                which=fake_which,
                runner=fake_runner,
            )
            self.assertEqual(
                manifest["status"], "VISUAL_VERIFICATION_UNAVAILABLE"
            )


class SkillContractTests(unittest.TestCase):
    def test_required_wording(self):
        skill = (
            ROOT / "latex" / "verify-tikz-layout" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("COMPILED — VISUAL VERIFICATION UNAVAILABLE", skill)
        self.assertIn("It must never emit VISUALLY_VERIFIED", skill)


if __name__ == "__main__":
    unittest.main()
~~~

- [ ] **Step 2: confirm the tests fail because the helper is absent**

Run:

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests/verify-tikz-layout -p 'test_*.py' -v
~~~

Expected: FAIL with ModuleNotFoundError for prepare_tikz_review.

- [ ] **Step 3: commit the red tests**

~~~powershell
git add tests/verify-tikz-layout/test_prepare_tikz_review.py
git commit -m "test: define TikZ preparation and fail-closed behavior"
~~~

## Task 3: Implement the compile-render helper

**Files:**

- Create: latex/verify-tikz-layout/scripts/prepare_tikz_review.py
- Test: tests/verify-tikz-layout/test_prepare_tikz_review.py

- [ ] **Step 1: implement the helper**

~~~python
#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ALLOWED_PREPARATION_STATUSES = {
    "COMPILE_FAILED",
    "RENDER_FAILED",
    "RENDERED_PENDING_REVIEW",
    "VISUAL_VERIFICATION_UNAVAILABLE",
}
COMPILER_ORDER = ("latexmk", "tectonic", "pdflatex", "lualatex", "xelatex")
RENDERER_ORDER = ("pdftoppm", "mutool")
WARNING_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"overfull \\[hv]box",
        r"underfull \\[hv]box",
        r"missing character",
        r"undefined control sequence",
        r"undefined references?",
        r"font warning",
        r"tikz error",
    )
)


def detect_context(text):
    match = re.search(
        r"\\documentclass(?:\[[^\]]*\])?\{([^}]+)\}", text, re.IGNORECASE
    )
    if match:
        document_class = match.group(1).strip().lower()
        if document_class == "beamer":
            return "beamer"
        if document_class in {"standalone", "tikz"}:
            return "standalone"
        return "paper"
    if re.search(r"\\begin\{tikzpicture\}", text, re.IGNORECASE):
        return "standalone"
    return "paper"


def has_document(text):
    return bool(re.search(r"\\documentclass", text, re.IGNORECASE))


def parse_pages(value):
    if not value:
        return None
    pages = []
    for item in value.split(","):
        item = item.strip()
        if "-" in item:
            start, end = (int(part) for part in item.split("-", 1))
            if start < 1 or end < 1:
                raise ValueError("page numbers must be positive")
            if end < start:
                raise ValueError("descending page ranges are not allowed")
            candidates = range(start, end + 1)
        else:
            page = int(item)
            if page < 1:
                raise ValueError("page numbers must be positive")
            candidates = (page,)
        for page in candidates:
            if page not in pages:
                pages.append(page)
    return pages or None


def scan_log(text):
    return [
        line.strip()
        for line in text.splitlines()
        if any(pattern.search(line) for pattern in WARNING_PATTERNS)
    ]


def program_name(path):
    return Path(path).stem.lower()


def discover(requested, order, which):
    if requested != "auto":
        return which(requested)
    for name in order:
        found = which(name)
        if found:
            return found
    return None


def build_compile_command(compiler, source, output_dir):
    name = program_name(compiler)
    if name == "latexmk":
        return [
            compiler, "-pdf", "-interaction=nonstopmode", "-halt-on-error",
            f"-outdir={output_dir}", source.name,
        ]
    if name == "tectonic":
        return [compiler, "--keep-logs", "--outdir", str(output_dir), source.name]
    return [
        compiler, "-interaction=nonstopmode", "-halt-on-error",
        f"-output-directory={output_dir}", source.name,
    ]


def build_render_commands(renderer, pdf, prefix, pages, dpi):
    name = program_name(renderer)
    if name == "pdftoppm":
        if pages:
            commands, expected = [], []
            for page in pages:
                page_prefix = Path(f"{prefix}-page-{page}")
                commands.append([
                    renderer, "-png", "-r", str(dpi), "-f", str(page),
                    "-l", str(page), "-singlefile", str(pdf), str(page_prefix),
                ])
                expected.append(Path(f"{page_prefix}.png"))
            return commands, expected
        return [[renderer, "-png", "-r", str(dpi), str(pdf), f"{prefix}-page"]], []

    if pages:
        commands, expected = [], []
        for page in pages:
            output = Path(f"{prefix}-page-{page}.png")
            commands.append([
                renderer, "draw", "-r", str(dpi), "-o", str(output),
                str(pdf), str(page),
            ])
            expected.append(output)
        return commands, expected
    return [[
        renderer, "draw", "-r", str(dpi), "-o",
        f"{prefix}-page-%03d.png", str(pdf),
    ]], []


def write_manifest(output_dir, manifest):
    path = output_dir / "manifest.json"
    path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    manifest["manifest_path"] = str(path.resolve())
    return manifest


def write_harness(fragment, output_dir):
    template = (
        Path(__file__).resolve().parents[1] / "assets" / "standalone-harness.tex"
    ).read_text(encoding="utf-8")
    harness = output_dir / "standalone-harness.tex"
    harness.write_text(
        template.replace("@@TIKZ_SOURCE@@", fragment.resolve().as_posix()),
        encoding="utf-8",
    )
    return harness


def prepare(
    source,
    output_dir,
    requested_context,
    requested_engine,
    pages,
    dpi,
    which=None,
    runner=None,
):
    which = which or shutil.which
    runner = runner or subprocess.run
    source = Path(source).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    context = detect_context(text) if requested_context == "auto" else requested_context

    compile_source, compile_cwd = source, source.parent
    if context == "standalone" and not has_document(text):
        compile_source = write_harness(source, output_dir)
        compile_cwd = output_dir

    manifest = {
        "source": str(source),
        "compile_source": str(compile_source),
        "context": context,
        "requested_pages": pages,
        "dpi": dpi,
        "status": "COMPILE_FAILED",
        "compiler": None,
        "renderer": None,
        "compile_command": None,
        "render_commands": [],
        "warnings": [],
        "images": [],
        "error": None,
    }

    compiler = discover(requested_engine, COMPILER_ORDER, which)
    if not compiler:
        manifest["error"] = "No supported LaTeX compiler was found."
        return write_manifest(output_dir, manifest)

    manifest["compiler"] = compiler
    command = build_compile_command(compiler, compile_source, output_dir)
    manifest["compile_command"] = command
    completed = runner(
        command, cwd=str(compile_cwd), capture_output=True, text=True, check=False
    )
    log = (completed.stdout or "") + "\n" + (completed.stderr or "")
    (output_dir / "compile.log").write_text(log, encoding="utf-8")
    manifest["warnings"] = scan_log(log)

    pdf = output_dir / f"{compile_source.stem}.pdf"
    if completed.returncode != 0 or not pdf.exists():
        manifest["error"] = (
            f"LaTeX compilation failed with return code {completed.returncode}."
        )
        return write_manifest(output_dir, manifest)

    renderer = discover("auto", RENDERER_ORDER, which)
    if not renderer:
        manifest["status"] = "VISUAL_VERIFICATION_UNAVAILABLE"
        manifest["error"] = (
            "Compilation succeeded, but no supported PDF renderer was found."
        )
        return write_manifest(output_dir, manifest)

    manifest["renderer"] = renderer
    commands, expected = build_render_commands(
        renderer, pdf, output_dir / "target", pages, dpi
    )
    manifest["render_commands"] = commands
    for render_command in commands:
        rendered = runner(
            render_command,
            cwd=str(output_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if rendered.returncode != 0:
            manifest["status"] = "RENDER_FAILED"
            manifest["error"] = (
                f"PDF rendering failed with return code {rendered.returncode}."
            )
            return write_manifest(output_dir, manifest)

    images = expected or sorted(output_dir.glob("target-page*.png"))
    images = [path for path in images if path.exists()]
    if not images:
        manifest["status"] = "RENDER_FAILED"
        manifest["error"] = "The renderer produced no PNG files."
        return write_manifest(output_dir, manifest)

    manifest["images"] = [str(path.resolve()) for path in images]
    manifest["status"] = "RENDERED_PENDING_REVIEW"
    return write_manifest(output_dir, manifest)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Compile and render TikZ evidence for mandatory inspection."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--context",
        choices=("auto", "standalone", "paper", "beamer"),
        default="auto",
    )
    parser.add_argument("--engine", default="auto")
    parser.add_argument("--pages", type=parse_pages)
    parser.add_argument("--dpi", type=int, default=200)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.dpi < 72:
        raise SystemExit("--dpi must be at least 72")
    manifest = prepare(
        args.source, args.output_dir, args.context, args.engine, args.pages, args.dpi
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0 if manifest["status"] == "RENDERED_PENDING_REVIEW" else 1


if __name__ == "__main__":
    sys.exit(main())
~~~

- [ ] **Step 2: run tests, syntax check, and CLI help**

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests/verify-tikz-layout -p 'test_*.py' -v
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m py_compile latex/verify-tikz-layout/scripts/prepare_tikz_review.py
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' latex/verify-tikz-layout/scripts/prepare_tikz_review.py --help
~~~

Expected: all tests pass; syntax compilation is silent; help lists context, engine, pages, dpi, and output-dir.

- [ ] **Step 3: commit**

~~~powershell
git add latex/verify-tikz-layout/scripts/prepare_tikz_review.py
git commit -m "feat: prepare rendered TikZ evidence"
~~~

## Task 4: Add modular verification guidance

**Files:**

- Create: latex/verify-tikz-layout/references/visual-acceptance.md
- Create: latex/verify-tikz-layout/references/standalone-figures.md
- Create: latex/verify-tikz-layout/references/papers.md
- Create: latex/verify-tikz-layout/references/beamer-slides.md

- [ ] **Step 1: create visual-acceptance.md**

~~~markdown
# Visual Acceptance Criteria

Inspect every required image at readable zoom. Logs and manifests cannot substitute for inspection.

A target fails for node, label, panel, legend, caption, or annotation overlap; arrows crossing text or unintended objects; hidden arrowheads; clipping; unreadable or cramped text; ambiguous routing; unclear hierarchy; visibly inconsistent scaling or typography; or any required page, frame, or overlay not inspected.

Repair in this order: clipping, semantic ambiguity, overlaps, readability, then alignment and balance. Prefer relative positioning, anchors, text width, node distance, and routed bends over unexplained coordinate nudges.

Record VISUALLY VERIFIED only after every required image passes. Automated checks may reject but cannot award a pass.
~~~

- [ ] **Step 2: create standalone-figures.md**

~~~markdown
# Standalone TikZ Figures

Use the bundled harness for fragments. Inspect the entire bounding box, external margins, cropping, internal spacing, alignment, arrows, and labels at intended output size. Reject excess whitespace and elements touching crop boundaries. Rerender the whole figure after each repair.

A standalone pass does not cover paper or slide placement; load the other module when the figure is embedded.
~~~

- [ ] **Step 3: create papers.md**

~~~markdown
# Papers and Articles

A paper figure requires isolated and page-context evidence. Render the diagram alone, compile the real paper, and inspect every page containing it. Check column width, page boundaries, float placement, captions, notes, surrounding text, and final-size typography. Treat visible margin intrusion and relevant overfull boxes as blocking. Rerun multipass compilation when placement depends on references.

Never award a paper-context pass from the isolated rendering alone.
~~~

- [ ] **Step 4: create beamer-slides.md**

~~~markdown
# Beamer Slides

Compile the real Beamer entry point and map every affected frame and distinct overlay to PDF pages. Inspect all mapped pages. Check title and footer regions, frame-safe margins, projected readability, balance, and collisions between newly revealed and persistent content. Reject global shrinking when spacing or slide decomposition is the real problem. Reinspect every overlay after each repair.

Passing only the final overlay is insufficient.
~~~

- [ ] **Step 5: commit**

~~~powershell
git add latex/verify-tikz-layout/references
git commit -m "docs: add context-specific TikZ visual checks"
~~~

## Task 5: Add harness and adversarial fixtures

**Files:**

- Create: latex/verify-tikz-layout/assets/standalone-harness.tex
- Create: tests/verify-tikz-layout/fixtures/standalone-overlap.tex
- Create: tests/verify-tikz-layout/fixtures/paper-column-pressure.tex
- Create: tests/verify-tikz-layout/fixtures/beamer-overlays.tex

- [ ] **Step 1: create standalone-harness.tex**

~~~latex
\documentclass[tikz,border=8pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,backgrounds,calc,fit,positioning,shapes.geometric}
\begin{document}
\input{@@TIKZ_SOURCE@@}
\end{document}
~~~

- [ ] **Step 2: create standalone-overlap.tex**

~~~latex
\begin{tikzpicture}[
  box/.style={draw, rounded corners, minimum width=30mm, minimum height=10mm},
  >=Latex
]
\node[box] (cause) at (0,0) {Weather shock};
\node[box] (outcome) at (0.4,0) {Outcome response};
\draw[->] (cause) -- node[above] {effect} (outcome);
\end{tikzpicture}
~~~

Expected defect: two wide nodes occupy nearly the same coordinates and obscure the arrow label.

- [ ] **Step 3: create paper-column-pressure.tex**

~~~latex
\documentclass[twocolumn]{article}
\usepackage[margin=1in]{geometry}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
\begin{document}
\section{Mechanism}
The figure is deliberately wider than one column.
\begin{figure}[ht]
\centering
\begin{tikzpicture}[
  box/.style={draw, rounded corners, minimum width=38mm, minimum height=10mm},
  node distance=28mm,
  >=Latex
]
\node[box] (a) {Instrument};
\node[box, right=of a] (b) {Endogenous exposure};
\node[box, right=of b] (c) {Outcome};
\draw[->] (a) -- node[above] {first stage} (b);
\draw[->] (b) -- node[above] {causal effect} (c);
\end{tikzpicture}
\caption{A diagram that fits poorly in one column.}
\end{figure}
\end{document}
~~~

Expected defect: understandable internal order but visible one-column overflow.

- [ ] **Step 4: create beamer-overlays.tex**

~~~latex
\documentclass[aspectratio=169]{beamer}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
\begin{document}
\begin{frame}{Overlay states must each remain readable}
\centering
\begin{tikzpicture}[
  box/.style={draw, rounded corners, minimum width=34mm, minimum height=10mm},
  >=Latex
]
\node[box] (shock) at (-3,0) {Weather shock};
\only<1>{\node[box] (exposure) at (1,0) {Exposure};}
\only<2>{%
  \node[box] (exposure) at (1,0) {Exposure};
  \node[box] (mechanism) at (1.2,0) {Behavioral response};
}
\draw[->] (shock) -- node[above] {changes} (exposure);
\end{tikzpicture}
\end{frame}
\end{document}
~~~

Expected defect: overlay 1 is readable; overlay 2 has overlapping nodes.

- [ ] **Step 5: test and commit**

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests/verify-tikz-layout -p 'test_*.py' -v
git add latex/verify-tikz-layout/assets tests/verify-tikz-layout/fixtures
git commit -m "test: add adversarial TikZ layout fixtures"
~~~

Expected: tests pass before the fixture commit.

## Task 6: Run real render-inspect-repair validation

**Files:**

- Create: tests/verify-tikz-layout/VALIDATION.md
- Generate temporarily: tests/verify-tikz-layout/.artifacts
- Modify temporarily: work copies under .artifacts/work
- Create or modify: .gitignore

- [ ] **Step 1: diagnose the runtime**

Use the latex-doctor skill to find Tectonic, TeX Live, or MacTeX and run its smoke test. Run:

~~~powershell
Get-Command pdftoppm, mutool -ErrorAction SilentlyContinue
~~~

Expected: at least one compiler and renderer. If unavailable, record VISUAL_VERIFICATION_UNAVAILABLE and do not claim a pass.

- [ ] **Step 2: render and inspect standalone evidence**

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' latex/verify-tikz-layout/scripts/prepare_tikz_review.py tests/verify-tikz-layout/fixtures/standalone-overlap.tex --context standalone --output-dir tests/verify-tikz-layout/.artifacts/standalone
~~~

Expected: RENDERED_PENDING_REVIEW and PNG evidence. Open every PNG. Record the node and label collision. Repair a work copy with relative positioning, rerun, and inspect again. Pass only after the corrected image has no blocking defect.

- [ ] **Step 3: render and inspect the paper**

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' latex/verify-tikz-layout/scripts/prepare_tikz_review.py tests/verify-tikz-layout/fixtures/paper-column-pressure.tex --context paper --output-dir tests/verify-tikz-layout/.artifacts/paper
~~~

Expected: paper-page PNG evidence. Open every page, confirm the one-column failure, repair a work copy without deleting content, and inspect both isolated geometry and final page after rerendering.

- [ ] **Step 4: render and inspect every Beamer overlay**

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' latex/verify-tikz-layout/scripts/prepare_tikz_review.py tests/verify-tikz-layout/fixtures/beamer-overlays.tex --context beamer --output-dir tests/verify-tikz-layout/.artifacts/beamer
~~~

Expected: at least two PNGs. Open both, verify overlay 1 is readable and overlay 2 fails, repair a work copy, then rerender and inspect both again.

- [ ] **Step 5: verify fail-closed behavior**

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests/verify-tikz-layout -p 'test_*.py' -v
~~~

Expected: the missing-renderer case yields VISUAL_VERIFICATION_UNAVAILABLE and no allowed preparation state includes VISUALLY_VERIFIED.

- [ ] **Step 6: write VALIDATION.md**

Record exact tool versions, commands, statuses, images opened, defects seen, repairs applied to work copies, post-repair verdicts, and the missing-renderer result. Do not record PASS for an image that was not opened in this execution.

- [ ] **Step 7: exclude temporary artifacts**

Create .gitignore if absent, or append only missing lines:

~~~gitignore
tests/verify-tikz-layout/.artifacts/
__pycache__/
*.pyc
~~~

- [ ] **Step 8: commit evidence, not build artifacts**

~~~powershell
git add tests/verify-tikz-layout/VALIDATION.md .gitignore
git commit -m "test: validate TikZ render and inspection workflow"
~~~

Expected: .artifacts remains untracked and uncommitted.

## Task 7: Correct and extend README

**Files:**

- Modify: README.md
- Verify: docs/superpowers/specs/2026-07-16-verify-tikz-layout-design.md

- [ ] **Step 1: correct the structure tree**

Remove the misleading top-level skills wrapper. Add:

~~~text
latex/                    LaTeX visual verification
└── verify-tikz-layout
~~~

beside economics, engineering, planning, and meta.

- [ ] **Step 2: add the catalog entry**

~~~markdown
### latex/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| **verify-tikz-layout** | Compile, render, visually inspect, and iteratively repair TikZ diagrams in standalone files, papers, and Beamer; compilation alone never counts as visual verification | Willie Song |
~~~

- [ ] **Step 3: document personal Codex installation**

Add that latex/verify-tikz-layout should be copied to:

~~~text
%USERPROFILE%\.codex\skills\verify-tikz-layout
~~~

- [ ] **Step 4: verify paths and commit**

~~~powershell
rg -n 'skills/latex|agent-skills/skills/latex' README.md docs/superpowers/specs/2026-07-16-verify-tikz-layout-design.md
rg -n 'latex/verify-tikz-layout|VISUAL VERIFICATION UNAVAILABLE' README.md docs/superpowers/specs/2026-07-16-verify-tikz-layout-design.md latex/verify-tikz-layout
git add README.md
git commit -m "docs: publish TikZ verification skill"
~~~

Expected: the first search has no matches; the second finds the canonical path and strict wording; README matches the real repository.

## Task 8: Final validation, personal installation, and publication

**Files:**

- Validate: latex/verify-tikz-layout
- Install: C:/Users/HKUBS/.codex/skills/verify-tikz-layout
- Push: origin/main

- [ ] **Step 1: run structural validation**

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\HKUBS\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'latex\verify-tikz-layout'
~~~

Expected: skill is valid.

- [ ] **Step 2: run all automated tests**

~~~powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests/verify-tikz-layout -p 'test_*.py' -v
~~~

Expected: all tests pass.

- [ ] **Step 3: audit success-state language**

~~~powershell
rg -n 'VISUALLY_VERIFIED|VISUAL VERIFICATION UNAVAILABLE|RENDERED_PENDING_REVIEW' latex/verify-tikz-layout tests/verify-tikz-layout
~~~

Expected: VISUALLY_VERIFIED appears only in the agent-only gate or tests prohibiting script emission; the helper cannot award it.

- [ ] **Step 4: verify clean history**

~~~powershell
git status --short
git log --oneline -8
~~~

Expected: status is empty and commits appear in design, tests, implementation, validation, and documentation order.

- [ ] **Step 5: install the canonical folder personally**

After filesystem approval, copy latex/verify-tikz-layout recursively to:

~~~text
C:\Users\HKUBS\.codex\skills\verify-tikz-layout
~~~

If that exact destination already exists, remove only that destination before copying; do not alter other personal skills.

- [ ] **Step 6: prove installation identity**

Generate relative-path SHA-256 inventories for the canonical and personal folders and compare them. Expected: identical file lists and hashes. Run quick_validate.py on the personal folder and expect success.

- [ ] **Step 7: push validated commits to main**

~~~powershell
git push origin main
~~~

Expected: origin/main advances to the validated local commit.

- [ ] **Step 8: read back published content**

Fetch from main:

- latex/verify-tikz-layout/SKILL.md
- latex/verify-tikz-layout/scripts/prepare_tikz_review.py
- tests/verify-tikz-layout/VALIDATION.md
- README.md

Expected: GitHub returns the committed files and lists the latex category.

- [ ] **Step 9: final handoff**

Report the GitHub commit and canonical link, personal installation path, structural-validation result, automated-test count, figures/pages/frames/overlays actually inspected, unresolved runtime limitations, and the strict distinction between compilation and visual verification.
