# How to: check a test's assumptions

**Use this when:** you are about to run (or have run) a t-test, ANOVA, regression or chi-squared test and want to know whether its fine print is a problem. The reasoning is on the [Checking assumptions](../checking-assumptions.md) page.

## Steps

1. **Independence first, by thinking, not plotting.** Are there repeated measurements on the same unit, relatives in the same family, patients in the same clinic, or data ordered in time? If so, a plain test is overconfident; see [Clustered data](../../07-special-data-structures/clustered-and-hierarchical-data.md) and [Time series data](../../07-special-data-structures/time-series-data.md).
2. **Plot the data by group**: boxplots with the raw points, and a QQ-plot per group (for a regression, the residuals instead).
3. **Compare the spread** across groups with the plain numbers, not just a test.
4. **Ask whether it matters.** Run the standard analysis next to the robust alternative. If the conclusions agree, the shaky assumption isn't driving your result.
5. **If it does matter, switch** to the robust alternative (below) and report that.

## Code: groups and a numeric outcome

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

df = pd.read_csv("my_data.csv")
outcome, group = "ldl_mmol", "carrier_status"

groups = {name: values.dropna() for name, values in df.groupby(group)[outcome]}
fig, axes = plt.subplots(1, 1 + len(groups), figsize=(4.5 * (1 + len(groups)), 4))

sns.boxplot(data=df, x=group, y=outcome, ax=axes[0])
sns.stripplot(data=df, x=group, y=outcome, color="black", alpha=0.3, ax=axes[0])
for ax, (name, values) in zip(axes[1:], groups.items()):
    stats.probplot(values, plot=ax)          # QQ-plot: points on the line = bell-shaped
    ax.set_title(f"QQ-plot: {name}")
plt.tight_layout()
plt.show()

sds = pd.Series({name: values.std() for name, values in groups.items()})
print(sds.round(2))
print("SD ratio, largest / smallest:", round(sds.max() / sds.min(), 2))
```

## Code: a regression's residuals

For a regression (including ANOVA with covariates), check the *residuals* of the fitted model, not the raw outcome:

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

model = smf.ols(f"{outcome} ~ C({group}) + age", data=df).fit()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sm.qqplot(model.resid, line="s", ax=axes[0])
axes[0].set_title("Residual QQ-plot")
axes[1].scatter(model.fittedvalues, model.resid, alpha=0.6)
axes[1].axhline(0, color="red", linestyle="--")
axes[1].set(xlabel="fitted values", ylabel="residuals", title="Residuals vs. fitted")
plt.tight_layout()
plt.show()
```

## Code: does it matter? Standard next to robust

```python
a, b = list(groups.values())[:2]   # two groups
print("Student (equal variances):", stats.ttest_ind(a, b))
print("Welch (unequal variances):", stats.ttest_ind(a, b, equal_var=False))
print("Mann-Whitney (rank-based):", stats.mannwhitneyu(a, b))
```

## Code: chi-squared tables

```python
table = pd.crosstab(df["treatment"], df["disease"])
chi2, p, dof, expected = stats.chi2_contingency(table)
print(pd.DataFrame(expected, index=table.index, columns=table.columns).round(1))  # expected counts
if (expected < 5).any():
    print("Small expected counts; Fisher's exact test (2x2 tables):", stats.fisher_exact(table))
```

## Reading the plots

| What you see | What it means | What to do |
|---|---|---|
| QQ-plot points follow the line | Roughly bell-shaped | Nothing |
| Points curve away at one end, usually upward on the right | Right skew (common for triglycerides, concentrations, counts) | Consider a nonparametric test, a bootstrap, or analyzing on the log scale |
| Both ends peel away (an S shape) or a few isolated points | Heavy tails or outliers | Check the outliers are real; use robust standard errors or a rank-based test |
| One group's box is much taller than another's (a rough rule of thumb: SD ratio above 2) | Unequal variances | Welch's t-test / Welch's ANOVA, or a regression with robust standard errors |
| Residuals fan out as fitted values grow | Variance rises with the level | Robust standard errors (`cov_type="HC3"`), or model the log of the outcome |
| Residuals show a curve | The relationship isn't straight | Add a term (e.g. a squared term) or a different model |
| Expected counts below 5 | The chi-squared approximation is poor | Fisher's exact test |

## Calibrate your eye

QQ-plots are easy to misread the first time. These three samples are made up; look at what each shape looks like before judging your own data:

```python
import numpy as np

rng = np.random.default_rng(0)
samples = {
    "bell-shaped": rng.normal(size=100),
    "right-skewed": rng.lognormal(size=100),
    "heavy tails": rng.standard_t(2, size=100),
}
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, (name, values) in zip(axes, samples.items()):
    stats.probplot(values, plot=ax)
    ax.set_title(name)
plt.tight_layout()
plt.show()
```

## If it goes wrong

- **Don't treat a normality test as a verdict.** Shapiro-Wilk will pass almost anything at small n and flag trivial wiggles at large n; use it, if at all, as a supplement to the plot (`stats.shapiro(values)`).
- **Large samples forgive more.** With enough data per group, mild non-normality rarely changes a t-test's result; unequal variances (especially with unequal group sizes) and outliers matter more. That is why step 4 (compare with the robust version) is the practical check.
- **Rank-based tests don't compare means or medians in general.** They ask whether one group tends to produce larger values; say so when you report them.
- **Independence problems aren't fixed by switching tests.** They need a different model, not a different p-value.
