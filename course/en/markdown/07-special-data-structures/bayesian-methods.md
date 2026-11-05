# Bayesian Methods

**In plain terms:** Bayesian statistics answers the same kinds of questions as everything earlier in this course, but reframes them as "how should my beliefs about an unknown quantity update, given this data?" instead of "how surprising would this data be if there were truly no effect?"

## The core idea

Instead of a single p-value, a Bayesian analysis produces a **posterior distribution**: a full probability distribution over the plausible values of whatever you're estimating (an effect size, a group's average, a regression coefficient), combining your data with a **prior** — your stated beliefs *before* seeing the data (which can be deliberately vague/uninformative if you don't want to assume much). From the posterior, you can report a **credible interval** — a range that can be interpreted as "there is a 95% chance the true value is in here," which is a more direct statement than a classical confidence interval allows.

## Why this is especially natural for the multilevel models in this module

The [partial-pooling / multilevel approach](./clustered-and-hierarchical-data.md) to grouped data — where small, noisy groups get pulled toward the overall average — is a Bayesian idea even when fit with classical ("frequentist") software: the "pooling" is mathematically a built-in prior belief that groups are similar to each other. A fully Bayesian version of the same model makes this explicit and lets you add other sensible prior beliefs on top of it, and tends to behave better with small or sparse groups, where classical software can struggle or give unstable estimates. The same goes for a [meta-analysis](./meta-analysis.md), which is a multilevel model with studies as groups: with only a handful of studies, a prior on how much the true effects differ between studies is often more stable than estimating that spread from the data alone.

## Tools, if you want to go this route

- **PyMC**: a Python library for building Bayesian models directly and flexibly — you write out exactly what you believe about each unknown quantity. More control, more code.
- **Bambi**: a simpler interface built on top of PyMC, which lets you describe many common models (including multilevel ones) with a short formula, similar in spirit to how you'd write a regression formula elsewhere in this course. Usually the faster way in, unless you need a custom model PyMC gives you more direct control over.

## Should you reach for this?

Not by default. It is a heavier tool, useful when you need a full distribution over an estimate (not just a point and an interval), when there are many small/sparse groups, or when there is prior information worth incorporating formally. If you are not sure you need it, the classical (non-Bayesian) version of the same model from [Clustered and hierarchical data](./clustered-and-hierarchical-data.md) is a reasonable place to start.

> **Learn more**
>
> - [Johnson, Ott & Dogucu (2022)](https://www.bayesrulesbook.com/), *Bayes Rules! An Introduction to Applied Bayesian Modeling* (free online), Ch. 1–2 for the core idea and Ch. 15–17 for hierarchical models.
> - McElreath (2020), *Statistical Rethinking* (2nd ed.), Ch. 2 "Small Worlds and Large Worlds" and Ch. 13 "Models With Memory".
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §9.5 "Uniform, weakly informative, and informative priors in regression", pp. 123–128.

---
**Previous:** [Meta-analysis: bias and pitfalls](./meta-analysis-pitfalls.md) · [Module home](./README.md) · [Home](../README.md) · [Glossary](../glossary.md)
