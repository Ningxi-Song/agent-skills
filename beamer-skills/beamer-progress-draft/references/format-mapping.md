# Progress Draft Format Mapping

The HTML editor exports a JSON object with `version`, `template`, and ordered `slides` fields.

| Draft type | Beamer output |
|---|---|
| `title` | `\title{}`, optional `\subtitle{}`, and a plain `\titlepage` frame |
| `itemize` | A titled frame containing one `itemize` environment |

The generator escapes LaTeX special characters and warns about empty titles, more than five bullets, unknown slide types, and titles likely to wrap. Warnings do not alter the draft.

The HTML preview is a content notebook, not the final publication layout. Before delivering a formal deck, apply the `beamer-format` rules: one point per slide, conclusion-driven titles, readable body text, balanced whitespace, and a final appendix where needed.
