# How to: check for multicollinearity

**Use this when:** your model has more than one predictor and you plan to interpret individual coefficients. The idea behind it is on the [Multicollinearity](../multicollinearity.md) page.

## Steps

1. Look at the pairwise correlations between your predictors. Anything above roughly 0.8 in absolute value is worth a second look.
2. Compute the **VIF** (variance inflation factor) for every predictor. Correlations only catch overlap between pairs; VIF also catches a predictor that is explained by a combination of several others.
3. Decide what to do (below). Re-run the check after any change.

## Code

```python
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv("my_data.csv")
predictors = ["variant_a", "variant_b", "age"]  # the numeric predictors in your model (variant columns = allele counts 0/1/2)

print(df[predictors].corr().round(2))

X = sm.add_constant(df[predictors].dropna())  # VIF needs an intercept column
vif = pd.Series(
    [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
    index=X.columns,
).drop("const")
print(vif.round(1))
```

Categorical predictors need to be dummy-coded first (`pd.get_dummies(df[col], drop_first=True)`) before they can go into the VIF calculation.

## Reading the output

Example output on made-up data for Mia's cohort, where variants A and B sit close together on the chromosome and are almost always inherited together (linkage disequilibrium):

```text
variant_a    29.8
variant_b    29.9
age           1.0
```

- **About 1**: no overlap with the other predictors.
- **Above 5**: look closer.
- **Above 10**: a clear warning sign. The two high values here belong to the overlapping pair, and `age` is unaffected.

These cutoffs are rough guides, not rules (O'Brien 2007). Judge by what you want to do with the model: VIF only matters for interpreting individual coefficients, not for prediction.

## If a VIF is high

- **Two predictors measure the same thing**: drop one. Here, keep either `variant_a` or `variant_b`, and say which one you chose and why.
- **They belong together**: combine them into a single score, if that makes sense scientifically.
- **You only need predictions**: you can leave them in and use [regularization](./validate-a-predictive-model.md) instead.
- **The high VIF comes from `x` and `x²`, or from an interaction term**: those are correlated by construction. Centering `x` (subtracting its mean) before squaring removes most of the overlap.

> Dropping a variable changes what the remaining coefficient means. If you were adjusting for a confounder, don't drop it just to lower a VIF; see [Causal diagrams](../../05-prediction-vs-causation/causal-diagrams.md).
