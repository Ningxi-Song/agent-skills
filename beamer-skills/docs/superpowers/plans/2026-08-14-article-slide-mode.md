# Article Slide Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `beamer-progress-draft` from a bullet-only editor into a structured article-slide drafting mode while preserving the existing notes workflow.

**Architecture:** Add an article slide contract with claim, figure, equation, theorem, takeaway, and speaker-note fields. Extend the self-contained HTML renderer and the JSON-to-Beamer generator to support these types. Add content-quality checks that flag bullet-only article decks and missing narrative components.

**Tech Stack:** Self-contained HTML/CSS/JavaScript, JSON, Python standard library, unittest.

---

### Task 1: Define the article slide contract

**Files:**
- Modify: `beamer-progress-draft/SKILL.md`
- Modify: `beamer-progress-draft/references/format-mapping.md`
- Test: `tests/beamer-progress-draft/test_article_contract.py`

- [ ] **Step 1: Write failing contract tests** for article slide types, required fields, and narrative quality checks.
- [ ] **Step 2: Run the tests and confirm they fail because the contract is not implemented.**
- [ ] **Step 3: Document the article mode and required fields.**
- [ ] **Step 4: Run the contract tests again.**

### Task 2: Extend the HTML draft editor

**Files:**
- Modify: `beamer-progress-draft/assets/progress-draft.html`
- Test: `tests/beamer-progress-draft/test_html_contract.py`

- [ ] **Step 1: Add failing tests for article mode selection, figure/equation/theorem rendering, and notes editing.**
- [ ] **Step 2: Run the tests and confirm the new assertions fail.**
- [ ] **Step 3: Implement the structured renderers and article starter deck.**
- [ ] **Step 4: Run all HTML contract tests.**

### Task 3: Extend JSON-to-Beamer generation

**Files:**
- Modify: `beamer-progress-draft/scripts/generate.py`
- Test: `tests/beamer-progress-draft/test_generate.py`

- [ ] **Step 1: Add failing tests for claim, equation, theorem, figure, and speaker-note conversion.**
- [ ] **Step 2: Run the generator tests and confirm the new assertions fail.**
- [ ] **Step 3: Implement minimal LaTeX mappings and warnings for unsupported article fields.**
- [ ] **Step 4: Run the generator test suite.**

### Task 4: Validate with the AI lemons article

**Files:**
- Create: `examples/ai-lemons-article-progress.json`
- Modify: `beamer-progress-draft/assets/progress-draft.html`
- Test: `tests/beamer-progress-draft/test_article_contract.py`

- [ ] **Step 1: Add a structured article fixture with claims, figures, equations, theorem, takeaways, and notes.**
- [ ] **Step 2: Run the article contract and HTML tests.**
- [ ] **Step 3: Open the HTML draft and inspect the narrative sequence.**
- [ ] **Step 4: Run all relevant tests and record any remaining limitations.**
