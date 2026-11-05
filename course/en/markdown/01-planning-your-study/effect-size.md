# Effect Size

**In plain terms:** effect size answers "how big," as opposed to a p-value, which only answers "how sure."

## Why "is there a difference" isn't the useful question

With enough data, almost *any* real-world difference becomes "statistically significant" — even a trivially small one. If Theo's new blood-pressure drug lowers blood pressure by an average of 0.1 mmHg, a large enough trial will find that "significant," even though it is medically meaningless. Effect size is what tells you whether a result is significant *and* large enough to matter.

## Some common effect-size measures

- **Difference in means** (in the outcome's natural units, e.g. "lowered blood pressure by 8 mmHg") — the most interpretable when the units mean something to your audience.
- **Standardized difference (Cohen's d)** — the difference in means divided by the data's spread (standard deviation). Useful for comparing effect sizes across studies that measured things differently, or when the outcome's raw units aren't intuitive. Conventionally, d≈0.2 is "small," d≈0.5 is "medium," d≈0.8 is "large" — but treat these as rough conventions, not laws of nature; what counts as a meaningful effect depends on the subject matter.
- **Correlation (r)** — strength of a linear relationship between two continuous variables, from -1 to 1.
- **Odds ratio / risk ratio** — for yes/no outcomes (e.g. "treated patients were 2x as likely to recover").

## Where effect size shows up

- **Before data collection**: you need a *guess* at the effect size to plan sample size (see [Sample size and power](./sample-size-and-power.md)).
- **After data collection**: report the effect size (with a confidence interval) alongside — or instead of — a bare p-value. "Carriers had 6% higher LDL cholesterol (95% CI: 1–11%)" says much more than "p = 0.03."
- **Combining studies**: effect sizes (and their standard errors) are what a [meta-analysis](../07-special-data-structures/meta-analysis.md) pools, which is why all studies must report on the same scale.

## Common mistake

Treating a "significant" result as automatically important, or a "non-significant" result as automatically meaning "no effect." A small study can easily produce a non-significant result even for a real, meaningful effect — that's a power problem, not evidence of "no effect." Always ask about the size and the uncertainty around it, not just the p-value.

> **Do it yourself**
>
> [How to: plan a sample size](./how-to/plan-a-sample-size.md) — turn a raw difference and an SD into Cohen's d and a sample size.

> **Learn more**
>
> - [Lakens (2022)](https://lakens.github.io/statistical_inferences/), *Improving Your Statistical Inferences*, Ch. 6 "Effect Sizes" — how to compute, interpret and report common effect sizes.
> - Sullivan & Feinn (2012), "Using effect size — or why the P value is not enough," *Journal of Graduate Medical Education* 4(3), 279–282 — a short, readable primer.
> - Cohen (1988), *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.), Ch. 2 "The t Test for Means" — origin of the small/medium/large conventions for d; treat them as conventions, not laws.

---
**Previous:** [Sample size and power](./sample-size-and-power.md) · [Module home](./README.md) · **Next:** [Other design-phase considerations →](./design-considerations.md) · [Glossary](../glossary.md)
