# Sample Size and Power

**In plain terms:** power is the chance your study will detect a real effect, *if there truly is one*. Sample-size planning is working backward from "how sure do I want to be" to "how many subjects do I need."

## Mia's example

Mia thinks carrying her LDLR variant raises LDL cholesterol by about 10%, based on a small earlier clinic series (6 carriers and 6 non-carriers). Before running the full cohort study, she needs to know: how many patients does she need per group to reliably detect a 10% difference, if it's real?

## The four ingredients of a power calculation

Every sample-size calculation needs four numbers, and fixing any three tells you the fourth:

1. **Effect size** — how big a difference you're trying to detect (see [Effect size](./effect-size.md)). This is usually the hardest to pin down.
2. **Alpha (significance level)** — your tolerance for false positives, conventionally 0.05.
3. **Power** — your tolerance for false negatives, conventionally 0.80 (an 80% chance of detecting the effect if it's real).
4. **Sample size** — what you're usually solving for.

As a rule of thumb: smaller effects, lower tolerance for errors, and more variable data all require *larger* samples.

## Using a pilot study's effect size directly

Small pilot studies give noisy estimates of effect size, and noisy estimates from small samples tend to be larger than the true effect on average (sometimes called the "winner's curse"). If Mia's earlier clinic series had only 6 patients per group, the "10% increase" it showed might be closer to 3%, or zero. Plugging the pilot's raw number into a sample-size calculator can produce a study that looks adequately powered on paper but is not in practice.

**Better alternatives**: use the smallest effect size that would be *useful* to detect (e.g. "an LDL increase smaller than 5% would not change how a carrier is managed in the clinic"), look up effect sizes from published studies, or compute sample size across a small range of plausible effect sizes and compare the results.

## Power isn't just for experiments

If there's no single pre-planned test — e.g. Mia is instead running an open-ended survey of LDL cholesterol across many clinics — the right question becomes a **precision** one: "how large a sample do I need to estimate the average LDL within, say, ±5%?" This is answered the same way (more data → narrower interval) but doesn't require picking a single hypothesis to test.

## The trap in the other direction: "observed power"

It is tempting, after a study is done, to compute "the power we achieved" from the result itself. This number is a repackaging of the p-value already in hand and adds no new information. To assess a finished study's result, look at the width of its confidence interval, and check whether the effect's sign or size might be exaggerated (a **Type S/Type M error** check) rather than computing power retroactively.

> **Do it yourself**
>
> - [How to: plan a sample size](./how-to/plan-a-sample-size.md) — power and precision calculations in Python, with a sensitivity table.
> - [Notebook: power and pilot studies](../notebooks/power-and-pilot-studies.ipynb) — see why a small pilot's effect size misleads.

> **Learn more**
>
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §16.1 "The problem with statistical power" (pp. 291–293) and §16.5 "Design calculations after the data have been collected" (pp. 304–306) — the Type S/Type M alternative to retroactive power.
> - [Lakens (2022)](https://lakens.github.io/statistical_inferences/), *Improving Your Statistical Inferences*, Ch. 8 "Sample Size Justification" — power analysis plus other defensible justifications.
> - Hoenig & Heisey (2001), "The abuse of power," *The American Statistician* 55(1), 19–24 — why "observed power" is just a restatement of the p-value.

---
**Previous:** [Module home](./README.md) · **Next:** [Effect size →](./effect-size.md) · [Glossary](../glossary.md)
