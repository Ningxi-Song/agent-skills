# Summary Statistics Table Examples

Each example follows: clear sample documentation, variable definitions with units,
mean/SD/N per group, difference test, full notes.

---

## Example 1: Standard Summary Statistics (Single Sample)

```
Table 1. Summary Statistics

                         Mean      SD     Median    p25     p75       N
------------------------------------------------------------------------
Dependent variable
  Log wage               3.456   0.623     3.412   3.013   3.834   2,534
  Employed (0/1)         0.723   0.447     1.000   0.000   1.000   2,534

Key independent variables
  Education (years)     12.345   3.211    12.000  10.000  14.000   2,534
  Experience (years)    18.234  11.456    17.000   9.000  26.000   2,534
  Female (0/1)           0.487   0.500     0.000   0.000   1.000   2,534
  Married (0/1)          0.612   0.487     1.000   0.000   1.000   2,534
  Union member (0/1)     0.143   0.350     0.000   0.000   0.000   2,534

Control variables
  SMSA resident (0/1)    0.456   0.498     0.000   0.000   1.000   2,534
  Region: Northeast       0.234   0.423     0.000   0.000   0.000   2,534
  Region: Midwest         0.267   0.442     0.000   0.000   1.000   2,534
  Region: South           0.312   0.463     0.000   0.000   1.000   2,534
  Region: West            0.187   0.390     0.000   0.000   0.000   2,534

Notes: Log wage is the natural logarithm of hourly wage in 2023 USD.
Education is years of completed schooling.
Experience is potential experience (age - education - 6).
SMSA: Standard Metropolitan Statistical Area.
Data source: Current Population Survey (CPS) Outgoing Rotation Groups, 2023.
Sample restricted to individuals aged 25-64, working 20+ hours per week.
Winsorized at 1st and 99th percentiles: log wage, experience.
```

---

## Example 2: By-Group Comparison with Difference Test

```
Table 1. Summary Statistics and Balance Test

                     Full Sample   Treatment    Control    Diff.
                       (N=800)      (N=200)     (N=600)   (T - C)
------------------------------------------------------------------
Panel A: Outcome variables
  Employment rate       68.345        72.456      66.912     5.544***
  (percentage points)  (12.345)     (11.234)    (12.567)
                        [800]        [200]       [600]

  Log monthly earnings   7.234         7.345       7.198     0.147**
  (log CNY)             (0.567)      (0.523)     (0.578)
                        [800]        [200]       [600]

Panel B: Household characteristics
  Household size         3.456         3.512       3.438     0.074
  (persons)             (1.234)      (1.198)     (1.245)
                        [800]        [200]       [600]

  Age of household head 45.234        44.987      45.312    -0.325
  (years)               (11.345)     (10.876)    (11.512)
                        [800]        [200]       [600]

  Female head (0/1)      0.234         0.245       0.231     0.014
                         (0.423)      (0.431)     (0.422)
                        [800]        [200]       [600]

  Education of head     10.234         9.876      10.345    -0.469
  (years)               (3.456)      (3.234)     (3.512)
                        [800]        [200]       [600]

Panel C: County-level characteristics
  Log population        12.345        12.234      12.378    -0.144
  (log persons)         (1.234)      (1.256)     (1.223)
                        [800]        [200]       [600]

  Fiscal revenue p.c.    3.456         3.512       3.438     0.074
  (thousand CNY)        (1.234)      (1.198)     (1.245)
                        [800]        [200]       [600]

------------------------------------------------------------------
Notes: Standard deviations in parentheses. Observations in brackets.
*** p<0.01, ** p<0.05, * p<0.10 for t-test of difference in means.
Employment rate: employed persons / working-age population x 100.
Log monthly earnings: natural logarithm of monthly earnings in CNY.
Household size: number of persons in household.
Female head: 1 if household head is female, 0 otherwise.
Fiscal revenue p.c.: fiscal revenue per capita, in thousand CNY.
All monetary variables deflated to 2020 constant CNY using provincial CPI.
Data source: County Statistical Yearbook matched to household survey, 2015.
Treatment defined as counties receiving the pilot policy in 2016.
Sample restricted to counties with complete pre-treatment data for 2013-2015.
```

---

## Example 3: Sample Selection with Attrition Table

```
Table 1. Sample Selection

                                     Observations    Mean of
Step                                 retained        log wage
------------------------------------------------------------------
1. CPS ORG full sample, 2023           167,234         3.512
2. Drop age < 25 or age > 64          -32,456          3.567
   Working sample, ages 25-64          134,778         3.489
3. Drop hours < 20                     -18,234         3.534
   Working sample, full-time           116,544         3.478
4. Drop self-employed                   -8,234         3.612
   Wage and salary workers             108,310         3.456
5. Drop missing education               -1,234         3.423
   Estimation sample                   107,076         3.456

Notes: CPS ORG = Current Population Survey Outgoing Rotation Groups.
Hours: usual weekly hours worked.
Self-employed: incorporated and unincorporated self-employed excluded.
Education missing rate: 1.1% of wage and salary workers, comparable
to the 1.0% rate in the full CPS sample (no systematic bias).
The estimation sample is 64.0% of the original ORG sample.
The mean log wage of the estimation sample (3.456) is close to the
full-sample mean (3.512), suggesting limited selection on the outcome.
```

---

## Example 4: Detailed Variable Definition Table

```
Table 1. Variable Definitions and Summary Statistics

Variable          Definition                              Mean     SD       N
--------------------------------------------------------------------------------
Dependent variable
  log_revenue     Log of annual operating revenue         9.234   1.456   12,450
                  (thousand CNY, deflated to 2015)

Key independent variables
  log_employment  Log of number of employees              5.123   1.234   12,450
  log_capital     Log of net fixed assets                 8.567   1.678   12,450
                  (thousand CNY, deflated to 2015)
  rd_intensity    R&D expenditure / total assets          0.034   0.045   12,450
                  (winsorized at 1st and 99th percentiles)
  export          Dummy = 1 if export revenue > 0         0.234   0.423   12,450
  foreign         Dummy = 1 if foreign equity > 25%       0.189   0.392   12,450
  leverage        Total liabilities / total assets        0.567   0.234   12,450
  firm_age        Current year - founding year + 1       12.456   8.912   12,450
  soe             Dummy = 1 if state ownership > 50%      0.089   0.285   12,450

Fixed effects
  industry_2digit 2-digit industry code (GB/T 4754)          89 categories
  province        31 province-level administrative regions   31 categories
  year            2005-2015                                  11 years

--------------------------------------------------------------------------------
Notes: All continuous variables winsorized at the 1st and 99th percentiles
unless otherwise noted.
All monetary values deflated to 2015 constant CNY using provincial-level
producer price indices from the China Statistical Yearbook.
Data source: China Industrial Enterprise Database (CIED), 2005-2015.
CIED covers all state-owned firms and non-state firms with annual
revenue above 5 million CNY (the "above-scale" threshold). This excludes
small and micro enterprises, which account for approximately 30% of
industrial output during the sample period. Results should be interpreted
as applying to above-scale industrial firms only.
```
