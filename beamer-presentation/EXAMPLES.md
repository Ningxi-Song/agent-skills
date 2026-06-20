# Beamer Presentation Examples

Each example follows: one point per slide, conclusion-driven titles, 3-5 bullets,
figures over tables, minimal tables with coefficient/SE/baseline/N only.

---

## Example 1: Full Slide Deck Outline (DiD Paper)

```
Slide 1  - Title slide
           "The Employment Effects of Minimum Wage Hikes:
            Evidence from County-Level Variation"
           Author, Institution, Date

Slide 2  - Motivation
           "Minimum wage debates hinge on whether jobs are destroyed"
           * Policy debate: 40+ states raised minimum wages since 2010
           * Theory is ambiguous: labor demand elasticity vs. monopsony
           * Existing evidence mixed and concentrated on teens/restaurants
           * This paper: county-level variation, all sectors, 2000-2020

Slide 3  - This Paper in One Slide
           "We find no evidence of job loss from minimum wage increases"
           * Setting: 3,000+ U.S. counties, 2000-2020
           * Design: stacked difference-in-differences
           * Main result: elasticity of employment to minimum wage = -0.03
             (not statistically different from zero)
           * No disemployment even in low-wage sectors

Slide 4  - Institutional Background
           "Minimum wages vary substantially across counties and over time"
           * Federal minimum: $7.25 (unchanged since 2009)
           * State minimums: $7.25-$15.00 (30 states above federal)
           * County and city minimums add further variation
           * [Figure: Map of minimum wage levels across counties, 2020]

Slide 5  - Data
           "We combine QCEW employment data with minimum wage laws"
           * QCEW: quarterly employment and wages by county-industry
           * 2000-2020, 3,142 counties, 20 NAICS sectors
           * Minimum wage panel: hand-coded from state/city legislation
           * Final sample: 1.2 million county-sector-year observations

Slide 6  - Empirical Strategy
           "Stacked DiD compares counties that raised wages to those that did not"
           * Treatment: county experiences a minimum wage increase of >=10%
           * Control: counties with no increase in the same period
           * Identifying assumption: parallel trends in employment
           * We use stacked DiD (Cengiz et al., 2019) with clean controls

Slide 7  - Parallel Trends Evidence
           "Treated and control counties follow parallel pre-trends"
           * [Figure: Event-study plot, -4 to +4 years around wage increase]
           * Flat pre-trends for overall employment
           * No anticipatory effects before treatment
           * Also holds for low-wage sectors (Appendix Figure A1)

Slide 8  - Main Result
           "Minimum wage increases have no detectable effect on employment"
           * [Figure: Coefficient plot for overall employment]
           * Elasticity: -0.03 (SE = 0.05)
           * Baseline employment: 45,000 per county-sector
           * Implies a change of -1,350 jobs, statistically indistinguishable from zero
           * [Table: coefficient, SE, baseline mean, N]

Slide 9  - Economic Magnitude
           "Even the upper bound implies trivial job loss"
           * Upper bound of 95% CI: elasticity = -0.13
           * At a 10% minimum wage increase: employment falls by at most 1.3%
           * Wage gains for affected workers: +7.2% on average
           * Net effect on labor income is positive for low-wage workers

Slide 10 - Heterogeneity: Low-Wage Sectors
           "No disemployment even in the most exposed sectors"
           * [Figure: Coefficient plot by sector wage quartile]
           * Restaurants (highest exposure): elasticity = -0.08 (SE = 0.09)
           * Retail: elasticity = -0.02 (SE = 0.06)
           * No sector shows significant negative employment effects

Slide 11 - Mechanisms
           "Firms adjust through prices and turnover, not layoffs"
           * Restaurant prices rise by 0.8% after a 10% wage increase
           * No change in establishment entry or exit
           * Worker turnover (churn) decreases slightly
           * Evidence consistent with monopsony or efficiency wage models

Slide 12 - Robustness
           "Results are robust to alternative specifications"
           * Continuous DiD (variation in bite, not binary treatment)
           * Border-county pair design
           * Excluding counties with city-level minimum wages
           * All in Appendix B

Slide 13 - Conclusion
           "Minimum wage increases raise pay without destroying jobs"
           * Main finding: near-zero employment elasticity
           * Policy implication: moderate minimum wage increases benefit
             low-wage workers without adverse employment effects
           * Caveat: results apply to state/county variation up to $15;
             very large federal increases may differ

Slide 14+ - Appendix
           * Appendix A: Full summary statistics table
           * Appendix B: Full regression tables
           * Appendix C: Robustness checks
           * Appendix D: Variable definitions and data sources
           * Appendix E: Additional figures
```

---

## Example 2: Slide Content Examples (Good vs. Bad)

### Bad: Dense Regression Table

```
\begin{frame}{Results}
\begin{table}
  \begin{tabular}{lcccccc}
  \toprule
                    & (1)    & (2)    & (3)    & (4)    & (5)    & (6) \\
  \midrule
  Post x Treat      & 2.34** & 1.98** & 1.87** & 2.12** & 1.76** & 1.65* \\
                    & (0.98) & (0.87) & (0.82) & (0.91) & (0.78) & (0.85) \\
  Education         &        & 0.45***& 0.43***& 0.41***& 0.39***& 0.38***\\
                    &        & (0.08) & (0.08) & (0.08) & (0.08) & (0.08) \\
  Age               &        &        & 0.01   & 0.01   & 0.01   & 0.01   \\
                    &        &        & (0.01) & (0.01) & (0.01) & (0.01) \\
  Female            &        &        &        & -0.12**& -0.11**& -0.11**\\
                    &        &        &        & (0.05) & (0.05) & (0.05) \\
  Constant          & 68.3***& 65.2***& 64.8***& 65.1***& 64.9***& 65.0***\\
                    & (0.45) & (0.52) & (0.54) & (0.56) & (0.57) & (0.58) \\
  \midrule
  Year FE           & No     & No     & Yes    & Yes    & Yes    & Yes    \\
  County FE         & No     & No     & No     & Yes    & Yes    & Yes    \\
  R-squared         & 0.02   & 0.12   & 0.15   & 0.23   & 0.24   & 0.25   \\
  Observations      & 3,420  & 3,420  & 3,420  & 3,420  & 3,420  & 3,420  \\
  \bottomrule
  \end{tabular}
\end{table}
\end{frame}
```

Why bad: too many columns, too many rows, font too small, title not a conclusion,
control variables clutter the slide, audience cannot process this in 30 seconds.

### Good: Single-Coefficient Highlight Table

```
\begin{frame}{The reform increased employment by 5.4 percentage points}
\begin{table}
\centering
\begin{tabular}{lccc}
\toprule
Outcome & (1) OLS & (2) FE & Baseline Mean \\
\midrule
Employment rate & 2.34** & 1.87** & 68.3 \\
                & (0.98) & (0.82) & \\
\bottomrule
\end{tabular}
\end{table}
\vspace{0.3cm}
\begin{itemize}
  \item 1.87 pp increase = 2.7\% relative to baseline mean of 68.3\%
  \item Both specifications include year and county fixed effects
  \item Full table with controls and robustness in Appendix B
\end{itemize}
\end{frame}
```

Why good: only the key coefficient, clear title, baseline mean for magnitude,
bullet points add interpretation, full table moved to appendix.

### Good: Event-Study Figure

```
\begin{frame}{Employment effects emerge gradually after the reform}
\begin{figure}
\centering
\includegraphics[width=0.85\textwidth]{event_study.pdf}
\end{figure}
\vspace{0.1cm}
\begin{itemize}
  \item No pre-trend: coefficients not significantly different from zero before t=0
  \item Effect builds over 3 years post-reform, reaching 5.4 pp at t=3
  \item 95\% confidence intervals shown with vertical bars
\end{itemize}
\end{frame}
```

Why good: visual evidence of parallel trends, shows dynamics, easier to process
than a coefficient table, title states the finding.

---

## Example 3: Bad vs. Good Slide Titles

| Bad (Label) | Good (Conclusion) |
|-------------|-------------------|
| Data | We use administrative tax records covering 40 million firms |
| Summary Statistics | Treated firms are larger and more productive at baseline |
| Empirical Strategy | Stacked DiD compares firms in reform counties to neighboring counties |
| Results | The reform increased firm revenue by 8.3% |
| Robustness | Results are unchanged with alternative standard error clustering |
| Conclusion | Place-based tax incentives increase investment without displacing nearby activity |
| Identification | Treatment and control counties had parallel pre-trends in employment |
| Mechanisms | The effect operates through new firm entry, not incumbent expansion |

---

## Example 4: Bad vs. Good Slide Density

### Bad: Overcrowded

```
\begin{frame}{Data and Summary Statistics}
\begin{itemize}
  \item We use the China Industrial Enterprise Database (CIED) 2005-2015, which covers
    all state-owned firms and non-state firms with annual revenue above 5 million CNY,
    including detailed balance sheet and income statement variables for approximately
    400,000 firms per year, with firm identifiers that allow us to construct a panel
  \item We merge this with county-level fiscal data from the County Statistical Yearbook
    and patent data from the State Intellectual Property Office (SIPO)
  \item We drop firms with fewer than 8 employees, negative assets, or negative revenue,
    which removes approximately 5\% of observations
  \item We winsorize all continuous variables at the 1st and 99th percentiles
  \item Final sample: 2.3 million firm-year observations across 2,500 counties
  \item Table 1 shows summary statistics for the full sample, treatment group,
    and control group, with t-tests for differences in means
\end{itemize}
\end{frame}
```

Why bad: 6 dense bullets, full sentences, too much to read, audience reads slide
instead of listening.

### Good: Split into Two Slides

```
Slide A:

\begin{frame}{We use administrative firm data merged with county fiscal records}
\begin{itemize}
  \item China Industrial Enterprise Database (CIED), 2005-2015
  \item 400,000+ firms per year, balance sheet and income statement
  \item Merged with county fiscal data and patent records
  \item Final sample: 2.3 million firm-year observations
\end{itemize}
\end{frame}

Slide B:

\begin{frame}{Treated firms are larger and more export-oriented at baseline}
\begin{itemize}
  \item Treatment group: 23\% larger by assets (p < 0.01)
  \item Treatment group: 8 pp more likely to export (p < 0.05)
  \item No significant difference in productivity or age
  \item [Minimal table: 4 key variables, treatment vs. control means]
\end{itemize}
\end{frame}
```

Why good: each slide has one job, 4 bullets max, bullet fragments not full
sentences, title is a conclusion.
