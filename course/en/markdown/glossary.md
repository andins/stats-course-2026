# Glossary

Short, plain-language definitions of terms used across these explainers. Alphabetical. Each term links back to the page that explains it in more depth, where one exists.

**Adjustment set** — the list of variables you statistically "control for" in a model to try to isolate the effect of one variable on another. See [Causal diagrams](./05-prediction-vs-causation/causal-diagrams.md).

**Allele** — one version of a gene. A person inherits two copies of most genes, so they carry two alleles at each; a variant is an allele that differs from the usual (reference) one.

**Alpha (significance level)** — the false-positive rate you're willing to accept, chosen *before* looking at the data. Conventionally 0.05 (a 1-in-20 chance). See [P-values and significance](./03-hypothesis-testing/p-values-and-significance.md).

**Attenuation bias** — the tendency of a regression slope to be biased toward zero when a predictor is measured with random error. Does not shrink with more data. See [Measurement error](./06-building-models/measurement-error.md).

**Autocorrelation** — when a value in a time-ordered series is correlated with its own past values (today's temperature predicts tomorrow's). See [Time series data](./07-special-data-structures/time-series-data.md).

**Bayesian inference** — a framework that treats unknown quantities as probability distributions that get updated as data arrives, rather than producing a single p-value. See [Bayesian methods](./07-special-data-structures/bayesian-methods.md).

**Carrier** — a person who has at least one copy of a particular gene variant. "Heterozygous" carriers have one copy, "homozygous" carriers have two.

**Collider** — a variable caused by *both* your exposure and your outcome. Conditioning on it can create a fake association where none exists. See [Causal diagrams](./05-prediction-vs-causation/causal-diagrams.md).

**Confidence interval (CI)** — a range of plausible values for an unknown quantity (like a true effect size), built so that, if you repeated the study many times, about 95% of such intervals would contain the true value. See [P-values and significance](./03-hypothesis-testing/p-values-and-significance.md).

**Confounder** — a variable that causally affects *both* your exposure and your outcome, creating an association between them even if neither directly causes the other. See [Causal diagrams](./05-prediction-vs-causation/causal-diagrams.md).

**Cross-validation** — repeatedly splitting data into "fit" and "test" portions to see how well a model generalizes to data it hasn't seen. See [Cross-validation and model checking](./06-building-models/cross-validation-and-model-checking.md).

**DAG (Directed Acyclic Graph)** — a diagram of arrows between variables showing assumed cause-and-effect directions, with no loops. See [Causal diagrams](./05-prediction-vs-causation/causal-diagrams.md).

**Effect size** — how *big* a difference or relationship is, in meaningful units — not just whether it's "significant." See [Effect size](./01-planning-your-study/effect-size.md).

**Exploratory vs. confirmatory analysis** — whether you're looking for patterns you haven't decided on yet (exploratory) vs. testing one specific, pre-decided comparison (confirmatory). See [Exploratory vs. confirmatory](./02-exploring-data/exploratory-vs-confirmatory.md).

**Forest plot** — the standard picture of a meta-analysis: one row per study (its estimate and interval) and a diamond for the pooled estimate. See [Meta-analysis](./07-special-data-structures/meta-analysis.md).

**Garden of forking paths** — the many small, unrecorded decisions (which outliers to drop, which subgroup to look at) that can turn noise into an apparently "significant" result, even with good intentions. See [Exploratory vs. confirmatory](./02-exploring-data/exploratory-vs-confirmatory.md).

**Genotype** — which versions (alleles) of a gene or variant a person has, e.g. no copies, one copy or two copies of a variant. Often coded as 0, 1 or 2 for analysis.

**GLM (Generalized Linear Model)** — the regression family that extends ordinary regression to outcomes that aren't plain continuous numbers (yes/no, counts). See [Generalized linear models](./04-regression-basics/generalized-linear-models.md).

**Heterogeneity** — in a meta-analysis, real differences between the true effects of the studies, beyond chance. Measured by τ (their standard deviation) and I² (the share of the variability that is real rather than chance). See [Meta-analysis](./07-special-data-structures/meta-analysis.md).

**Imputation** — filling in missing values with a plausible estimate instead of dropping the row. See [Missing data](./02-exploring-data/missing-data.md).

**Linkage disequilibrium (LD)** — the tendency of genetic variants that sit close together on a chromosome to be inherited together, so their genotypes are strongly correlated. A source of multicollinearity between variants. See [Multicollinearity](./06-building-models/multicollinearity.md).

**Measurement error** — the gap between an observed, recorded value and the true quantity it's meant to stand in for (e.g. a noisy instrument or a self-reported proxy). Error in a predictor biases a regression slope toward zero (see Attenuation bias); error in an outcome mostly adds noise. See [Measurement error](./06-building-models/measurement-error.md).

**Mediator** — a variable that sits *on the causal path* between your exposure and outcome (exposure causes it, and it causes the outcome). Don't adjust for it if you want the total effect. See [Causal diagrams](./05-prediction-vs-causation/causal-diagrams.md).

**Meta-analysis** — combining the effect estimates (and their standard errors) from several studies of the same question into one pooled estimate, weighting precise studies more, and measuring how much the studies disagree. See [Meta-analysis](./07-special-data-structures/meta-analysis.md).

**Multicollinearity** — when predictors in a model are highly correlated with each other, making it hard to tell their individual effects apart. See [Multicollinearity](./06-building-models/multicollinearity.md).

**Multilevel / mixed-effects model** — a model for grouped data that partially shares (“pools”) information across groups instead of treating them as fully separate or fully identical. See [Clustered and hierarchical data](./07-special-data-structures/clustered-and-hierarchical-data.md).

**Observational data** — data where the "exposure" of interest wasn't assigned by anyone running an experiment — it's just whatever happened. See [Experiments vs. observational data](./05-prediction-vs-causation/experiments-vs-observational-data.md).

**Overfitting** — when a model learns the noise in your specific sample rather than the general pattern, performing well on the data it was built on and poorly on new data. See [Overfitting and regularization](./06-building-models/overfitting-and-regularization.md).

**P-value** — the probability of seeing a result at least this extreme *if there were truly no effect*. It is not the probability that the effect is real, and it's only well-calibrated for a single hypothesis decided before seeing the data, ideally from a well-designed experiment — even then, an effect-size estimate with a confidence interval is more informative than the verdict alone. See [P-values and significance](./03-hypothesis-testing/p-values-and-significance.md).

**Polygenic score** — a single risk number for a person, built by adding up the small effects of many genetic variants. Fitting one to a small sample is a textbook overfitting risk. See [Overfitting and regularization](./06-building-models/overfitting-and-regularization.md).

**Pooling (no/complete/partial)** — three strategies for grouped data: analyze each group separately (no pooling), ignore the grouping (complete pooling), or share information across groups with shrinkage (partial pooling/multilevel). See [Clustered and hierarchical data](./07-special-data-structures/clustered-and-hierarchical-data.md).

**Power (statistical)** — the probability a study will detect a true effect of a given size, if it exists. Low power means even real effects often go undetected. See [Sample size and power](./01-planning-your-study/sample-size-and-power.md).

**Prediction interval (meta-analysis)** — the range where the true effect of a *new* study would be expected to fall. Wider than the confidence interval of the average effect, and often the more honest summary when studies differ. See [Meta-analysis](./07-special-data-structures/meta-analysis.md).

**Publication bias** — the published literature overstates effects because studies with striking results are more likely to be published than studies that found nothing. See [Meta-analysis: bias and pitfalls](./07-special-data-structures/meta-analysis-pitfalls.md).

**Random-effects model (meta-analysis)** — assumes every study has its own true effect, scattered around an average, rather than one common true effect. The usual default for combining life-science studies. See [Meta-analysis](./07-special-data-structures/meta-analysis.md).

**Randomized experiment** — a study where the exposure/treatment is assigned to units by a chance mechanism the researcher controls, which is what makes causal claims credible. See [Experiments vs. observational data](./05-prediction-vs-causation/experiments-vs-observational-data.md).

**Regularization** — deliberately shrinking a model's coefficients toward zero to reduce overfitting, at a small cost in bias. See [Overfitting and regularization](./06-building-models/overfitting-and-regularization.md).

**Residual** — the gap between what a model predicted and what was observed, for a single data point.

**Type I error** — a false positive: concluding there's an effect when there isn't one.

**Type II error** — a false negative: missing a real effect.

**Type S / Type M error** — getting the *sign* (S) or *magnitude* (M) of an effect wrong, a more useful way to think about errors in small/noisy studies than power alone. See [Sample size and power](./01-planning-your-study/sample-size-and-power.md).

**Variant of uncertain significance (VUS)** — a genetic variant whose clinical meaning is not yet known, for example whether it raises disease risk. Studies like Mia's try to provide the evidence.

**VIF (Variance Inflation Factor)** — a number quantifying how much a predictor's uncertainty is inflated by its correlation with other predictors. See [Multicollinearity](./06-building-models/multicollinearity.md).
