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
   The user edits text **directly in the preview panel**, then exports the draft.
2. **Transpile** — the user returns the exported draft (JSON or HTML); the agent
   binds it to a Beamer template and generates a final `.tex` / `.pdf`.

It is a *visual scratchpad and translator*, not a replacement for
[beamer-format](../beamer-format/SKILL.md) — that skill owns the
content/design rules; this one owns the editable preview → source pipeline.

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
  (e.g. `./beamer-draft.html`) so the browser can save the exported file there,
  then opens it with `present_files` — this renders it in WorkBuddy's built-in
  browser preview panel (the right side).
- The page scales to fit the panel width and uses `contenteditable` regions for
  every text field, so the user edits in place (no code, no LaTeX).

### 3. Content-return interface 内容回传接口

The preview is a live browser, so the return path is **export-then-paste**
(not an auto-postback):

- The editor's **导出 JSON** button:
  - downloads `draft.json` next to the HTML, **and**
  - copies the same JSON to the clipboard.
  - The agent reads the returned JSON (pasted into chat, or from the saved
    `draft.json` file) — this is the preferred, structured form.
- **导出 HTML** copies the full rendered HTML (fallback if the user prefers to
  paste the page). The agent can parse title/frametitle/items out of the HTML
  if needed.
- **导入 JSON** re-loads a previously exported `draft.json` for further editing.

Agent-side rule: accept whichever the user returns. If they say "用刚导出的
draft.json 生成", read that file directly instead of asking them to paste.

### 4. Template binding & generation 模板绑定与生成流程

- Templates live in `templates/`, one full Beamer document per theme, each with
  two placeholders: `<<TITLEBLOCK>>` (filled from the first `title` slide) and
  `<<SLIDES>>` (all frames). Current keys: `clean` (Madrid), `metropolis`,
  `rochester`. See [references/templates.md](references/templates.md) for the
  registry and how to add a custom template.
- The editor's **theme selector** sets `template` in the exported JSON, binding
  the draft to a template key.
- `scripts/generate.py` does the transpile:

  ```bash
  python scripts/generate.py draft.json --out slides.tex --compile
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
   re-arranges slides. No agent action needed during this phase.
3. **Receive draft.** User clicks **导出 JSON** and pastes the JSON (or points
   you at the saved `draft.json`). If they pasted HTML instead, parse it.
4. **Transpile.** Run `scripts/generate.py <draft.json> --out slides.tex
   [--compile]`. If `--compile` is requested but no LaTeX engine exists, report
   the `.tex` path and the compile command.
5. **Deliver.** `present_files` the `.tex` (or `.pdf`). Optionally open
   [beamer-format](../beamer-format/SKILL.md) rules to sanity-check
   formatting (single-line frame titles, 3–5 bullets, no empty bottom).

### Tips for the agent

- Keep the editable HTML and the `draft.json` in the same folder so re-import
  works and the user can iterate.
- If the user wants a custom Beamer theme, add a `<key>.tex` to `templates/`
  (copy `clean.tex` as a base) and tell them to pick it in the selector.
- The JSON is the contract between draft and source — if the user only pastes
  partial text, ask for the full exported JSON to preserve slide order.
