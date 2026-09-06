# Academic Trend Plots Design

## Purpose

Create a narrowly scoped `academic-trend-plots` skill for time-series trend plots used in academic papers and Beamer presentations. The initial version records only the two user-approved y-axis rules; later principles can extend it deliberately.

## Scope

The skill applies to ordinary time-series trend lines. It is intended for figures that may appear in either a paper or Beamer deck. It does not yet prescribe plotting software, event-study figures, colours, annotations, or other chart-design choices.

## Approved rules

1. **Displayed-range coverage.** Let the plotted variable span `R = max(x) - min(x)` and let the displayed y-axis span `S = ymax - ymin`. Require `R >= 0.60 * S`, equivalently `S <= R / 0.60`. This is an upper bound on the displayed range; the axis may be tighter if it contains the data and leaves usable margins.
2. **Symmetric vertical margins.** Subject to the displayed-range rule, choose y-axis limits so the lower margin `min(x) - ymin` and upper margin `ymax - max(x)` are as equal as practical. For a series spanning 30--90 and an axis span of 100, use 10--110 rather than 0--100.

## Deliverables

- `academic-trend-plots/SKILL.md`: concise, discoverable instructions containing the scope and the two rules.
- `docs/superpowers/plans/2026-09-06-academic-trend-plots.md`: implementation record for the narrow initial skill.

## Validation

Run the bundled skill validator, then inspect the final file to confirm it contains the formula, the symmetric-margin criterion, and the 30--90 example without adding unapproved chart rules.
