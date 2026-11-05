"""
Template: meta-analysis of study-level effect estimates.

Use when the unit of analysis is a *study*: the user has (or can extract) an
effect estimate and its standard error from each of several studies of the same
question and wants one combined answer, or asks about heterogeneity, forest or
funnel plots, or publication bias. If the user has the raw data from every
site, this is NOT the right tool: analyze it as clustered data with site as the
cluster (see clustered_and_timeseries_template.py).

What the helpers do, in the order a meta-analysis usually goes:

1. `effect_sizes_from_summaries()` -- put every study on one scale (raw mean
   difference, Hedges' g, log odds ratio, log risk ratio) from group summaries.
2. `pool_random_effects()` -- the default analysis: random-effects pooled
   estimate with CI, optional Hartung-Knapp interval (few studies), and the
   spread of the true effects: tau, I^2, Q and a prediction interval for a new
   study. Report the prediction interval, not just the CI of the mean
   (INTHOUT_2016). Also returns the common-effect estimate for comparison.
3. `forest_plot()` -- look at it before trusting any number.
4. `leave_one_out()` -- how fragile is the pooled estimate?
5. `funnel_plot()` and `egger_test()` -- publication bias / small-study
   effects. Weak with fewer than ~10 studies (STERNE_2011); a warning, not proof.

Defaults and cautions to state in the answer:
- Random effects is the default for life-science studies, which are rarely
  exact replications; choose the model by what is believed about the studies,
  not by which gives the smaller p-value (BORENSTEIN_2009).
- Pool estimates, never p-values or "significant / not significant" counts.
- With few studies (roughly under 5-10) tau^2 is poorly estimated: use
  `hksj=True` (INTHOUT_2014) or suggest a Bayesian model; say how few studies there are.
- A meta-analysis inherits the biases of its studies and of how they were
  found (selection, publication bias); say so, do not hide it behind a tight
  interval. Several estimates from the same study are not independent.
- Meta-regression/subgroup analyses are exploratory: study characteristics are
  not randomized. Not implemented here on purpose.

Requires: numpy, pandas, scipy, statsmodels, matplotlib.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.meta_analysis import combine_effects, effectsize_2proportions, effectsize_smd

# --------------------------------------------------------------------------
# KEY PARAMETERS -- fill these in for the dataset/question at hand.
# --------------------------------------------------------------------------
DATA_PATH = None             # e.g. "studies.csv"; synthetic demo data used if None
STUDY_COL = "study"          # study label
EFFECT_COL = "effect"        # effect estimate on ONE common scale (log scale for odds/risk ratios)
SE_COL = "se"                # standard error of that estimate (not the SD, not the variance)
TAU2_METHOD = "iterated"     # "iterated" (Paule-Mandel) or "dl" (DerSimonian-Laird)
HKSJ = False                 # True: Hartung-Knapp interval, recommended with few studies
SEED = 0


def load_study_data(path=DATA_PATH, seed=SEED) -> pd.DataFrame:
    """One row per study with study, effect, se. Synthetic heterogeneous studies if no path is given."""
    if path is not None:
        return pd.read_csv(path)
    rng = np.random.default_rng(seed)
    k = 12
    se = rng.uniform(0.1, 0.45, k)
    true_effect = 0.4 + rng.normal(0, 0.3, k)              # each study has its own true effect (tau = 0.3)
    return pd.DataFrame({
        STUDY_COL: [f"Study {i + 1}" for i in range(k)],
        EFFECT_COL: true_effect + rng.normal(0, se),
        SE_COL: se,
    })


def effect_sizes_from_summaries(df: pd.DataFrame, kind: str = "mean_difference") -> pd.DataFrame:
    """Return a frame with `effect` and `se` columns computed from group summaries.

    kind="mean_difference" or "smd": needs mean_t, sd_t, n_t, mean_c, sd_c, n_c.
        Use the raw mean difference when every study used the same unit; use the
        standardized mean difference (Hedges' g) when units or instruments differ.
    kind="log_odds_ratio" or "log_risk_ratio": needs events_t, n_t, events_c, n_c.
        Pool on the log scale and exponentiate the pooled result for reporting.
        Zero cells need a correction; see `zero_correction` in
        statsmodels' effectsize_2proportions and check the result is not driven by it.
    """
    if kind == "mean_difference":
        effect = df["mean_t"] - df["mean_c"]
        se = np.sqrt(df["sd_t"] ** 2 / df["n_t"] + df["sd_c"] ** 2 / df["n_c"])
    elif kind == "smd":
        effect, variance = effectsize_smd(df["mean_t"], df["sd_t"], df["n_t"], df["mean_c"], df["sd_c"], df["n_c"])
        se = np.sqrt(variance)
    elif kind in ("log_odds_ratio", "log_risk_ratio"):
        statistic = "odds-ratio" if kind == "log_odds_ratio" else "risk-ratio"
        effect, variance = effectsize_2proportions(
            df["events_t"], df["n_t"], df["events_c"], df["n_c"], statistic=statistic,
        )
        se = np.sqrt(variance)
    else:
        raise ValueError(f"unknown kind: {kind!r}")
    return pd.DataFrame({EFFECT_COL: np.asarray(effect), SE_COL: np.asarray(se)}, index=df.index)


def pool_random_effects(df: pd.DataFrame, effect_col: str = EFFECT_COL, se_col: str = SE_COL,
                        study_col: str | None = STUDY_COL, method: str = TAU2_METHOD,
                        hksj: bool = HKSJ, alpha: float = 0.05) -> dict:
    """Random-effects pooling plus heterogeneity and a prediction interval.

    Returns a dict with: k, estimate, se, ci (low, high), tau, tau2, i2 (0-1), q, q_p,
    prediction_interval (None when k < 3), fixed_estimate, fixed_ci, and `result`
    (the statsmodels object, used by forest_plot).
    """
    effect, variance = df[effect_col], df[se_col] ** 2
    k = len(df)
    if k < 2:
        raise ValueError("a meta-analysis needs at least two studies")
    names = list(df[study_col]) if study_col in df.columns else None
    res = combine_effects(effect.to_numpy(), variance.to_numpy(), method_re=method, row_names=names)

    tau2 = float(res.tau2)
    weights = 1 / (variance + tau2)
    estimate = float((weights * effect).sum() / weights.sum())
    se = float(np.sqrt(1 / weights.sum()))
    if hksj:
        se_hksj = np.sqrt((weights * (effect - estimate) ** 2).sum() / ((k - 1) * weights.sum()))
        se = float(max(se_hksj, se))                    # never narrower than the usual interval
        crit = stats.t.ppf(1 - alpha / 2, k - 1)
    else:
        crit = stats.norm.ppf(1 - alpha / 2)

    fixed_se = float(res.sd_eff_w_fe)
    z = stats.norm.ppf(1 - alpha / 2)
    prediction = None
    if k >= 3:
        half = stats.t.ppf(1 - alpha / 2, k - 2) * np.sqrt(tau2 + se ** 2)
        prediction = (estimate - half, estimate + half)

    return {
        "k": k,
        "estimate": estimate,
        "se": se,
        "ci": (estimate - crit * se, estimate + crit * se),
        "tau": float(np.sqrt(tau2)),
        "tau2": tau2,
        "i2": max(0.0, float(res.i2)),
        "q": float(res.q),
        "q_p": float(stats.chi2.sf(res.q, k - 1)),
        "prediction_interval": prediction,
        "fixed_estimate": float(res.mean_effect_fe),
        "fixed_ci": (float(res.mean_effect_fe) - z * fixed_se, float(res.mean_effect_fe) + z * fixed_se),
        "result": res,
    }


def summarize(pooled: dict, unit: str = "") -> str:
    """Plain-text summary to paste into an answer (the prediction interval is on purpose)."""
    low, high = pooled["ci"]
    lines = [
        f"{pooled['k']} studies. Random-effects estimate {pooled['estimate']:.2f}{unit} (95% CI {low:.2f} to {high:.2f}).",
        f"Heterogeneity: tau = {pooled['tau']:.2f}, I2 = {100 * pooled['i2']:.0f}%, Q p = {pooled['q_p']:.3f}.",
    ]
    if pooled["prediction_interval"] is not None:
        p_low, p_high = pooled["prediction_interval"]
        lines.append(f"95% prediction interval for a new study: {p_low:.2f} to {p_high:.2f}.")
    f_low, f_high = pooled["fixed_ci"]
    lines.append(f"(Common-effect estimate for comparison: {pooled['fixed_estimate']:.2f}, 95% CI {f_low:.2f} to {f_high:.2f}.)")
    return "\n".join(lines)


def forest_plot(pooled: dict):
    """Forest plot of the studies and the pooled estimates (matplotlib figure)."""
    return pooled["result"].plot_forest()


def leave_one_out(df: pd.DataFrame, study_col: str = STUDY_COL, **kwargs) -> pd.DataFrame:
    """Re-pool with each study left out in turn; a big change flags an influential study."""
    rows = []
    for name in df[study_col]:
        rest = df[df[study_col] != name]
        p = pool_random_effects(rest, study_col=study_col, **kwargs)
        rows.append({"left_out": name, "estimate": p["estimate"], "tau": p["tau"], "i2": p["i2"]})
    return pd.DataFrame(rows)


def egger_test(df: pd.DataFrame, effect_col: str = EFFECT_COL, se_col: str = SE_COL) -> dict:
    """Egger's regression for small-study effects: standardized effect on precision.

    An intercept far from zero suggests funnel-plot asymmetry (publication bias or real
    differences between small and large studies). Low power below ~10 studies: a
    non-significant result is not evidence of no bias.
    """
    k = len(df)
    precision = (1 / df[se_col]).rename("precision")
    fit = sm.OLS(df[effect_col] / df[se_col], sm.add_constant(precision)).fit()
    return {"intercept": float(fit.params["const"]), "p_value": float(fit.pvalues["const"]), "k": k,
            "low_power": k < 10}


def funnel_plot(df: pd.DataFrame, pooled: dict, effect_col: str = EFFECT_COL, se_col: str = SE_COL):
    """Effect against standard error; most precise studies at the top. Returns the figure."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.scatter(df[effect_col], df[se_col])
    ax.axvline(pooled["estimate"], color="grey", linestyle="--")
    ax.invert_yaxis()
    ax.set_xlabel("effect")
    ax.set_ylabel("standard error")
    return fig


if __name__ == "__main__":
    import matplotlib

    matplotlib.use("Agg")

    data = load_study_data()
    pooled = pool_random_effects(data)
    print(summarize(pooled))
    pooled_hksj = pool_random_effects(data, hksj=True)
    print("Hartung-Knapp 95% CI:", tuple(round(float(v), 2) for v in pooled_hksj["ci"]))
    print(leave_one_out(data).round(2).to_string(index=False))
    egger = egger_test(data)
    print(f"Egger intercept {egger['intercept']:.2f} (p = {egger['p_value']:.2f}); low power: {egger['low_power']}")
    forest_plot(pooled)
    funnel_plot(data, pooled)

    # Group summaries -> effect and standard error, then pool.
    summaries = pd.DataFrame({
        "study": ["A", "B", "C", "D"],
        "mean_t": [24.1, 22.8, 25.0, 23.5], "sd_t": [3.2, 2.9, 3.6, 3.0], "n_t": [30, 45, 28, 60],
        "mean_c": [22.0, 22.1, 22.7, 22.9], "sd_c": [3.0, 3.1, 3.3, 3.2], "n_c": [30, 44, 29, 58],
    })
    converted = effect_sizes_from_summaries(summaries, "mean_difference").assign(study=summaries["study"])
    print(summarize(pool_random_effects(converted, hksj=True), unit=" kg"))
