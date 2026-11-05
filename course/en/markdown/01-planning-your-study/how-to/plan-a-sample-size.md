# How to: plan a sample size

**Use this when:** you are designing a study and need to decide how many units (patients, families, samples, animals, respondents) to collect. The reasoning is on the [Sample size and power](../sample-size-and-power.md) page.

To see why a small pilot's effect size is a poor input, and to experiment with power curves, use the [power and pilot studies notebook](../../notebooks/power-and-pilot-studies.ipynb) (download it and open it in Jupyter, VS Code or Colab).

## Steps

1. **Decide which question you have.** A planned test of a difference or effect needs a *power* calculation. An open-ended estimate ("what is the average LDL cholesterol, give or take 5%?") needs a *precision* calculation.
2. **Choose the inputs.** For power: alpha (0.05 by convention), target power (0.80 by convention), and an effect size. For the effect size, use the **smallest difference that would matter in practice**, or a value from the literature. Don't copy the raw estimate from a small pilot.
3. **Express the effect size as Cohen's d:** the raw difference divided by the SD of the outcome. You need a planning guess for that SD, from earlier data or the literature.
4. **Compute the sample size for several plausible effect sizes**, not just one, and see how much the answer moves.
5. **If your analysis isn't a plain t-test, ANOVA or proportion comparison** (covariates, a GLM, clustered data), find the sample size by simulation instead.

## Code: power for a two-group comparison

```python
import math
from statsmodels.stats.power import TTestIndPower

sd = 0.8   # planning guess for the SD of the outcome (LDL, mmol/L)
power_calc = TTestIndPower()

for diff in (0.3, 0.4, 0.6, 0.8):   # sensitivity table: raw differences worth detecting (mmol/L)
    d = diff / sd                    # Cohen's d
    n = power_calc.solve_power(effect_size=d, alpha=0.05, power=0.8)
    print(f"difference {diff:.1f} mmol/L (d = {d:.2f}): {math.ceil(n)} patients per group")
```

Already know how many units you can afford? Turn the question around and ask what power that gives you:

```python
print(f"power with 20 patients per group for d = 0.5: {power_calc.power(effect_size=0.5, nobs1=20, alpha=0.05):.2f}")
```

Other designs have an equivalent in the same module: `TTestPower` (one sample or paired), `FTestAnovaPower` (one-way ANOVA, effect size Cohen's f), and `NormalIndPower` with `proportion_effectsize(p1, p2)` (two proportions).

## Code: precision for a survey or an estimate

When there is no single test, plan the width of the confidence interval instead:

```python
from scipy import stats

z = stats.norm.ppf(0.975)

sd, margin = 0.8, 0.1            # estimate a mean LDL to within +/- 0.1 mmol/L
print("mean:", math.ceil((z * sd / margin) ** 2), "patients")

p_guess, margin = 0.5, 0.03      # estimate a proportion to within +/- 3 points; 0.5 is the most cautious guess
print("proportion:", math.ceil(z**2 * p_guess * (1 - p_guess) / margin**2), "respondents")
```

## Code: power by simulation, for anything else

Simulate your study many times under the effect you want to detect, run your planned analysis on each simulated dataset, and count how often it detects the effect. Here the analysis is a regression that adjusts for age:

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(0)


def power_by_simulation(n_per_group, effect=0.4, sd=0.8, n_sims=500, alpha=0.05):
    hits = 0
    for _ in range(n_sims):
        group = np.repeat([0, 1], n_per_group)          # 0 = non-carrier, 1 = carrier
        age = rng.normal(45, 12, 2 * n_per_group)
        y = 0.02 * age + effect * group + rng.normal(0, sd, 2 * n_per_group)
        fit = smf.ols("y ~ group + age", data=pd.DataFrame({"y": y, "group": group, "age": age})).fit()
        hits += fit.pvalues["group"] < alpha
    return hits / n_sims


for n in (20, 40, 60):
    print(f"{n} per group: power = {power_by_simulation(n):.2f}")
```

Change the data-generating lines to match your design (clustering, unequal groups, a binary outcome with `smf.logit`) and the `smf.ols` line to match the analysis you will actually run.

## Reading the output

Example output (it should look like this):

```text
difference 0.3 mmol/L (d = 0.37): 113 patients per group
difference 0.4 mmol/L (d = 0.50): 64 patients per group
difference 0.6 mmol/L (d = 0.75): 29 patients per group
difference 0.8 mmol/L (d = 1.00): 17 patients per group
```

- **Sample size grows fast as the effect shrinks.** Halving the effect roughly quadruples the sample, so the choice of effect size matters more than the choice of alpha or power.
- **Report the table, not a single number.** Choose the sample size you can defend for the smallest effect you care about, and say what you can detect if the true effect is larger.
- **The simulation's answer has Monte Carlo error** of a couple of percentage points with 500 simulations; raise `n_sims` if the power is close to your target.
- **Add a margin for losses.** If you expect 10% of units to drop out or fail, divide the sample size by 0.9.

## If it goes wrong

- **You only have a pilot's effect size:** it is probably inflated, so the resulting study will be underpowered (see the notebook). Use the smallest useful effect instead, or a published estimate, and show the sensitivity table.
- **The required sample is more than you can collect:** you have three honest options. Accept a lower power and say so, aim at a larger smallest-effect-of-interest, or reduce noise (better measurement, a covariate, a paired or blocked design). Don't adjust the assumptions until the number fits.
- **Never compute "observed power" after the study.** It restates the p-value. Look at the width of the confidence interval instead.
