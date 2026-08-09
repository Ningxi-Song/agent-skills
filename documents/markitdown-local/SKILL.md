---
name: markitdown-local
description: Use when reading, extracting, converting, summarizing, searching, or preparing PDF, DOCX, PPTX, XLS, XLSX, HTML, CSV, JSON, XML, EPUB, ZIP, image, or audio files with MarkItDown, especially when selective local extraction can reduce model context or avoid vision processing.
---

# MarkItDown Local

Convert documents locally to Markdown, then inspect only the content needed for the user's request. This often reduces unnecessary context, but never promise lower billing or perfect layout preservation.

## Workflow

1. Keep the source unchanged and choose a separate task-local output path.
2. Run `scripts/convert_document.py SOURCE -o OUTPUT --json` with the skill's isolated Python interpreter when available.
3. Inspect the Markdown's size and headings before reading its body.
4. Search or read bounded sections relevant to the request. Do not load the entire conversion by default.
5. State material extraction limits, especially for scans, diagrams, equations, and complex tables.

## Safety and escalation

- Use local file paths and the narrow `convert_local()` API.
- Plugins are disabled. Do not silently fetch remote URLs.
- Do not enable OCR, vision, transcription, Azure services, LLM clients, or other paid/external processing without explicit authorization.
- If local extraction is empty or inadequate, report that result and ask before escalating.
- Write cleaned or summarized derivatives separately; never overwrite the source or raw Markdown output.

## Commands

```powershell
& "$env:USERPROFILE\.codex\skills\markitdown-local\.venv\Scripts\python.exe" `
  scripts\convert_document.py input.pdf -o work\input.md --json
```

If the isolated interpreter is unavailable, use a Python 3.10+ environment in which the required MarkItDown format extras are installed.

The helper exits with code 2 for missing inputs, unavailable dependencies, unsupported inputs, or conversion failures. Use `--json` for resolved paths and character count.
