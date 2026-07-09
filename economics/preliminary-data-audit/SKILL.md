---
name: preliminary-data-audit
description: Produce a preliminary audit of a dataset by summarizing what the data are, their structure, coverage, units, variables, and basic dimensions. Use when first inspecting CSV, Excel, Stata, R, Python, or panel/cross-sectional datasets before deeper cleaning, analysis, or modeling.
---

# Preliminary Data Audit

Use this skill to give a first-pass description of a dataset. The goal is to help the user quickly understand what the dataset is, how it is organized, and what basic details define its coverage and contents.

Do not focus on research design, causal identification, regression readiness, or advanced cleaning unless the user explicitly asks for those.

## Workflow

1. Briefly introduce the dataset:
   - State what the dataset appears to measure.
   - Mention the main subject, sector, or topic.
   - Mention the broad geographic and time context when visible.
   - State the geographic scope when visible: national, subnational, regional, selected locations, or unclear.
   - Use a plain sentence, such as: "This is a county-level panel dataset of PM2.5 intensity in China."

2. Describe the data structure:
   - Identify whether the data appear to be panel, cross-sectional, time series, repeated cross-section, or unclear.
   - Identify the unit of observation.
   - Identify the geographic unit, such as country, province, city, county, grid cell, firm, household, or individual.
   - Identify the geographic coverage separately from the geographic unit: which country, states, provinces, cities, regions, or sample locations are included.
   - Say whether the coverage appears comprehensive for that geography, such as national coverage, all counties in a country, selected regions only, or unknown.
   - Identify the time period covered.
   - Identify the time frequency, such as daily, monthly, quarterly, yearly, or irregular.
   - If the data are panel data, note whether the panel appears balanced or unbalanced when this can be checked.

3. Summarize data details:
   - Number of observations.
   - Number of variables.
   - Key identifier variables.
   - Key time variables.
   - Main measurement variables.
   - Variable types, such as numeric, categorical, date/time, or text.
   - Obvious units, labels, or coding conventions.

4. Note immediate ambiguities:
   - Unclear row meaning.
   - Missing or unclear ID variables.
   - Missing or unclear time variables.
   - Ambiguous geographic units.
   - Ambiguous geographic coverage, such as whether the data are national or only cover selected regions.
   - Variable names that require a codebook.
   - Obvious duplicates or gaps in coverage.

## Output

Return a concise preliminary audit memo with these sections:

- Brief data introduction
- Data structure
- Geographic coverage
- Data details
- Immediate questions or concerns
- Suggested next checks

Keep the memo descriptive and practical. Prefer concrete statements backed by observed columns, row counts, time ranges, and examples from the dataset. If something is inferred rather than directly documented, say so.
