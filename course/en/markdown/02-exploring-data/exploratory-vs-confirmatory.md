# Exploratory vs. Confirmatory Analysis

**In plain terms:** confirmatory analysis tests one specific idea you committed to *before* seeing the data, ideally from a well-designed experiment. Exploratory analysis is looking around in data to find patterns you hadn't specified in advance. A p-value's advertised guarantees only hold in the first setting — it's not a matter of trusting it more or less, but of whether it's even the right tool to learn from the data.

## Mia's example, two ways

- **Confirmatory**: Mia designed a cohort study specifically to compare LDL cholesterol between carriers and non-carriers of a variant in the LDLR gene (a "carrier" has at least one copy of the variant), decided on that single comparison beforehand, and is now analyzing the results. This is the textbook setting classical hypothesis tests were built for — though even here, reporting the LDL difference with a confidence interval teaches more than a significant/non-significant verdict alone.
- **Exploratory**: Mia has a big spreadsheet of clinic data — age, sex, BMI, diet score, genotypes at many variants, LDL, and a dozen other columns — and wants to know "what's associated with higher LDL?" with no single comparison decided in advance.

Both are legitimate things to do with data. The mistake is treating the second one like the first.

## Why it matters: the "garden of forking paths"

If you look at a dataset with 10 variables and test all the pairwise relationships, you're very likely to find something that looks "significant" by chance alone — even if nothing in the data is related to anything else. The danger isn't just deliberately cherry-picking your favorite result (p-hacking); it's that *any* researcher, in good faith, makes dozens of small unrecorded decisions while exploring (which outliers to exclude, which grouping to use, which subgroup to focus on) that can each nudge a result toward "significant." This is sometimes called the **garden of forking paths**: even without intending to cheat, the many paths not taken still inflate how often you'll stumble on a false pattern.

## What to do instead, if you're exploring

- Don't present a p-value from an exploratory pass as if it settled the question. Call it what it is: a hypothesis to test properly later, not a confirmed finding.
- Lean on visualization first (see [EDA basics](./eda-basics.md)) rather than a battery of tests.
- If a pattern looks promising, the appropriate next step is collecting new, independent data (or holding some data back in advance) to test it properly — that is what turns an exploratory finding into a confirmatory one.

## A quick way to tell which one you're doing

Ask: **was this specific comparison decided before I saw this data?** If yes — a pre-registered experiment, a trial designed around one hypothesis — you're in confirmatory territory. If the comparison only became interesting *after* looking at the data, you're exploring, whether or not the word "test" comes up.

Note this is a separate question from whether the data came from a randomized experiment: a well-designed, randomized trial can still be analyzed exploratorily (e.g. scanning many secondary endpoints or subgroups it wasn't specifically designed to test) — randomization fixes *confounding*, not *which comparisons you go looking for*.

> **Learn more**
>
> - Gelman & Loken (2014), "The statistical crisis in science," *American Scientist* 102(6), 460–465 — the "garden of forking paths" in plain language.
> - Simmons, Nelson & Simonsohn (2011), "False-positive psychology," *Psychological Science* 22(11), 1359–1366 — how flexible analysis choices inflate false positives.
> - Wagenmakers et al. (2012), "An agenda for purely confirmatory research," *Perspectives on Psychological Science* 7(6), 632–638 — why the exploratory/confirmatory line matters.

---
**Previous:** [Module home](./README.md) · **Next:** [EDA basics →](./eda-basics.md) · [Glossary](../glossary.md)
