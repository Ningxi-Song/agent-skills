# Beamer Live Draft Full-Deck Fidelity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `beamer-live-draft` to preserve manual edits while supporting and auditing complete editable decks containing diagrams, formulas, tables, figures, flows, and rich text.

**Architecture:** Introduce a versioned component-based snapshot schema in `draft-state.mjs`, render components through a registry in the self-contained editor, and generate Beamer through explicit component handlers. A manifest-driven auditor compares the source deck with the draft and rejects silent bullet degradation or full-page raster substitution.

**Tech Stack:** JavaScript ES modules, browser `localStorage`, HTML/CSS/SVG, Python 3 standard library, `unittest`, Beamer/TikZ.

---

## File Map

- Modify `beamer-skills/beamer-live-draft/assets/draft-state.mjs`: schema versioning, validation, migration, last-good backup, atomic save.
- Modify `beamer-skills/beamer-live-draft/assets/beamer-draft.html`: component registry, editable HTML/SVG renderers, autosave status, backup export.
- Modify `beamer-skills/beamer-live-draft/scripts/generate.py`: strict component-to-Beamer generation.
- Create `beamer-skills/beamer-live-draft/scripts/audit_draft.py`: manifest comparison and prohibited-raster checks.
- Create `beamer-skills/tests/beamer-live-draft/test_draft_state.mjs`: state migration and preservation tests.
- Create `beamer-skills/tests/beamer-live-draft/test_generate.py`: component generation and failure tests.
- Create `beamer-skills/tests/beamer-live-draft/test_audit_draft.py`: positive and negative audit tests.
- Create `beamer-skills/tests/beamer-live-draft/fixtures/full-deck-manifest.json`: 35-slide regression manifest.
- Create `beamer-skills/tests/beamer-live-draft/fixtures/full-deck-draft.json`: representative component fixture.
- Modify `beamer-skills/tests/beamer-live-draft/test_html_contract.py`: renderer and autosave contract checks.
- Modify `beamer-skills/beamer-live-draft/SKILL.md`: mandatory full-deck review and fidelity rules.

### Task 1: Lock in failing preservation and schema tests

**Files:**
- Create: `beamer-skills/tests/beamer-live-draft/test_draft_state.mjs`
- Modify: `beamer-skills/tests/beamer-live-draft/test_html_contract.py`

- [ ] **Step 1: Write the failing migration and atomic-save test**

```js
import assert from 'node:assert/strict';
import { migrateState, saveStateAtomic, SCHEMA_VERSION } from '../../beamer-live-draft/assets/draft-state.mjs';

const store = new Map();
const adapter = { getItem: k => store.get(k) ?? null, setItem: (k, v) => store.set(k, v) };
const legacy = { template: 'clean', active: 1, slides: [{ type: 'itemize', frametitle: 'Edited', items: ['manual text'], unknown: 7 }] };
const migrated = migrateState(legacy);
assert.equal(migrated.schemaVersion, SCHEMA_VERSION);
assert.equal(migrated.slides[0].components[0].items[0], 'manual text');
assert.equal(migrated.slides[0].legacy.unknown, 7);
saveStateAtomic(adapter, 'deck', migrated);
assert.ok(store.has('deck:last-good'));
assert.deepEqual(JSON.parse(store.get('deck')), migrated);
```

- [ ] **Step 2: Extend the HTML contract test**

```python
def test_editor_declares_component_renderers_and_backup(self):
    for name in ("diagram", "formula", "table", "figure", "flow", "rich-text"):
        self.assertIn(f"'{name}'", self.text)
    self.assertIn("last-good", self.text)
    self.assertIn("导出备份", self.text)
```

- [ ] **Step 3: Run tests and verify RED**

Run: `node beamer-skills/tests/beamer-live-draft/test_draft_state.mjs && py -m unittest beamer-skills/tests/beamer-live-draft/test_html_contract.py -v`

Expected: FAIL because schema migration, atomic save, component registry, and backup controls do not exist.

- [ ] **Step 4: Commit the failing tests**

```bash
git add beamer-skills/tests/beamer-live-draft/test_draft_state.mjs beamer-skills/tests/beamer-live-draft/test_html_contract.py
git commit -m "test: define live draft preservation contract"
```

### Task 2: Implement versioned snapshots without losing manual edits

**Files:**
- Modify: `beamer-skills/beamer-live-draft/assets/draft-state.mjs`
- Modify: `beamer-skills/beamer-live-draft/assets/beamer-draft.html`
- Test: `beamer-skills/tests/beamer-live-draft/test_draft_state.mjs`

- [ ] **Step 1: Add the schema constants and validators**

```js
export const SCHEMA_VERSION = 2;
export const COMPONENT_TYPES = new Set(['diagram', 'formula', 'table', 'figure', 'flow', 'rich-text']);

export function validateState(state) {
  if (!state || state.schemaVersion !== SCHEMA_VERSION || !Array.isArray(state.slides)) throw new Error('invalid draft state');
  for (const slide of state.slides) {
    if (!slide.id || !Array.isArray(slide.components)) throw new Error(`invalid slide ${slide.id ?? '<missing>'}`);
    for (const component of slide.components) if (!COMPONENT_TYPES.has(component.type)) throw new Error(`unsupported component ${component.type}`);
  }
  return state;
}
```

- [ ] **Step 2: Implement legacy migration with unknown-field preservation**

```js
export function migrateState(input) {
  if (input?.schemaVersion === SCHEMA_VERSION) return validateState(structuredClone(input));
  const slides = (input?.slides ?? []).map((slide, index) => ({
    id: slide.id ?? `slide-${index + 1}`,
    frametitle: slide.frametitle ?? slide.title ?? '',
    components: legacyComponents(slide),
    legacy: Object.fromEntries(Object.entries(slide).filter(([k]) => !['id','type','frametitle','title','items','left','right','blocktitle','body'].includes(k))),
  }));
  return validateState({ schemaVersion: SCHEMA_VERSION, deckId: input?.deckId ?? 'default', template: input?.template ?? 'clean', active: input?.active ?? 0, slides });
}
```

- [ ] **Step 3: Implement atomic save and last-good recovery**

```js
export function saveStateAtomic(store, key, state) {
  const validated = validateState(structuredClone(state));
  const previous = store.getItem(key);
  if (previous !== null) store.setItem(`${key}:last-good`, previous);
  const encoded = JSON.stringify(validated);
  store.setItem(`${key}:pending`, encoded);
  validateState(JSON.parse(store.getItem(`${key}:pending`)));
  store.setItem(key, encoded);
}
```

- [ ] **Step 4: Wire editor restore/save to a stable pathname-based deck key**

Use `beamer-live-draft:${location.pathname}:v2`; never include `location.search`. Restore live state before reading seed slides. On migration failure, show a persistent error and retain the old key.

- [ ] **Step 5: Run preservation tests**

Run: `node beamer-skills/tests/beamer-live-draft/test_draft_state.mjs`

Expected: PASS, including manual text, unknown fields, and `last-good` assertions.

- [ ] **Step 6: Commit**

```bash
git add beamer-skills/beamer-live-draft/assets/draft-state.mjs beamer-skills/beamer-live-draft/assets/beamer-draft.html
git commit -m "feat: preserve versioned live draft state"
```

### Task 3: Add editable component renderers

**Files:**
- Modify: `beamer-skills/beamer-live-draft/assets/beamer-draft.html`
- Modify: `beamer-skills/tests/beamer-live-draft/test_html_contract.py`

- [ ] **Step 1: Add a registry contract test**

Assert that every component registers `render`, every editable field calls `scheduleSave`, diagram edges are SVG elements, and `figure` rejects `fullPageRaster: true`.

- [ ] **Step 2: Implement the registry**

```js
const componentRenderers = {
  'rich-text': renderRichText,
  formula: renderFormula,
  table: renderTable,
  figure: renderFigure,
  flow: renderFlow,
  diagram: renderDiagram,
};

function renderComponent(component, host) {
  const renderer = componentRenderers[component.type];
  if (!renderer) throw new Error(`Unsupported component: ${component.type}`);
  renderer(component, host);
}
```

- [ ] **Step 3: Implement editable table/formula/rich-text renderers**

Every text-bearing element uses `contenteditable`, mutates the component object on `input`, and invokes `scheduleSave()`.

- [ ] **Step 4: Implement editable flow and diagram renderers**

Nodes are positioned HTML boxes with editable labels; edges are SVG `line`/`path` elements keyed by node IDs. Reject edges whose endpoints do not exist.

- [ ] **Step 5: Implement genuine figure rendering and raster-page rejection**

```js
function renderFigure(component, host) {
  if (component.fullPageRaster) throw new Error('Full-page raster slides are prohibited');
  const image = new Image();
  image.src = component.src;
  image.alt = component.alt ?? '';
  host.append(image);
}
```

- [ ] **Step 6: Run contract tests**

Run: `py -m unittest beamer-skills/tests/beamer-live-draft/test_html_contract.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add beamer-skills/beamer-live-draft/assets/beamer-draft.html beamer-skills/tests/beamer-live-draft/test_html_contract.py
git commit -m "feat: render editable complex slide components"
```

### Task 4: Generate strict Beamer for every component

**Files:**
- Modify: `beamer-skills/beamer-live-draft/scripts/generate.py`
- Create: `beamer-skills/tests/beamer-live-draft/test_generate.py`
- Create: `beamer-skills/tests/beamer-live-draft/fixtures/full-deck-draft.json`

- [ ] **Step 1: Write failing generator tests**

```python
def test_unknown_component_fails(self):
    with self.assertRaisesRegex(ValueError, "slide-2.*mystery"):
        slide_to_frame({"id":"slide-2","frametitle":"Bad","components":[{"id":"c1","type":"mystery"}]})

def test_table_and_diagram_emit_native_beamer(self):
    tex = slide_to_frame(self.fixture["slides"][1])
    self.assertIn(r"\begin{tabular}", tex)
    self.assertIn(r"\begin{tikzpicture}", tex)
```

- [ ] **Step 2: Replace silent skipping with explicit dispatch**

```python
COMPONENT_BUILDERS = {
    "rich-text": rich_text_to_tex,
    "formula": formula_to_tex,
    "table": table_to_tex,
    "figure": figure_to_tex,
    "flow": flow_to_tikz,
    "diagram": diagram_to_tikz,
}
```

Unknown slide/component types raise `ValueError` containing stable slide and component IDs.

- [ ] **Step 3: Implement component builders**

Use display math for formulas, `tabular` for tables, `includegraphics` only for genuine figures, and TikZ nodes/edges for flows and diagrams. Escape user text separately from trusted formula strings.

- [ ] **Step 4: Run generator tests**

Run: `py -m unittest beamer-skills/tests/beamer-live-draft/test_generate.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add beamer-skills/beamer-live-draft/scripts/generate.py beamer-skills/tests/beamer-live-draft/test_generate.py beamer-skills/tests/beamer-live-draft/fixtures/full-deck-draft.json
git commit -m "feat: generate native Beamer components"
```

### Task 5: Add the full-deck fidelity auditor

**Files:**
- Create: `beamer-skills/beamer-live-draft/scripts/audit_draft.py`
- Create: `beamer-skills/tests/beamer-live-draft/test_audit_draft.py`
- Create: `beamer-skills/tests/beamer-live-draft/fixtures/full-deck-manifest.json`

- [ ] **Step 1: Write failing positive and negative audit tests**

```python
def test_detects_missing_slide_wrong_type_and_raster(self):
    report = audit(manifest, broken_draft)
    codes = {issue["code"] for issue in report["issues"]}
    self.assertEqual({"slide-count", "component-type", "full-page-raster"}, codes)
```

- [ ] **Step 2: Implement manifest comparison**

The manifest records each slide ID, title, order, and required component types. `audit()` returns `{ok, slideCount, issues}` and never mutates inputs.

- [ ] **Step 3: Add layout evidence fields**

Accept renderer-produced `layoutChecks` with `titleWrap`, `overflow`, `missingAsset`, and `emptyBody`. Treat any true value as a failure with slide/component IDs.

- [ ] **Step 4: Add CLI output and exit codes**

Run: `py beamer-skills/beamer-live-draft/scripts/audit_draft.py manifest.json draft.json`

Expected: exit 0 with per-slide `PASS`; exit 1 with per-slide issue codes and descriptions.

- [ ] **Step 5: Run tests**

Run: `py -m unittest beamer-skills/tests/beamer-live-draft/test_audit_draft.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add beamer-skills/beamer-live-draft/scripts/audit_draft.py beamer-skills/tests/beamer-live-draft/test_audit_draft.py beamer-skills/tests/beamer-live-draft/fixtures/full-deck-manifest.json
git commit -m "feat: audit full-deck draft fidelity"
```

### Task 6: Update the skill workflow and run regression verification

**Files:**
- Modify: `beamer-skills/beamer-live-draft/SKILL.md`
- Modify: `beamer-skills/beamer-live-draft/references/templates.md` only if component packages require template changes.

- [ ] **Step 1: Add mandatory full-deck intake rules**

Document: inspect every source page; classify each slide; create a manifest; never silently degrade diagrams/formulas/tables to bullets; never use a full-page raster as an editable slide; preserve live state before any revision.

- [ ] **Step 2: Add completion checklist**

Require count/order/title/component audit, browser overflow inspection, save/reload test, generator test, and explicit unsupported-component failures before delivery.

- [ ] **Step 3: Run the complete suite**

```bash
node beamer-skills/tests/beamer-live-draft/test_draft_state.mjs
py -m unittest discover -s beamer-skills/tests/beamer-live-draft -p "test_*.py" -v
py -m unittest beamer-skills/tests/test_catalog.py -v
```

Expected: all tests PASS.

- [ ] **Step 4: Run fixture audit and generation**

```bash
py beamer-skills/beamer-live-draft/scripts/audit_draft.py beamer-skills/tests/beamer-live-draft/fixtures/full-deck-manifest.json beamer-skills/tests/beamer-live-draft/fixtures/full-deck-draft.json
py beamer-skills/beamer-live-draft/scripts/generate.py beamer-skills/tests/beamer-live-draft/fixtures/full-deck-draft.json --out .workbuddy/beamer-live-draft-regression.tex
```

Expected: audit reports 35/35 PASS; generator writes the TeX file without warnings or skipped components.

- [ ] **Step 5: Commit**

```bash
git add beamer-skills/beamer-live-draft/SKILL.md beamer-skills/beamer-live-draft/references/templates.md
git commit -m "docs: require full-deck fidelity review"
```

### Task 7: Deploy safely

**Files:** none beyond prior tasks.

- [ ] **Step 1: Inspect scope**

Run: `git status --short && git diff --stat HEAD~6..HEAD`

Expected: only the planned skill, tests, fixtures, spec, and plan files appear.

- [ ] **Step 2: Verify no secrets or generated scratch files are staged**

Run: `git diff --cached --name-status && git status --short`

- [ ] **Step 3: Push the current branch**

Run: `git push -u origin HEAD`

Expected: GitHub reports the updated branch successfully.

- [ ] **Step 4: Install the updated skill globally**

Copy only `beamer-skills/beamer-live-draft` into the global Codex skill directory after preserving the installed copy or confirming it matches the source baseline.

- [ ] **Step 5: Smoke-test the installed version**

Verify the next Codex turn discovers the updated description and that the editor restores a migrated manually edited snapshot.
