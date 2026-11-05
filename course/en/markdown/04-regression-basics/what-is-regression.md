# What Is Regression?

**In plain terms:** regression fits the "best" line (or curve) through your data, describing how one variable tends to change as another changes.

## The simplest case

Plot age (x-axis) against LDL cholesterol (y-axis) for Mia's 300 patients. Regression finds the straight line that best fits the cloud of points — described by two numbers: where the line crosses zero (the **intercept**) and how steeply it rises or falls (the **slope**, or **coefficient**). "LDL rises by 0.02 mmol/L for every extra year of age" is a slope, in plain English.

![Scatter plot of age against LDL cholesterol for 70 simulated patients with a rising regression line extended back to age 0. Annotations mark the intercept where the line meets age 0, the slope as the rise over 20 years, and one residual as the vertical gap between a patient and the line.](../figures/regression_anatomy.png)

*The parts of a fitted line: intercept, slope and residual. Simulated data.*

## Why it's more than "just a line"

Regression is not limited to one predictor. You can add carrier status, sex, and age into the same model, and each coefficient then tells you "the effect of this variable, *holding the others fixed*." This is more informative than a single two-group comparison — it separates "carrying the variant raised LDL" from "carriers in this sample happened to be older."

## Key vocabulary

- **Outcome / dependent variable**: the thing you're trying to explain or predict (LDL cholesterol).
- **Predictor(s) / independent variable(s)**: the things you think might explain it (carrier status, age).
- **Coefficient**: how much the outcome changes per unit change in a predictor, holding the others fixed.
- **Residual**: the gap between what the model predicted for a data point and what was observed. Good models have small, patternless residuals.

## Why this skill leans on regression so heavily

Regression reproduces t-tests, ANOVA, and chi-squared tests exactly (see [Tests as regressions](./tests-as-regressions.md)), extends naturally to yes/no or count outcomes (see [GLMs](./generalized-linear-models.md)), and is the standard tool for both prediction and causal-effect estimation (Module 5). The same framework covers most of the material in this course.

> **Learn more**
>
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §6.3 "Interpret coefficients as comparisons, not effects" (pp. 84–85) and §7.1 (pp. 93–97) for a worked single-predictor example.
> - [James, Witten, Hastie & Tibshirani (2021)](https://www.statlearning.com/), *An Introduction to Statistical Learning* (2nd ed., free online), §3.1 "Simple Linear Regression", pp. 61–71.
> - McElreath (2020), *Statistical Rethinking* (2nd ed.), Ch. 4 "Geocentric Models" — regression built up from a generative model.

---
**Previous:** [Module home](./README.md) · **Next:** [Tests as regressions →](./tests-as-regressions.md) · [Glossary](../glossary.md)
