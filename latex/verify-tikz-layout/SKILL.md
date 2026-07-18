---
name: verify-tikz-layout
description: Use when creating, editing, or reviewing LaTeX TikZ diagrams in standalone files, papers, or Beamer slides, especially before claiming completion or when nodes, arrows, labels, panels, pages, frames, or overlays may overlap, clip, crowd, or route ambiguously.
---

# Verify TikZ Layout

Compilation is not visual verification. Never claim a layout is complete or verified until every required rendered image has been opened and inspected.

## Route the task

1. Locate the TeX entry point and affected TikZ source.
2. Classify each target as standalone, paper, or Beamer.
3. Read `references/visual-acceptance.md`.
4. Read every applicable context module:
   - `references/standalone-figures.md`
   - `references/papers.md`
   - `references/beamer-slides.md`

## Prepare rendered evidence

Run:

    python scripts/prepare_tikz_review.py SOURCE.tex --output-dir OUTPUT

Pass `--context`, `--engine`, or `--pages` when automatic discovery is insufficient. Inspect `manifest.json` and `compile.log`.

The helper may emit only:

- `COMPILE_FAILED`
- `RENDER_FAILED`
- `RENDERED_PENDING_REVIEW`
- `VISUAL_VERIFICATION_UNAVAILABLE`

It must never emit `VISUALLY_VERIFIED`.

## Mandatory visual gate

For every manifest image:

1. Open it with the available image-inspection tool.
2. Apply every check in `references/visual-acceptance.md`.
3. Record defects by object and location.
4. Edit layout without changing analytical meaning.
5. Recompile, rerender, and inspect again.

Inspect paper figures both in isolation and on the final page. Inspect every distinct Beamer overlay state.

Repeat for at most five repair cycles per target unless the user changes the limit. At the limit, stop and report remaining defects.

## Semantic preservation

You may change coordinates, anchors, node distances, text widths, bends, routes, layers, scaling, and margins. Do not remove or relabel nodes, relationships, arrows, panels, or substantive content merely to obtain a pass.

## Status language

Award `VISUALLY_VERIFIED` only after personally opening and inspecting every required image.

Do not call a target complete under a compile-only, isolated-only, final-overlay-only, or similarly narrowed criterion. A user may reduce scope, but uninspected visual states remain unverified.

If image inspection is unavailable, say exactly:

`COMPILED — VISUAL VERIFICATION UNAVAILABLE`

Then state that overlaps, clipping, or other layout defects may remain.

## Red flags

- “Compilation is enough.”
- “The isolated figure probably fits the page.”
- “Only the final overlay matters.”
- “The deadline makes inspection optional.”
- “The user accepted the risk, so call it complete.”

All mean: report the verified evidence precisely and keep visual status unverified.

## Final report

Report context and files; pages, frames, and overlays inspected; repair-cycle count; remaining compiler warnings; final status; and unresolved defects with evidence paths.
