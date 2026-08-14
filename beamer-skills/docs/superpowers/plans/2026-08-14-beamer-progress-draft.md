# Beamer Progress Draft Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an independent slide-oriented HTML progress-note editor and JSON-to-Beamer generator without changing the existing `beamer-live-draft` workflow.

**Architecture:** Create a self-contained `beamer-progress-draft` skill with its own HTML editor, generator, templates, and documentation. The editor emits a small title/itemize JSON contract; the generator validates and escapes it, emits format warnings, binds a selected template, and optionally compiles the resulting `.tex`.

**Tech Stack:** Dependency-free HTML/CSS/JavaScript, Python 3 standard library, LaTeX Beamer templates, `unittest`.

---

### Task 1: Add failing generator tests

**Files:**
- Create: `tests/beamer-progress-draft/test_generate.py`

- [ ] Write tests for valid title and itemize JSON conversion.
- [ ] Write tests for LaTeX escaping of special characters.
- [ ] Write tests for malformed top-level data and invalid slide entries.
- [ ] Write tests for unknown slide warnings and format warnings.
- [ ] Write tests for missing template fallback and output generation without compilation.
- [ ] Run the test module and confirm it fails because the new generator does not exist.

### Task 2: Implement the progress-draft generator

**Files:**
- Create: `beamer-progress-draft/scripts/generate.py`

- [ ] Implement JSON loading and validation with clear `ValueError` messages.
- [ ] Implement safe defaults for optional fields and preserve slide order.
- [ ] Implement LaTeX escaping, title-page conversion, and itemize-frame conversion.
- [ ] Implement warnings for empty titles, more than five bullets, risky long titles, and unknown slide types.
- [ ] Implement template selection with clean-template fallback.
- [ ] Implement `.tex` writing and optional compiler detection using the standard library.
- [ ] Run the generator tests and confirm they pass.

### Task 3: Add templates and format mapping documentation

**Files:**
- Create: `beamer-progress-draft/templates/clean.tex`
- Create: `beamer-progress-draft/templates/metropolis.tex`
- Create: `beamer-progress-draft/templates/rochester.tex`
- Create: `beamer-progress-draft/references/format-mapping.md`

- [ ] Copy the existing template conventions while keeping the two placeholders `<<TITLEBLOCK>>` and `<<SLIDES>>`.
- [ ] Document the JSON-to-Beamer mapping and the distinction between draft warnings and final `beamer-format` review.
- [ ] Run a sample JSON generation command and inspect the resulting `.tex` text.

### Task 4: Build the standalone HTML progress editor

**Files:**
- Create: `beamer-progress-draft/assets/progress-draft.html`

- [ ] Implement a dependency-free 16:9 slide editor with a slide navigator and single-slide stage.
- [ ] Support title slides and title-plus-bullets slides only.
- [ ] Add controls for creating, deleting, reordering, and selecting slides.
- [ ] Add controls for adding and deleting bullets and editing all visible text in place.
- [ ] Add template selection, JSON import, JSON export, and a starter project-progress deck.
- [ ] Add non-blocking warnings for empty titles and more than five bullets.
- [ ] Run static checks for required control IDs, JSON serialization, and absence of external dependencies.

### Task 5: Document and register the new skill

**Files:**
- Create: `beamer-progress-draft/SKILL.md`
- Modify: `beamer-live-draft/references/templates.md` only if a shared-template note is needed

- [ ] Document trigger phrases, the HTML-to-JSON-to-Beamer workflow, supported slide types, and generator commands.
- [ ] State that `beamer-format` remains authoritative for publication formatting.
- [ ] State that `beamer-live-draft` is unchanged and explain when to use each skill.
- [ ] Keep the skill description focused on when to use it.

### Task 6: Run end-to-end verification

**Files:**
- Create: `tests/beamer-progress-draft/fixtures/sample-progress.json`
- Create: `tests/beamer-progress-draft/test_html_contract.py`

- [ ] Generate `.tex` from the sample JSON without `--compile` and verify expected frames and escaped text.
- [ ] Run the HTML contract smoke tests for required controls and export/import logic.
- [ ] Run all new tests with `py -m unittest discover -s tests/beamer-progress-draft -p 'test_*.py' -v`.
- [ ] Run `py -m py_compile` on the generator.
- [ ] If a LaTeX compiler is available, compile the sample; otherwise record that `.tex` generation was verified and PDF compilation was unavailable.
- [ ] Run `git diff --check` and report the existing TikZ test path mismatch separately rather than mixing it into this feature.

### Task 7: Review the final diff

- [ ] Confirm no existing `beamer-live-draft` files were modified unintentionally.
- [ ] Confirm all generated files are in English unless they are UI labels intentionally matching the existing Chinese editor convention.
- [ ] Confirm no external network dependency was introduced.
- [ ] Attempt to stage/commit only if repository Git permissions allow it; otherwise report the exact permission limitation.
