# Academic Trend Plots Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a focused skill that governs y-axis range and vertical margins for academic time-series trend plots.

**Architecture:** A single self-contained `SKILL.md` keeps invocation guidance and the two approved rules together. No scripts or references are needed because the rules are short and tool-independent.

**Tech Stack:** Markdown with YAML frontmatter.

---

### Task 1: Create the academic trend-plot skill

**Files:**

- Create: `academic-trend-plots/SKILL.md`

- [ ] **Step 1: Write the skill entrypoint**

Create `academic-trend-plots/SKILL.md` with frontmatter naming the skill `academic-trend-plots`. State that it applies to ordinary academic time-series trend lines, not event-study plots. Include the displayed-range formula `R >= 0.60 * S`, its equivalent `S <= R / 0.60`, the lower- and upper-margin definitions, and the 30--90 example that prefers 10--110 over 0--100.

- [ ] **Step 2: Validate the skill structure**

Run: `python C:\\Users\\HKUBS\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py academic-trend-plots`

Expected: the validator reports no frontmatter, name, or placeholder errors.

- [ ] **Step 3: Commit the focused skill**

Run `git add academic-trend-plots/SKILL.md docs/superpowers/specs/2026-09-06-academic-trend-plots-design.md docs/superpowers/plans/2026-09-06-academic-trend-plots.md` followed by `git commit -m "feat: add academic trend plot skill"`.

Expected: one commit containing the new skill and its design and implementation records.
