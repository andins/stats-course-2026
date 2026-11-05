"""
Template: power / sample-size analysis for a planned (not-yet-collected) study.

Use this when the data hasn't been collected yet and the question is "how
many samples do I need" -- a design-phase question, not an analysis of
existing data (see references/analysis-triage.md, Question 0). Two flavors:

1. Power analysis for a planned hypothesis test: given alpha, target power,
   and an effect size, find the required n. Use `analytic_sample_size()` for
   designs covered by a closed form (t-test, ANOVA, proportions, correlation,
   chi-squared); fall back to `simulate_power()` / `find_sample_size_by_simulation()`
   (Monte Carlo) for anything else -- regression with covariates, GLMs,
   clustering, unequal allocation, multilevel designs.
2. Precision/CI-width planning when there's no single pre-specified test
   (e.g. "how big a sample to estimate this proportion within +/-3 points"):
   use `precision_sample_size_mean()` / `precision_sample_size_proportion()`.

Effect-size sourcing caution: don't plug in a point estimate from a small
pilot at face value -- small studies give noisy, often inflated effect-size
estimates (Type M error, GELMAN_CARLIN_2014). Prefer the smallest effect size
of practical interest, a literature/meta-analytic estimate, or report a
sensitivity table across a few plausible effect sizes rather than one number
presented as exact.

Never compute "observed/post-hoc power" from data you already collected --
it's a deterministic, monotonic function of the p-value and adds no
information beyond it (HOENIG_HEISEY_2001). If you want to assess a result
after the fact, look at the CI width and do a Type S/M error check
(GELMAN_CARLIN_2014) instead.

Requires: numpy, scipy, statsmodels.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats
from statsmodels.stats.power import FTestAnovaPower, GofChisquarePower, NormalIndPower, TTestIndPower, TTestPower
from statsmodels.stats.proportion import proportion_effectsize

# --------------------------------------------------------------------------
# KEY PARAMETERS -- fill these in for the design question at hand.
# --------------------------------------------------------------------------
ALPHA = 0.05
TARGET_POWER = 0.8
EFFECT_SIZE = 0.5   # units depend on TEST_TYPE -- see analytic_sample_size() docstring


def analytic_sample_size(test_type: str, effect_size: float, alpha: float = ALPHA,
                          power: float = TARGET_POWER, **kwargs) -> float:
    """Closed-form required sample size for common designs via statsmodels.stats.power.

    `test_type` and the matching `effect_size` convention:
    - "one_sample_t" / "paired_t": Cohen's d; returns n (one group / number of pairs).
    - "two_sample_t": Cohen's d; returns n per group (pass `ratio=` for unequal
      group sizes, default 1.0).
    - "anova_oneway": Cohen's f; requires `k_groups=`; returns total n across groups.
    - "two_proportions": Cohen's h -- compute via
      `statsmodels.stats.proportion.proportion_effectsize(p1, p2)`; returns n per group.
    - "chi_squared_gof": Cohen's w; requires `n_bins=` (number of categories);
      returns total n.
    - "correlation": Pearson r itself (not a converted effect size); returns
      total n via the Fisher-z approximation (COHEN_POWER).
    """
    if test_type in ("one_sample_t", "paired_t"):
        return TTestPower().solve_power(effect_size=effect_size, alpha=alpha, power=power, **kwargs)
    if test_type == "two_sample_t":
        return TTestIndPower().solve_power(effect_size=effect_size, alpha=alpha, power=power, **kwargs)
    if test_type == "anova_oneway":
        return FTestAnovaPower().solve_power(effect_size=effect_size, alpha=alpha, power=power, **kwargs)
    if test_type == "two_proportions":
        return NormalIndPower().solve_power(effect_size=effect_size, alpha=alpha, power=power, **kwargs)
    if test_type == "chi_squared_gof":
        return GofChisquarePower().solve_power(effect_size=effect_size, alpha=alpha, power=power, **kwargs)
    if test_type == "correlation":
        return _sample_size_correlation(effect_size, alpha=alpha, power=power)
    raise ValueError(f"Unsupported test_type: {test_type!r}")


def _sample_size_correlation(r: float, alpha: float = ALPHA, power: float = TARGET_POWER) -> float:
    """Required total n to detect a Pearson correlation of magnitude `r` (two-sided, Fisher-z, COHEN_POWER)."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    z_r = 0.5 * math.log((1 + r) / (1 - r))
    return ((z_alpha + z_power) / z_r) ** 2 + 3


def precision_sample_size_mean(sigma: float, margin_of_error: float, alpha: float = ALPHA) -> float:
    """Required n so a two-sided (1-alpha) CI for a mean has half-width <= `margin_of_error`.

    `sigma`: a planning guess at the population SD (from a pilot or literature).
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    return (z_alpha * sigma / margin_of_error) ** 2


def precision_sample_size_proportion(p_guess: float, margin_of_error: float, alpha: float = ALPHA) -> float:
    """Required n so a two-sided (1-alpha) CI for a proportion has half-width <= `margin_of_error`.

    `p_guess`: a planning guess at the true proportion; use 0.5 (most conservative,
    largest required n) if there's no prior guess.
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    return (z_alpha ** 2) * p_guess * (1 - p_guess) / (margin_of_error ** 2)


def simulate_power(simulate_fn, test_fn, n, n_sims: int = 2000, alpha: float = ALPHA, seed: int = 0) -> float:
    """Monte Carlo power estimate for a design with no closed form above.

    `simulate_fn(n, rng) -> dataset` must simulate one dataset of size `n` under
    the assumed true effect (the "alternative"). `test_fn(dataset) -> p_value`
    must run the planned analysis and return its p-value. Power is estimated as
    the fraction of simulated datasets where p_value < alpha.
    """
    rng = np.random.default_rng(seed)
    rejections = 0
    for _ in range(n_sims):
        dataset = simulate_fn(n, rng)
        p_value = test_fn(dataset)
        rejections += p_value < alpha
    return rejections / n_sims


def find_sample_size_by_simulation(simulate_fn, test_fn, n_grid, target_power: float = TARGET_POWER,
                                    n_sims: int = 500, alpha: float = ALPHA, seed: int = 0) -> dict:
    """Smallest n in `n_grid` (ascending) whose simulated power reaches `target_power`.

    Returns the full {n: power} curve too, since reporting a one-point answer
    without the surrounding sensitivity is misleading -- show how power moves
    with n near the chosen value.
    """
    curve = {n: simulate_power(simulate_fn, test_fn, n, n_sims=n_sims, alpha=alpha, seed=seed) for n in n_grid}
    required_n = next((n for n, p in curve.items() if p >= target_power), None)
    return {"required_n": required_n, "power_curve": curve}


if __name__ == "__main__":
    # 1. Analytic: two-sample t-test, Cohen's d = 0.5, alpha = .05, power = .8.
    n_per_group = analytic_sample_size("two_sample_t", effect_size=0.5)
    print(f"Two-sample t-test: need ~{math.ceil(n_per_group)} per group (d=0.5, alpha=.05, power=.8).")

    # Sensitivity table -- don't present a single effect size as certain.
    for d in (0.2, 0.35, 0.5, 0.8):
        n = analytic_sample_size("two_sample_t", effect_size=d)
        print(f"  d={d}: ~{math.ceil(n)} per group")

    # 2. Precision-based: survey sample size for a proportion within +/-3 points.
    n_precision = precision_sample_size_proportion(p_guess=0.5, margin_of_error=0.03)
    print(f"Proportion within +/-3 points (p guess 0.5): need ~{math.ceil(n_precision)} respondents.")

    # 3. Simulation-based fallback: logistic regression effect of x on binary y.
    import statsmodels.api as sm

    true_log_odds_effect = 0.5

    def simulate_logistic(n, rng):
        x = rng.normal(0, 1, n)
        p = 1 / (1 + np.exp(-(true_log_odds_effect * x)))
        y = rng.binomial(1, p)
        return x, y

    def test_logistic(dataset):
        x, y = dataset
        model = sm.GLM(y, sm.add_constant(x), family=sm.families.Binomial()).fit()
        return model.pvalues[1]

    result = find_sample_size_by_simulation(
        simulate_logistic, test_logistic, n_grid=[50, 100, 150, 200, 300], n_sims=300,
    )
    print("Logistic regression power curve (simulation):", result["power_curve"])
    print("Required n (simulation):", result["required_n"])
