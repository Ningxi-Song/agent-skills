---
name: beamer-live-draft
description: Use when visually drafting or editing Beamer decks in HTML, converting an existing PDF or TeX deck into an editable draft, or generating Beamer from a live draft.
---

# Beamer Live Draft

Use the bundled HTML editor as the visual drafting surface, then transpile its exported state into Beamer. The HTML is a structured editor, not a screenshot viewer: content remains editable through rich-text, diagram, formula, table, figure, and flow components.

This skill owns the editable preview-to-source pipeline. Use `beamer-format` for academic slide design rules and the PDF skill when source-page rendering or inspection is needed.

## Full-deck intake (mandatory)

When a PDF, TeX file, or existing slide deck is the source, inspect every source slide before presenting the draft. Do not stop after a representative sample.

Create a source manifest recording the complete slide count, order, titles, and expected component types. Classify each slide's meaningful content as title, rich text, diagram, formula, table, figure, or flow. Treat the manifest as the acceptance contract for the HTML draft.

Never silently degrade a diagram, formula, table, figure, or flow into generic bullet text. Recreate diagrams and flows with editable HTML/SVG structures, preserve formulas as editable math source, represent tables structurally, and use individual figure assets only when the source truly contains a figure. A full-page raster image is forbidden because it is not an editable slide implementation.

Review the complete draft against the source manifest yourself. Do not wait for the user to identify mismatches one slide at a time.

## Preserving user edits (mandatory)

The live state is the source of truth after the editor is opened. It uses a schema-versioned `localStorage` key based on the stable pathname, migrates legacy state, preserves unknown fields, and keeps a last-good snapshot.

Before changing an existing draft:

1. Capture the active editor state without reloading first.
2. Apply the requested change to that captured state. Preserve IDs, slide order, deleted content, component structure, theme, and active slide unless the user requests otherwise.
3. Let the editor save the revision. Export a JSON backup before replacing editor code.
4. After an editor update, test save, reload, and restore, including last-good recovery.

Never reconstruct an edited deck from the initial seed or original prompt. If live state is unavailable, restore the exported backup or last-good snapshot before considering reconstruction.

## Workflow

1. Copy `assets/beamer-draft.html` to a stable writable workspace path such as `beamer-draft.html`.
2. For an existing deck, complete the full-deck intake and source manifest first. For a new deck, define the intended outline and component types.
3. Seed every slide and meaningful component in the structured draft state.
4. Serve the workspace over local HTTP and open the editor in the preview panel.
5. Preserve live edits on every follow-up; do not rewrite the HTML merely to change slide contents.
6. Export or capture the current JSON state and run `scripts/generate.py`.
7. For an existing deck, run `scripts/audit_draft.py` against the source manifest.
8. Compile and visually inspect the generated Beamer output.

## Draft state

The state contains deck metadata and an ordered `slides` array. Slides contain typed, editable components with stable IDs. Preserve slide and component IDs across revisions so saved edits remain attached to the correct content.

Supported component types are:

- `rich-text`: headings, paragraphs, and lists
- `diagram`: editable nodes, edges, labels, and styles
- `formula`: editable LaTeX math source
- `table`: editable headers, rows, cells, and alignment
- `figure`: a real figure asset with editable caption and sizing
- `flow`: editable process nodes and connectors

Unknown fields must survive migration. Unknown component types must not be silently converted.

## Generation and audit

Generate Beamer source with:

```powershell
py scripts/generate.py draft.json --out slides.tex --compile
```

The generator maps structured components to native Beamer/LaTeX structures. Unsupported content must fail with its slide ID and component ID; it must not quietly substitute bullets.

Audit an existing-deck draft with:

```powershell
py scripts/audit_draft.py source-manifest.json draft.json
```

The audit compares full-deck count, order, titles, component types, forbidden full-page raster use, and recorded layout checks such as title wrapping, overflow, missing assets, and empty bodies.

Templates live in `templates/` and use `<<TITLEBLOCK>>` and `<<SLIDES>>`. See `references/templates.md` for the registry.

## Completion checklist

- Inspect every source slide and build a source manifest.
- Confirm count, order, titles, and component types match the source.
- Ensure every slide remains editable and no full-page raster is used.
- Ensure complex visuals are recreated structurally rather than degraded to bullets.
- Run `audit_draft.py` and resolve every reported fidelity or layout issue.
- Verify save, reload, and restore, including migration and last-good recovery.
- Generate `.tex`, compile when possible, and visually inspect the resulting deck.
