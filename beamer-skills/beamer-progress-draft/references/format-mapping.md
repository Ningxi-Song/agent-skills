# Progress Draft Format Mapping

The HTML editor exports a JSON object with `version`, `template`, and ordered `slides` fields.

| Draft type | Beamer output |
|---|---|
| `title` | `\title{}`, optional `\subtitle{}`, and a plain `\titlepage` frame |
| `itemize` | A titled frame containing one `itemize` environment |

The generator escapes LaTeX special characters and warns about empty titles, more than five bullets, unknown slide types, and titles likely to wrap. Warnings do not alter the draft.

The HTML preview is a content notebook, not the final publication layout. Before delivering a formal deck, apply the `beamer-format` rules: one point per slide, conclusion-driven titles, readable body text, balanced whitespace, and a final appendix where needed.

For article mode, map structured content instead of flattening it into bullets:

| HTML type | Purpose | Beamer treatment |
| --- | --- | --- |
| `claim` | audience-facing statement with evidence | claim title, short evidence bullets, optional takeaway |
| `figure` | mechanism, result, or conceptual diagram | centered figure with caption and interpretation |
| `equation` | key model relationship | centered equation, variable definitions, economic meaning |
| `theorem` | formal result | theorem statement plus intuition, proof details in appendix |
| `takeaway` | transition or conclusion | one highlighted conclusion and optional speaker notes |

`speakerNotes` are for the presenter and should not be rendered as body paragraphs. A valid article draft should contain at least one claim, one visual or equation, one formal result or takeaway, and one conclusion.
