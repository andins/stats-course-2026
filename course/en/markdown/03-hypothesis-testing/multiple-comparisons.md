# Multiple Comparisons

**In plain terms:** the more tests you run, the more likely *at least one* will look "significant" by pure chance — even if nothing real is going on anywhere.

## A simple illustration

If you flip 20 fair coins and ask "is any one of them unfair?", testing each individually at the usual 5% significance threshold, you'd expect roughly one "significant" result on average — purely by chance, even though every coin is perfectly fair. Run enough tests on enough variables, and you *will* find "significant" results in pure noise.

## Where this shows up in practice

- Comparing many pairs of groups after an ANOVA (e.g. all possible pairs among 5 genotype groups).
- Testing many genes, many biomarkers, or many outcome measures against the same grouping variable.
- Any exploratory scan across many variables (see [Exploratory vs. confirmatory analysis](../02-exploring-data/exploratory-vs-confirmatory.md) — this is the same underlying issue).

## The classic fix: corrections

Methods like the Bonferroni or Holm correction make each individual test's threshold stricter, in proportion to how many tests you're running, so the *overall* chance of any false positive stays controlled. This works, but it applies the same correction regardless of structure — treating 20 unrelated genes and 20 related repeated measurements identically, for instance.

## A more modern alternative: partial pooling

When you're comparing many related groups (e.g. LDL cholesterol across 30 different families, or a biomarker across 50 patients), a **multilevel model** (see [Clustered and hierarchical data](../07-special-data-structures/clustered-and-hierarchical-data.md)) often handles the "many comparisons" problem more gracefully than a blanket correction — it naturally pulls noisy, extreme-looking individual estimates back toward the overall average, which is conceptually similar to what a correction is trying to achieve, but tends to produce better-calibrated, more usable estimates for each group rather than just a stricter threshold.

## The takeaway

If you're running — or see — many tests at once, ask how the "many comparisons" problem was handled, the same way you'd ask about any other assumption. "We ran 40 tests and 2 were significant at p<0.05" is close to what you'd expect from pure chance alone, and isn't evidence of anything by itself.

> **Learn more**
>
> - Benjamini & Hochberg (1995), "Controlling the false discovery rate," *Journal of the Royal Statistical Society B* 57(1), 289–300 — the paper behind FDR control.
> - Gelman, Hill & Yajima (2012), "Why we (usually) don't have to worry about multiple comparisons," *Journal of Research on Educational Effectiveness* 5(2), 189–211 — the partial-pooling alternative.
> - Wasserman (2004), *All of Statistics*, Ch. 10 "Hypothesis Testing and p-values" (multiple-testing section) — a compact, rigorous treatment of Bonferroni and FDR.

---
**Previous:** [Checking assumptions](./checking-assumptions.md) · [Module home](./README.md) · **Next module:** [Regression basics →](../04-regression-basics/README.md) · [Glossary](../glossary.md)
