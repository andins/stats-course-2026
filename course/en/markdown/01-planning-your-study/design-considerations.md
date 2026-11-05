# Other Design-Phase Considerations

**In plain terms:** sample size isn't the only decision that has to be made before data collection starts. Two others matter just as much, and neither can be fixed later: how precisely you measure your variables, and which variables you bother to record at all.

## Reduce measurement noise upfront, with better instruments

A noisy measurement doesn't just add random variation you can average away — if it's on a predictor, it biases the estimated effect toward zero (**attenuation bias**, see [Measurement error](../06-building-models/measurement-error.md)), and that bias does not shrink with a bigger sample. The cheapest point to deal with this is the design phase, before data collection starts:

- Favor the more precise instrument or protocol you can afford (a calibrated device over a self-report, a standardized assay over an ad hoc one) rather than accepting noise and trying to collect your way out of it.
- If a more precise instrument genuinely isn't feasible, plan for **replicate measurements** on at least a subsample — they let you estimate the measurement error's size later and correct for it, instead of having to guess.
- If Theo knows his home blood-pressure cuff is noisy, switching to a clinical-grade device (or taking triplicate readings per visit, averaged) fixes the problem far more effectively than simply enrolling more patients.

## Make sure the design captures what a causal question will need

If the eventual goal is to interpret an effect causally (not just describe an association), the design/data-collection plan has to anticipate that before data collection, not after:

- Think through, in advance, what else is likely to affect both the exposure and the outcome (**confounders** — see [Causal diagrams](../05-prediction-vs-causation/causal-diagrams.md)) and make sure those variables are actually being recorded. A confounder that was never measured can't be adjusted for later, no matter how good the model is.
- This matters less for a well-designed randomized experiment, where random assignment handles confounding by design (see [Experiments vs. observational data](../05-prediction-vs-causation/experiments-vs-observational-data.md)) — but it's still worth recording plausible **pre-treatment** covariates, which sharpen precision even there.
- For an observational design, this is not optional: an incomplete variable list at the design stage caps what any later causal analysis can credibly claim, regardless of sample size or modeling sophistication.

## The takeaway

Sample size answers "how much data." Instrument choice and variable list answer "how trustworthy is that data" and "can I even ask the question I want to ask with it" — get both right before collecting a single data point, since neither is fixable by better analysis afterward.

> **Learn more**
>
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §2.2 "Validity and reliability", pp. 23–25 — what makes a measurement trustworthy before you analyze it.
> - [Hernán & Robins (2020)](https://miguelhernan.org/whatifbook), *Causal Inference: What If* (free online), §3.6 "The target trial" (p. 41 onward) and §7.6 "Confounding adjustment" (pp. 102–108) — deciding up front what a causal question requires you to measure.

---
**Previous:** [Effect size](./effect-size.md) · [Module home](./README.md) · **Next module:** [Exploring your data →](../02-exploring-data/README.md) · [Glossary](../glossary.md)
