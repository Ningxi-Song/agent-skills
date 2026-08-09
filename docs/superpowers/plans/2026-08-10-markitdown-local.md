# MarkItDown Local Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, validate, publish, and personally install a local-first MarkItDown skill that reduces unnecessary model context when processing documents.

**Architecture:** The canonical package lives in `documents/markitdown-local`. A concise `SKILL.md` routes document tasks to a deterministic Python wrapper, which invokes MarkItDown locally and emits Markdown plus machine-readable metadata. Tests validate trigger language, structural integrity, conversion behavior, source preservation, error handling, and absence of implicit external services.

**Tech Stack:** Agent Skills Markdown/YAML, Python 3.10+, MarkItDown, `unittest`, Git, PowerShell.

---

### Task 1: Establish failing structural and policy tests

**Files:**
- Create: `tests/markitdown-local/test_skill.py`
- Create: `tests/markitdown-local/fixtures/sample.html`

- [ ] **Step 1: Add a representative local fixture**

```html
<!doctype html><html><body><h1>Quarterly Note</h1><p>Local conversion only.</p><table><tr><th>Metric</th><th>Value</th></tr><tr><td>Users</td><td>42</td></tr></table></body></html>
```

- [ ] **Step 2: Write tests that require the package, trigger metadata, local-only policy, helper CLI, and README entry**

```python
import importlib.util
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "documents" / "markitdown-local"

class SkillTests(unittest.TestCase):
    def test_required_files_and_trigger_terms(self):
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(body.startswith("---\nname: markitdown-local\n"))
        for term in ("PDF", "DOCX", "PPTX", "XLSX", "HTML", "MarkItDown"):
            self.assertIn(term, body)
        self.assertIn("explicit authorization", body)
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file())
        self.assertTrue((SKILL / "scripts" / "convert_document.py").is_file())

    def test_readme_lists_skill(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("documents/", readme)
        self.assertIn("markitdown-local", readme)

    def test_source_preserved_and_markdown_written(self):
        source = ROOT / "tests" / "markitdown-local" / "fixtures" / "sample.html"
        before = source.read_bytes()
        output = source.parent / "sample.md"
        command = [sys.executable, str(SKILL / "scripts" / "convert_document.py"), str(source), "-o", str(output)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(source.read_bytes(), before)
        self.assertIn("Quarterly Note", output.read_text(encoding="utf-8"))
        output.unlink()

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the tests and verify RED**

Run: `python -m unittest discover -s tests/markitdown-local -v`

Expected: failures because `documents/markitdown-local` and the README entry do not exist.

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/markitdown-local
git commit -m "test: define MarkItDown skill behavior"
```

### Task 2: Implement the minimal skill package

**Files:**
- Create: `documents/markitdown-local/SKILL.md`
- Create: `documents/markitdown-local/agents/openai.yaml`
- Create: `documents/markitdown-local/scripts/convert_document.py`

- [ ] **Step 1: Write concise metadata and workflow instructions**

Create `SKILL.md` with `name: markitdown-local` and a third-person `description` beginning with `Use when`. Require local extraction first, bounded inspection of headings/sections, unchanged sources, separate outputs, and explicit authorization before plugins, remote URLs, OCR, vision, transcription, Azure, or other paid/external processing.

- [ ] **Step 2: Add UI metadata**

```yaml
interface:
  display_name: "MarkItDown Local"
  short_description: "Convert documents locally before selective AI analysis"
  default_prompt: "Use $markitdown-local to extract this document locally and inspect only the sections needed for my request."
```

- [ ] **Step 3: Implement a deterministic CLI wrapper**

```python
from __future__ import annotations
import argparse
import json
from pathlib import Path

def convert(source: Path, output: Path) -> dict[str, object]:
    if not source.is_file():
        raise FileNotFoundError(f"Input file does not exist: {source}")
    from markitdown import MarkItDown
    result = MarkItDown(enable_plugins=False).convert_local(source)
    text = result.text_content
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return {"source": str(source.resolve()), "output": str(output.resolve()), "characters": len(text)}

def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a local document to Markdown without plugins or cloud services.")
    parser.add_argument("source", type=Path)
    parser.add_argument("-o", "--output", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        metadata = convert(args.source, args.output)
    except (FileNotFoundError, ValueError, RuntimeError, ImportError) as exc:
        parser.exit(2, f"markitdown-local: {exc}\n")
    print(json.dumps(metadata) if args.json else args.output)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run tests and verify remaining failures are limited to README**

Run: `python -m unittest discover -s tests/markitdown-local -v`

Expected: package/conversion tests pass when MarkItDown is installed; README test still fails.

- [ ] **Step 5: Commit the package**

```bash
git add documents/markitdown-local
git commit -m "feat: add local MarkItDown skill"
```

### Task 3: Document and harden distribution

**Files:**
- Modify: `README.md`
- Modify: `tests/markitdown-local/test_skill.py`

- [ ] **Step 1: Add `documents/` to the repository tree and skill table**

Document `markitdown-local` as local-first document conversion for selective AI analysis, credited to Willie Song with Microsoft MarkItDown as its runtime dependency.

- [ ] **Step 2: Add failure-path and metadata tests**

Add tests asserting a nonexistent source returns exit code 2 without creating output, `--json` contains resolved source/output and a positive character count, and no strings configuring Azure endpoints or API keys appear in the helper.

- [ ] **Step 3: Run the complete test suite**

Run: `python -m unittest discover -s tests -v`

Expected: all discovered tests pass.

- [ ] **Step 4: Run hygiene checks**

Run: `git diff --check` and `python -m py_compile documents/markitdown-local/scripts/convert_document.py`.

Expected: both commands exit 0 with no errors.

- [ ] **Step 5: Commit documentation and hardening**

```bash
git add README.md tests/markitdown-local/test_skill.py
git commit -m "docs: publish MarkItDown skill guidance"
```

### Task 4: Install isolated runtime and personal skill copy

**Files:**
- Create outside repository: `%USERPROFILE%\.codex\skills\markitdown-local\`
- Create outside repository: `%USERPROFILE%\.codex\skills\markitdown-local\.venv\`

- [ ] **Step 1: Create the isolated virtual environment**

Run: `py -3.12 -m venv %USERPROFILE%\.codex\skills\markitdown-local\.venv`

Expected: Python environment is created without changing project dependencies.

- [ ] **Step 2: Install MarkItDown with supported document extras**

Run: `%USERPROFILE%\.codex\skills\markitdown-local\.venv\Scripts\python.exe -m pip install "markitdown[pdf,docx,pptx,xlsx,xls]"`

Expected: pip exits 0 and `markitdown` imports in the isolated interpreter.

- [ ] **Step 3: Copy the validated canonical package without repository test artifacts**

Copy `SKILL.md`, `agents/`, and `scripts/` to `%USERPROFILE%\.codex\skills\markitdown-local`, preserving `.venv`.

- [ ] **Step 4: Verify installed and canonical files match**

Compare SHA-256 hashes for `SKILL.md`, `agents/openai.yaml`, and `scripts/convert_document.py`.

Expected: every corresponding hash matches.

- [ ] **Step 5: Run a smoke conversion with the isolated interpreter**

Convert `tests/markitdown-local/fixtures/sample.html` to a temporary Markdown file, verify the heading and table text, then remove only that temporary output.

### Task 5: Publish and verify GitHub state

**Files:**
- No new files.

- [ ] **Step 1: Confirm the exact commits and clean worktree**

Run: `git status --short` and `git log -5 --oneline`.

Expected: no uncommitted changes and the design, tests, skill, and documentation commits are visible.

- [ ] **Step 2: Push main to origin**

Run: `git push origin main`.

Expected: Git reports `main -> main` without rejection.

- [ ] **Step 3: Verify remote main contains the published commit**

Run: `git ls-remote origin refs/heads/main` and compare with `git rev-parse HEAD`.

Expected: hashes are identical.

- [ ] **Step 4: Report limitations accurately**

State that the skill reduces unnecessary context for many text-based documents but does not guarantee lower billing, perfect layout preservation, or successful extraction of scanned/complex visual documents without separately authorized OCR or vision processing.
