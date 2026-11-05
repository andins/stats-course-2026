# EDA Basics (Exploratory Data Analysis)

**In plain terms:** before modeling or testing anything, look at your data — literally, with plots — from several angles.

## Why plots before models

Summary statistics can hide a lot. One example (Anscombe's quartet) shows four datasets with *identical* averages, variances, and correlations — but when plotted, one is a straight line, one is a curve, one has a single outlier driving everything, and one is nearly constant with one extreme point. The summary numbers do not distinguish these cases; the plots do.

## What to look at

A thorough first pass usually covers:

- **Missingness** — which columns have gaps, and how many? (see [Missing data](./missing-data.md))
- **Individual variables** — histograms for numeric columns, bar counts for categories. Do values look plausible, or are there typos/impossible values (negative LDL values, ages of 200)?
- **Pairs of variables** — scatterplots between numeric variables, box plots of a numeric variable split by a category. Looking for: does the relationship look linear or curved? Are there outliers? Does the pattern differ by subgroup?
- **Trends over time**, if there's a time/date column.

## Mia's example

Before testing anything, Mia plots LDL cholesterol by carrier status (boxplot), checks whether LDL is roughly bell-shaped within each group (histogram), scatter-plots LDL against age to see if that's a bigger driver than carrier status, and checks which samples have missing genotype calls or LDL measurements and why.

## This isn't "cheating"

One distinction matters here: checking data *quality* (impossible values, missingness, obvious outliers) is standard practice and is appropriate regardless of whether your analysis is exploratory or confirmatory. What the [previous page](./exploratory-vs-confirmatory.md) warns against is peeking at the *hypothesis itself* and letting what you see change which comparison you report as "the test." Looking at your data is not the issue; selecting which comparison to report after seeing the results is.

> **Do it yourself**
>
> - [How to: explore a dataset](./how-to/explore-a-dataset.md) — a checklist and code for data quality, distributions, pairs and trends.
> - [Notebook: EDA walkthrough](../notebooks/eda-walkthrough.ipynb) — practice on a made-up dataset with planted problems, or point it at your own CSV.

> **Learn more**
>
> - [Wickham, Çetinkaya-Rundel & Grolemund (2023)](https://r4ds.hadley.nz/EDA.html), *R for Data Science* (2nd ed., free online), Ch. 10 "Exploratory data analysis" — a hands-on walk-through of variation and covariation.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §2.3 "All graphs are comparisons", pp. 25–31 — how to make plots that answer a question.
> - Anscombe (1973), "Graphs in statistical analysis," *The American Statistician* 27(1), 17–21 — the classic case for plotting before summarizing.

---
**Previous:** [Exploratory vs. confirmatory](./exploratory-vs-confirmatory.md) · [Module home](./README.md) · **Next:** [Missing data →](./missing-data.md) · [Glossary](../glossary.md)
