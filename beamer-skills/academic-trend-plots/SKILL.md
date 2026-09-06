---
name: academic-trend-plots
description: Create or review ordinary time-series trend plots for academic papers or Beamer slides, with explicit y-axis range and vertical-margin checks. Do not use for event-study plots.
---

# Academic Trend Plots

Use this skill for ordinary time-series trend lines in academic papers or Beamer presentations.

## Y-axis range

Let `R = max(x) - min(x)` be the plotted variable's range and `S = ymax - ymin` be the displayed y-axis range. Require `R >= 0.60 * S`; equivalently, `S <= R / 0.60`.

This is a maximum y-axis range, not a required range. Use a tighter range when it contains the data and leaves usable margins.

## Vertical margins

Within the permitted y-axis range, make the lower and upper margins as equal as practical:

- lower margin: `min(x) - ymin`
- upper margin: `ymax - max(x)`

For a series spanning 30--90, an axis from 10--110 has equal 20-unit margins and satisfies the 60% coverage rule. An axis from 0--100 satisfies the coverage rule but has asymmetric margins, so prefer 10--110.
