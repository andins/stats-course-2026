# Measurement Error

**In plain terms:** if what you recorded isn't quite the same as what you actually meant to measure — a noisy proxy rather than the true quantity — a model doesn't just get noisier. It gets biased, usually toward "no effect."

## A concrete picture

Theo measures blood pressure with a home cuff accurate to only ±5 mmHg, instead of a clinical-grade device. Each reading is the true blood pressure plus random error. If Theo regresses an outcome on these noisy readings, the estimated slope comes out systematically smaller than the true relationship — even with a huge sample — simply because the predictor is a blurred version of the thing that actually matters.

## Why it's not "just noise"

- Random error in the **outcome** mostly inflates residual variance and widens the confidence interval — it doesn't bias the slope on average.
- Random error in a **predictor** is different: it biases the estimated slope toward zero, a pattern called **attenuation bias** (or regression dilution). This is a bias, not a variance problem — it does **not** shrink as the sample size grows.
- Practically, this can look like "no relationship found" when a real relationship exists but got diluted by imprecise measurement.

## Common sources

- Self-reported quantities (diet recall, self-reported exercise or adherence, survey instruments).
- Lab assays or sensors with known measurement variability.
- A proxy standing in for the construct you actually care about (e.g. BMI as a proxy for body fat).

## What to do about it

- Name it explicitly when a variable is a known imprecise proxy, rather than treating the observed value as if it were exact.
- If you have a sense of the error's size (from the instrument's documented precision, or from repeated measurements on the same unit), a **measurement-error / errors-in-variables model** — regression calibration, SIMEX, or a Bayesian model with an explicit latent "true value" — can correct the bias; plain OLS on the observed value cannot (FULLER_MEASUREMENT_ERROR).
- If replicate measurements exist, use them to estimate the error variance rather than guessing it.
- More data alone does not fix this — attenuation bias persists at any sample size, so don't treat it as a power problem.

## The takeaway

A coefficient is only as good as the variable that went into it. If a predictor (or outcome) is a known noisy stand-in for what you actually care about, say so, and consider a measurement-error-aware model rather than reporting the naive, likely-attenuated estimate as the final answer.

> **Do it yourself**
>
> - [How to: estimate and correct for measurement error](./how-to/handle-measurement-error.md) — estimate reliability from replicates and correct the slope.
> - [Notebook: watch the slope shrink](../notebooks/measurement-error-attenuation.ipynb) — simulate the bias and see that more data doesn't remove it.

> **Learn more**
>
> - [Hernán & Robins (2020)](https://miguelhernan.org/whatifbook), *Causal Inference: What If* (free online), §9.1–9.2 "Measurement error" and "The structure of measurement error", pp. 125–128.
> - Fuller (1987), *Measurement Error Models*, Ch. 1 "A Single Explanatory Variable" — the classical treatment of attenuation bias and corrections.
> - McElreath (2020), *Statistical Rethinking* (2nd ed.), Ch. 15, §15.1 "Measurement error" — a Bayesian, measurement-error-aware model.

---
**Previous:** [Multicollinearity](./multicollinearity.md) · **Module home:** [Building models](./README.md) · **Next module:** [Special data structures →](../07-special-data-structures/README.md) · [Glossary](../glossary.md)
