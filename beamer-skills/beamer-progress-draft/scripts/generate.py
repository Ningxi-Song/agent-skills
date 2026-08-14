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


def notes_comment(slide):
    notes = slide.get("speakerNotes", "")
    return "% Speaker notes: " + latex_escape(notes) if notes else ""


def article_quality_warnings(data):
    if data.get("mode") != "article":
        return
    slides = data.get("slides", [])
    types = {slide.get("type") for slide in slides}
    if "claim" not in types:
        _warn("article deck needs a claim slide")
    if not ({"figure", "equation"} & types):
        _warn("article deck needs a figure or equation")
    if not ({"theorem", "takeaway"} & types):
        _warn("article deck needs a formal result or takeaway")
    if sum(slide.get("type") == "itemize" for slide in slides) > len(slides) / 2:
        _warn("article deck is mostly bullet-only; consider structured slide types")


def article_frame(slide, index):
    title = latex_escape(slide.get("frametitle", ""))
    slide_type = slide.get("type")
    if slide_type == "claim":
        body = [r"\textbf{%s}" % latex_escape(slide.get("claim", "")), items_list(slide.get("evidence", []))]
        if slide.get("takeaway"):
            body.append(r"\begin{block}{Takeaway}" + latex_escape(slide["takeaway"]) + r"\end{block}")
    elif slide_type == "equation":
        body = [r"\begin{equation*}" + latex_escape(slide.get("equation", "")) + r"\end{equation*}", items_list(slide.get("definitions", []))]
        if slide.get("meaning"):
            body.append(r"\textit{%s}" % latex_escape(slide["meaning"]))
    elif slide_type == "theorem":
        body = [r"\begin{block}{Result}" + latex_escape(slide.get("statement", "")) + r"\end{block}"]
        if slide.get("intuition"):
            body.append(r"\textit{Intuition:} " + latex_escape(slide["intuition"]))
    elif slide_type == "takeaway":
        body = [r"\begin{block}{Takeaway}" + latex_escape(slide.get("takeaway", "")) + r"\end{block}"]
    elif slide_type == "figure":
        body = [r"\begin{figure}\centering\includegraphics[width=0.86\textwidth]{%s}" % latex_escape(slide.get("src", ""))]
        if slide.get("caption"):
            body.append(r"\caption{%s}" % latex_escape(slide["caption"]))
        body.append(r"\end{figure}")
        if slide.get("takeaway"):
            body.append(r"\textit{%s}" % latex_escape(slide["takeaway"]))
    else:
        return ""
    notes = notes_comment(slide)
    return r"\begin{frame}{%s}" % title + "\n" + "\n".join(body) + ("\n" + notes if notes else "") + "\n" + r"\end{frame}"


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
    if slide_type in {"claim", "figure", "equation", "theorem", "takeaway"}:
        _title_warnings(slide, index)
        return article_frame(slide, index)
    _warn("unknown slide type '%s' on slide %d" % (slide_type, index))
    return ""


def build(data, template_dir):
    validate_data(data)
    article_quality_warnings(data)
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
