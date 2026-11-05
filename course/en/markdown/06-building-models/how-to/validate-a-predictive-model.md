# How to: validate a predictive model

**Use this when:** your goal is to predict an outcome for new cases and you want an honest estimate of how well the model will do. The reasoning is on the [Cross-validation and model checking](../cross-validation-and-model-checking.md) and [Overfitting and regularization](../overfitting-and-regularization.md) pages.

## Steps

1. **Set aside a test set first** (e.g. 25% of the rows) and don't touch it until the very end.
2. **Put every step that learns from the data inside a pipeline**: scaling, regularization and anything else fitted to the data. Otherwise information from the test rows leaks into the model and the score looks better than it should.
3. **Cross-validate on the training set.** This gives you an estimate of performance, and its spread, without spending the test set.
4. **Score once on the test set.** Compare it with the cross-validated score and with the training score.

## Code

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("my_data.csv")
outcome = "ldl_mmol"
predictors = ["variant_a", "variant_b", "age"]

data = df[[outcome] + predictors].dropna()  # listwise deletion; report how many rows this drops
X, y = data[predictors], data[outcome]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Scaling puts predictors on comparable footing; ElasticNetCV picks the amount of shrinkage by CV.
model = make_pipeline(StandardScaler(), ElasticNetCV(cv=5))
cv_rmse = -cross_val_score(model, X_train, y_train, cv=5, scoring="neg_root_mean_squared_error")
model.fit(X_train, y_train)

rmse = lambda a, b: np.sqrt(mean_squared_error(a, b))
print(f"cross-validated RMSE (training data): {cv_rmse.mean():.2f} +/- {cv_rmse.std():.2f}")
print(f"training RMSE:  {rmse(y_train, model.predict(X_train)):.2f}")
print(f"test RMSE:      {rmse(y_test, model.predict(X_test)):.2f}   (SD of outcome: {y_test.std():.2f})")
print(f"test R^2:       {r2_score(y_test, model.predict(X_test)):.2f}")
```

**Yes/no outcome?** Swap in a logistic model and score with AUC:

```python
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_auc_score

model = make_pipeline(StandardScaler(), LogisticRegressionCV(cv=5, scoring="roc_auc", max_iter=5000))
model.fit(X_train, y_train)
print("test AUC:", roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))
```

## Reading the output

Example output on made-up data:

```text
cross-validated RMSE (training data): 0.62 +/- 0.02
training RMSE:  0.61
test RMSE:      0.65   (SD of outcome: 0.71)
test R^2:       0.15
```

- **Test RMSE versus the SD of the outcome.** Predicting every case with the average gives an RMSE equal to the outcome's SD. A model has to beat that to be useful, and here it does, modestly (R² = 0.15).
- **Training versus cross-validated/test score.** A training error much lower than the others is the signature of overfitting. Here the three are close, so the model isn't memorizing noise.
- **The ± on the cross-validated score** shows how much the answer moves between folds. With a small dataset, that spread (and the test-set score) is noisy, so don't over-read small differences between models.

## If it goes wrong

- **Big gap between training and test performance**: the model is too flexible for the data. Use fewer predictors, or a stronger penalty.
- **Few rows**: a 25% test set is itself noisy. Report the cross-validated score on all the data instead (`cross_val_score(model, X, y, cv=5, ...)`).
- **Grouped or repeated measurements, or data ordered in time**: a random split puts near-duplicates in both train and test, which flatters the score. Split by group (`GroupKFold`) or by time (`TimeSeriesSplit`); see [Clustered data](../../07-special-data-structures/clustered-and-hierarchical-data.md) and [Time series](../../07-special-data-structures/time-series-data.md).
- **You want to know if X *causes* Y**: a good held-out score doesn't tell you that. See [Prediction vs. explanation](../../05-prediction-vs-causation/prediction-vs-explanation.md).
