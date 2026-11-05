"""
Template: build a (G)LM to quantify relationships and/or predict an outcome.

Use this once references/analysis-triage.md has settled (a) the analysis is
confirmatory-enough to model, (b) whether the goal is PREDICTION or CAUSAL
INTERPRETATION, and (c) for a causal goal, whether the exposure was assigned
by a well-designed EXPERIMENT or is OBSERVATIONAL (Question 2a) -- the three
resulting modes diverge in what "a good model" means (SHMUELI_EXPLAIN_PREDICT):

- Predictive mode: judge the model by out-of-sample performance (CV / held-
  out test set). Flexible/regularized models and every available predictor
  are fair game; no coefficient needs to be believed causal.
- Causal, experimental mode: the experiment's design (random/as-good-as-random
  assignment) is what identifies the effect, not adjustment. Only add
  PRE-TREATMENT covariates, and only for precision (ANCOVA-style) -- never
  adjust for anything measured after assignment (IMBENS_RUBIN).
- Causal, observational mode: judge the model by whether it isolates the
  exposure's effect. Only adjust for the variables identified via the
  causal-DAG step (see causal_dag_builder.py) -- adding more "just in case"
  can introduce collider/mediator bias instead of removing confounding.
  Report the exposure coefficient with a CI, not a bare p-value, and be
  explicit that the estimate is only causal under the DAG's assumptions (no
  unmeasured confounding in the adjustment set, correct functional form, etc.)
  (HERNAN_ROBINS; PEARL_CAUSALITY).

Missing data: every fit_*/estimate_* function below does listwise deletion via
`prepare_model_data()` and reports how many rows were dropped. That's a
reasonable default under MCAR; if a large fraction of rows are dropped, or
missingness plausibly depends on the outcome or an unobserved variable
(MAR/MNAR), don't just keep dropping rows -- see LITTLE_RUBIN_MISSING for
multiple imputation / model-based alternatives.

Requires: pandas, numpy, statsmodels, scikit-learn.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import KFold, train_test_split
from sklearn.linear_model import ElasticNetCV, LogisticRegressionCV
from sklearn.metrics import mean_squared_error, r2_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# --------------------------------------------------------------------------
# KEY PARAMETERS -- fill these in for the dataset/question at hand.
# --------------------------------------------------------------------------
MODE = "predictive"             # "predictive" or "causal"
IDENTIFICATION = "observational"  # "experiment" or "observational" -- causal mode only (Question 2a)
DATA_PATH = None                # e.g. "mydata.csv"; synthetic demo data used if None
OUTCOME = "y"
OUTCOME_TYPE = "continuous"     # "continuous" or "binary" -- selects GLM family / sklearn model
EXPOSURE = "x"                  # variable of primary causal interest (causal mode only)
ADJUSTMENT_SET: list[str] = []      # from the causal DAG step (observational causal mode) -- NOT "all available covariates"
PRECISION_COVARIATES: list[str] = []  # pre-treatment covariates only (experimental causal mode) -- never post-treatment
PREDICTORS: list[str] = []      # full predictor list (predictive mode) -- can be large
TEST_SIZE = 0.25
N_SPLITS = 5
SEED = 0


def load_data(path=DATA_PATH) -> pd.DataFrame:
    if path is not None:
        return pd.read_csv(path)
    rng = np.random.default_rng(SEED)
    n = 400
    confounder = rng.normal(0, 1, n)
    x = 0.8 * confounder + rng.normal(0, 1, n)
    y = 1.2 * x + 0.9 * confounder + rng.normal(0, 1, n)
    return pd.DataFrame({"x": x, "confounder": confounder, "y": y})


def prepare_model_data(df: pd.DataFrame, columns) -> pd.DataFrame:
    """Default missing-data handling: listwise deletion, reported explicitly.

    Assumes missingness is unrelated to the variables involved (MCAR). If a
    large fraction of rows are dropped, or missingness plausibly depends on
    the outcome or an unobserved variable (MAR/MNAR), don't just keep
    dropping rows -- see LITTLE_RUBIN_MISSING for multiple imputation or
    model-based alternatives instead of improvising a fix here.
    """
    columns = list(columns)
    complete = df[columns].dropna()
    n_dropped = len(df) - len(complete)
    if n_dropped:
        print(
            f"prepare_model_data: dropping {n_dropped}/{len(df)} rows "
            f"({n_dropped / len(df):.1%}) with missing values in {columns}."
        )
    return df.loc[complete.index]


def fit_explanatory_model(df: pd.DataFrame, outcome: str, predictors, family="gaussian", robust=True):
    """Fit a (G)LM to quantify relationships; report coefficients with CIs, not just p-values.

    `family`: "gaussian" (OLS) or "binomial" (logistic). Extend with Poisson /
    negative binomial the same way for count outcomes.
    """
    df = prepare_model_data(df, [outcome] + list(predictors))
    formula = f"{outcome} ~ {' + '.join(predictors)}"
    if family == "gaussian":
        model = smf.ols(formula, data=df).fit(cov_type="HC3" if robust else "nonrobust")
    elif family == "binomial":
        model = smf.glm(formula, data=df, family=sm.families.Binomial()).fit()
    else:
        raise ValueError(f"Unsupported family: {family}")

    ci = model.conf_int()
    coefs = pd.DataFrame(
        {"estimate": model.params, "ci_low": ci[0], "ci_high": ci[1], "p_value": model.pvalues}
    )
    return model, coefs


def estimate_experimental_effect(df: pd.DataFrame, outcome: str, exposure: str,
                                  precision_covariates=None, family="gaussian"):
    """Effect estimate when the exposure was assigned by a well-designed experiment.

    Identification comes from the experiment's design (random/as-good-as-random
    assignment), not from adjustment (IMBENS_RUBIN). `precision_covariates`
    should be PRE-TREATMENT variables only, included solely to tighten the CI
    (the ANCOVA move) -- never include anything measured after assignment,
    since that can reintroduce bias even inside a randomized experiment.
    """
    model, coefs = fit_explanatory_model(
        df, outcome, [exposure] + list(precision_covariates or []), family=family
    )
    return model, coefs.loc[[exposure]]


def estimate_observational_effect(df: pd.DataFrame, outcome: str, exposure: str, adjustment_set, family="gaussian"):
    """Adjustment-set estimate of the exposure -> outcome effect (observational exposure).

    Valid as a causal estimate only if `adjustment_set` satisfies the
    backdoor criterion for this DAG (PEARL_CAUSALITY) -- i.e. it blocks all
    backdoor paths and contains no mediator/collider. This function does not
    verify that for you; it assumes the Question 2a / DAG step already
    identified the set. This is the weakest common causal identification
    strategy -- if a quasi-experimental design (instrument, discontinuity,
    DID) is available instead, that is likely more credible than adjustment
    alone (out of scope for this template).
    """
    if not adjustment_set:
        print(
            "Warning: empty adjustment set -- the exposure coefficient below is "
            "unadjusted and almost certainly confounded for observational data "
            "(for an experiment, use estimate_experimental_effect instead)."
        )
    model, coefs = fit_explanatory_model(df, outcome, [exposure] + list(adjustment_set), family=family)
    return model, coefs.loc[[exposure]]


def fit_predictive_model(
    df: pd.DataFrame, outcome: str, predictors, outcome_type="continuous",
    test_size=TEST_SIZE, n_splits=N_SPLITS, seed=SEED,
):
    """Regularized model with proper out-of-sample evaluation (train/test + CV).

    Judge this model purely on held-out performance -- coefficients here are
    not meant to be interpreted causally, even if some look large. Predictors
    are standardized inside the pipeline: ElasticNet/logistic penalties act on
    raw coefficient magnitude, so unscaled features would be penalized
    unevenly purely because of their units, independent of their real
    importance.
    """
    df = prepare_model_data(df, [outcome] + list(predictors))
    X = df[predictors].to_numpy()
    y = df[outcome].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
    cv = KFold(n_splits=n_splits, shuffle=True, random_state=seed)

    if outcome_type == "continuous":
        model = make_pipeline(StandardScaler(), ElasticNetCV(cv=cv, random_state=seed))
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = {
            "test_r2": r2_score(y_test, y_pred),
            "test_rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        }
    elif outcome_type == "binary":
        model = make_pipeline(StandardScaler(), LogisticRegressionCV(cv=cv, random_state=seed, max_iter=5000))
        model.fit(X_train, y_train)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        metrics = {"test_auc": roc_auc_score(y_test, y_pred_proba)}
    else:
        raise ValueError(f"Unsupported outcome_type: {outcome_type}")

    return model, metrics


if __name__ == "__main__":
    data = load_data()

    if MODE == "causal":
        if IDENTIFICATION == "experiment":
            model, effect = estimate_experimental_effect(
                data, outcome=OUTCOME, exposure=EXPOSURE,
                precision_covariates=PRECISION_COVARIATES, family="gaussian",
            )
            print("Experimental exposure effect:\n", effect)
        elif IDENTIFICATION == "observational":
            model, effect = estimate_observational_effect(
                data, outcome=OUTCOME, exposure=EXPOSURE,
                adjustment_set=ADJUSTMENT_SET or ["confounder"], family="gaussian",
            )
            print("Observational (adjustment-based) exposure effect:\n", effect)
        else:
            raise ValueError(f"Unsupported IDENTIFICATION: {IDENTIFICATION!r}")
    else:
        model, metrics = fit_predictive_model(
            data, outcome=OUTCOME, predictors=PREDICTORS or ["x", "confounder"],
            outcome_type=OUTCOME_TYPE if OUTCOME_TYPE in ("continuous", "binary") else "continuous",
        )
        print("Predictive performance (held-out):", metrics)

