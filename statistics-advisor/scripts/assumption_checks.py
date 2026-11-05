"""
Assumption-checking helpers for classical statistical tests.

Use these as building blocks inside a simulation notebook (see SKILL.md ->
"Notebook workflow"). Each function returns the numeric diagnostic AND
produces/returns a plot, because single p-values from "assumption tests"
are an unreliable substitute for looking at the data (they're underpowered
at small n and over-sensitive at large n — see references/test-regression-
equivalents.md, "General diagnostics philosophy").

Requires: numpy, scipy, matplotlib, pandas, statsmodels (statsmodels only
needed for `check_residual_diagnostics` and `check_multicollinearity`).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools import add_constant


def check_normality(data, label: str = "", ax=None):
    """Shapiro-Wilk test + QQ-plot for a single sample.

    Returns
    -------
    dict with keys: statistic, p_value, n
    """
    data = np.asarray(data)
    stat, p = stats.shapiro(data)

    if ax is None:
        _, ax = plt.subplots(figsize=(4, 4))
    stats.probplot(data, dist="norm", plot=ax)
    ax.set_title(f"QQ-plot {label}\nShapiro-Wilk p={p:.3f} (n={len(data)})")

    return {"statistic": stat, "p_value": p, "n": len(data)}


def check_variance_homogeneity(*groups, labels=None):
    """Levene's test (robust to non-normality) for equal variance across groups.

    Pass each group's data as a separate positional argument.
    Returns dict with statistic, p_value, and per-group variance for inspection.
    """
    stat, p = stats.levene(*groups)
    variances = [np.var(g, ddof=1) for g in groups]
    labels = labels or [f"group{i}" for i in range(len(groups))]
    return {
        "statistic": stat,
        "p_value": p,
        "variances": dict(zip(labels, variances)),
        "variance_ratio_max_min": max(variances) / min(variances),
    }


def check_residual_diagnostics(fitted_ols_model, ax_qq=None, ax_resid=None):
    """Residual QQ-plot + residuals-vs-fitted for a fitted statsmodels OLS result.

    Pass the object returned by `smf.ols(...).fit()`.
    """
    resid = fitted_ols_model.resid
    fitted = fitted_ols_model.fittedvalues

    if ax_qq is None or ax_resid is None:
        _, (ax_qq, ax_resid) = plt.subplots(1, 2, figsize=(9, 4))

    stats.probplot(resid, dist="norm", plot=ax_qq)
    ax_qq.set_title("Residual QQ-plot")

    ax_resid.scatter(fitted, resid, alpha=0.6)
    ax_resid.axhline(0, color="red", linestyle="--", linewidth=1)
    ax_resid.set_xlabel("Fitted values")
    ax_resid.set_ylabel("Residuals")
    ax_resid.set_title("Residuals vs. fitted")

    shapiro_stat, shapiro_p = stats.shapiro(resid)
    return {"shapiro_statistic": shapiro_stat, "shapiro_p_value": shapiro_p}


def expected_counts_ok(contingency_table, min_expected: float = 5.0):
    """Check the common chi-squared rule of thumb on expected cell counts.

    `contingency_table`: 2D array-like of observed counts.
    Returns dict with the expected-counts table and whether the heuristic
    (all cells >= min_expected) is satisfied -- treat this as a heuristic,
    not a hard requirement; inspect the table itself too.
    """
    _, _, _, expected = stats.chi2_contingency(contingency_table)
    return {
        "expected": expected,
        "all_cells_ok": bool(np.all(expected >= min_expected)),
        "min_expected_cell": float(np.min(expected)),
    }


def check_multicollinearity(df, predictors):
    """Variance Inflation Factor (VIF) for a set of numeric predictors.

    Relevant whenever a model has more than one predictor/adjustment covariate
    (e.g. the causal-observational or predictive explanatory models in
    regression_modeling_template.py) -- high collinearity inflates coefficient
    standard errors and makes individual estimates unstable, even though
    overall model fit is unaffected.

    Rule of thumb: VIF > 5 is worth a look, > 10 is a clear warning sign --
    treat both as heuristics, not hard thresholds (OBRIEN_2007). Drops rows
    with missing values in `predictors` (see `prepare_model_data` in
    regression_modeling_template.py for the same default elsewhere).
    """
    X = add_constant(pd.DataFrame(df)[list(predictors)].dropna())
    vifs = pd.Series(
        [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
        index=X.columns,
    ).drop("const")
    return {
        "vif": vifs.to_dict(),
        "any_above_5": bool((vifs > 5).any()),
        "any_above_10": bool((vifs > 10).any()),
    }
