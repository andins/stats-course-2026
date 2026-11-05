# Analysis triage: the questions to answer before picking a method

This is the decision guide for [SKILL.md](../SKILL.md) Step 0/1. Answer these questions *before* reaching for a test or building a model — they determine which parts of this skill apply. References use short keys resolved in [core-references.md](./core-references.md).

## Question 0: Has the data already been collected?

If the data doesn't exist yet and the question is "how many samples do I need," this is a design-phase (power/precision) question, not an analysis of existing data — resolve it before anything else and only move on to Question 1 once data collection is planned or already done.

- **Power analysis for a planned hypothesis test**: needs alpha, target power (0.8 is conventional, but say so as a convention, not a law), a test type, and an effect size. **Effect-size sourcing is the hard part**: don't plug in a point estimate from a small pilot at face value — small studies produce noisy, often *inflated* effect-size estimates (Type M/magnitude error, GELMAN_CARLIN_2014), so a power calculation built on one can be badly underpowered in practice. Prefer the smallest effect size of practical/clinical interest, a literature or meta-analytic estimate, or report a small sensitivity table across a few plausible effect sizes rather than a single number presented as exact.
- **Precision/CI-width planning**: for when there's no single pre-specified test — e.g. "how big a sample to estimate this proportion within ±3 points" (common when planning a survey or an exploratory data-collection effort). Plan for a CI width/margin of error directly rather than forcing the question into a power-analysis shape it doesn't have.
- Use [power_analysis_template.py](../scripts/power_analysis_template.py): `analytic_sample_size()` covers the standard closed-form designs (t-test, ANOVA, proportions, correlation, chi-squared) via `statsmodels.stats.power`; `simulate_power()` / `find_sample_size_by_simulation()` is the Monte Carlo fallback for anything a closed form doesn't cover (regression with covariates, GLMs, clustering, unequal allocation, multilevel designs) — same simulate-many-times-and-check ethos as the test-vs-regression notebooks. `precision_sample_size_mean()` / `precision_sample_size_proportion()` cover the CI-width case.
- **Never compute "observed/post-hoc power"** from data you've already collected and treat it as informative — it's a deterministic, monotonic function of the p-value and adds nothing beyond it (HOENIG_HEISEY_2001). If the goal is to assess a result after the fact, look at the CI width and do a Type S/M error check (GELMAN_CARLIN_2014) instead of computing power retroactively.

## Question 1: Exploratory or confirmatory?

Classical hypothesis testing (p-values, pre-specified alpha, "reject/fail to reject") is only well-calibrated for **confirmatory analysis**: a specific hypothesis decided *before* looking at this data, ideally from a well-designed, controlled experiment or a pre-registered comparison. Outside that setting it should generally be avoided, not merely used with extra caution. Even inside it, treat the dichotomized verdict as the least useful part of the output — leading with the effect-size estimate and its confidence interval teaches more from the same data than "reject/fail to reject" does (GELMAN_CARLIN_2014). Most real-world requests — "what's going on in this dataset", "what drives X", open-ended dashboards, observational convenience samples — are **exploratory**, even when the user phrases the question as "is there a difference / effect / association".

**Signals it's confirmatory**: a designed experiment or RCT; a single pre-specified comparison decided before data collection; a pre-registration or analysis plan; a replication of a specific known effect.

**Signals it's exploratory**: "what's driving/associated with...", "find patterns/segments", dashboarding or reporting, observational/convenience data with no pre-registered comparison, many candidate variables with no single comparison singled out in advance, the user hasn't decided the comparison until after seeing the data.

**If it's not clear from context, ask directly** — e.g. "Was this comparison/hypothesis decided before you saw this data (e.g. from a pre-registered experiment), or are we looking for patterns in data you already have?" Don't default to confirmatory just because the user used the word "test" or "significant" — ask or infer from the data-collection story.

### If exploratory
- **Warn before running any classical test as "the answer."** Multiple implicit comparisons and researcher degrees of freedom inflate false-positive rates even without explicit p-hacking (GELMAN_LOKEN_2014, "garden of forking paths"). A p-value from an exploratory pass is at best a hypothesis-generating signal, not a confirmed finding.
- **Propose visualization-first EDA as the first concrete step** — see [eda_template.py](../scripts/eda_template.py) and the Notebook Workflow in SKILL.md. Look at the data from many angles (univariate distributions, missingness, pairwise relationships, subgroup structure, trends over time) before any model or test (TUKEY_EDA; GELMAN_EXPLORATORY_CONFIRMATORY).
- **Offer regression/GLM framing as a descriptive tool**, not a significance-test replacement: fit the relationship, report effect sizes and intervals, and frame them as "this is what the data show in this sample" rather than "this is confirmed." If the user wants a confirmed answer, the honest path is collecting (or holding out) independent data for a true confirmatory test.
- Once a pattern worth taking seriously emerges, it's fine to *also* report a p-value for it — just label it as exploratory/hypothesis-generating, not confirmatory.
- **Don't confuse "no exploratory tests" with "don't look at the data at all."** Checking missingness, impossible values, outliers, and data-entry errors is data hygiene, not forking paths — do it regardless of exploratory vs. confirmatory, before any model or test. The thing to avoid is peeking at the *hypothesis/comparison itself* and letting that peek steer which comparison you report.

### If confirmatory
Proceed with the classical hypothesis-testing workflow, but lead with the effect-size estimate and its confidence interval rather than the significant/non-significant verdict — even in this best-case setting, the estimate is more informative than the dichotomy (the course page "P-values and significance" in module 3 explains why). Look up the test family in [test-regression-equivalents.md](./test-regression-equivalents.md) for assumptions, checks, and the regression-equivalent formulation, per the existing SKILL.md workflow. If the comparison concerns the effect of a treatment/exposure (not just "is this sample different from that one"), it is also a causal question — carry it into Question 2 below rather than stopping at the test's p-value.

## Question 1c (evidence synthesis only): is the unit of analysis a study?

This is a different kind of request from the exploratory/confirmatory split above: the user is not analyzing raw observations but **combining the results of several studies** of the same question ("what do the published trials say overall", "pool these effect sizes", "is there publication bias", "why do the studies disagree"). Signals: a table with one row per study (effect, standard error, sample size), words like meta-analysis, systematic review, pooled estimate, heterogeneity, I², forest plot, funnel plot. Route to Step 1c of SKILL.md and [meta_analysis_template.py](../scripts/meta_analysis_template.py). Ask, if not already clear:

- **Is it really a meta-analysis?** If the user holds the raw data from every site or study (every patient, every plant), the better analysis is a multilevel/clustered model with site as the cluster, not pooling summaries.
- **Is the effect on one common scale for every study?** (same unit, or a standardized mean difference, or log odds/risk ratio.) If not, convert first (`effect_sizes_from_summaries()`); each study needs an effect and its *standard error* (not the SD, not the variance).
- **How were the studies found and selected?** A systematic, pre-specified search, or whatever the user happened to know? A convenience set of studies limits what any pooled number means; say so rather than hiding it behind a tight interval.
- **How many studies?** Under about 5-10, tau^2 is poorly estimated: use the Hartung-Knapp interval or a Bayesian model, and say how few there are. Two or three very different studies may be better shown side by side.
- **Is every estimate independent?** Several estimates from one study (two doses against one control, several outcomes) or from one group are not independent; choose one per study or model the dependence (clustering).
- **What designs are mixed?** Randomized and observational studies should not be blended into one number without a reason; the pooled estimate is no more causal than its studies (see Question 2a).

Pool estimates, never p-values or counts of significant studies. Report the random-effects estimate with its CI, the heterogeneity (tau, I^2) and a prediction interval, show a forest plot, and state the limits (study quality, selection, publication bias; the funnel/Egger checks have little power under ~10 studies, STERNE_2011). Meta-regression and subgroup comparisons are exploratory because study characteristics are not randomized. Citations: BORENSTEIN_2009; COCHRANE_HANDBOOK; INTHOUT_2016; PAGE_PRISMA_2021.

## Question 2: Prediction or causal interpretation?

This matters whenever the goal is to relate variables to each other — including a confirmatory test of a treatment/exposure effect, not just open-ended modeling. Ask if it isn't obvious from context — e.g. "Do you need to predict/forecast this outcome for new cases, or do you need to know whether changing X would actually change Y (i.e., would an intervention on X work)?" (SHMUELI_EXPLAIN_PREDICT).

- **Predictive goal**: you need accurate estimates/forecasts for new data, and you don't need to trust any individual coefficient as a causal effect. Any available predictor is fair game, flexible/regularized models are fine, and the model should be judged purely on out-of-sample performance (train/test split, cross-validation, proper scoring rules) — not on p-values or in-sample fit. Go straight to the modeling step.
- **Causal goal**: you need to know what would happen *if you intervened* on a variable (changing a price, a policy, a treatment) — i.e., a "why"/"what if" question, not just "what correlates." This requires an identification strategy, not just a well-fitting model. **Go to Question 2a before modeling.**

### Question 2a (causal branch only): was the exposure assigned by a well-designed experiment?

This is the single most important fork in the causal branch, and it's easy to skip past straight to "build a DAG" — don't. Ask it explicitly: "Was [exposure] assigned to units by you/the researcher (or by some other mechanism outside anyone's control) in a way that didn't depend on the units' other characteristics — e.g. randomized assignment in a designed experiment?"

- **Yes, a well-designed experiment (randomized, or as-good-as-randomized assignment)**: random assignment is, by construction, independent of every pre-treatment variable — measured or not — so it already blocks every backdoor path. This is the strongest causal identification strategy available, stronger than any adjustment-based estimate from observational data (IMBENS_RUBIN). Consequences:
  - The unadjusted difference between arms (e.g. the two-sample test/regression from Question 1's confirmatory branch) is *already* a valid causal estimate of the average treatment effect. A full confounding-oriented DAG is not required.
  - A lightweight DAG/covariate list is still useful, but only to pick **baseline (pre-treatment) covariates to adjust for to reduce residual variance and tighten the CI** (the ANCOVA move) — this improves precision, not validity.
  - **Never adjust for anything measured *after* assignment** (post-treatment variables/mediators/outcomes of the treatment itself) — conditioning on them reintroduces bias even inside a randomized experiment, because they're affected by the very treatment whose effect you're estimating.
  - Proceed to the modeling step in **experimental** causal mode.
- **No, the exposure was observed/self-selected (observational data)**: there is no design-based guarantee that confounders are balanced across exposure levels. Proceed to full DAG elicitation below, and when reporting the result, say explicitly that this is an adjustment-based ("selection on observables") estimate — the weakest common causal identification strategy, valid only if the adjustment set captures *all* confounding and nothing else (HERNAN_ROBINS). If the user describes something that sounds like a natural experiment, an instrument, a discontinuity in an assignment rule, or a clean pre/post comparison with a control group, flag that a quasi-experimental design (instrumental variables, difference-in-differences, regression discontinuity) might identify the effect more credibly than adjustment alone — but treating those methods is out of scope for this version of the skill; note it as a direction for further investigation rather than implementing it here.

### Building a causal DAG with the user

Use [causal_dag_builder.py](../scripts/causal_dag_builder.py): `create_schema_template()` generates an editable schema pre-populated with one node per *recorded* column in the dataset, so nothing already in hand is silently forgotten. The user (guided by the agent) then fills in roles and edges, and can add nodes for variables that were **never recorded** but are believed to matter causally — e.g. unmeasured confounders — making that assumption explicit instead of silently assuming it away (PEARL_CAUSALITY; PEARL_BOOK_OF_WHY). This step is required for the observational branch of Question 2a, and optional (precision-covariates only) for the experimental branch.

Facilitate this with the user by asking, in order:

1. **Outcome**: "What is the outcome you ultimately care about?"
2. **Exposure**: "What is the variable whose causal effect you want to know — the thing you'd imagine 'intervening on'?"
3. **Role of each recorded covariate**: for each remaining variable, ask whether it's plausibly (a) a cause of the exposure, (b) a cause of the outcome, (c) both — i.e. a **confounder**, needs adjustment — (d) a consequence of the exposure — a **mediator**: don't adjust for it if you want the *total* effect — or (e) a consequence of both exposure and outcome — a **collider**: never condition on it, doing so can create a spurious association.
4. **Direction via timing**: "What happened first?" Causes must (weakly) precede effects in time — use the sequence of events to rule out implausible edge directions. (In the experimental branch, this question is already answered for the exposure itself — anything measured after assignment is out of bounds for adjustment regardless of its role.)
5. **Mechanism check**: "Can you describe *how* A would affect B?" If no plausible mechanism comes to mind, be skeptical of that edge rather than including it just because the variables are correlated.
6. **Unmeasured variables**: explicitly ask, "Is there anything you believe affects [exposure] and/or [outcome] that wasn't recorded in this dataset?" Add these as `recorded: false` nodes in the schema even without data for them.
7. Keep a running list of edges the user is unsure about (`open_questions` in the schema) — an approximate DAG the team can revisit beats silence on an assumption.

Once sketched, call `validate_schema()` first (checks the graph is acyclic and every edge references a known node — a cyclic graph breaks every guarantee below, so treat a validation failure as "go back and fix the DAG," not a warning to ignore), then use `draw_dag()` to visualize it back to the user for a sanity check, and `naive_adjustment_set()` for a first-pass candidate adjustment set. That heuristic (common ancestors of exposure and outcome, excluding exposure's descendants) is **not** a full implementation of Pearl's backdoor criterion — for anything beyond a small/simple DAG, say so explicitly and recommend validating with a dedicated tool (e.g. R's `dagitty`) or a domain expert before trusting the adjustment set (PEARL_CAUSALITY).

### After Question 2a / the DAG (or, if purely predictive, directly)

Move to the modeling step — see [regression_modeling_template.py](../scripts/regression_modeling_template.py) — which branches three ways: predictive mode is scored by held-out performance; causal-experimental mode reports the (optionally precision-adjusted) exposure coefficient with a CI, identified by the experiment's design; causal-observational mode reports the exposure coefficient adjusted for the DAG-identified set, with a CI and an explicit statement that the estimate is causal only under the no-unmeasured-confounding assumption (HERNAN_ROBINS; IMBENS_RUBIN).

## Missing data: a default, not a full treatment

Missing-data methodology is its own thorny topic; this skill takes a pragmatic default rather than a full treatment of it. After the EDA step surfaces how much is missing and in which columns (`plot_missingness()`):

- **Default**: use listwise deletion (drop rows with missing values in the columns the current model actually uses) and say explicitly how many rows were dropped and what fraction that is. This is simple and unbiased under MCAR (missingness unrelated to any variable, observed or not).
- **When to get more careful**: if a large fraction of rows are dropped, or missingness plausibly depends on the outcome or on an unobserved variable (MAR/MNAR), listwise deletion can bias estimates — flag this explicitly rather than silently dropping rows, and point the user to `LITTLE_RUBIN_MISSING` for multiple imputation or model-based alternatives rather than improvising a fix in the moment.

