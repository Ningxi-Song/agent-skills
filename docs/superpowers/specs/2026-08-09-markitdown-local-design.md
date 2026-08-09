# MarkItDown Local Skill — Design Specification

**Date:** 2026-08-09  
**Status:** Approved for implementation  
**Target repository:** `Ningxi-Song/agent-skills`  
**Skill name:** `markitdown-local`

## Purpose

Create a personal, globally discoverable skill that converts supported documents to compact Markdown locally before an agent reads or analyzes them. The goal is to reduce unnecessary model context and avoid visual/OCR processing when ordinary local extraction is sufficient.

## Package

```text
documents/markitdown-local/
├── SKILL.md
├── agents/openai.yaml
└── scripts/convert_document.py
```

The repository copy is canonical. After validation it is copied to `%USERPROFILE%\.codex\skills\markitdown-local`.

## Trigger and routing

The skill triggers for reading, extracting, converting, summarizing, or preparing PDF, DOCX, PPTX, XLS/XLSX, HTML, CSV, JSON, XML, EPUB, ZIP, image, or audio inputs with MarkItDown.

It uses this order:

1. Prefer deterministic local MarkItDown extraction.
2. Save Markdown to a task-local temporary/output path rather than loading everything into model context.
3. Inspect headings and document size, then read only relevant sections when possible.
4. Escalate to OCR, vision, transcription, or cloud services only when local extraction is inadequate and the user authorizes any paid or external processing.

## Runtime

Use an isolated virtual environment owned by the skill. The helper script accepts an input path, an output path, and optional format-specific controls. It must not send document contents over the network. Installation may download Python packages, but conversion is local unless an explicitly configured MarkItDown integration requires otherwise.

The script reports unsupported formats and conversion errors clearly. It never claims that Markdown preserves the original visual layout.

## Token-efficiency rules

- Do not paste a whole converted document into chat by default.
- Start with metadata, headings, and bounded excerpts.
- Search the Markdown and load only sections relevant to the request.
- Preserve tables and structural markers when useful; remove repeated boilerplate only in a derived cleaned file.
- Treat “fewer tokens” as an optimization, not a guaranteed billing reduction.

## Security

- Prefer local paths and MarkItDown's narrowest applicable conversion API.
- Do not accept untrusted remote URLs by default.
- Never enable plugins, cloud OCR, Azure services, or LLM image description implicitly.
- Keep source files unchanged and write conversion results separately.

## Validation

Validation covers metadata structure, trigger behavior, a successful local conversion fixture, bounded section inspection, unsupported input handling, source-file preservation, and confirmation that no network service is invoked during conversion.

## Distribution

Update the repository README with the `documents/` category and skill entry. Commit and push the canonical skill to `main`, then install an identical copy into the personal Codex skill directory.

## Acceptance criteria

- The skill validates structurally and triggers for supported document tasks.
- Local conversion works in an isolated environment without modifying the source.
- The workflow reads converted content selectively by default.
- External or paid processing requires explicit authorization.
- Repository and personal installed copies match.
- The published commit is visible on `Ningxi-Song/agent-skills` main.
