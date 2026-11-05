# How to: run a meta-analysis

**Use this when:** you have an effect estimate and its standard error from each of several studies of the same question (studies of one gene variant, trials of one drug), and you want one combined answer. The ideas are on the [Meta-analysis](../meta-analysis.md) page; the traps are on [Meta-analysis: bias and pitfalls](../meta-analysis-pitfalls.md).

## Steps

1. **Fix the question and the eligibility rules before you look at results.** Which treatment, which outcome, which kinds of study count? Write it down; searching and selecting studies is the part that most affects the answer.
2. **Put every study on the same scale.** One row per study with an `effect` and its standard error `se`. Last code block below shows how to get them from group means or counts.
3. **Pool with a random-effects model.** Report the pooled estimate with its interval.
4. **Report the spread of the true effects:** heterogeneity (τ, I²) and the prediction interval, not just the pooled mean.
5. **Draw the forest plot** and look at it before trusting any number.
6. **Check how fragile the result is:** leave one study out at a time, and compare with the fixed-effect estimate.
7. **Look for publication bias** (funnel plot, Egger's regression), keeping in mind that with fewer than about 10 studies it cannot tell you much.
8. **Report** the number of studies, how they were found, and the limits above.

## Code: pool the studies

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.meta_analysis import combine_effects

df = pd.read_csv("my_data.csv")    # one row per study: study, effect (difference in LDL, mmol/L), se (its standard error)
k = len(df)

res = combine_effects(df["effect"].to_numpy(), (df["se"] ** 2).to_numpy(), method_re="iterated", row_names=list(df["study"]))
pooled, pooled_se = res.mean_effect_re, res.sd_eff_w_re              # random effects
fixed, fixed_se = res.mean_effect_fe, res.sd_eff_w_fe                # one common true effect
tau2, i2 = res.tau2, max(0.0, res.i2)                                # between-study variance; share of spread beyond chance
q_p = stats.chi2.sf(res.q, k - 1)
pi_half = stats.t.ppf(0.975, k - 2) * np.sqrt(tau2 + pooled_se ** 2)

print(f"{k} studies")
print(f"random effects: {pooled:.2f} (95% CI {pooled - 1.96 * pooled_se:.2f} to {pooled + 1.96 * pooled_se:.2f})")
print(f"fixed effect:   {fixed:.2f} (95% CI {fixed - 1.96 * fixed_se:.2f} to {fixed + 1.96 * fixed_se:.2f})")
print(f"tau = {np.sqrt(tau2):.2f}, I2 = {100 * i2:.0f}%, heterogeneity test p = {q_p:.3f}")
print(f"95% prediction interval for a new study: {pooled - pi_half:.2f} to {pooled + pi_half:.2f}")

res.plot_forest()
plt.show()
```

## Code: few studies? Widen the interval honestly

With a handful of studies, τ² is poorly estimated and the usual interval is too narrow. The Hartung-Knapp (HKSJ) adjustment uses the observed scatter of the studies and a t distribution:

```python
w = 1 / (df["se"] ** 2 + tau2)
mu = (w * df["effect"]).sum() / w.sum()
se_hksj = np.sqrt((w * (df["effect"] - mu) ** 2).sum() / ((k - 1) * w.sum()))
se_hksj = max(se_hksj, np.sqrt(1 / w.sum()))                   # never narrower than the usual interval
t_crit = stats.t.ppf(0.975, k - 1)
print(f"random effects, Hartung-Knapp: {mu:.2f} (95% CI {mu - t_crit * se_hksj:.2f} to {mu + t_crit * se_hksj:.2f})")
```

## Code: how fragile is the result?

```python
rows = []
for name in df["study"]:
    rest = df[df["study"] != name]
    r = combine_effects(rest["effect"].to_numpy(), (rest["se"] ** 2).to_numpy(), method_re="iterated")
    rows.append({"left out": name, "estimate": r.mean_effect_re, "tau": np.sqrt(r.tau2)})
leave_one_out = pd.DataFrame(rows).round(2)
print(leave_one_out.to_string(index=False))
```

## Code: publication bias

```python
precision = (1 / df["se"]).rename("precision")
egger = sm.OLS(df["effect"] / df["se"], sm.add_constant(precision)).fit()     # Egger's regression
print(f"Egger intercept = {egger.params['const']:.2f} (p = {egger.pvalues['const']:.2f}); "
      f"{k} studies, so treat this as a weak check")

fig, ax = plt.subplots()
ax.scatter(df["effect"], df["se"])
ax.axvline(pooled, color="grey", linestyle="--")
ax.invert_yaxis()                                                # the most precise studies at the top
ax.set_xlabel("effect")
ax.set_ylabel("standard error")
plt.show()
```

## Code: get an effect and a standard error from each study

If a paper gives group summaries instead of an effect and a standard error, compute them yourself. Use the same scale for every study.

```python
from statsmodels.stats.meta_analysis import effectsize_2proportions, effectsize_smd

# Continuous outcome, same unit in every study: the raw mean difference and its standard error
means = pd.DataFrame({
    "mean_t": [24.1, 22.8, 25.0], "sd_t": [3.2, 2.9, 3.6], "n_t": [30, 45, 28],
    "mean_c": [22.0, 22.1, 22.7], "sd_c": [3.0, 3.1, 3.3], "n_c": [30, 44, 29],
})
diff = means["mean_t"] - means["mean_c"]
se_diff = np.sqrt(means["sd_t"] ** 2 / means["n_t"] + means["sd_c"] ** 2 / means["n_c"])

# Different units or instruments across studies: the standardized mean difference (Hedges' g)
g, var_g = effectsize_smd(means["mean_t"], means["sd_t"], means["n_t"],
                          means["mean_c"], means["sd_c"], means["n_c"])

# Yes/no outcome: the log odds ratio (pool on the log scale, then exponentiate)
counts = pd.DataFrame({"events_t": [12, 9, 20], "n_t": [60, 40, 90], "events_c": [20, 15, 31], "n_c": [60, 42, 88]})
log_or, var_log_or = effectsize_2proportions(counts["events_t"], counts["n_t"], counts["events_c"], counts["n_c"],
                                             statistic="odds-ratio")

print(pd.DataFrame({"difference": diff, "se": se_diff, "g": g, "se_g": np.sqrt(var_g),
                    "log_or": log_or, "se_log_or": np.sqrt(var_log_or)}).round(2))
```

## Reading the output

Example output on made-up data (10 studies of an LDLR variant, effect in mmol/L of extra LDL cholesterol in carriers):

```text
10 studies
random effects: 0.34 (95% CI 0.23 to 0.45)
fixed effect:   0.30 (95% CI 0.23 to 0.38)
tau = 0.13, I2 = 66%, heterogeneity test p = 0.002
95% prediction interval for a new study: 0.01 to 0.67
random effects, Hartung-Knapp: 0.34 (95% CI 0.21 to 0.47)
left out  estimate  tau
 Study 1      0.32 0.14
 ...
 Study 9      0.39 0.02
Study 10      0.33 0.14
Egger intercept = 3.17 (p = 0.11); 10 studies, so treat this as a weak check
```

- **The pooled estimate is the average effect, not the effect everywhere.** On average carrying the variant adds about 0.34 mmol/L of LDL. But τ = 0.13 mmol/L and I² = 66% say the studies genuinely differ, and the prediction interval (0.01 to 0.67 mmol/L) says a new study could show anything from no effect to twice the average. That is the honest summary; the CI of the mean alone sounds much more certain.
- **Random effects gave a wider interval than fixed effect** (0.23 to 0.45 against 0.23 to 0.38) because it counts the differences between studies as uncertainty. When heterogeneity is low the two agree.
- **The Hartung-Knapp interval is wider still** (0.21 to 0.47), as expected with only 10 studies. Report it if you have few studies.
- **Leaving out Study 9 shrinks τ from 0.13 to 0.02** and moves the estimate to 0.39. Much of the heterogeneity comes from one study. Look at what was different there (a different ancestry? a different assay?) before deciding whether it belongs in the pool. Do not drop it just because it is inconvenient: report both results.
- **Egger's intercept points toward small studies with larger effects** (3.17), though not "significantly" (p = 0.11). With 10 studies this test has little power, so absence of significance is not evidence of no publication bias. Look at the funnel plot, and treat the pooled estimate as possibly optimistic.

## Which approach when

| Your situation | Use |
|---|---|
| Studies measured the same thing on the same scale | Raw mean difference (or log odds ratio) and random effects |
| Studies used different instruments or units | Standardized mean difference, with the caveat that it also depends on how variable each sample was |
| Fewer than about 5-10 studies | Random effects with the Hartung-Knapp interval, or a Bayesian model; say how few studies there were |
| Several effects from the same study (two doses against one control, several outcomes) | They are not independent: pick one per study, or treat study as a cluster (see [Clustered and hierarchical data](../clustered-and-hierarchical-data.md)) |
| You have the raw data from every site | Not a meta-analysis problem: analyze it as clustered data with site as the cluster, see [How to: analyze clustered data](./analyze-clustered-data.md) |
| You want to know why studies differ | A meta-regression on study-level characteristics, read as exploratory: the characteristics are not randomized |

## If it goes wrong

- **τ² comes out as zero but the forest plot clearly scatters:** with few or imprecise studies τ² is badly estimated. Report the prediction interval and the Hartung-Knapp interval rather than concluding the studies agree.
- **I² is very high (above about 75%):** the average may not describe any real setting. Look for what differs between studies (dose, ancestry, assay, design) before reporting one number.
- **One study dominates the weights, or leaving it out changes the answer:** say so, and report the result with and without it.
- **The funnel plot is lopsided:** small studies with large effects and no small studies with null effects suggest publication bias, but also real differences between small and large studies. The pooled estimate may be too optimistic; say so.
- **Studies report different things (medians, no standard errors):** conversion formulas exist (see the Cochrane Handbook), but each conversion adds assumptions; state them.
- **A binary outcome with zero events in a group:** the log odds ratio is not defined; use `zero_correction` in `effectsize_2proportions` and check the result is not driven by the correction.
