"""
Worked template: two-sample t-test vs. its OLS-regression equivalent.

This is the structural pattern to adapt for other tests (see
references/test-regression-equivalents.md for the mapping, e.g. ANOVA ->
`y ~ C(group)`, chi-squared -> logistic/Poisson regression). When building a
notebook for a user, copy this pattern into notebook cells, keep the
"KEY PARAMETERS" block as an early, clearly-commented cell, and prefer
plotting over printing wherever both are possible.

Requires: numpy, scipy, pandas, statsmodels, matplotlib.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

# --------------------------------------------------------------------------
# KEY PARAMETERS -- change these to explore the behavior of the test(s).
# --------------------------------------------------------------------------
N_PER_GROUP = 30          # sample size per group
TRUE_EFFECT = 0.5         # true difference in means (in units of group A's SD)
SD_A, SD_B = 1.0, 1.0     # set SD_B != SD_A to explore heteroskedasticity
SKEW = 0.0                # set > 0 for right-skewed, non-normal data (via lognormal mix)
ALPHA = 0.05              # significance level
SEED = 0


def simulate(n=N_PER_GROUP, effect=TRUE_EFFECT, sd_a=SD_A, sd_b=SD_B, skew=SKEW, seed=SEED):
    """Simulate two independent groups with a known, controllable ground truth."""
    rng = np.random.default_rng(seed)

    if skew <= 0:
        a = rng.normal(loc=0.0, scale=sd_a, size=n)
        b = rng.normal(loc=effect, scale=sd_b, size=n)
    else:
        # lognormal shift gives a right-skewed, strictly-positive-noise sample
        a = rng.normal(0.0, sd_a, n) + rng.lognormal(mean=0.0, sigma=skew, size=n) - np.exp(skew ** 2 / 2)
        b = rng.normal(effect, sd_b, n) + rng.lognormal(mean=0.0, sigma=skew, size=n) - np.exp(skew ** 2 / 2)

    df = pd.DataFrame(
        {
            "value": np.concatenate([a, b]),
            "group": ["A"] * n + ["B"] * n,
        }
    )
    return df


def run_classical_tests(df: pd.DataFrame):
    a = df.loc[df["group"] == "A", "value"]
    b = df.loc[df["group"] == "B", "value"]

    student = stats.ttest_ind(a, b, equal_var=True)
    welch = stats.ttest_ind(a, b, equal_var=False)
    mannwhitney = stats.mannwhitneyu(a, b, alternative="two-sided")

    return {
        "student_t": {"statistic": student.statistic, "p_value": student.pvalue},
        "welch_t": {"statistic": welch.statistic, "p_value": welch.pvalue},
        "mann_whitney_u": {"statistic": mannwhitney.statistic, "p_value": mannwhitney.pvalue},
    }


def run_regression_equivalent(df: pd.DataFrame):
    """OLS with a dummy for group == the two-sample Student's t-test.

    Using HC3 (heteroskedasticity-consistent) standard errors reproduces the
    Welch-style robustness to unequal variances without a separate named test.
    """
    model = smf.ols("value ~ group", data=df).fit()
    model_robust = smf.ols("value ~ group", data=df).fit(cov_type="HC3")

    coef_name = [c for c in model.params.index if c != "Intercept"][0]
    return {
        "ols_classical_se": {
            "estimate": model.params[coef_name],
            "p_value": model.pvalues[coef_name],
        },
        "ols_hc3_robust_se": {
            "estimate": model_robust.params[coef_name],
            "p_value": model_robust.pvalues[coef_name],
        },
        "fitted_model": model,
    }


def compare(df: pd.DataFrame):
    classical = run_classical_tests(df)
    regression = run_regression_equivalent(df)

    summary = pd.DataFrame(
        [
            ("Student's t-test", classical["student_t"]["p_value"]),
            ("OLS (classical SE)", regression["ols_classical_se"]["p_value"]),
            ("Welch's t-test", classical["welch_t"]["p_value"]),
            ("OLS (HC3 robust SE)", regression["ols_hc3_robust_se"]["p_value"]),
            ("Mann-Whitney U", classical["mann_whitney_u"]["p_value"]),
        ],
        columns=["method", "p_value"],
    )
    return summary, classical, regression


if __name__ == "__main__":
    data = simulate()
    summary, classical, regression = compare(data)
    print(summary.to_string(index=False))
    print(
        "\nNote: Student's t-test p-value should match the classical-SE OLS "
        "p-value almost exactly, and Welch's t-test should closely track the "
        "HC3-robust OLS p-value -- that correspondence is the point of this "
        "comparison (see references/test-regression-equivalents.md)."
    )
