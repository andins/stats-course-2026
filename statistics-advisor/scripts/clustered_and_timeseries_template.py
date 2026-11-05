"""
Template: modeling choices for clustered/hierarchical data and time-dependent data.

Two topics bundled together because both are really the same question: "is the
independence assumption behind a plain (G)LM reasonable here, and if not, what's
the simplest adequate fix?"

## Clustered / hierarchical data

When observations come in groups (students in schools, repeated visits per
patient, stores in regions), pick one of three strategies -- in increasing
order of complexity and of information-sharing across groups:

- **Complete pooling** (`fit_complete_pooling`): ignore the grouping, fit one
  model on all the data. Simplest; fine when group differences aren't of
  interest and there's no reason the relationship of interest varies by
  group. Still use cluster-robust standard errors (`cluster_col=`) if
  observations within a group are correlated -- otherwise SEs are too small
  and p-values too optimistic even though the point estimate itself is fine.
- **No pooling** (`fit_no_pooling`): a separate intercept per group (a
  fixed-effect dummy per cluster). Best when there are few groups, each with
  enough data for its own stable estimate, and the groups themselves are the
  thing of interest (not a sample from a larger population of groups) -- e.g.
  comparing exactly these 4 manufacturing plants. Downside: groups with
  little data get noisy estimates, and the model can't generalize to a new,
  unseen group.
- **Partial pooling / multilevel** (`fit_multilevel`): group-level estimates
  are shrunk toward the overall mean, with the amount of shrinkage depending
  on how much data each group has (small/noisy groups get pulled further
  toward the pooled estimate). Best when there are many groups, especially
  with uneven group sizes, and/or the goal is to generalize to new groups not
  in the data (GELMAN_HILL_YAJIMA; MCELREATH_RETHINKING). More complex to fit
  and interpret -- **build this only if the user asks for a multilevel
  model**; default to complete or no pooling otherwise, picking between those
  two by context (few groups that are themselves the object of interest ->
  no pooling; groups are a nuisance, not the focus -> complete pooling +
  cluster-robust SEs).

## Time-dependent data

Don't assume a time-series-specific model is required just because a date
column exists -- check first:

1. **Check for residual autocorrelation** with `check_autocorrelation()` (ACF
   plot + Ljung-Box test) after fitting the plain (G)LM. If it's small/not
   significant, treating the data as iid is a reasonable approximation and
   the plain model is fine as is -- say so explicitly rather than reflexively
   reaching for a time-series model.
2. **If autocorrelation is present but modest, and inference (SEs/CIs) is the
   only concern**: refit with heteroskedasticity-and-autocorrelation-consistent
   (HAC / Newey-West) standard errors (`fit_regression_hac`) -- the point
   estimate is unchanged, only the SEs are corrected (NEWEY_WEST_1987).
3. **If the dependence structure itself matters** (forecasting, strong or
   seasonal autocorrelation): move to an actual time-series model -- an
   autoregressive term / lag of the outcome as a predictor, or a dedicated
   model (`statsmodels.tsa.arima.model.ARIMA` / `SARIMAX` for a univariate
   series with trend/seasonality, or a mixed model with an AR covariance
   structure for panel data). `sketch_arima_fit()` below is a minimal
   starting point, not a complete time-series workflow.

## Bayesian multilevel option (only if the user asks for it)

`fit_bayesian_multilevel()` fits the same partial-pooling model in PyMC,
using `bambi` (an lme4/brms-style formula interface on top of PyMC) when
available, which is usually the faster path unless the user needs a custom
likelihood/priors that PyMC gives direct control over (MCELREATH_RETHINKING).
Both are optional, heavier dependencies than the rest of this skill -- reach
for them only when Bayesian inference is specifically wanted.

Requires: pandas, numpy, statsmodels. Optional (Bayesian section only):
pymc, bambi, arviz (`pip install pymc bambi arviz`).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox

# --------------------------------------------------------------------------
# KEY PARAMETERS -- fill these in for the dataset/question at hand.
# --------------------------------------------------------------------------
DATA_PATH = None            # e.g. "mydata.csv"; synthetic demo data used if None
OUTCOME = "y"
PREDICTORS: list[str] = ["x"]
CLUSTER_COL = "cluster"
SEED = 0


def load_clustered_data(path=DATA_PATH, seed=SEED) -> pd.DataFrame:
    if path is not None:
        return pd.read_csv(path)
    rng = np.random.default_rng(seed)
    n_clusters, n_per_cluster = 20, 15
    cluster_ids = np.repeat(np.arange(n_clusters), n_per_cluster)
    cluster_intercepts = rng.normal(0, 1.5, n_clusters)  # true group-level variation
    x = rng.normal(0, 1, n_clusters * n_per_cluster)
    y = cluster_intercepts[cluster_ids] + 1.0 * x + rng.normal(0, 1, n_clusters * n_per_cluster)
    return pd.DataFrame({"x": x, "y": y, "cluster": cluster_ids})


def fit_complete_pooling(df: pd.DataFrame, outcome: str, predictors, cluster_col: str | None = None):
    """Ignore groups (or use cluster-robust SEs if `cluster_col` is given).

    Cluster-robust SEs correct inference for within-cluster correlation
    without changing the point estimate or requiring a separate model per cluster.
    """
    formula = f"{outcome} ~ {' + '.join(predictors)}"
    if cluster_col is not None:
        return smf.ols(formula, data=df).fit(cov_type="cluster", cov_kwds={"groups": df[cluster_col]})
    return smf.ols(formula, data=df).fit()


def fit_no_pooling(df: pd.DataFrame, outcome: str, predictors, cluster_col: str):
    """Separate intercept per cluster (fixed effects) -- best for a handful of
    clusters that are themselves of interest, each with enough data for a
    stable individual estimate.
    """
    formula = f"{outcome} ~ C({cluster_col}) + {' + '.join(predictors)}"
    return smf.ols(formula, data=df).fit()


def fit_multilevel(df: pd.DataFrame, outcome: str, predictors, cluster_col: str):
    """Partial-pooling (random-intercept) model via statsmodels MixedLM.

    Build this only when the user asks for a multilevel model specifically --
    default to `fit_complete_pooling`/`fit_no_pooling` otherwise.
    """
    formula = f"{outcome} ~ {' + '.join(predictors)}"
    return smf.mixedlm(formula, data=df, groups=df[cluster_col]).fit()


def fit_bayesian_multilevel(df: pd.DataFrame, outcome: str, predictors, cluster_col: str,
                             draws: int = 1000, chains: int = 4, seed: int = SEED):
    """Bayesian partial-pooling model -- only build this if the user asks for a Bayesian approach.

    Tries `bambi` first (formula interface on top of PyMC); falls back to a
    hand-written PyMC model if bambi isn't installed. Requires
    `pip install pymc bambi arviz` -- not part of this skill's baseline deps.
    """
    try:
        import bambi as bmb
    except ImportError:
        return _fit_bayesian_multilevel_pymc(df, outcome, predictors, cluster_col, draws, chains, seed)

    formula = f"{outcome} ~ {' + '.join(predictors)} + (1|{cluster_col})"
    model = bmb.Model(formula, data=df)
    idata = model.fit(draws=draws, chains=chains, random_seed=seed, progressbar=False)
    return model, idata


def _fit_bayesian_multilevel_pymc(df, outcome, predictors, cluster_col, draws, chains, seed):
    import pymc as pm

    cluster_codes, cluster_labels = pd.factorize(df[cluster_col])
    X = df[list(predictors)].to_numpy()
    y = df[outcome].to_numpy()

    with pm.Model() as model:
        mu_alpha = pm.Normal("mu_alpha", 0, 10)
        sigma_alpha = pm.HalfNormal("sigma_alpha", 10)
        alpha = pm.Normal("alpha", mu_alpha, sigma_alpha, shape=len(cluster_labels))
        beta = pm.Normal("beta", 0, 10, shape=X.shape[1])
        sigma = pm.HalfNormal("sigma", 10)
        mu = alpha[cluster_codes] + X @ beta
        pm.Normal("obs", mu, sigma, observed=y)
        idata = pm.sample(draws=draws, chains=chains, random_seed=seed, progressbar=False)
    return model, idata


def load_time_series_data(n: int = 200, ar_coef: float = 0.0, seed: int = SEED) -> pd.DataFrame:
    """Synthetic demo series. `ar_coef` controls how much autocorrelation is baked
    into the noise -- 0.0 gives (near-)iid errors, closer to 1.0 gives strong
    autocorrelation, so the same loader can demonstrate both branches of the
    "is iid a fine approximation here?" decision above.
    """
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, n)
    noise = np.zeros(n)
    for t in range(1, n):
        noise[t] = ar_coef * noise[t - 1] + rng.normal(0, 1)
    y = 1.0 * x + noise
    return pd.DataFrame({"x": x, "y": y})


def check_autocorrelation(residuals, lags: int = 10, ax=None):
    """ACF plot + Ljung-Box test for leftover autocorrelation in model residuals.

    If the Ljung-Box p-value isn't small and the ACF plot shows no structure
    beyond sampling noise, treating the data as iid is a reasonable
    approximation -- say so explicitly rather than reaching for a
    time-series model by default.
    """
    residuals = np.asarray(residuals)
    lb = acorr_ljungbox(residuals, lags=[lags], return_df=True)
    if ax is None:
        import matplotlib.pyplot as plt
        _, ax = plt.subplots(figsize=(6, 4))
    plot_acf(residuals, lags=lags, ax=ax)
    p_value = float(lb["lb_pvalue"].iloc[-1])
    ax.set_title(f"Residual ACF (Ljung-Box p={p_value:.3f}, lags={lags})")
    return {"ljung_box_stat": float(lb["lb_stat"].iloc[-1]), "ljung_box_p_value": p_value}


def fit_regression_hac(df: pd.DataFrame, outcome: str, predictors, maxlags: int | None = None):
    """OLS with Newey-West (HAC) standard errors (NEWEY_WEST_1987).

    Fixes inference under residual autocorrelation without changing the point
    estimate or requiring a full time-series model. `maxlags` defaults to a
    common rule of thumb (n^(1/4)) if not given.
    """
    formula = f"{outcome} ~ {' + '.join(predictors)}"
    maxlags = maxlags if maxlags is not None else int(len(df) ** 0.25)
    return smf.ols(formula, data=df).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})


def sketch_arima_fit(series, order=(1, 0, 0)):
    """Minimal ARIMA fit -- a starting point for when the dependence structure
    itself matters (forecasting, strong/seasonal autocorrelation), not a
    complete time-series workflow.
    """
    from statsmodels.tsa.arima.model import ARIMA

    return ARIMA(series, order=order).fit()


if __name__ == "__main__":
    # --- Clustered data: compare complete pooling, no pooling, and multilevel. ---
    clustered = load_clustered_data()
    complete = fit_complete_pooling(clustered, OUTCOME, PREDICTORS, cluster_col=CLUSTER_COL)
    no_pool = fit_no_pooling(clustered, OUTCOME, PREDICTORS, CLUSTER_COL)
    multilevel = fit_multilevel(clustered, OUTCOME, PREDICTORS, CLUSTER_COL)
    print("Complete pooling (cluster-robust SE) slope on x:", complete.params["x"], "+/-", complete.bse["x"])
    print("No pooling slope on x:", no_pool.params["x"], "+/-", no_pool.bse["x"])
    print("Multilevel slope on x:", multilevel.params["x"], "+/-", multilevel.bse["x"])

    # --- Time series: negligible autocorrelation case. ---
    ts_iid = load_time_series_data(ar_coef=0.0)
    model_iid = fit_complete_pooling(ts_iid, "y", ["x"])
    diag_iid = check_autocorrelation(model_iid.resid)
    print("Near-iid noise -- Ljung-Box p-value:", diag_iid["ljung_box_p_value"], "(expect: not small)")

    # --- Time series: strong autocorrelation case -- HAC SE fixes inference. ---
    ts_ar = load_time_series_data(ar_coef=0.8)
    model_ar = fit_complete_pooling(ts_ar, "y", ["x"])
    diag_ar = check_autocorrelation(model_ar.resid)
    print("Strong AR(1) noise -- Ljung-Box p-value:", diag_ar["ljung_box_p_value"], "(expect: small)")
    model_ar_hac = fit_regression_hac(ts_ar, "y", ["x"])
    print("Plain OLS SE on x:", model_ar.bse["x"], " HAC SE on x:", model_ar_hac.bse["x"])
