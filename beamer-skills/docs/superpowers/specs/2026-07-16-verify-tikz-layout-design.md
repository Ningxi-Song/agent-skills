# Verify TikZ Layout Skill — Design Specification

**Date:** 2026-07-16  
**Status:** Approved for implementation  
**Target repository:** `Ningxi-Song/agent-skills`  
**Skill name:** `verify-tikz-layout`

## 1. Purpose

LaTeX compilation proves syntactic validity, not visual correctness. A TikZ diagram may compile while nodes overlap, labels collide with arrows, content is clipped, or a figure fails in its paper or Beamer context. This skill establishes a strict render–inspect–repair workflow and prevents agents from claiming visual verification without inspecting rendered output.

The skill supports three contexts:

1. standalone TikZ figures;
2. TikZ diagrams embedded in full papers;
3. TikZ diagrams embedded in Beamer presentations, including overlays.

## 2. Goals

The skill must:

- identify the document context and load only the relevant instructions;
- compile the relevant source and retain diagnostic logs;
- render the target figure, page, frame, or overlay state to high-resolution images;
- require actual inspection of every rendered target;
- diagnose visual defects and iteratively repair the TikZ source;
- inspect embedded diagrams both in isolation and in their final document context;
- distinguish compilation success from visual-verification success;
- fail closed when rendering or image inspection is unavailable;
- preserve the semantic content of the diagram during layout repair;
- produce a concise, evidence-backed verification report.

## 3. Non-goals

The skill will not:

- treat successful compilation as proof of correct layout;
- rely solely on compiler warnings, image heuristics, or static TikZ parsing;
- remove nodes, relationships, labels, or substantive content merely to make a layout pass;
- guarantee aesthetic optimality when multiple defensible layouts exist;
- silently continue beyond its repair limit;
- claim that an uninspected image has passed visual review.

## 4. Architecture

The skill is a single modular package with one trigger and a shared verification core:

```text
latex/verify-tikz-layout/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── visual-acceptance.md
│   ├── standalone-figures.md
│   ├── papers.md
│   └── beamer-slides.md
├── scripts/
│   └── prepare_tikz_review.py
└── assets/
    └── standalone-harness.tex
```

`SKILL.md` acts as a router. It identifies the source context and directs the agent to read the shared visual criteria plus exactly one context module. If a task spans multiple contexts, the agent reads every applicable module.

The helper script handles deterministic preparation: tool discovery, compilation, log capture, PDF-to-image rendering, artifact naming, and manifest generation. Its name intentionally avoids implying that visual verification is automated. The script must never grant a visual-pass status.

## 5. State model and strict verification gate

Each target moves through explicit states:

```text
DISCOVERED
  ├─> COMPILE_FAILED
  └─> COMPILED
         ├─> RENDER_FAILED
         └─> RENDERED_PENDING_REVIEW
                ├─> VISUAL_DEFECTS
                │      └─> repair and repeat
                ├─> VISUAL_VERIFICATION_UNAVAILABLE
                └─> VISUALLY_VERIFIED
```

Only an agent that has actually opened and inspected every required rendered image may set `VISUALLY_VERIFIED`. Automated checks can block a pass, but they cannot independently award one.

If image inspection is unavailable, the terminal wording must be:

> COMPILED — VISUAL VERIFICATION UNAVAILABLE

The report must also state that overlaps or other layout defects may remain.

## 6. Core workflow

1. Discover the relevant TeX entry point, TikZ source, build instructions, output format, and affected pages or frames.
2. Classify the context as standalone, paper, Beamer, or mixed.
3. Read `visual-acceptance.md` and the applicable context module.
4. Compile using the project’s declared workflow when available; otherwise use a conservative detected engine.
5. Scan the log for TikZ errors, undefined references, missing fonts, clipping indicators, and overfull or underfull boxes.
6. Render every required target to high-resolution PNG images.
7. Open and visually inspect every rendered target.
8. Record defects precisely, including the affected node, label, arrow, panel, page, frame, or overlay.
9. Repair layout while preserving semantics.
10. Recompile, rerender, and reinspect.
11. Repeat until all acceptance checks pass or the repair limit is reached.
12. Produce the verification report with artifact paths and an honest terminal status.

The default repair limit is five cycles per target. A user may override it. At the limit, the skill stops, preserves the latest artifacts, and reports unresolved defects without claiming success.

## 7. Shared visual acceptance criteria

Every inspected target must be checked for:

- node–node, node–label, label–label, and panel overlap;
- arrows or connectors passing through text or unintended objects;
- arrowheads obscured by nodes or labels;
- clipped content or incorrect bounding boxes;
- unreadable text, cramped text blocks, or unsuitable scaling;
- misalignment, inconsistent spacing, and accidental asymmetry;
- excessive whitespace or visually unbalanced composition;
- legends, annotations, captions, and footnotes colliding with content;
- unintended line crossings or ambiguous relationship routing;
- elements extending beyond the target canvas, column, page, or frame;
- inconsistent typography relative to the surrounding document.

The agent may adjust coordinates, anchors, relative positioning, node distances, text widths, bends, connector routes, layers, scaling, and margins. It must preserve nodes, labels, relationships, and analytical meaning unless the user explicitly authorizes substantive changes.

## 8. Context-specific behavior

### 8.1 Standalone figures

The standalone module focuses on:

- the full TikZ bounding box;
- cropping and external margins;
- internal spacing and alignment;
- whether labels and arrowheads remain legible at intended output size.

When the original source is only a `tikzpicture` fragment, the skill uses the bundled harness without modifying the fragment’s semantics.

### 8.2 Papers

Paper figures require two inspections:

1. an isolated rendering for internal geometry; and
2. the figure in the rendered paper page.

The page-context inspection checks column width, float placement, captions, notes, scaling, page boundaries, nearby text, and journal-style legibility. An isolated pass is insufficient for a paper-context pass.

### 8.3 Beamer presentations

Beamer diagrams are inspected as complete frames at presentation size. The skill checks frame-safe boundaries, title and footer regions, projected readability, and balance with other slide content.

For overlays, every distinct rendered overlay state must be inspected. Passing only the final overlay is insufficient.

## 9. Artifacts and reporting

The helper script writes artifacts to a temporary or user-approved output directory and produces a manifest containing:

- source and entry-point paths;
- detected context;
- compiler and renderer used;
- compile return code;
- relevant warning summary;
- rendered image paths mapped to figures, pages, frames, and overlays;
- iteration number;
- preparation status.

The agent’s final report adds:

- targets actually inspected;
- defects found and repairs made;
- number of repair cycles;
- unresolved compiler warnings;
- final visual-verification status;
- unresolved defects and evidence paths.

Generated artifacts should not be committed unless they are explicit test fixtures or the user requests them.

## 10. Error handling

- **Missing compiler:** report the missing dependency and do not claim compilation or visual verification.
- **Compilation failure:** preserve the log, diagnose the first actionable failure, and repair only within task scope.
- **Missing renderer:** report that visual verification is unavailable.
- **Missing image-inspection capability:** use the strict unverified terminal status.
- **Ambiguous entry point:** inspect project build instructions; if still ambiguous and the choice materially affects output, ask the user.
- **Multiple affected pages or overlays:** inspect all of them before passing.
- **Repair limit reached:** stop with evidence and a precise unresolved-defect list.
- **Pre-existing unrelated warnings:** distinguish them from warnings introduced or affected by the diagram changes.

## 11. Validation strategy

Implementation will be tested with four fixtures:

1. a standalone figure containing intentional node and label overlaps;
2. a paper containing a figure that fits in isolation but fails in its page or column context;
3. a Beamer frame with crowded content and multiple overlay states;
4. a controlled environment where rendering or visual inspection is unavailable.

The validation must demonstrate:

- correct context routing;
- compilation and rendering artifact creation;
- detection and repair through an actual render–inspect loop;
- inspection of paper page context and every Beamer overlay;
- enforcement of the five-cycle limit;
- strict unverified wording when inspection cannot occur;
- valid skill metadata and directory structure.

## 12. Distribution

The canonical version will live at:

```text
Ningxi-Song/agent-skills/latex/verify-tikz-layout/
```

The repository README will add the `latex/` category, describe the skill, and state its strict visual-verification guarantee.

The validated package will also be installed at:

```text
C:\Users\HKUBS\.codex\skills\verify-tikz-layout
```

The personal installation must match the committed canonical version. Publication is directly to the repository’s `main` branch unless branch protection prevents it.

## 13. Acceptance criteria

Implementation is complete only when:

- the skill package passes structural validation;
- all required files and context modules exist;
- the helper script is exercised successfully where dependencies are available;
- all four validation scenarios have evidence-backed outcomes;
- no workflow path equates compilation with visual verification;
- the README accurately documents installation and behavior;
- the personal installation matches the GitHub version;
- the final GitHub commit is visible on `main`.
