# Verify TikZ Layout Validation

Validation was performed on 2026-07-18 on Windows in the repository checkout. Build artifacts remain under the ignored `tests/verify-tikz-layout/.artifacts/` directory and are not committed.

## Runtime

- Python: 3.12.13
- LaTeX: TeX Live 2024, pdfTeX 1.40.26
- Build driver: latexmk 4.85
- Renderer used: TeX Live `pdftoppm.exe` 24.03.0
- Skill validator: `quick_validate.py`, with `PYTHONUTF8=1`

The bundled LaTeX doctor timed out after 64 seconds, so availability was confirmed directly. The bundled `pdftoppm.cmd` wrapper returned exit code 3 because its delegated path failed; direct `pdftoppm.exe` worked. A regression test was added and the helper now prefers native `.exe` renderers before command wrappers on Windows.

## Automated behavior

Command:

```powershell
& 'C:\Users\HKUBS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests/verify-tikz-layout -p 'test_*.py' -v
```

Result: 15 tests passed. The controlled missing-renderer test returned `VISUAL_VERIFICATION_UNAVAILABLE`, and `VISUALLY_VERIFIED` is absent from `ALLOWED_PREPARATION_STATUSES`. Regression tests also prove that stale PDFs and PNGs cannot satisfy a later run and that each manifest records its repair iteration plus page/figure/frame/overlay mappings.

## Skill pressure tests

Three baseline agents were tested without the skill. Under deadline and user pressure, two incorrectly accepted compile-only or isolated-only work as done; the Beamer agent correctly withheld completion. The skill added explicit counters for compile-only, isolated-only, final-overlay-only, deadline, and user-accepted-risk rationalizations.

The same three scenarios were rerun with the skill. All three withheld `VISUALLY_VERIFIED` until the required images were inspected. The missing-renderer scenario used the exact status `COMPILED — VISUAL VERIFICATION UNAVAILABLE`; the paper scenario required the rendered paper page; the Beamer scenario required all overlays.

## Visual render-inspect-repair evidence

### Standalone figure

- Initial image opened: `.artifacts/standalone/target-page-1.png`
- Defects observed: both nodes occupied the same region; node text and borders overlapped; the arrow and `effect` label crossed node content.
- Repair: replaced absolute coordinates with `right=of`, set `text width`, `align`, and `inner sep`, used a 12 mm node gap, and drew the arrow from `.east` to `.west` after node layout.
- Final image opened: `.artifacts/standalone-fixed/target-page-1.png`
- Repair cycles: 1
- Final verdict: `VISUALLY_VERIFIED`; no overlaps, clipping, crowded text, or ambiguous routing.

### Two-column paper

- Initial page opened: `.artifacts/paper/target-page-1.png` (plus a 100 dpi full-page preview)
- Initial isolated image opened: `.artifacts/paper-isolated/target-page-1.png`
- Defects observed: the isolated horizontal chain was internally readable, but the paper page overflowed one column by 255.01926 pt and crossed into the neighboring column.
- First repair: narrowed three horizontal nodes. Its isolated render was opened and rejected because `Instrument` and `Endogenous exposure` crossed node borders; the log contained relevant overfull boxes.
- Second repair: changed to a vertical causal chain using `below=of`, 35 mm text widths, adaptive node heights, 12 mm boundary gaps, explicit `.south`/`.north` arrows, and side labels.
- Final isolated image opened: `.artifacts/paper-isolated-fixed/target-page-1.png`
- Final page opened: `.artifacts/paper-fixed/target-page-1.png` (plus a 100 dpi full-page preview)
- Repair cycles: 2
- Final verdict: `VISUALLY_VERIFIED`; the diagram fits one column, the final log has no relevant warnings, and the caption and surrounding page content remain clear.

### Beamer overlays

- Initial images opened: `.artifacts/beamer/target-page-1.png` and `.artifacts/beamer/target-page-2.png`
- Defects observed: overlay 1 crowded `changes` into node boundaries; overlay 2 additionally overlapped `Exposure` and `Behavioral response`.
- Repair: used relative right/below positioning, explicit 31 mm text widths and inner padding, a 16 mm horizontal gap, a 12 mm vertical gap, stable overlay space via `\uncover`, and an anchor-to-anchor arrow drawn after node placement.
- Final images opened: `.artifacts/beamer-fixed/target-page-1.png` and `.artifacts/beamer-fixed/target-page-2.png`
- Repair cycles: 1
- Final verdict: both overlays are `VISUALLY_VERIFIED`; no objects overlap, the reveal is stable, and all content remains within the frame-safe area.

## Final status

All corrected standalone, paper, and Beamer targets were compiled, rendered, opened, and inspected. The helper itself only reports `RENDERED_PENDING_REVIEW`; the visual verdicts above were awarded after image inspection.
