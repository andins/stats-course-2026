# How to: estimate and correct for measurement error

**Use this when:** a predictor is a noisy measurement of the thing you care about, and you can get an idea of how noisy it is. The reasoning is on the [Measurement error](../measurement-error.md) page.

To see the bias appear and persist as the sample grows, play with the [attenuation notebook](../../notebooks/measurement-error-attenuation.ipynb) first (download it and open it in Jupyter, VS Code or Colab).

## Steps

1. **Get a handle on the size of the error.** The best source is **replicates**: two or more independent measurements of the same unit (Theo measures each patient twice). The alternative is an error SD from the instrument's documentation or a validation study; use a standard deviation, not a "±" range.
2. **Compute the reliability** of your predictor: the share of its variation that is real signal rather than noise. 1 means no measurement error; 0.5 means half the variance is noise.
3. **Correct the slope.** With a single noisy predictor, the naive slope is the true slope multiplied by the reliability, so dividing by the reliability undoes the attenuation.
4. **Get an interval by bootstrapping the whole procedure**, including the reliability estimate. The naive confidence interval doesn't cover the extra uncertainty from the correction.

## Code

Two replicate readings per patient, `bp_1` and `bp_2`, and an `outcome` column:

```python
import numpy as np
import pandas as pd

df = pd.read_csv("my_data.csv")  # columns: bp_1, bp_2, outcome


def corrected_slope(d):
    r1, r2, y = d["bp_1"], d["bp_2"], d["outcome"]
    x = (r1 + r2) / 2                                  # average of the replicates
    var_error = ((r1 - r2) ** 2).mean() / 2            # measurement-error variance of one reading
    reliability = 1 - (var_error / 2) / x.var()        # share of var(x) that is signal
    naive = np.cov(x, y)[0, 1] / x.var()               # ordinary regression slope
    return naive, reliability, naive / reliability


naive, reliability, corrected = corrected_slope(df)
boot = [corrected_slope(df.sample(frac=1, replace=True, random_state=i))[2] for i in range(1000)]
low, high = np.percentile(boot, [2.5, 97.5])
print(f"reliability {reliability:.2f}; naive slope {naive:.2f}; "
      f"corrected {corrected:.2f} (95% CI {low:.2f} to {high:.2f})")
```

If you have no replicates but know the error SD of a single reading, skip the averaging: use `x = df["bp"]` and `reliability = 1 - sd ** 2 / x.var()`.

## Reading the output

Example output on made-up data, where the true slope is 0.50:

```text
reliability 0.80; naive slope 0.41; corrected 0.52 (95% CI 0.44 to 0.60)
```

- **Reliability** tells you how much attenuation to expect. At 0.80 the naive slope is about 20% too small; at 0.5 it is half the true value.
- **The corrected slope** is the estimate to report, together with its bootstrap interval, and an explicit statement of the assumption behind it: the errors are random and unrelated to the true value or to the outcome.
- If reliability is close to 1, the correction is negligible and the naive result is fine.

## Limits of this recipe

- It is valid for **one** noisy predictor, with the error unrelated to everything else. With several predictors (or covariates you adjust for), the correction is more involved (regression calibration, SIMEX, or a Bayesian model with a latent true value); that is the point to involve a statistician.
- It does not help with **systematic** error (a device that always reads 5 mmHg high), which a slope doesn't pick up.
- Error in the **outcome** doesn't bias the slope; it only widens the interval, so no correction is needed.
- It can't be fixed by collecting more of the same noisy data. Better measurements or replicates are what help, and planning them at the design stage is cheapest (see [Design considerations](../../01-planning-your-study/design-considerations.md)).
