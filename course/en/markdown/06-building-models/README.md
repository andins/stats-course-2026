# Module 6: Building Models

Once you know *why* you're modeling (Module 5), there are a handful of practical concerns that apply almost regardless of the specific model.

## Pages

1. [Overfitting and regularization](./overfitting-and-regularization.md) — why a model that fits your data perfectly can still be a bad model.
2. [Cross-validation and model checking](./cross-validation-and-model-checking.md) — how to tell if a model is good.
3. [Multicollinearity](./multicollinearity.md) — what happens when your predictors overlap too much.
4. [Measurement error](./measurement-error.md) — what happens when a predictor or outcome is a noisy proxy for what you actually meant to measure.

## How-to guides

Hands-on recipes in Python for doing these checks yourself, without needing an assistant:

- [How to: validate a predictive model](./how-to/validate-a-predictive-model.md)
- [How to: check multicollinearity](./how-to/check-multicollinearity.md)
- [How to: estimate and correct for measurement error](./how-to/handle-measurement-error.md), with an [attenuation notebook](../notebooks/measurement-error-attenuation.ipynb)

> **Learn more**
>
> - [James, Witten, Hastie & Tibshirani (2021)](https://www.statlearning.com/), *An Introduction to Statistical Learning* (2nd ed., free online), Ch. 5 "Resampling Methods" and Ch. 6 "Linear Model Selection and Regularization", pp. 197–288.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §11.6–11.8 "Residual standard deviation" to "Cross validation", pp. 168–180.

---
**Previous module:** [Prediction vs. causation](../05-prediction-vs-causation/README.md) · **Next:** [Special data structures →](../07-special-data-structures/README.md) · [Home](../README.md) · [Glossary](../glossary.md)
