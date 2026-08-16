# Beamer Live Draft: Full-Deck Fidelity Upgrade

## Goal

Upgrade `beamer-live-draft` so an existing Beamer/PDF deck is reviewed and converted as a complete editable deck. Complex slides must not silently degrade to bullet lists or rasterized page screenshots.

## Scope

- Extend the draft schema with `diagram`, `formula`, `table`, `figure`, `flow`, and `rich-text` components.
- Render component text, table cells, and diagram node labels as editable HTML/SVG elements.
- Extend Beamer generation for every supported component; unsupported components fail explicitly.
- Add a full-deck audit covering page count, order, titles, component type, missing content, overflow, and raster-page substitution.
- Use the 35-slide `one_instrument_multiple_pathways` deck as the regression fixture.

## Preservation Contract

The live browser state remains authoritative after the editor first opens.

1. Use a stable deck identifier that does not change with URL query strings or cache-busting parameters.
2. Save after every content, layout, order, theme, and active-slide change.
3. Store a versioned schema and migrate snapshots without deleting unknown fields.
4. Before migration, copy the current snapshot to a `last-good` backup key.
5. Write and validate the migrated snapshot before replacing the active snapshot.
6. If migration or validation fails, retain the old snapshot, surface an error, and stop.
7. Never overwrite live state from the starter HTML or reconstruct it from the original prompt.
8. Keep a JSON backup/export path because clearing browser site data can remove `localStorage`.

## Architecture

### Draft schema

Each slide has a stable ID, title, layout, and ordered component list. Each component has a stable ID, type, editable content, and type-specific geometry or table data. Schema versions are explicit.

### Editor

The self-contained HTML editor uses a component registry. Each component supplies rendering, serialization, validation, and edit-event handling. HTML/SVG is used for editable diagrams; full-page PDF screenshots are forbidden as slide substitutes. Normal figure assets remain allowed.

### Generator

`generate.py` maps supported components to Beamer structures: TikZ for diagrams/flows, math environments for formulas, tabular environments for tables, and `includegraphics` for genuine figure assets. Unknown components produce a descriptive failure.

### Auditor

`audit_draft.py` compares a source manifest with the draft and reports per-slide PASS/FAIL for count, order, title, expected component class, missing elements, overflow indicators, and prohibited page-raster backgrounds.

## Failure Handling

- Missing source or unsupported source structure: report the affected slide; do not invent a bullet fallback.
- Autosave quota failure: preserve in-memory state and show a persistent warning with JSON export guidance.
- Migration failure: restore `last-good` and leave the original key untouched.
- Generation failure: identify slide/component IDs and stop without producing a misleading partial deck.

## Tests

1. Baseline pressure test: existing complex deck must expose the current bullet-degradation failure.
2. Schema round trip: edit, reorder, reload, and recover every component type.
3. Migration: upgrade an old four-type snapshot while preserving manual edits and unknown fields.
4. Full-deck regression: 35 pages, titles, order, and component classes match the fixture manifest.
5. Negative audit tests: missing page, wrong component, overflow marker, and full-page screenshot are detected.
6. Generator tests: every supported component emits valid Beamer; unsupported components fail explicitly.

## Completion Criteria

- Manual edits survive refresh, reopening, cache-busting query changes, and schema upgrade.
- All 35 regression slides pass the audit.
- No complex slide is silently converted to bullets or a raster page.
- The generated Beamer project compiles when a LaTeX engine is available.
