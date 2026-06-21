---
name: beamer-presentation
description: >
  Design academic presentation slides (Beamer) for economics research.
  Use when user wants to create presentation slides, seminar slides,
  conference talk, job market paper slides, Beamer template, academic
  presentation, or research deck. Enforces one-point-per-slide logic,
  minimal tables, large fonts, and conclusion-driven titles.
---

# Beamer Presentation

Produce academic presentation slides that meet economics seminar standards.
See [EXAMPLES.md](EXAMPLES.md) for a complete deck outline.

## Core Principle

Slides serve the audience, not the paper. Every slide must advance understanding
by exactly one point. The deck should tell a story: what you studied, why it
matters, what you found, and why we should believe you.

---

## Content Standards

### 1. Classic Slide Arc

Follow this sequence:
```
Title → Motivation → Research Question → Setting/Institutional Background →
Data → Empirical Strategy → Results (main) → Mechanisms / Heterogeneity →
Robustness → Conclusion → Appendix
```

### 2. Open Fast

First 3-5 slides must establish:
- What you study and why it matters.
- The headline finding.
- The setting and research design in brief.

### 3. One Point Per Slide

Each slide conveys exactly one idea. If you find yourself adding a second
bullet group, split the slide.

### 4. Conclusion-Driven Titles

Every slide title must be a **claim**, not a label.

- No: "Data" or "Results" or "Summary Statistics"
- Yes: "Treated and control counties follow parallel pre-trends"
- Yes: "The reform increased employment by 5.4 percentage points"
- Yes: "Effects are concentrated among low-education workers"

### 5. Identification Strategy Must Be Clear

Dedicate slides to:
- Who is treated, who is the control group.
- What is the identifying assumption.
- How you validate it (pre-trend plots, balance tests, placebo tests).
- What threats remain and how you address them.

### 6. Results: Highlight Main Coefficient and Magnitude

Do not paste full regression tables. Instead show:
- The coefficient of interest with standard error / confidence interval.
- The baseline mean of the dependent variable.
- The implied economic magnitude (e.g., "a 12% increase relative to the mean").
- A coefficient plot or event-study figure is preferred over a table.

### 7. Appendix Must Be Comprehensive

The main deck tells the headline story. The appendix holds:
- Full regression tables.
- Variable definitions.
- Robustness checks.
- Additional figures.
- Data construction details.

---

## Format Standards

### 1. Clean Slides

Per slide: **3-5 bullet points maximum**. Never full paragraphs.
Each bullet: one line, preferably one clause.

### 2. Large Fonts

- Body text: at least **18pt**.
- Figure axis labels and legends: readable from the back of the room.
- Table cell text: at least **14pt**.

### 3. Figures Over Tables

Prefer: trend plots, event-study plots, coefficient plots, maps, bar charts,
scatter plots with fitted lines.

Avoid: dense regression tables with 8+ columns, full summary statistics tables,
correlation matrices.

### 4. Minimal Tables

When a table is necessary, show only:
- Outcome variable name.
- Coefficient.
- Standard error or confidence interval.
- Baseline mean.
- Observations (N).

No: control variable rows, fixed effects rows, R-squared rows (move to appendix).

### 5. Layout Consistency

- Title position identical on every slide.
- Font family, size, color scheme consistent throughout.
- Footer (author, institution, date, slide number) uniform.
- Figure and table styles match (same colors, line widths, marker sizes).

### 6. Single-Line Frame Titles

Every frame title (the slide title bar at the top of each content slide)
must fit on one line. If a frame title wraps, shorten it.

The main title on the title slide may span multiple lines.

### 7. Adequate Spacing

Content must breathe. Whitespace is not wasted space -- it guides attention.

**Minimum spacing rules:**
- Whitespace should occupy approximately 35%-40% of the total slide area
  (content should fill no more than 60%-65%). Never let content exceed 75%.
- At least one blank line equivalent between the title frame and body.
- At least one blank line equivalent between a figure/table and the bullets
  that follow.
- Itemize environments: use `\setlength{\itemsep}{4pt}` or similar -- never
  the default tight item spacing, never stretched to fill the page.

**What to avoid:**
- `\vfill` between every element -- creates uneven, floating gaps.
- `[shrink]` frame option -- if content needs shrinking, it belongs on two
  slides or the appendix.
- Content touching or nearly touching the frame edges -- keep natural
  Beamer margins intact.
- Single bullet filling the entire text width as a long line -- shorten
  it or break into sub-bullets.

**Horizontal balance:**
- Content must be roughly horizontally centered within the frame.
- Whitespace must be distributed evenly on all sides, never concentrated on
  one side.
- Never: content clustered on the left with a large empty area on the right.
- Use `\centering` for figures and tables, and let Beamer's default margins
  handle horizontal alignment for itemize blocks.

**Visual check:** if you squint at the slide and content looks like a solid
block, there is not enough whitespace. You should see a clear separation
between title, body, and each visual element. Whitespace should feel
balanced, not pushed to one side.

### 8. Emphasis Formatting Use Sparingly

Bold, italic, color, and block environments highlight key points. Overuse
defeats their purpose -- when everything is emphasized, nothing is.

- Use emphasis on at most **one element per slide** (e.g., the main coefficient).
- Use bold or color to mark the **main finding** in a bullet or table cell.
- Use block environments (`\begin{block}...`) only for the central takeaway.
- Never: entire bullet lists in bold, colored text throughout, blocks on
  every slide.

### 9. Bullet Points, Never Paragraphs

Full sentences and paragraphs belong in the paper, not on slides. The audience
reads slides faster than the speaker talks; paragraphs make them read instead
of listen.

- Every text element must fit on **one line** (no multi-line bullets).
- Break complex statements into a bullet group of 2-3 short items.
- If a point requires a paragraph of explanation, move it to speaker notes
  or the appendix.

### 10. Consistent Font Sizes Within Category

Text in the same category must share the same font size. Unjustified size
variation signals carelessness and confuses the reading hierarchy.

- All bullet text: same size throughout the slide.
- All table cell text: same size within a table.
- All figure axis labels and legends: same size across all figures.
- Takeaway boxes (`\begin{block}`) inside a slide: same font size as
  surrounding bullets, not larger to "stand out."

Never: a bullet at 18pt with a nearby "takeaway" at 22pt, or table body
at 14pt with a footnote at 12pt and a header at 16pt.

---

## Beamer Structure Template

```latex
% Slide with bullet points
\begin{frame}{Claim-Driven Title Here}
\begin{itemize}
  \item First point (one line)
  \item Second point (one line)
  \item Third point (one line)
\end{itemize}
\end{frame}

% Slide with figure
\begin{frame}{Claim About the Figure}
\begin{figure}
  \centering
  \includegraphics[width=0.85\textwidth]{figure.pdf}
\end{figure}
\end{frame}

% Slide with minimal table
\begin{frame}{Main Result: Treatment Effect on Employment}
\begin{table}
  \centering
  \begin{tabular}{lcc}
  \toprule
  Outcome & Coefficient & Baseline Mean \\
  \midrule
  Employment rate & 5.43*** & 68.3 \\
                 & (1.23)   & \\
  \bottomrule
  \end{tabular}
\end{table}
\end{frame}
```

## Workflow

1. **Outline the arc**: motivation → RQ → setting → data → strategy → results → mechanisms → robustness → conclusion.
2. **Write titles first**: every slide gets a claim-driven title before content.
3. **One point per slide**: verify no slide has two distinct messages.
4. **Replace tables with figures** wherever possible.
5. **Strip tables to essentials**: coefficient, SE, baseline mean, N only.
6. **Build appendix**: move all full tables, definitions, extra checks there.
7. **Check formatting**: single-line frame titles, >=18pt body, 3-5 bullets, proper spacing,
   emphasis used only once per slide, no paragraphs, consistent font sizes within category,
   every text item fits on one line.
