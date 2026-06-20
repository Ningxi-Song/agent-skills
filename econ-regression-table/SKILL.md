---
name: econ-regression-table
description: >
  Format regression tables to economics journal standards. Use when user wants
  to create, format, or review regression result tables, mentions Stata/R/Python
  regression output, asks for "regression table", "estimation results",
  "summary statistics table", or discusses coefficient reporting conventions.
---

# Economics Regression Table

Produce regression tables that conform to economics journal conventions.
See [EXAMPLES.md](EXAMPLES.md) for complete specimen tables.

## Required Specification

Every regression table MUST include:

1. **Dependent variable** stated at top of the table.
2. **Coefficients** reported to **three decimal places**.
3. **Significance stars** attached to coefficients:
   - `***` p < 0.01
   - `**`  p < 0.05
   - `*`   p < 0.10
4. **Standard errors** in parentheses immediately below each coefficient.
5. **Fixed effects** row (YES/NO per specification) at bottom.
6. **R-squared** row.
7. **Observations** (sample size) row.
8. **Notes** section below the table with:
   - Exact text of significance declaration.
   - Variable definitions (what each regressor measures).
   - Variable units (currency, percentage points, log, etc.).
   - Data source (if known).
   - Any sample restrictions.

## Number Formatting Rules

| Element | Format | Example |
|---------|--------|---------|
| Coefficient | 3 decimal places | `0.123***` |
| Standard error | 3 decimal places | `(0.045)` |
| R-squared | 3 decimal places | `0.234` |
| t/z-statistic | 2 decimal places | `2.73` |

## Star Placement

Stars attach directly to coefficients, no space:
```
0.123***
0.045**
0.067*
-0.011
```

Standard errors never carry stars.

## Table Structure

```
                    (1)            (2)            (3)
VARIABLE_NAME      Model 1        Model 2        Model 3
----------------------------------------------------------
X1                 0.123***       0.098**        0.105***
                  (0.045)        (0.041)        (0.039)
X2                 0.067*         0.054          0.071*
                  (0.038)        (0.036)        (0.040)
X3                 0.210***       0.189***       0.201***
                  (0.052)        (0.049)        (0.051)
----------------------------------------------------------
Fixed Effects       YES            YES            YES
R-squared          0.234          0.287          0.312
Observations       1,234          1,234          1,234

Notes: Standard errors in parentheses.
*** p<0.01, ** p<0.05, * p<0.10.
[Variable definitions and units follow here...]
```

## Workflow

1. **Determine specification**: DV, key IVs, controls, fixed effects.
2. **Collect estimates**: coefficients, SEs, p-values from output.
3. **Assign stars** based on p-values per thresholds above.
4. **Build table** following structure — columns = models, rows = variables.
5. **Write notes**: significance legend, then each variable's definition and unit.
6. **Verify**: every coefficient has 3 decimals, every SE in parentheses, stars match p-values.
