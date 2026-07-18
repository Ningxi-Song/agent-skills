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
