# How to: analyze clustered data

**Use this when:** your observations come in groups (relatives within families, patients within clinics, repeated measurements on the same patient), so rows from the same group resemble each other. The ideas are on the [Clustered and hierarchical data](../clustered-and-hierarchical-data.md) page.

To see how much a plain analysis can mislead you, and what partial pooling does to small groups, use the [clustered data notebook](../../notebooks/clustered-data-overconfidence.ipynb) (download it and open it in Jupyter, VS Code or Colab).

## Steps

1. **Identify the cluster column and the level of each predictor.** Does the predictor of interest vary *between* clusters (a variant carried by whole families) or *within* them (a measurement on each relative, such as age)? This determines which options are available.
2. **Measure how much the clustering matters:** the intraclass correlation (ICC) and the design effect. An ICC near 0 means clustering hardly matters; a high ICC means 300 rows may carry the information of far fewer independent observations.
3. **Fit the default model:** the plain regression with **cluster-robust standard errors** (complete pooling). It leaves the estimate alone and corrects the interval.
4. **Compare with one alternative** that suits your situation (table below): cluster means, family fixed effects (no pooling), or a multilevel model (partial pooling).
5. **Report the estimate with its interval and say how many clusters there were.** The number of clusters, not rows, drives the precision for a cluster-level predictor.

## Code: how much does clustering matter?

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("my_data.csv")
outcome, predictor, cluster = "ldl_mmol", "carrier", "family"   # in this simplified example the variant is carried by whole families

empty = smf.mixedlm(f"{outcome} ~ 1", data=df, groups=df[cluster]).fit()
between, within = empty.cov_re.iloc[0, 0], empty.scale
icc = between / (between + within)                                  # share of variance that lies between clusters
cluster_size = df.groupby(cluster).size().mean()
design_effect = 1 + (cluster_size - 1) * icc

print(f"{df[cluster].nunique()} clusters, {cluster_size:.0f} rows each; ICC = {icc:.2f}; design effect = {design_effect:.1f}")
print(f"{len(df)} rows carry about as much information as {len(df) / design_effect:.0f} independent ones (for a cluster-level predictor)")
```

## Code: a predictor that varies between clusters

```python
naive = smf.ols(f"{outcome} ~ {predictor}", data=df).fit()          # ignores clusters: too confident
robust = smf.ols(f"{outcome} ~ {predictor}", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df[cluster]}, use_t=True,
)                                                                   # same estimate, honest interval
mixed = smf.mixedlm(f"{outcome} ~ {predictor}", data=df, groups=df[cluster]).fit()   # multilevel
cluster_means = df.groupby([cluster, predictor], as_index=False)[outcome].mean()
means_model = smf.ols(f"{outcome} ~ {predictor}", data=cluster_means).fit()           # one row per cluster

rows = {}
for label, model in [("ignoring clusters", naive), ("cluster-robust SE", robust),
                     ("multilevel model", mixed), ("analysis of cluster means", means_model)]:
    low, high = model.conf_int().loc[predictor]
    rows[label] = {"estimate": model.params[predictor], "ci_low": low, "ci_high": high}
print(pd.DataFrame(rows).T.round(2))
```

## Code: a predictor that varies within clusters

When the predictor varies from relative to relative inside each family (here `age`), you can give each family its own intercept:

```python
within = smf.ols(f"{outcome} ~ age + C({cluster})", data=df).fit()      # no pooling
within_robust = smf.ols(f"{outcome} ~ age", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df[cluster]}, use_t=True,
)                                                                        # complete pooling
for label, model in [("family fixed effects", within), ("cluster-robust SE", within_robust)]:
    low, high = model.conf_int().loc["age"]
    print(f"{label:21s} {model.params['age']:.3f} (95% CI {low:.3f} to {high:.3f})")
```

Family fixed effects compare relatives *within* the same family, which removes everything about families (shared genes, diet, household) from the comparison. They can't estimate the effect of something that is constant within a family, like the carrier status above: the family dummies absorb it entirely.

## Reading the output

Example output on made-up data (15 families of 20 relatives, the variant carried by whole families, true effect 0.3 mmol/L):

```text
15 clusters, 20 rows each; ICC = 0.52; design effect = 10.8
300 rows carry about as much information as 28 independent ones (for a cluster-level predictor)
                           estimate  ci_low  ci_high
ignoring clusters              0.47    0.30     0.64
cluster-robust SE              0.47   -0.12     1.06
multilevel model               0.47   -0.09     1.03
analysis of cluster means      0.47   -0.15     1.09
family fixed effects  0.020 (95% CI 0.015 to 0.025)
cluster-robust SE     0.023 (95% CI 0.015 to 0.031)
```

- **The estimates agree; the intervals don't.** "Ignoring clusters" treats 300 patients as independent and reports an interval that excludes zero. The three honest analyses give intervals more than three times as wide, which include zero. With only 15 families, the data can't pin the carrier effect down, and the naive analysis hid that.
- **The ICC and design effect** tell you how bad it would have been. A design effect of about 11 means the 300 rows carry about the information of 28 independent ones.
- **With equal-sized clusters, cluster means and the multilevel model give the same estimate;** they differ when cluster sizes are uneven, because the multilevel model weights clusters by how well each is measured.
- **For the within-family predictor,** the family fixed-effects interval (0.015 to 0.025) is narrower than the pooled one (0.015 to 0.031), because comparing relatives inside the same family removes family-to-family variation from the comparison.

## Which approach when

| Your situation | Use |
|---|---|
| Clusters are a nuisance; many of them (a few dozen or more) | Complete pooling with cluster-robust standard errors |
| Predictor assigned to whole clusters; few clusters | Analysis of cluster means, or a multilevel model. Cluster-robust SEs are too optimistic with few clusters, even with `use_t=True` |
| Few clusters that are the point of interest (these 4 clinics), predictor varies within them | Family/clinic fixed effects (no pooling) |
| Many unevenly sized clusters, or you want to generalize to new clusters | Multilevel model (partial pooling) |
| Repeated measures over time on the same unit | Same ideas; also check time dependence, see [Time series data](../time-series-data.md) |

## If it goes wrong

- **The multilevel model warns about convergence or a singular fit:** the variance between clusters is probably near zero (ICC close to 0), so the extra complexity is not needed; fall back to the cluster-robust regression.
- **Very few clusters (fewer than about 10):** no method rescues a cluster-level comparison. Say how few clusters there were and treat the interval as approximate.
- **You want a Bayesian multilevel model:** see [Bayesian methods](../bayesian-methods.md); it is heavier machinery and not needed for the cases above.
- **A binary or count outcome:** the same structure applies with `smf.logit` / `smf.glm` and cluster-robust standard errors; a multilevel GLM needs a dedicated tool (`statsmodels` `BinomialBayesMixedGLM`, or R's `lme4`/`glmmTMB`).
