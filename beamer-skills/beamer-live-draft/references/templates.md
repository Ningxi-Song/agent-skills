# Beamer Templates — Registry & Extension

The `beamer-live-draft` skill binds a draft JSON to a Beamer template by key.
Templates live in `templates/` next to this file.

## Placeholders

Every template is a **complete** Beamer document with exactly two placeholders
that `scripts/generate.py` replaces:

| Placeholder      | Replaced by                                                              |
|------------------|--------------------------------------------------------------------------|
| `<<TITLEBLOCK>>` | `\title{}` / `\subtitle{}` / `\author{}` / `\institute{}` / `\date{}` from the first `title` slide. Empty if there is no title slide. |
| `<<SLIDES>>`     | One `\begin{frame}...\end{frame}` per slide (title → `\titlepage`; itemize → `itemize`; columns → `columns`; block → `block`). |

Do **not** pre-fill these — the generator injects them. Keep everything else
(preamble, `\usetheme`, packages) in the template.

## Current registry

| Key        | Theme            | Notes                                  |
|------------|------------------|----------------------------------------|
| `clean`    | `Madrid` (14pt)  | Default. Balanced, safe for seminars.  |
| `metropolis` | `metropolis`   | Modern, minimal, sans-serif.           |
| `rochester` | `Rochester`    | Strong color sidebar, compact header.  |

The editor's theme selector lists these three. The `template` field in the
exported JSON must match one of these keys; unknown keys fall back to `clean`.

## Adding a custom template

1. Copy an existing template as a starting point:
   ```bash
   cp templates/clean.tex templates/mytheme.tex
   ```
2. Edit the preamble: set `\usetheme{...}`, add packages, fonts, colors.
   Keep `<<TITLEBLOCK>>` and `<<SLIDES>>` untouched.
3. (Optional) Register it in the editor's selector so users can pick it:
   open `assets/beamer-draft.html`, find the `<select id="theme">` block, and add
   `<option value="mytheme">主题: My Theme</option>`.
4. Tell the user to choose `mytheme` in the selector, or set `"template":"mytheme"`
   in the JSON before running `generate.py`.

## Compiling

`generate.py --compile` auto-detects `pdflatex`, then `xelatex`, then `lualatex`,
runs two passes, and writes `<name>.pdf` next to the `.tex`. With no engine
installed it keeps the `.tex` and prints the manual command, e.g.:

```bash
pdflatex slides.tex
```

For CJK decks, prefer `xelatex` with a CJK-aware preamble (add
`\usepackage{xeCJK}` and a CJK font in your custom template).
