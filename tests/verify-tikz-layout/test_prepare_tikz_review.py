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
    def test_renderer_discovery_prefers_executable_before_wrapper(self):
        paths = {
            "pdftoppm": "C:/runtime/pdftoppm.cmd",
            "pdftoppm.exe": "C:/texlive/pdftoppm.exe",
        }

        discovered = review.discover(
            "auto", review.RENDERER_ORDER, paths.get
        )

        self.assertEqual(discovered, "C:/texlive/pdftoppm.exe")

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

    def test_stale_pdf_cannot_satisfy_current_compile(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "paper.tex"
            output = root / "out"
            output.mkdir()
            source.write_text(
                r"\documentclass{article}\begin{document}x\end{document}",
                encoding="utf-8",
            )
            (output / "paper.pdf").write_bytes(b"stale")

            manifest = review.prepare(
                source, output, "paper", "auto", None, 200,
                which=lambda name: "pdflatex" if name == "pdflatex" else None,
                runner=lambda command, **kwargs: subprocess.CompletedProcess(
                    command, 0, "compiled without output", ""
                ),
            )

            self.assertEqual(manifest["status"], "COMPILE_FAILED")

    def test_stale_png_cannot_satisfy_current_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "paper.tex"
            output = root / "out"
            output.mkdir()
            source.write_text(
                r"\documentclass{article}\begin{document}x\end{document}",
                encoding="utf-8",
            )
            (output / "target-page-1.png").write_bytes(b"stale")

            def fake_which(name):
                return {"pdflatex": "pdflatex", "pdftoppm.exe": "pdftoppm.exe"}.get(name)

            def fake_runner(command, **kwargs):
                if command[0] == "pdflatex":
                    output_arg = next(
                        item for item in command if item.startswith("-output-directory=")
                    )
                    compile_output = Path(output_arg.split("=", 1)[1])
                    (compile_output / "paper.pdf").write_bytes(b"%PDF-current")
                return subprocess.CompletedProcess(command, 0, "ok", "")

            manifest = review.prepare(
                source, output, "paper", "auto", [1], 200,
                which=fake_which,
                runner=fake_runner,
            )

            self.assertEqual(manifest["status"], "RENDER_FAILED")

    def test_manifest_records_iteration_and_target_mapping(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "slides.tex"
            output = root / "out"
            source.write_text(
                r"\documentclass{beamer}\begin{document}x\end{document}",
                encoding="utf-8",
            )

            def fake_which(name):
                return {"pdflatex": "pdflatex", "pdftoppm.exe": "pdftoppm.exe"}.get(name)

            def fake_runner(command, **kwargs):
                if command[0] == "pdflatex":
                    output_arg = next(
                        item for item in command if item.startswith("-output-directory=")
                    )
                    compile_output = Path(output_arg.split("=", 1)[1])
                    compile_output.mkdir(parents=True, exist_ok=True)
                    (compile_output / "slides.pdf").write_bytes(b"%PDF-current")
                else:
                    prefix = Path(command[-1])
                    Path(f"{prefix}.png").write_bytes(b"png")
                return subprocess.CompletedProcess(command, 0, "ok", "")

            target_map = {3: {"figure": "causal-chain", "frame": 2, "overlay": 3}}
            manifest = review.prepare(
                source, output, "beamer", "auto", [3], 200,
                iteration=2,
                target_map=target_map,
                which=fake_which,
                runner=fake_runner,
            )

            self.assertEqual(manifest["iteration"], 2)
            self.assertEqual(
                manifest["rendered_targets"],
                [{
                    "path": str((output / "target-page-3.png").resolve()),
                    "page": 3,
                    "figure": "causal-chain",
                    "frame": 2,
                    "overlay": 3,
                }],
            )


class SkillContractTests(unittest.TestCase):
    def test_required_wording(self):
        skill = (
            ROOT / "latex" / "verify-tikz-layout" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("COMPILED — VISUAL VERIFICATION UNAVAILABLE", skill)
        self.assertIn("It must never emit `VISUALLY_VERIFIED`", skill)
        self.assertIn("at most five repair cycles", skill)


if __name__ == "__main__":
    unittest.main()
