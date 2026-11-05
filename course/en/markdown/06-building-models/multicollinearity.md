# Multicollinearity

**In plain terms:** if two of your predictors are themselves highly correlated with each other, a model can struggle to tell their individual effects apart — even if it can still predict the outcome just fine overall.

## A concrete picture

Suppose Mia records genotypes at two variants, A and B, that sit close together on the same chromosome. Variants that close tend to be inherited together — a pattern called **linkage disequilibrium** (LD) — so the number of copies of A and of B end up almost perfectly correlated across her patients. A regression trying to estimate the separate effects of variant A and variant B on LDL cholesterol will struggle: the data does not contain many people who carry one without the other, so there is little information left to distinguish "LDL responds to variant A specifically" from "LDL responds to variant B specifically." The individual coefficient estimates become unstable — small changes in the data can swing them wildly, or even flip their sign.

## What it does and doesn't break

- **What it breaks**: trust in any *individual* coefficient and its standard error/confidence interval — these become unreliable.
- **What it doesn't break**: the model's overall fit and its predictions. A model with severe multicollinearity can still predict LDL well — it just can't reliably tell you *which* of the two overlapping predictors is "doing the work."

This means multicollinearity mostly matters when your goal is to **interpret individual coefficients** (an explanatory/causal use), and matters much less when your only goal is **prediction**.

## How to check it: VIF

The **Variance Inflation Factor (VIF)** quantifies, for each predictor, how much its uncertainty is inflated by its correlation with the other predictors. A VIF around 1 indicates no issue; conventionally, VIF above 5 warrants a closer look and above 10 is a clear warning sign — treat these as rough guides, not hard cutoffs.

## What to do about it

- Drop one of the overlapping predictors, if they measure the same underlying thing.
- Combine them into a single composite variable, if that's substantively sensible.
- Collect more/different data where the predictors vary more independently of each other, if that's feasible.
- Or, if prediction (not interpretation) is the actual goal, consider leaving it as is and using [regularization](./overfitting-and-regularization.md) instead, which handles correlated predictors more gracefully than plain regression.

> **Do it yourself**
>
> [How to: check multicollinearity](./how-to/check-multicollinearity.md) — compute and read VIFs in a few lines of Python.

> **Learn more**
>
> - [James, Witten, Hastie & Tibshirani (2021)](https://www.statlearning.com/), *An Introduction to Statistical Learning* (2nd ed.), §3.3.3 "Potential Problems", the "Collinearity" item (pp. 100–103), including the VIF.
> - O'Brien (2007), "A caution regarding rules of thumb for variance inflation factors," *Quality & Quantity* 41(5), 673–690 — why VIF cutoffs of 5 or 10 are heuristics.
> - McElreath (2020), *Statistical Rethinking* (2nd ed.), Ch. 6, §6.1 "Multicollinearity".

---
**Previous:** [Cross-validation and model checking](./cross-validation-and-model-checking.md) · [Module home](./README.md) · **Next:** [Measurement error →](./measurement-error.md) · [Glossary](../glossary.md)
