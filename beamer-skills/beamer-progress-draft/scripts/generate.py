#!/usr/bin/env python3
"""Convert a project-progress draft JSON file into Beamer source."""

import argparse
import json
import os
import shutil
import subprocess
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(HERE, "..", "templates"))
MAX_TITLE_CHARS = 70


def latex_escape(value):
    value = "" if value is None else str(value)
    value = value.replace("\\", r"\textbackslash{}")
    for char, replacement in [
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        value = value.replace(char, replacement)
    return value


def validate_data(data):
    if not isinstance(data, dict):
        raise ValueError("draft must be a JSON object")
    slides = data.get("slides")
    if not isinstance(slides, list):
        raise ValueError("draft must contain a slides list")
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            raise ValueError("slide %d must be an object" % index)
        if not slide.get("type"):
            raise ValueError("slide %d must have a type" % index)
    return data


def _warn(message):
    print("Warning: " + message)


def _title_warnings(slide, index):
    if not slide.get("frametitle", "").strip():
        _warn("slide %d has an empty title" % index)
    if len(slide.get("frametitle", "")) > MAX_TITLE_CHARS:
        _warn("slide %d title may wrap on one line" % index)


def titleblock(slides):
    first = next((slide for slide in slides if slide.get("type") == "title"), None)
    if not first:
        return ""
    lines = []
    if first.get("title"):
        lines.append(r"\title{%s}" % latex_escape(first["title"]))
    if first.get("subtitle"):
        lines.append(r"\subtitle{%s}" % latex_escape(first["subtitle"]))
    return "\n".join(lines)


def items_list(items):
    lines = [r"\begin{itemize}"]
    for item in items or []:
        lines.append(r"  \item " + latex_escape(item))
    lines.append(r"\end{itemize}")
    return "\n".join(lines)


def slide_to_frame(slide, index):
    slide_type = slide.get("type")
    if slide_type == "title":
        return r"\begin{frame}[plain]" + "\n\\titlepage\n" + r"\end{frame}"
    if slide_type == "itemize":
        _title_warnings(slide, index)
        items = slide.get("items") or []
        if len(items) > 5:
            _warn("slide %d has more than five bullets" % index)
        title = latex_escape(slide.get("frametitle", ""))
        return r"\begin{frame}{%s}" % title + "\n" + items_list(items) + "\n" + r"\end{frame}"
    _warn("unknown slide type '%s' on slide %d" % (slide_type, index))
    return ""


def build(data, template_dir):
    validate_data(data)
    template_key = data.get("template", "clean")
    template_path = os.path.join(template_dir, template_key + ".tex")
    if not os.path.exists(template_path):
        _warn("template '%s' not found; falling back to clean" % template_key)
        template_path = os.path.join(template_dir, "clean.tex")
    with open(template_path, encoding="utf-8") as handle:
        template = handle.read()
    frames = []
    for index, slide in enumerate(data["slides"], start=1):
        frame = slide_to_frame(slide, index)
        if frame:
            frames.append(frame)
    return template.replace("<<TITLEBLOCK>>", titleblock(data["slides"])).replace(
        "<<SLIDES>>", "\n\n".join(frames)
    )


def compile_tex(tex_path):
    for engine in ("pdflatex", "xelatex", "lualatex"):
        if not shutil.which(engine):
            continue
        try:
            for _ in range(2):
                subprocess.run(
                    [engine, "-interaction=nonstopmode", "-halt-on-error", tex_path],
                    cwd=os.path.dirname(os.path.abspath(tex_path)),
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            return engine, os.path.splitext(tex_path)[0] + ".pdf"
        except (OSError, subprocess.CalledProcessError):
            continue
    return None, None


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate Beamer source from a progress draft JSON file.")
    parser.add_argument("json", help="progress JSON exported from progress-draft.html")
    parser.add_argument("--out", default="slides.tex")
    parser.add_argument("--template-dir", default=TEMPLATE_DIR)
    parser.add_argument("--compile", action="store_true")
    args = parser.parse_args(argv)
    with open(args.json, encoding="utf-8") as handle:
        data = json.load(handle)
    output = build(data, args.template_dir)
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(output)
    print("Wrote", args.out)
    if args.compile:
        engine, pdf = compile_tex(args.out)
        if engine:
            print("Compiled with %s -> %s" % (engine, pdf))
        else:
            print("No LaTeX engine found; kept .tex only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
