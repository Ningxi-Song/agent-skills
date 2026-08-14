#!/usr/bin/env python3
"""Convert a Beamer draft JSON (exported from beamer-draft.html) into a
Beamer .tex file, optionally compiled to PDF.

Usage:
    python generate.py draft.json [--out slides.tex] [--template-dir DIR] [--compile]

The JSON shape produced by the editor:
    {
      "template": "clean" | "metropolis" | "rochester" | <key of a .tex in template-dir>,
      "slides": [
        {"type":"title", "title":..., "subtitle":..., "author":..., "institute":..., "date":...},
        {"type":"itemize", "frametitle":..., "items":[...]},
        {"type":"columns", "frametitle":..., "left":[...], "right":[...]},
        {"type":"block", "frametitle":..., "blocktitle":..., "body":...}
      ]
    }
"""
import argparse
import json
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(HERE, "..", "templates"))


def latex_escape(s):
    if s is None:
        s = ""
    s = str(s)
    s = s.replace("\\", r"\textbackslash{}")
    for ch, rep in [
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
        s = s.replace(ch, rep)
    return s


def titleblock(slides):
    first = next((s for s in slides if s.get("type") == "title"), None)
    if not first:
        return ""
    lines = []
    if first.get("title"):
        lines.append(r"\title{%s}" % latex_escape(first["title"]))
    if first.get("subtitle"):
        lines.append(r"\subtitle{%s}" % latex_escape(first["subtitle"]))
    if first.get("author"):
        lines.append(r"\author{%s}" % latex_escape(first["author"]))
    if first.get("institute"):
        lines.append(r"\institute{%s}" % latex_escape(first["institute"]))
    if first.get("date"):
        lines.append(r"\date{%s}" % latex_escape(first["date"]))
    return "\n".join(lines)


def items_list(arr):
    out = [r"\begin{itemize}"]
    for it in arr or []:
        out.append(r"  \item " + latex_escape(it))
    out.append(r"\end{itemize}")
    return "\n".join(out)


def slide_to_frame(s):
    t = s.get("type")
    if t == "title":
        return r"\begin{frame}[plain]" + "\n\\titlepage\n" + r"\end{frame}"
    ft = latex_escape(s.get("frametitle", ""))
    if t == "itemize":
        body = items_list(s.get("items"))
        return r"\begin{frame}{%s}" % ft + "\n" + body + "\n" + r"\end{frame}"
    if t == "columns":
        left = items_list(s.get("left"))
        right = items_list(s.get("right"))
        body = (
            r"\begin{columns}"
            + "\n"
            + r"\column{0.48\textwidth}"
            + "\n"
            + left
            + "\n"
            + r"\column{0.48\textwidth}"
            + "\n"
            + right
            + "\n"
            + r"\end{columns}"
        )
        return r"\begin{frame}{%s}" % ft + "\n" + body + "\n" + r"\end{frame}"
    if t == "block":
        bt = latex_escape(s.get("blocktitle", ""))
        bd = latex_escape(s.get("body", ""))
        body = r"\begin{block}{%s}" % bt + "\n" + bd + "\n" + r"\end{block}"
        return r"\begin{frame}{%s}" % ft + "\n" + body + "\n" + r"\end{frame}"
    return "% unknown slide type skipped: %s" % t


def build(data, template_dir):
    template_key = data.get("template", "clean")
    tpl_path = os.path.join(template_dir, template_key + ".tex")
    if not os.path.exists(tpl_path):
        print("Warning: template '%s' not found, falling back to clean." % template_key)
        tpl_path = os.path.join(template_dir, "clean.tex")
    with open(tpl_path, encoding="utf-8") as f:
        tpl = f.read()
    slides = data.get("slides", [])
    tb = titleblock(slides)
    frames = "\n\n".join(slide_to_frame(s) for s in slides)
    return tpl.replace("<<TITLEBLOCK>>", tb).replace("<<SLIDES>>", frames)


def compile_tex(tex_path):
    engines = ["pdflatex", "xelatex", "lualatex"]
    base = os.path.splitext(tex_path)[0]
    for eng in engines:
        if shutil.which(eng):
            try:
                subprocess.run(
                    [eng, "-interaction=nonstopmode", "-halt-on-error", tex_path],
                    cwd=os.path.dirname(tex_path),
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                # second pass for cross-references / TOC
                subprocess.run(
                    [eng, "-interaction=nonstopmode", "-halt-on-error", tex_path],
                    cwd=os.path.dirname(tex_path),
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                return eng, base + ".pdf"
            except (subprocess.CalledProcessError, OSError):
                continue
    return None, None


def main():
    ap = argparse.ArgumentParser(description="Generate Beamer .tex/PDF from a draft JSON.")
    ap.add_argument("json", help="draft.json exported from the Beamer draft editor")
    ap.add_argument("--out", default="slides.tex", help="output .tex path")
    ap.add_argument("--template-dir", default=None, help="directory with <key>.tex templates")
    ap.add_argument("--compile", action="store_true", help="try to compile to PDF")
    args = ap.parse_args()

    tdir = args.template_dir or TEMPLATE_DIR
    with open(args.json, encoding="utf-8") as f:
        data = json.load(f)

    tex = build(data, tdir)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(tex)
    print("Wrote", args.out)

    if args.compile:
        eng, pdf = compile_tex(args.out)
        if eng:
            print("Compiled with %s -> %s" % (eng, pdf))
        else:
            print(
                "No LaTeX engine found (pdflatex/xelatex/lualatex). "
                "Kept .tex only; compile manually, e.g. pdflatex %s" % args.out
            )


if __name__ == "__main__":
    main()
