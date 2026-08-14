---
name: beamer-progress-draft
description: Use when drafting project progress, research notes, or work-in-progress updates as editable Beamer-like slides before producing a formal presentation.
---

# Beamer Progress Draft

Use this skill for a slide-oriented project notebook. It provides a self-contained HTML editor whose slides map one-to-one to future Beamer frames.

## Article mode

Use `?article=1` or import an article JSON when turning a paper into a deck. Article mode is claim-driven rather than bullet-driven: each slide should have one audience-facing claim and may add a figure, equation, theorem, takeaway, and speaker notes.

Supported article slide types are `claim`, `figure`, `equation`, `theorem`, and `takeaway`, in addition to `title` and `itemize`. Build the narrative in this order when appropriate: motivation, headline finding, mechanism, model, equilibrium logic, main result, welfare or policy, empirical implications, conclusion, and appendix.

The visible slide is concise; `speakerNotes` stores the explanation that should not be placed on the slide. Do not turn every paper paragraph into bullets. Prefer a claim plus evidence, a diagram plus interpretation, or an equation plus economic meaning.

## Workflow

1. Open `assets/progress-draft.html` in a browser.
2. Edit the title and bullet slides directly.
3. Export the draft as `progress.json`.
4. Generate Beamer source:

   ```text
   python scripts/generate.py progress.json --out slides.tex
   python scripts/generate.py progress.json --out slides.tex --compile
   ```

5. Review the `.tex` or `.pdf` with the `beamer-format` rules before treating it as a formal deck.

## Supported content

- Title slides with title and subtitle.
- Title-plus-bullets slides.
- Structured article slides: claim, figure, equation, theorem, takeaway, and speaker notes.
- Add, delete, reorder, import, and export controls.
- `clean`, `metropolis`, and `rochester` templates.

The editor shows warnings for empty titles, more than five bullets, bullet-only article decks, and missing narrative components but does not block drafting. The generator preserves user wording and reports formatting risks; it does not invent evidence or guarantee publication-ready formatting.

## Boundaries

Use `beamer-live-draft` for general Beamer drafts with columns or blocks. Use `beamer-format` for academic content and layout rules. Use `verify-tikz-layout` only when TikZ figures are later added.
