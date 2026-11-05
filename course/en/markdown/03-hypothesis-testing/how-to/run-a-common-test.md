# How to: run a common test and report it properly

**Use this when:** you have a specific comparison that was decided *before* looking at the data (see [Exploratory vs. confirmatory](../../02-exploring-data/exploratory-vs-confirmatory.md)) and want to run the matching classical test. The test table is on the [Common tests](../common-tests.md) page; the p-value caveats are on [P-values and significance](../p-values-and-significance.md).

## Steps

1. **Pick the recipe below** from the type of outcome and the design: two independent groups, the same units measured twice, three or more groups, two categories, or two numbers.
2. **Check the assumptions** with the plots in [How to: check a test's assumptions](./check-test-assumptions.md) before trusting the result.
3. **Report the estimate and its confidence interval first**, the p-value second. "Carriers had LDL cholesterol 0.35 mmol/L higher (95% CI 0.12 to 0.59)" tells the reader more than "p = 0.001".
4. **If the question is about a treatment's effect,** remember that a test only compares groups; whether the difference is *causal* depends on the design (see [Experiments vs. observational data](../../05-prediction-vs-causation/experiments-vs-observational-data.md)).

Every recipe below can also be written as a regression, which is easier to extend with covariates; see [How to: run a test as a regression](../../04-regression-basics/how-to/run-a-test-as-a-regression.md).

## Two independent groups: Welch's t-test

```python
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import CompareMeans, DescrStatsW

df = pd.read_csv("my_data.csv")
carriers = df.loc[df["carrier_status"] == "carrier", "ldl_mmol"].dropna()
non_carriers = df.loc[df["carrier_status"] == "non-carrier", "ldl_mmol"].dropna()

diff = carriers.mean() - non_carriers.mean()
low, high = CompareMeans(DescrStatsW(carriers), DescrStatsW(non_carriers)).tconfint_diff(usevar="unequal")
welch = stats.ttest_ind(carriers, non_carriers, equal_var=False)

pooled_sd = np.sqrt(((len(carriers) - 1) * carriers.var() + (len(non_carriers) - 1) * non_carriers.var())
                    / (len(carriers) + len(non_carriers) - 2))
print(f"difference in means {diff:.2f} mmol/L (95% CI {low:.2f} to {high:.2f}); "
      f"Cohen's d = {diff / pooled_sd:.2f}; Welch p = {welch.pvalue:.3f}")

# If the data are far from bell-shaped or have outliers: rank-based alternative
print(stats.mannwhitneyu(carriers, non_carriers))
```

Welch's version doesn't assume equal variances and costs almost nothing when they are equal, so use it by default.

## The same units measured twice: paired t-test

```python
paired = pd.read_csv("my_paired_data.csv")   # one row per patient
change = paired["bp_after"] - paired["bp_before"]

low, high = DescrStatsW(change).tconfint_mean()
print(f"mean change {change.mean():.1f} mmHg (95% CI {low:.1f} to {high:.1f}); "
      f"paired t-test p = {stats.ttest_rel(paired['bp_after'], paired['bp_before']).pvalue:.2g}")

# Rank-based alternative on the differences
print(stats.wilcoxon(change))
```

Analyze the *differences*; don't run the independent-groups test on paired data.

## Three or more groups: one-way ANOVA

```python
groups = [values.dropna() for _, values in df.groupby("genotype")["ldl_mmol"]]
print(stats.f_oneway(*groups))                      # overall: do the groups differ at all?

summary = df.groupby("genotype")["ldl_mmol"].agg(["count", "mean", "sem"])
summary["ci_low"] = summary["mean"] - stats.t.ppf(0.975, summary["count"] - 1) * summary["sem"]
summary["ci_high"] = summary["mean"] + stats.t.ppf(0.975, summary["count"] - 1) * summary["sem"]
print(summary.round(2))                              # each group's mean with its own 95% CI

from statsmodels.stats.multicomp import pairwise_tukeyhsd
clean = df.dropna(subset=["ldl_mmol"])
print(pairwise_tukeyhsd(clean["ldl_mmol"], clean["genotype"]))   # pairwise differences with CIs, adjusted for multiplicity

print(stats.kruskal(*groups))                       # rank-based alternative
```

The overall F-test only says "not all groups are equal". The pairwise table is what answers "which ones, and by how much"; see [Multiple comparisons](../multiple-comparisons.md) for why the adjustment matters.

## Two categories: chi-squared test

```python
from statsmodels.stats.proportion import confint_proportions_2indep

table = pd.crosstab(df["treatment"], df["disease"])
chi2, p, dof, expected = stats.chi2_contingency(table)

counts = table["yes"]
totals = table.sum(axis=1)
print((counts / totals).round(3))                    # share with the disease in each group
low, high = confint_proportions_2indep(counts.iloc[0], totals.iloc[0], counts.iloc[1], totals.iloc[1],
                                       compare="diff", method="newcomb")
print(f"difference in proportions {counts.iloc[0] / totals.iloc[0] - counts.iloc[1] / totals.iloc[1]:.3f} "
      f"(95% CI {low:.3f} to {high:.3f}); chi-squared p = {p:.3f}")

if (expected < 5).any():                             # small expected counts: use the exact test (2x2 tables)
    print(stats.fisher_exact(table))
```

Report the proportions in each group, not just the p-value.

## Two numbers: correlation

```python
pair = df[["age", "ldl_mmol"]].dropna()
r = stats.pearsonr(pair["age"], pair["ldl_mmol"])
low, high = r.confidence_interval()
print(f"r = {r.statistic:.2f} (95% CI {low:.2f} to {high:.2f}), p = {r.pvalue:.3g}")

print(stats.spearmanr(pair["age"], pair["ldl_mmol"]))   # for curved-but-steadily-rising relationships or outliers
```

Always plot the scatter first: a single r can't tell a line from a curve or an outlier-driven pattern.

## Reading the output

Example output on made-up data, from the first (Welch) recipe:

```text
difference in means 0.35 mmol/L (95% CI 0.12 to 0.59); Cohen's d = 0.39; Welch p = 0.004
```

- **The difference and its CI** are the result. The CI shows the range of effects compatible with the data; if it spans differences that would matter in practice and ones that wouldn't, the study can't settle the question, whatever the p-value says.
- **Cohen's d** puts the difference in units of the outcome's SD, which is handy for comparing across studies and for [power calculations](../../01-planning-your-study/how-to/plan-a-sample-size.md). Around 0.2 is conventionally small, 0.5 medium and 0.8 large, but what matters is your field's scale, not those labels.
- **The p-value** answers a narrow question: how surprising would data like these be if there were truly no difference? Don't read a large p-value as "no effect" or a small one as "important".

## If it goes wrong

- **An assumption looks shaky:** run the alternative shown in each recipe and see whether the conclusion changes.
- **You ran several tests and are reporting the significant ones:** that is the multiple-comparisons problem, see [Multiple comparisons](../multiple-comparisons.md).
- **You chose the comparison after looking at the plots:** label it exploratory. A p-value from it is a lead, not a confirmation.
- **Your data are grouped or repeated** (relatives within families, several visits per patient): these tests assume independent observations; see [Clustered data](../../07-special-data-structures/clustered-and-hierarchical-data.md).
