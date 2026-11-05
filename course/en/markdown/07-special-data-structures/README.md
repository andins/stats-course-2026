# Module 7: Special Data Structures

Three situations that need more than the basic tests and models: observations that are not independent (grouped or time-ordered data), and data that are themselves a collection of studies.

## Pages

1. [Clustered and hierarchical data](./clustered-and-hierarchical-data.md) — when observations come in groups (patients in hospitals, relatives in families, repeated measures on the same subject).
2. [Time series data](./time-series-data.md) — when observations are ordered in time, and today might depend on yesterday.
3. [Meta-analysis](./meta-analysis.md) — combining the estimates from several studies of the same question, and measuring how much they disagree.
4. [Meta-analysis: bias and pitfalls](./meta-analysis-pitfalls.md) — why a pooled number can mislead: study selection, publication bias, mixing different studies.
5. [Bayesian methods](./bayesian-methods.md) — a different, optional, more advanced framework, relevant to the models in this module.

## Why these get their own module

Nothing earlier in this course breaks when data is clustered or time-ordered — it gives you overconfident results (standard errors that are too small, confidence intervals that are too narrow) unless you account for it. The first two pages cover recognizing when that is happening and what to do about it. Meta-analysis is the natural next step: a study is a cluster, so combining studies is a multilevel model whose observations are study-level estimates, and it is a tool to use when one study is rarely the last word.

## How-to guides

- [How to: analyze clustered data](./how-to/analyze-clustered-data.md), with a [clustered data notebook](../notebooks/clustered-data-overconfidence.ipynb)
- [How to: run a meta-analysis](./how-to/run-a-meta-analysis.md)

> **Learn more**
>
> - Gelman & Hill (2007), *Data Analysis Using Regression and Multilevel/Hierarchical Models*, Ch. 11 "Multilevel structures" and Ch. 12 "Multilevel linear models: the basics".
> - [Hyndman & Athanasopoulos (2021)](https://otexts.com/fpp3/), *Forecasting: Principles and Practice* (3rd ed., free online), §2.8 "Autocorrelation" and Ch. 10 "Dynamic regression models".
> - [Harrer, Cuijpers, Furukawa & Ebert (2021)](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/), *Doing Meta-Analysis with R: A Hands-On Guide* (free online) — for meta-analysis.

---
**Previous module:** [Building models](../06-building-models/README.md) · [Home](../README.md) · [Glossary](../glossary.md)
