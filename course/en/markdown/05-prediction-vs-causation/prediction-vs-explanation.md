# Prediction vs. Explanation

**In plain terms:** a predictive model answers "what will probably happen?" An explanatory/causal model answers "what would happen *if I changed something*?" They are judged by completely different standards.

## An example: correlation without causation

Ice cream sales and drowning deaths are strongly correlated across the year — both rise in summer. A model using ice cream sales to *predict* drowning rates would work reasonably well. Banning ice cream would not prevent any drowning — the underlying cause (hot weather, more people swimming) affects both. Ice cream sales are a good **predictor** of drowning risk and not a variable that, if changed, would change drowning risk.

## Mia and Theo's examples

- **Prediction**: Mia wants a model that predicts a patient's risk of early coronary disease from clinical and genetic features (age, cholesterol, family history, variant genotypes) — she doesn't need to know *why* these predict risk, just that they do, reliably, on new patients.
- **Causation**: Theo wants to know whether *giving* the drug *causes* blood pressure to drop — he specifically cares whether intervening (prescribing it) would change the outcome, not just whether drug-takers happen to have lower blood pressure for some other reason.

## Why you can't always tell which one a model answers by looking at it

The same regression equation can be fit either way — the math doesn't know your intent. What changes is:

- **How you judge success.** A predictive model is judged by how well it predicts *new* data it hasn't seen (see [Cross-validation](../06-building-models/cross-validation-and-model-checking.md)) — any predictor that helps is fair game, including ice cream sales. A causal model is judged by whether it correctly isolates the effect of *intervening* on one variable — which requires much more care about *which* other variables you include (see [Causal diagrams](./causal-diagrams.md)), and throwing in "every available predictor" can actively hurt it.
- **What you need before trusting the answer.** A causal claim needs an **identification strategy** — some reason to believe you've accounted for (or ruled out) the other explanations for the association. See [Experiments vs. observational data](./experiments-vs-observational-data.md).

## One question that distinguishes the two

Ask: *do I need this model's answer to hold if I change the input, or do I only need it to generate reliable forecasts on data I haven't seen yet?* The first is causal; the second is predictive. Decide this before building anything.

> **Learn more**
>
> - Shmueli (2010), "To explain or to predict?," *Statistical Science* 25(3), 289–310 — why the two goals call for different modeling choices.
> - Hernán, Hsu & Healy (2019), "A second chance to get causal inference right: a classification of data science tasks," *CHANCE* 32(1), 42–49 — description vs. prediction vs. causal inference.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §6.3 "Interpret coefficients as comparisons, not effects", pp. 84–85.

---
**Previous:** [Module home](./README.md) · **Next:** [Experiments vs. observational data →](./experiments-vs-observational-data.md) · [Glossary](../glossary.md)
