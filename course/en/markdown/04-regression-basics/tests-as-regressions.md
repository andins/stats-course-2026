# Tests as Regressions

**In plain terms:** the "named" tests from Module 3 aren't a separate toolbox — each one is a regression, wearing a different hat.

## Some concrete equivalences

| Named test | Regression equivalent |
|---|---|
| Two-sample t-test | Regress the outcome on a single yes/no (0/1) predictor for group membership. The slope *is* the difference in means. |
| One-way ANOVA | Regress the outcome on a categorical predictor with one dummy variable per group (minus one). The overall test *is* the ANOVA F-test. |
| Chi-squared test of independence | Logistic regression of one categorical variable on the other. |
| Correlation significance test | The slope's test in a simple regression of y on x. |

This reflects that all of these tests ask the same underlying question ("does this grouping/variable explain variation in the outcome?"), packaged for specific, simple cases.

## Why this matters practically

Once a test is written as "a regression with one predictor," extending it is straightforward:

- **Need to add a covariate?** (e.g. control for age while comparing genotype classes) Just add it as another term in the regression. There's no separate "ANCOVA test" to look up — it's the same regression with one more predictor.
- **Unequal variability across groups?** Fit the same regression but ask for *robust standard errors* — this reproduces Welch's t-test without needing a differently-named procedure.
- **Clustered or repeated data?** Same regression, different standard-error calculation, or a mixed-effects version — see [Clustered and hierarchical data](../07-special-data-structures/clustered-and-hierarchical-data.md).

## The takeaway

If a classical test feels like a dead end — it doesn't let you add the covariate you need, or handle the complication your data has — the fix is almost always "write it as a regression and modify from there," not "search for a more exotic named test."

> **Do it yourself**
>
> [How to: run a test as a regression](./how-to/run-a-test-as-a-regression.md) — each classical test next to its regression form, with numbers that match.

> **Learn more**
>
> - [Lindeløv (2019)](https://lindeloev.github.io/tests-as-linear/), "Common statistical tests are linear models" (free online) — each named test next to its `lm()` equivalent, with R code.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §7.3 (pp. 99–101) and §10.5 "Formulating paired or blocked designs as a regression problem" (pp. 139–140).

---
**Previous:** [What is regression](./what-is-regression.md) · [Module home](./README.md) · **Next:** [Generalized linear models →](./generalized-linear-models.md) · [Glossary](../glossary.md)
