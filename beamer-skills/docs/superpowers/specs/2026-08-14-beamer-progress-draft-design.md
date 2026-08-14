# Beamer Progress Draft Design Specification

## 1. Purpose

Add a standalone `beamer-progress-draft` skill for creating project-progress and research-note slides in an editable HTML preview, then converting the exported draft into a Beamer `.tex` file and optionally a PDF.

The feature is intentionally slide-oriented: every HTML slide maps to one future Beamer frame. It is a separate skill so it can evolve without coupling project-progress workflows to the existing general-purpose `beamer-live-draft` skill.

## 2. Goals

- Provide a new self-contained HTML editor for progress notes written as slides.
- Support title slides and title-plus-bullets slides only in the first version.
- Allow users to add, remove, reorder, and edit slides and bullet points directly in the browser.
- Export and import a structured JSON draft.
- Convert the JSON draft to Beamer source using the existing project conventions.
- Support the existing `clean`, `metropolis`, and `rochester` template styles.
- Leave the existing `beamer-live-draft` behavior unchanged.
- Make the handoff point explicit: content drafting happens in HTML; slide-format compliance is applied during Beamer generation.

## 3. Non-goals

- No hidden or non-exported private notes area.
- No columns, blocks, figures, tables, progress bars, or custom widgets in the first version.
- No automatic rewriting of research content.
- No guarantee that every draft satisfies the `beamer-format` rules; the generator should expose warnings and preserve content for user review.

## 4. User workflow

```text
Open progress-draft.html
  -> edit title and bullet slides
  -> export progress.json
  -> run the progress generator
  -> apply Beamer template and formatting checks
  -> write slides.tex
  -> optionally compile slides.pdf
```

The HTML editor is the source of truth during drafting. The JSON file is the stable handoff contract. The generated `.tex` is an output artifact and should not be edited as the primary draft.

## 5. Proposed module boundary

```text
beamer-progress-draft/
├── SKILL.md
├── assets/
│   └── progress-draft.html
├── references/
│   └── format-mapping.md
├── scripts/
│   └── generate.py
└── templates/
    ├── clean.tex
    ├── metropolis.tex
    └── rochester.tex
```

The new skill may reuse implementation ideas from `beamer-live-draft`, but its files should be independently usable and its trigger description should clearly identify project-progress or research-note slide drafting.

## 6. Draft JSON contract

The minimum contract is:

```json
{
  "version": 1,
  "template": "clean",
  "slides": [
    {
      "type": "title",
      "title": "Project progress",
      "subtitle": "Research workflow"
    },
    {
      "type": "itemize",
      "frametitle": "Data preparation is complete",
      "items": [
        "Merged the administrative and survey data",
        "Resolved duplicate observations",
        "Next: run the baseline specification"
      ]
    }
  ]
}
```

The generator must accept missing optional fields with safe defaults, preserve slide order, escape LaTeX special characters, and reject malformed top-level data with a clear error. Unknown slide types should produce a warning rather than silently disappearing.

## 7. HTML editor behavior

The editor should be dependency-free and self-contained, following the existing draft editor's browser-first pattern.

Required controls:

- Add title slide.
- Add bullet slide.
- Delete slide.
- Move slide up or down.
- Edit slide title and bullet text in place.
- Add and remove bullets.
- Import JSON.
- Export JSON.
- Select the Beamer template.

The visual layout should resemble a 16:9 Beamer deck and make slide boundaries obvious. The editor should show compact warnings when a slide has more than five bullets or an empty title, but it should not block export.

## 8. Generator behavior

`generate.py` should provide:

```text
python generate.py progress.json --out slides.tex
python generate.py progress.json --out slides.tex --compile
```

It should:

1. Load and validate the JSON contract.
2. Select the requested template, falling back to `clean` with a warning when needed.
3. Convert title slides to `\titlepage` frames and bullet slides to `itemize` frames.
4. Escape user text for LaTeX.
5. Emit format warnings for empty titles, more than five bullets, and multi-line-risky titles.
6. Optionally detect `pdflatex`, `xelatex`, or `lualatex` and compile the output.
7. Keep the `.tex` output even when compilation is unavailable or fails.

The generator does not perform semantic rewriting. It should preserve the user's wording and report formatting risks for later revision.

## 9. Integration with existing skills

- `beamer-live-draft` remains the general editable Beamer draft skill.
- `beamer-progress-draft` owns the project-progress slide workflow.
- `beamer-format` remains the authoritative source for academic slide design rules.
- `verify-tikz-layout` is not required for the first version because the new editor has no TikZ support, but it can be used later when figures are added.

The new skill documentation should explicitly direct agents to apply `beamer-format` rules during or after generation rather than treating the HTML preview as the final publication layout.

## 10. Testing and acceptance criteria

- JSON validation tests cover valid drafts, missing optional fields, malformed top-level data, unknown slide types, and LaTeX escaping.
- Generator tests confirm title and itemize conversion, template fallback, and warning behavior.
- A browser-facing smoke test or static inspection confirms the HTML asset contains the required editing and import/export controls.
- Existing tests remain unchanged in behavior.
- A sample JSON draft can generate a `.tex` file without a LaTeX installation.
- If a LaTeX compiler is available, the sample can compile to PDF; otherwise the generator reports the limitation without deleting `.tex`.

## 11. Open implementation constraint

The repository currently has a path mismatch in the TikZ tests: tests reference `latex/verify-tikz-layout`, while the checked-out skill is at top-level `verify-tikz-layout`. Fixing that mismatch is useful, but it is a separate maintenance change and should not be mixed into the first progress-draft implementation unless the tests must be run together.
