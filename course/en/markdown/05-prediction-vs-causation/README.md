# Module 5: Prediction vs. Causation

Two very different questions get asked using the same regression tools, and mixing them up is one of the most consequential mistakes in applied statistics.

## Pages

1. [Prediction vs. explanation](./prediction-vs-explanation.md) — "will this work on new data" vs. "did X cause Y."
2. [Experiments vs. observational data](./experiments-vs-observational-data.md) — why *how* the data was collected changes what you're allowed to conclude.
3. [Causal diagrams](./causal-diagrams.md) — a simple way to reason about confounders, mediators, and colliders.

## Why this distinction gets its own module

A model that predicts well is not the same as a model that tells you what will happen if you *intervene* — change a policy, give a treatment, change a drug dose. Confusing the two leads to practical mistakes: acting on a correlation as if it were something you could change, when it is a byproduct of something else entirely.

## How-to guides

- [How to: draw and use a causal diagram](./how-to/draw-and-use-a-causal-diagram.md), with a [confounder, mediator, collider notebook](../notebooks/confounder-mediator-collider.ipynb)

> **Learn more**
>
> - Shmueli (2010), "To explain or to predict?," *Statistical Science* 25(3), 289–310.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §18.1–18.3 "Basics of causal inference" to "Randomized experiments", pp. 339–346.

---
**Previous module:** [Regression basics](../04-regression-basics/README.md) · **Next:** [Building models →](../06-building-models/README.md) · [Home](../README.md) · [Glossary](../glossary.md)
