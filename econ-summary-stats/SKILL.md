---
name: econ-summary-stats
description: >
  Produce summary (descriptive) statistics tables for economics papers.
  Use when user wants summary statistics, descriptive statistics, balance
  tables, "Table 1", sample description, variable means/SD, or treatment-control
  comparison tables. Covers data documentation, variable definitions, and
  sample transparency per top-journal standards.
---

# Economics Summary Statistics

Produce descriptive statistics tables that meet top economics journal standards.
See [EXAMPLES.md](EXAMPLES.md) for complete specimen tables.

## Core Principle

Good descriptive statistics are not a data dump -- they convince the reader that
the sample is reliable, variables are well-defined, treatment and control groups
are comparable, and subsequent identification and results carry economic meaning.

## Required Specification

Every summary statistics table MUST include:

### 1. Sample Documentation

State at minimum:
- **Data source** (survey name, administrative database, platform, etc.).
- **Time range** (start year -- end year).
- **Geographic coverage** (country, region, cities).
- **Unit of observation** (individual, firm, county-year, etc.).
- **Sample size** (N).
- **Selection rules** (any filters applied, sample restrictions, and why).

### 2. Variable Definitions

For every variable, specify:
- **Construction** (formula or raw source field).
- **Unit** (currency, percentage points, log, index, binary 0/1, etc.).
- **Transformation** (log-transformed, winsorized at which percentiles, standardized).

### 3. Statistics Beyond the Mean

Report **at minimum**: **Mean**, **SD**, **N**.
Report **ideally**: **Median**, **p25**, **p75**.
For skewed or bounded variables, also report: **p90**, **p99**, or **proportion of zeros**.

### 4. Treatment vs. Control Comparison

For any quasi-experimental or experimental design, show columns for:
- Full sample
- Treatment group
- Control group
- Difference in means (with significance test)

This establishes **pre-treatment comparability** on outcomes and key covariates.

### 5. Serve the Identification Strategy

The table should help the reader judge:
- Who is treated and who is the control group.
- Whether the control group is a credible counterfactual.
- Whether pre-treatment trends are plausibly parallel.
- Whether the sample is large enough and credible.

### 6. Representativeness and Limitations

Discuss:
- What the data covers and what it omits (e.g., informal sector, small firms, rural areas).
- Whether the sample is representative of the population of interest.
- Known selection issues (e.g., platform data covers only users of that platform).

### 7. Magnitude Context

Report a **baseline mean** for the dependent variable so the reader can assess
whether regression coefficients are economically meaningful (e.g., a
coefficient of 0.05 on log wage means ~5% higher earnings).

### 8. Transparent Sample Selection and Outlier Treatment

- Report sample attrition at each filtering step (how many observations lost).
- State how outliers or extreme values are handled (winsorization at 1%/99%,
  trimming at 4*IQR, or none).
- State whether the working sample differs systematically from the raw sample.

## Number Formatting Rules

| Element | Format | Example |
|---------|--------|---------|
| Mean / Median / SD | number of decimal places appropriate to variable scale | `3.456` or `0.034` |
| Count (N) | integer with thousands separator | `12,450` |
| Proportion (0-1) | 3 decimal places | `0.234` |
| Percentage (%) | 1 decimal place | `23.4` |
| Difference in means | same decimals as the variable | `0.034***` |

## Significance Stars for Balance Tests

- `***` p < 0.01
- `**`  p < 0.05
- `*`   p < 0.10

Report the t-test or standardized difference in the difference column.

## Table Structure (Full Sample + By Group)

```
                         Full Sample    Treatment     Control     Diff.
Variable                   (N=X)         (N=Y)        (N=Z)     (T - C)
------------------------------------------------------------------------
Outcome variable
  Mean                     0.345          0.389        0.312      0.077***
  SD                      (0.123)        (0.134)      (0.109)
  N                        12,450         4,180        8,270

Key covariate
  Mean                     2.567          2.612        2.534      0.078
  SD                      (1.234)        (1.287)      (1.198)
  N                        12,450         4,180        8,270
------------------------------------------------------------------------
Notes: [Significance legend.]
[Variable definitions, units, data source, sample restrictions.]
```

## Workflow

1. **Document the sample**: source, time, geography, unit, N, selection rules.
2. **Define all variables** with construction, units, transformations.
3. **Compute statistics**: mean, SD, N, median, p25, p75 per group.
4. **Difference test**: t-test or normalized difference for treatment vs control.
5. **Build the table**: columns = groups + difference column; rows = variables.
6. **Write notes**: significance legend, variable definitions, units, data source,
   sample restrictions, representativeness caveats.
7. **Verify**: each variable has mean, SD, N; treatment and control groups are
   identified; difference test reported; notes are complete.
