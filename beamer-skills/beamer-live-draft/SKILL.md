---
name: beamer-live-draft
description: >
  Interactive Beamer draft editor + transpiler. When invoked, it renders a
  self-contained, Beamer-styled HTML preview in the right panel that the user
  edits directly (title/itemize/columns/block slides), then converts the
  returned draft into a real Beamer .tex (and optionally PDF) using a chosen
  template. Use when the user wants to "visually draft" slides, "edit a Beamer
  deck in HTML", "interactive beamer preview", "beamer 草稿", "beamer 可视化编辑",
  "beamer 中转", "slides editor", or "generate beamer from a draft".
---

# Beamer Live Draft — 可视化草稿编辑与中转

A skill that turns Beamer authoring into a two-step loop:

1. **Draft** — the agent emits a self-contained HTML editor that mimics a Beamer
   slide (16:9, color bar, frame title, itemize / two-column / block layouts).
   The user edits text **directly in the preview panel**; every change is saved
   automatically in that browser.
2. **Transpile** — the agent captures the current live state, binds it to a
   Beamer template, and generates a final `.tex` / `.pdf`.

It is a *visual scratchpad and translator*, not a replacement for
[beamer-format](../beamer-format/SKILL.md) — that skill owns the
content/design rules; this one owns the editable preview → source pipeline.

## Preserving user edits (mandatory)

The live editor's DOM and its URL-scoped `localStorage` snapshot are the source
of truth. The starter HTML file is **not** a source of truth after it has been
opened: it contains only the initial seed and writing it again can erase edits.

Before changing an existing draft, use this order:

1. Capture the active editor's current DOM/state in the existing browser
   session; do not reload it first.
2. Apply the requested change to that captured state only. Preserve slide
   order, deleted content, inline text, layout choices, theme, and the active
   slide unless the user asks to change them.
3. Let the editor persist the revised state automatically. Do not overwrite the
   editor HTML merely to update slide contents.

If the current state cannot be captured, stop and ask the user to reopen the
saved editor. Never reconstruct an existing deck from the original prompt,
cached seed, or the `let slides = [...]` initializer. In particular, do not
infer “second bullet” or “this slide” from the starter deck: resolve them from
the captured current order.

---

## Four design decisions (as requested)

### 1. Trigger 触发方式

The agent loads this skill when the user asks to draft/edit Beamer slides
visually or to turn an editable preview into a deck. Trigger phrases include:

- English: "beamer draft", "interactive beamer preview", "slides editor",
  "edit beamer in HTML", "generate beamer from a draft", "beamer transpiler"
- 中文: "beamer 草稿", "beamer 可视化编辑", "幻灯片草稿", "beamer 中转",
  "生成 beamer 预览", "把草稿变成 beamer"

On trigger, follow the **Workflow** below. Do not hand-write `.tex` for the
draft stage — the editor is the source of truth.

### 2. Right-panel rendering 右侧渲染区域

- The editor is a single self-contained file:
  `assets/beamer-draft.html` (inline CSS + JS, **no external dependencies**).
- The agent **copies** it to a writable location in the user's workspace
  (e.g. `./beamer-draft.html`) then opens it with `present_files` — this renders
  it in WorkBuddy's built-in
  browser preview panel (the right side).
- The page scales to fit the panel width and uses `contenteditable` regions for
  every text field, so the user edits in place (no code, no LaTeX).

### 3. Content-return interface 内容回传接口

The preview saves continuously in browser `localStorage`; it has no JSON
import/export controls. For a follow-up request, the agent reads the live
editor state from the existing browser session. For transpilation, the agent
may write a temporary JSON snapshot itself, but never asks the user to export,
paste, import, or manage JSON.

### 4. Template binding & generation 模板绑定与生成流程

- Templates live in `templates/`, one full Beamer document per theme, each with
  two placeholders: `<<TITLEBLOCK>>` (filled from the first `title` slide) and
  `<<SLIDES>>` (all frames). Current keys: `clean` (Madrid), `metropolis`,
  `rochester`. See [references/templates.md](references/templates.md) for the
  registry and how to add a custom template.
- The editor's **theme selector** saves the `template` key in the live snapshot.
- `scripts/generate.py` does the transpile:

  ```bash
  python scripts/generate.py snapshot.json --out slides.tex --compile
  ```

  It maps each slide type → Beamer frame (title→`\titlepage`, itemize→`itemize`,
  columns→`columns`, block→`block`), LaTeX-escapes all text, and (with
  `--compile`) auto-detects `pdflatex`/`xelatex`/`lualatex` and produces a PDF.
  If no engine is installed, it writes `.tex` only and tells the user to compile.
- The agent then `present_files` the resulting `slides.tex` (or `.pdf`).

---

## Workflow

1. **Kick off.** On trigger, tell the user you'll open an editable Beamer draft.
   Copy `assets/beamer-draft.html` into the workspace and `present_files` it.
   Seed a starter deck (title + itemize) by default; or ask the user for the
   topic / number of slides first if they gave none.
2. **User edits.** The user revises text in the right panel and (optionally)
   re-arranges slides. The live editor state now supersedes the initial HTML.
3. **Revise safely.** For every follow-up change, follow **Preserving user
   edits** above before editing any file.
4. **Transpile.** Capture the current state and write a temporary JSON snapshot
   for `scripts/generate.py`; do not disturb the saved live editor.
   Run `scripts/generate.py <snapshot.json> --out slides.tex
   [--compile]`. If `--compile` is requested but no LaTeX engine exists, report
   the `.tex` path and the compile command.
5. **Deliver.** `present_files` the `.tex` (or `.pdf`). Optionally open
   [beamer-format](../beamer-format/SKILL.md) rules to sanity-check
   formatting (single-line frame titles, 3–5 bullets, no empty bottom).

### Tips for the agent

- Keep the editable HTML at a stable local URL; the saved browser state is keyed
  to that URL.
- If the user wants a custom Beamer theme, add a `<key>.tex` to `templates/`
  (copy `clean.tex` as a base) and tell them to pick it in the selector.
- The live state is the contract between the draft and subsequent revisions.
