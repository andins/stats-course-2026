# Classical tests: assumptions, checks, and regression equivalents

This is the lookup table for [SKILL.md](../SKILL.md). For each test: purpose, assumptions, how to check them, the regression/GLM equivalent, and a robust/nonparametric/Bayesian fallback. References use short keys resolved in [core-references.md](./core-references.md).

## 1. One-sample t-test

- **Purpose**: is the mean of one group different from a fixed value μ₀?
- **Assumptions**: observations independent; population approximately normal (or n large enough for CLT to make the sampling distribution of the mean approximately normal).
- **Checks**: QQ-plot / histogram of the data; Shapiro-Wilk as a supplement, not a substitute — note it's underpowered for small n and over-sensitive for large n (don't let a single p-value decide this). See `check_normality()` in [assumption_checks.py](../scripts/assumption_checks.py).
- **Regression equivalent**: intercept-only OLS, `y ~ 1`; the t-statistic on the intercept equals the one-sample t-test statistic.
- **Fallback if violated**: Wilcoxon signed-rank test (nonparametric); bootstrap CI for the mean.
- **References**: GELMAN_ROS (regression framing); WASSERMAN (CLT, classical derivation); CASELLA_BERGER (exact theory).

## 2. Two-sample t-test (independent groups)

- **Purpose**: compare means of two independent groups.
- **Variants**: Student's (assumes equal variances) vs **Welch's** (does not).
- **Assumptions**: independence within and between groups; approximate normality of each group (or large n); Student's variant additionally assumes equal variances.
- **Checks**: QQ-plots per group; Levene's test (or Brown-Forsythe) for variance homogeneity — see `check_variance_homogeneity()`; boxplots/stripplots for outliers.
- **Default recommendation**: use **Welch's t-test by default** rather than Student's — it's nearly as powerful when variances are equal and much safer when they aren't (DELACRE_LAKENS_LEYS). Most software (`scipy.stats.ttest_ind(..., equal_var=False)`) makes this a one-line choice.
- **Regression equivalent**: `y ~ group` OLS with a 0/1 dummy for group; the slope's t-test equals Student's two-sample t-test. For the Welch-robust version, fit OLS and use heteroskedasticity-consistent (HC3) standard errors, or weighted least squares — this reproduces Welch's test without needing a separate named procedure.
- **Fallback if violated**: Mann-Whitney U / Wilcoxon rank-sum (nonparametric, tests stochastic dominance not strictly "means"); Yuen's trimmed-mean test or bootstrap (WILCOX_ROBUST); Bayesian "BEST" estimation (KRUSCHKE_2013) when you want full posterior distributions over the difference and effect size instead of a single p-value.

## 3. Paired t-test

- **Purpose**: compare two measurements on the same units (before/after, matched pairs).
- **Assumptions**: the *differences* are independent across pairs and approximately normal (not the raw scores).
- **Checks**: QQ-plot of the differences; Shapiro-Wilk on the differences.
- **Regression equivalent**: `diff ~ 1` OLS (same as one-sample t-test on the differences), or a mixed-effects model with a random intercept per pair if there are more than two repeated measurements.
- **Fallback if violated**: Wilcoxon signed-rank test on the differences.

## 4. One-way ANOVA

- **Purpose**: compare means across 3+ independent groups.
- **Assumptions**: independence; approximate normality of residuals within each group; homogeneity of variance across groups.
- **Checks**: residual QQ-plot and residual-vs-fitted plot (preferred over single test statistics); Levene's test for variance homogeneity.
- **Regression equivalent**: ANOVA **is** OLS with a categorical predictor (dummy-coded group); the F-test from `statsmodels.formula.api.ols('y ~ C(group)').fit()` is algebraically identical to the classical ANOVA F-test (LINDELOV; GELMAN_ROS).
- **If variances differ**: Welch's ANOVA (`scipy.stats.oneway... ` / `pingouin.welch_anova`, or OLS + HC3 robust SEs + a robust Wald F-test) rather than classical ANOVA.
- **Fallback if violated further**: Kruskal-Wallis (nonparametric rank-based); robust ANOVA on trimmed means (WILCOX_ROBUST).
- **Post-hoc**: if doing many pairwise comparisons after ANOVA, address multiplicity (Tukey HSD) but also read GELMAN_HILL_YAJIMA on why blanket multiple-comparisons corrections are often not the right framing — a multilevel/partial-pooling model is frequently a better answer than a correction factor.

## 5. Two-way / factorial ANOVA

- **Purpose**: effects of two categorical factors (and their interaction) on a continuous outcome.
- **Assumptions**: same as one-way ANOVA, applied to each cell; balanced vs unbalanced design changes which sum-of-squares type (I/II/III) is appropriate.
- **Regression equivalent**: `y ~ C(factor1) * C(factor2)` OLS; this is the natural and more transparent formulation, especially for unbalanced designs where "Type II vs III SS" confusion disappears if you just read the regression coefficients and do explicit contrasts.

## 6. Chi-squared test of independence (contingency tables)

- **Purpose**: are two categorical variables associated?
- **Assumptions**: independent observations; expected cell counts not too small (common rule of thumb: all expected counts ≥ 5, or ≥ 1 with no more than 20% of cells below 5 — treat this as a heuristic, not a hard law, and say so).
- **Checks**: inspect the expected-counts table directly (`scipy.stats.chi2_contingency` returns it) rather than only trusting a rule of thumb.
- **Small-sample fallback**: Fisher's exact test (exact, no expected-count assumption, but classically for 2×2 tables — extensions exist for larger tables).
- **Regression equivalent**: logistic regression (binary outcome) or Poisson/log-linear regression (counts) with the categorical predictors and their interaction; the likelihood-ratio test for the interaction term is asymptotically equivalent to the chi-squared test of independence, and it extends naturally to covariates, ordinal predictors, and non-independence (e.g. clustering) that the classical test can't handle.

## 7. Chi-squared goodness-of-fit

- **Purpose**: does one categorical variable's distribution match a hypothesized set of proportions?
- **Assumptions/checks**: same expected-count heuristic as above.
- **Regression equivalent**: Poisson regression with an offset, testing whether a saturated vs. constrained (hypothesized proportions) model fits significantly worse.

## 8. Pearson correlation / simple linear regression significance test

- **Purpose**: is there a linear association between two continuous variables?
- **Assumptions**: linearity; bivariate normality (strictly, for the classical significance test of r); homoscedasticity; independence.
- **Checks**: scatterplot (always, first); residual plot after fitting `y ~ x`.
- **Regression equivalent**: the t-test on the slope of `y ~ x` OLS is algebraically identical to the significance test on Pearson's r.
- **Fallback**: Spearman's rank correlation (monotonic, not necessarily linear, robust to outliers) or Kendall's tau.

## 9. Nonparametric rank tests (Mann-Whitney, Wilcoxon, Kruskal-Wallis)

- **What they actually test**: a common misconception is that they test "medians" — in general they test **stochastic dominance** (whether one distribution tends to produce larger values than the other), which equals a median comparison only under the added assumption of equal-shape distributions. State this caveat explicitly when recommending them.
- **Regression equivalent**: ordinal/rank regression, or the Van der Waerden / rank-based ANOVA formulation; for a quick robust alternative that keeps a regression interface, consider a quantile regression on the median instead.

## 10. Meta-analysis (pooling study-level estimates)

- **Purpose**: combine the effect estimates from several studies of the same question into one pooled estimate, and measure how much the studies disagree. The data are one `effect` and one standard error per study, on one common scale (raw mean difference, standardized mean difference, log odds ratio, log risk ratio) (BORENSTEIN_2009).
- **Assumptions**: studies are independent (one estimate per study, no overlapping samples); each study's standard error is known and correct; effects are on a comparable scale; under random effects, the true study effects are exchangeable draws from one distribution (roughly normal) around an average; the set of studies is not distorted by selection or publication bias.
- **Checks**: forest plot first (do intervals overlap, is one study extreme?); heterogeneity (Q, tau^2, I^2, HIGGINS_THOMPSON_2002) and a prediction interval (INTHOUT_2016); leave-one-out re-pooling; funnel plot and Egger's regression (EGGER_1997), which have little power below ~10 studies (STERNE_2011).
- **Regression equivalent**: an intercept-only weighted regression, `effect ~ 1`, with weights `1 / (se^2 + tau^2)`. The common-effect model sets tau^2 = 0. Random effects is a multilevel model with study as the cluster (partial pooling: noisy studies are shrunk toward the average). Meta-regression adds study-level covariates; treat it as exploratory (study characteristics are not randomized, and a relationship across studies need not hold within a study).
- **Default and fallbacks**: random effects by default for life-science studies, which are rarely exact replications (tau^2 by Paule-Mandel or REML; DERSIMONIAN_LAIRD_1986 is the traditional but less accurate default). With few studies use the Hartung-Knapp interval (INTHOUT_2014) or a Bayesian model; for dependent estimates (several per study) use cluster-robust SEs or a multilevel model with a study level; with raw data from every site, analyze it as clustered data instead of pooling summaries.
- **Reporting**: pool estimates, never p-values or counts of significant studies; give the number of studies and how they were found (PAGE_PRISMA_2021), the pooled estimate with CI, tau/I^2 and the prediction interval, and the limits of study quality and publication bias.

## General diagnostics philosophy

Favor **plots over single assumption-check p-values** wherever practical: a residual QQ-plot and residual-vs-fitted plot usually convey more about whether a classical test's assumptions matter *for this sample size and this effect* than a Shapiro-Wilk/Levene p-value alone, because (a) normality tests are underpowered to detect small deviations at small n (where deviations matter most) and overpowered to flag trivial deviations at large n (where the CLT protects you anyway), and (b) what actually matters is whether the deviation is large enough to bias the inference you care about, which a plot plus a sensitivity check (e.g., rerun with the robust alternative, see if conclusions change) answers directly.

**Multicollinearity** (whenever a model has more than one predictor/adjustment covariate): check Variance Inflation Factors with `check_multicollinearity()` in [assumption_checks.py](../scripts/assumption_checks.py). High collinearity inflates coefficient SEs and destabilizes individual estimates even though overall fit is unaffected — VIF > 5/10 are heuristic warning levels, not hard thresholds (OBRIEN_2007).

**Non-independence** (clustered/hierarchical or time-dependent data): a classical test's/regression's independence assumption can fail in two common ways this table doesn't cover row-by-row — grouped/repeated observations and autocorrelated (e.g. time-ordered) observations. See [clustered_and_timeseries_template.py](../scripts/clustered_and_timeseries_template.py) for the decision tree (complete pooling vs. no pooling vs. multilevel for clustering; checking autocorrelation before assuming a time-series model is even needed, then HAC SEs or a proper time-series model if it is).
