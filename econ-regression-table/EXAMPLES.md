# Regression Table Examples

Each example follows: coefficients to 3 decimal places, standard errors in parentheses,
stars * p<0.10, ** p<0.05, *** p<0.01.

---

## Example 1: Cross-Sectional Wage Regression

**Dependent variable:** Log hourly wage

```
                    (1)            (2)            (3)
                    OLS            OLS            OLS
----------------------------------------------------------
Education          0.085***       0.072***       0.068***
                  (0.004)        (0.004)        (0.004)
Experience         0.034***       0.030***       0.029***
                  (0.002)        (0.002)        (0.002)
Experience²/100   -0.056***      -0.049***      -0.047***
                  (0.005)        (0.004)        (0.004)
Female            -0.183***      -0.156***      -0.142***
                  (0.012)        (0.011)        (0.011)
Married                           0.087***       0.074***
                                  (0.013)        (0.013)
Union                                            0.123***
                                                (0.014)
Constant           1.523***       1.389***       1.305***
                  (0.060)        (0.058)        (0.057)
----------------------------------------------------------
Industry FE         NO             NO             YES
R-squared          0.302          0.318          0.345
Observations       2,534          2,534          2,534

Notes: Standard errors in parentheses.
*** p<0.01, ** p<0.05, * p<0.10.
Education: years of schooling completed.
Experience: years of potential labor market experience (age - education - 6).
Experience²/100: squared experience divided by 100.
Female: dummy variable, 1 if female, 0 if male.
Married: dummy variable, 1 if married, 0 otherwise.
Union: dummy variable, 1 if union member, 0 otherwise.
Industry FE: industry fixed effects (2-digit SIC).
Data source: Current Population Survey (CPS) 2023.
```

---

## Example 2: Panel Data with Firm Fixed Effects

**Dependent variable:** Log firm revenue

```
                    (1)            (2)            (3)
                    RE             FE             FE
----------------------------------------------------------
Log employment      0.612***       0.587***       0.563***
                  (0.023)        (0.025)        (0.024)
Log capital         0.298***       0.274***       0.289***
                  (0.019)        (0.021)        (0.020)
R&D intensity       0.045**        0.038*         0.041**
                  (0.022)        (0.020)        (0.019)
Export dummy                         0.067***       0.058**
                                   (0.024)        (0.023)
Leverage                                          -0.112***
                                                  (0.031)
Constant            2.156***       2.345***       2.401***
                  (0.145)        (0.152)        (0.148)
----------------------------------------------------------
Year FE              YES            YES            YES
Firm FE              NO             YES            YES
R-squared           0.612          0.678          0.694
Observations       12,450         12,450         12,450

Notes: Standard errors clustered at the firm level in parentheses.
*** p<0.01, ** p<0.05, * p<0.10.
Log employment: natural logarithm of number of employees.
Log capital: natural logarithm of fixed assets (thousands of CNY).
R&D intensity: R&D expenditure divided by total assets.
Export dummy: 1 if firm exports, 0 otherwise.
Leverage: total liabilities / total assets.
Year FE: year fixed effects.
Firm FE: firm fixed effects.
Data source: China Industrial Enterprise Database, 2005-2015.
```

---

## Example 3: Difference-in-Differences

**Dependent variable:** Employment rate (percentage points)

```
                    (1)            (2)            (3)
----------------------------------------------------------
Post × Treat        2.345***       1.987**        1.876**
                  (0.634)        (0.598)        (0.587)
Post                0.112         -0.045         -0.067
                  (0.423)        (0.401)        (0.398)
Treat               -1.234**      -0.987*        -0.934*
                  (0.512)        (0.534)        (0.528)
Population log                                     0.234
                                                  (0.189)
Constant           72.345***      68.234***      66.789***
                  (0.456)        (0.523)        (1.234)
----------------------------------------------------------
Year FE              NO             YES            YES
County FE            NO             NO             YES
R-squared           0.023          0.156          0.189
Observations        3,420          3,420          3,420

Notes: Standard errors clustered at the county level in parentheses.
*** p<0.01, ** p<0.05, * p<0.10.
Post: dummy, 1 for periods after policy implementation (2015+), 0 otherwise.
Treat: dummy, 1 for counties in the treatment group, 0 for control group.
Post x Treat: interaction term; the DiD estimator of the policy effect.
Population log: natural logarithm of county population.
Employment rate: employed persons / working-age population x 100.
Data source: County Statistical Yearbook, 2010-2020.
```

---

## Example 4: IV/2SLS Estimation

**Dependent variable:** Log GDP per capita

```
                    (1)            (2)
                    OLS            2SLS
----------------------------------------------------------
Institutions        0.456***       0.723***
                  (0.089)        (0.156)
Log population     -0.034         -0.041
                  (0.028)        (0.032)
Trade openness      0.123**        0.098*
                  (0.052)        (0.055)
Constant            6.789***       5.432***
                  (0.567)        (0.723)
----------------------------------------------------------
                                            First stage
Settler mortality                              -0.612***
                                              (0.098)
F-stat (excluded instrument)                    39.12
----------------------------------------------------------
Continent FE         YES            YES
R-squared           0.345          0.312
Observations          64             64

Notes: Standard errors in parentheses.
*** p<0.01, ** p<0.05, * p<0.10.
Institutions: index of protection against expropriation risk (0-10 scale,
higher = better institutions). Instrumented by log settler mortality in column (2).
Log population: natural logarithm of total population in 1995.
Trade openness: (exports + imports) / GDP.
Settler mortality: log of European settler mortality rate per 1,000.
F-stat: Kleibergen-Paap rk Wald F-statistic for weak instrument test.
Data source: Acemoglu, Johnson, and Robinson (2001).
```
