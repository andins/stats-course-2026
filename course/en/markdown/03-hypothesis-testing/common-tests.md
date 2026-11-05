# Common Tests: A Quick Tour

**In plain terms:** most "named" statistical tests ask "are these numbers different from those numbers (or from a reference value), in some specific way?" The table below maps the common ones.

| Test | Use it to ask... | Example |
|---|---|---|
| One-sample t-test | Is this group's average different from a fixed reference value? | Is average LDL cholesterol in this clinic different from the known population average? |
| Two-sample t-test | Do two independent groups have different averages? | Carriers vs. non-carriers of a gene variant, average LDL cholesterol. |
| Paired t-test | Did the same units change, on average, between two measurements? | Each patient's blood pressure before vs. after treatment. |
| One-way ANOVA | Do three or more independent groups differ in their averages? | LDL cholesterol across three genotype classes (non-carrier, heterozygous, homozygous). |
| Chi-squared test | Are two categorical variables associated? | Is "disease present" associated with "treatment group"? |
| Correlation (Pearson's r) | Is there a linear relationship between two continuous variables? | Age vs. LDL cholesterol. |

## Variants

- **Welch's t-test** vs. **Student's t-test**: Welch's doesn't assume the two groups have equal variability (spread), while Student's does. Welch's is the safer default — it costs almost nothing when variances *are* equal, and protects you when they aren't.
- **Nonparametric alternatives** (Mann-Whitney U, Wilcoxon, Kruskal-Wallis): used when the data is not close to bell-shaped, or has serious outliers. A common misconception: people often think these compare *medians* — in general they compare whether one group tends to produce *larger values* than the other (called **stochastic dominance**), which is the same as comparing medians only when the two groups' distributions have a similar shape.

## Tests and regression

Every test in this table can be rewritten as a **regression** — the same underlying question, phrased as "fit a line/model and look at a coefficient," rather than as a named recipe. The regression version is usually easier to extend (add more variables, handle unequal variability, etc.). See [What is regression](../04-regression-basics/what-is-regression.md) and [Tests as regressions](../04-regression-basics/tests-as-regressions.md).

## How to pick

Rather than memorizing this table, ask: *what kind of outcome do I have (continuous number, category, count)?* and *how many groups am I comparing?* That narrows it to one or two rows immediately.

> **Do it yourself**
>
> [How to: run a common test](./how-to/run-a-common-test.md) — each test in the table in Python, reported as an estimate with a confidence interval.

> **Learn more**
>
> - [Lindeløv (2019)](https://lindeloev.github.io/tests-as-linear/), "Common statistical tests are linear models" (free online) — a cheat sheet and worked R code for each test in the table.
> - Delacre, Lakens & Leys (2017), "Why psychologists should by default use Welch's t-test instead of Student's t-test," *International Review of Social Psychology* 30(1), 92–101.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §7.3 "Formulating comparisons as regression models", pp. 99–101.

---
**Previous:** [P-values and significance](./p-values-and-significance.md) · [Module home](./README.md) · **Next:** [Checking assumptions →](./checking-assumptions.md) · [Glossary](../glossary.md)
