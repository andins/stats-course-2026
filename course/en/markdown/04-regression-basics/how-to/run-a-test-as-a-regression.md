# How to: run a classical test as a regression

**Use this when:** you want an estimate with a confidence interval from a named test *and* the freedom to add a covariate, relax an assumption or handle clustering without switching tools. The idea is on the [Tests as regressions](../tests-as-regressions.md) page; the classical recipes are in [How to: run a common test](../../03-hypothesis-testing/how-to/run-a-common-test.md).

## Steps

1. **Write the comparison as a formula**: `outcome ~ predictor`. A yes/no or category on the right-hand side becomes dummy variables automatically.
2. **Fit it** with `statsmodels` and read the coefficient of interest with its confidence interval.
3. **Check that it matches the classical test** (once, to build trust). The numbers below do.
4. **Extend it:** add covariates, ask for robust standard errors, or cluster; the extension is one more argument, not a new procedure.

## Two groups: t-test as regression

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv("my_data.csv").dropna(subset=["ldl_mmol"])
df["carrier"] = (df["carrier_status"] == "carrier").astype(int)   # 0/1 group indicator (carrier = 1)

ols = smf.ols("ldl_mmol ~ carrier", data=df).fit()
print(ols.summary().tables[1])        # the 'carrier' row IS the difference in means, with its 95% CI

# Same thing as Student's t-test (equal variances assumed):
a = df.loc[df["carrier"] == 1, "ldl_mmol"]
b = df.loc[df["carrier"] == 0, "ldl_mmol"]
print("Student p:", round(stats.ttest_ind(a, b).pvalue, 4), "| regression p:", round(ols.pvalues["carrier"], 4))

# Close to Welch's t-test (unequal variances allowed): robust standard errors
robust = smf.ols("ldl_mmol ~ carrier", data=df).fit(cov_type="HC3")
print("Welch p:  ", round(stats.ttest_ind(a, b, equal_var=False).pvalue, 4), "| robust regression p:", round(robust.pvalues["carrier"], 4))
print(robust.conf_int().loc["carrier"].round(2).tolist(), "<- 95% CI for the difference")
```

## Three or more groups: ANOVA as regression

```python
anova_model = smf.ols("ldl_mmol ~ C(genotype)", data=df).fit()
print(sm.stats.anova_lm(anova_model, typ=2))                  # the F-test of classical one-way ANOVA
print("scipy F:", stats.f_oneway(*[g for _, g in df.groupby("genotype")["ldl_mmol"]]).statistic.round(3))
print(anova_model.params.round(2))                            # differences from the reference genotype
```

## Adding a covariate (what a plain test can't do)

```python
adjusted = smf.ols("ldl_mmol ~ carrier + age", data=df).fit(cov_type="HC3")
print(adjusted.params.round(3))
print(adjusted.conf_int().round(3))
```

The `carrier` coefficient is now the difference between groups *at the same age*. Adjusting for a covariate that was measured before the exposure or treatment was assigned often tightens the interval (this is what "ANCOVA" is). For the question of *which* covariates to include when the exposure was not randomized, see [How to: draw and use a causal diagram](../../05-prediction-vs-causation/how-to/draw-and-use-a-causal-diagram.md).

## Two categories: chi-squared as logistic regression

```python
df["sick"] = (df["disease"] == "yes").astype(int)
logit = smf.logit("sick ~ C(treatment)", data=df).fit(disp=False)

print("odds ratios:\n", np.exp(logit.params).round(2))
print("95% CI for the odds ratios:\n", np.exp(logit.conf_int()).round(2))
print("likelihood-ratio p:", round(logit.llr_pvalue, 4))
chi2_p = stats.chi2_contingency(pd.crosstab(df["treatment"], df["disease"]), correction=False)[1]
print("chi-squared p:", round(chi2_p, 4))
```

## Two numbers: correlation as a slope

```python
slope = smf.ols("ldl_mmol ~ age", data=df).fit()
print(slope.summary().tables[1])
print("slope p:", round(slope.pvalues["age"], 4), "| Pearson p:", round(stats.pearsonr(df["age"], df["ldl_mmol"]).pvalue, 4))
```

The slope's p-value is the same as the correlation test's. The slope has the extra advantage of being in useful units (mmol/L per year of age).

## Reading the output

| Classical test | Regression formula | Quantity to read |
|---|---|---|
| Two-sample t-test | `y ~ group` | the group coefficient: the difference in means |
| Paired t-test | `diff ~ 1` | the intercept: the mean change |
| One-way ANOVA | `y ~ C(group)` | the F-test from `anova_lm`; coefficients are differences from the reference group |
| Chi-squared (2 categories) | `smf.logit("outcome01 ~ C(group)")` | odds ratios and the likelihood-ratio p-value |
| Correlation | `y ~ x` | the slope (standardize both variables to get r) |

The p-values match to the printed digits for Student, ANOVA and correlation. The chi-squared and logistic p-values are asymptotically equivalent, so they are close rather than identical, and the robust (HC3) version is close to Welch's but not the same calculation.

## If it goes wrong

- **Which coefficient is the "difference"?** Dummy coding compares each group to a reference; for a 0/1 indicator you control the direction. For a text column, `C(group, Treatment(reference="non-carrier"))` chooses the reference.
- **Residuals look wrong:** the plots in [How to: check a test's assumptions](../../03-hypothesis-testing/how-to/check-test-assumptions.md) apply to the regression's residuals. Robust standard errors fix unequal variances, not a wrong functional form.
- **Observations aren't independent** (several relatives per family, repeated visits): add `cov_type="cluster", cov_kwds={"groups": df["family"]}`, or see [How to: analyze clustered data](../../07-special-data-structures/how-to/analyze-clustered-data.md).
- **A coefficient is a causal claim only if the design supports it.** A regression doesn't turn an observational association into an effect.
