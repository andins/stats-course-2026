# Checking Assumptions

**In plain terms:** every classical test comes with fine-print conditions. Most of them are best checked by looking at a plot, not by running a second test.

## Common assumptions

- **Independence**: each observation shouldn't be informative about another (two measurements from the same patient are *not* independent of each other). This is usually a question about how the data was collected, not something a plot can fix after the fact — see [Clustered and hierarchical data](../07-special-data-structures/clustered-and-hierarchical-data.md) and [Time series data](../07-special-data-structures/time-series-data.md) if you suspect it's violated.
- **Normality**: many tests assume the data (or the model's errors) are roughly bell-shaped. Check with a histogram or a "QQ-plot" (a plot that's a straight diagonal line if the data is normal, and curves away from it if not).
- **Equal variability across groups** (homogeneity of variance): checked by comparing spread visually (boxplots) or with Levene's test.

## Why a plot usually beats a "test for the assumption"

It's tempting to run a formal test (like Shapiro-Wilk for normality) and treat its p-value as a yes/no verdict on whether you're "allowed" to use a given test. This doesn't work well in either direction:
- With a **small** sample, these assumption-tests have very little power to detect a real deviation — so "it passed" doesn't mean much.
- With a **large** sample, they become hyper-sensitive and will flag even trivial, harmless deviations as "significant."

A quick look at the plot, combined with asking "would this deviation change my conclusion?", is usually more informative than a single p-value about an assumption.

## What to do if an assumption looks shaky

You're rarely stuck — there's almost always a standard, well-understood fallback:

- Unequal variances → use Welch's t-test (or Welch's ANOVA) instead of the standard version.
- Not close to normal / has outliers → use a nonparametric test (Mann-Whitney, Kruskal-Wallis), a trimmed-mean/bootstrap approach, or a Bayesian alternative.
- Small expected counts in a chi-squared table → use Fisher's exact test instead.

The right response to "an assumption looks violated" is almost always "switch to the known, more robust alternative" — not "panic" or "ignore it and hope."

> **Do it yourself**
>
> [How to: check test assumptions](./how-to/check-test-assumptions.md) — the plots to make, what they should look like, and what to do when they don't.

> **Learn more**
>
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §11.1–11.3 "Assumptions of regression analysis" to "Residual plots", pp. 153–163 — which assumptions matter most, and how to check them graphically.
> - Rochon, Gondan & Kieser (2012), "To test or not to test: preliminary assessment of normality when comparing two independent samples," *BMC Medical Research Methodology* 12, 81 — why pre-testing assumptions is a poor default.
> - Delacre, Lakens & Leys (2017), *International Review of Social Psychology* 30(1), 92–101 — the case for Welch's test as the robust default.

---
**Previous:** [Common tests](./common-tests.md) · [Module home](./README.md) · **Next:** [Multiple comparisons →](./multiple-comparisons.md) · [Glossary](../glossary.md)
