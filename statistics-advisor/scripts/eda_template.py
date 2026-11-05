"""
Template: exploratory data analysis (EDA) with visualization-first diagnostics.

Use this as the first concrete step whenever the analysis goal is exploratory
(see references/analysis-triage.md, Question 1). The point is to look at the
data from many angles *before* reaching for any hypothesis test, so patterns,
outliers, missingness, and candidate relationships surface on their own terms
(TUKEY_EDA). Prefer turning this into an actual `.ipynb` (one cell per plot,
per the Notebook Workflow in SKILL.md) over running it as a flat script, so
the user can scroll through and annotate what they notice.

Requires: pandas, numpy, matplotlib, seaborn.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------------------------------
# KEY PARAMETERS -- adjust to the dataset at hand.
# --------------------------------------------------------------------------
DATA_PATH = None               # e.g. "mydata.csv"; a synthetic demo dataset is used if None
TARGET = None                  # name of an outcome column of interest, if any (optional)
MAX_CATEGORIES = 15            # columns with <= this many unique values are treated as categorical
DATE_COLUMNS: list[str] = []   # explicit datetime columns, if auto-detection misses them


def load_data(path=DATA_PATH) -> pd.DataFrame:
    if path is not None:
        return pd.read_csv(path)
    # Synthetic demo dataset so the script runs standalone.
    rng = np.random.default_rng(0)
    n = 300
    group = rng.choice(["A", "B", "C"], size=n, p=[0.5, 0.3, 0.2])
    x = rng.normal(0, 1, n)
    group_effect = np.array([{"A": 0.0, "B": 1.5, "C": -1.0}[g] for g in group])
    y = 2 * x + group_effect + rng.normal(0, 1, n)
    date = pd.date_range("2023-01-01", periods=n, freq="D")
    df = pd.DataFrame({"x": x, "y": y, "group": group, "date": date})
    df.loc[rng.choice(n, size=15, replace=False), "x"] = np.nan  # inject missingness on purpose
    return df


def classify_columns(df: pd.DataFrame, max_categories: int = MAX_CATEGORIES, date_columns=DATE_COLUMNS):
    """Split columns into numeric / categorical / datetime buckets for plotting."""
    datetime_cols = list(date_columns) + [
        c for c in df.columns
        if pd.api.types.is_datetime64_any_dtype(df[c]) and c not in date_columns
    ]
    remaining = [c for c in df.columns if c not in datetime_cols]
    categorical_cols = [
        c for c in remaining
        if df[c].dtype == object or df[c].nunique(dropna=True) <= max_categories
    ]
    numeric_cols = [
        c for c in remaining
        if c not in categorical_cols and pd.api.types.is_numeric_dtype(df[c])
    ]
    return {"numeric": numeric_cols, "categorical": categorical_cols, "datetime": datetime_cols}


def plot_missingness(df: pd.DataFrame):
    """Bar chart of missing-value fraction per column -- always check this first."""
    frac_missing = df.isna().mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, max(3, 0.3 * len(frac_missing))))
    frac_missing.plot.barh(ax=ax)
    ax.set_xlabel("Fraction missing")
    ax.set_title("Missingness by column")
    fig.tight_layout()
    return fig


def plot_univariate(df: pd.DataFrame, numeric_cols, categorical_cols):
    """Histogram+KDE for numeric columns, count bar plot for categorical columns."""
    cols = numeric_cols + categorical_cols
    if not cols:
        return None
    fig, axes = plt.subplots(len(cols), 1, figsize=(6, 3 * len(cols)))
    axes = np.atleast_1d(axes)
    for ax, col in zip(axes, cols):
        if col in numeric_cols:
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
        else:
            df[col].value_counts(dropna=False).plot.bar(ax=ax)
        ax.set_title(col)
    fig.tight_layout()
    return fig


def plot_pairwise_numeric(df: pd.DataFrame, numeric_cols, hue=None):
    """Pairplot (scatter matrix) and correlation heatmap for numeric columns.

    Pairwise scatter is more informative than the correlation number alone --
    it catches nonlinearity, outliers, and subgroup structure a single
    Pearson r cannot.
    """
    if len(numeric_cols) < 2:
        return None, None
    pair_fig = sns.pairplot(df, vars=numeric_cols, hue=hue, corner=True)

    fig, ax = plt.subplots(figsize=(1 + len(numeric_cols), 1 + len(numeric_cols)))
    sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
    ax.set_title("Pearson correlation")
    fig.tight_layout()
    return pair_fig, fig


def plot_categorical_vs_numeric(df: pd.DataFrame, categorical_cols, numeric_cols):
    """Box + strip plots of each numeric column split by each categorical column."""
    figs = []
    for cat in categorical_cols:
        for num in numeric_cols:
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.boxplot(data=df, x=cat, y=num, ax=ax)
            sns.stripplot(data=df, x=cat, y=num, color="black", alpha=0.3, ax=ax)
            ax.set_title(f"{num} by {cat}")
            fig.tight_layout()
            figs.append(fig)
    return figs


def plot_time_series(df: pd.DataFrame, datetime_cols, numeric_cols):
    """Line plot of each numeric column over time, for any datetime column present."""
    figs = []
    for date_col in datetime_cols:
        ordered = df.sort_values(date_col)
        for num in numeric_cols:
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.plot(ordered[date_col], ordered[num])
            ax.set_title(f"{num} over {date_col}")
            fig.tight_layout()
            figs.append(fig)
    return figs


def plot_target_relationships(df: pd.DataFrame, target: str, columns):
    """Scatter (numeric predictor) or box plot (categorical predictor) against the target.

    Only run this once a specific outcome/target is named -- in a purely
    open-ended EDA, treat every variable symmetrically instead (the other
    plot_* functions) rather than anchoring everything to one column too early.
    """
    figs = []
    for col in columns:
        if col == target:
            continue
        fig, ax = plt.subplots(figsize=(5, 4))
        if pd.api.types.is_numeric_dtype(df[col]):
            ax.scatter(df[col], df[target], alpha=0.5)
        else:
            sns.boxplot(data=df, x=col, y=target, ax=ax)
        ax.set_title(f"{target} vs {col}")
        fig.tight_layout()
        figs.append(fig)
    return figs


def run_full_eda(df: pd.DataFrame, target=TARGET):
    """Run every angle above in sequence -- the standard "look at it first" pass."""
    kinds = classify_columns(df)
    plot_missingness(df)
    plot_univariate(df, kinds["numeric"], kinds["categorical"])
    plot_pairwise_numeric(df, kinds["numeric"], hue=kinds["categorical"][0] if kinds["categorical"] else None)
    plot_categorical_vs_numeric(df, kinds["categorical"], kinds["numeric"])
    plot_time_series(df, kinds["datetime"], kinds["numeric"])
    if target is not None:
        other_cols = [c for c in df.columns if c != target]
        plot_target_relationships(df, target, other_cols)
    return kinds


if __name__ == "__main__":
    data = load_data()
    run_full_eda(data, target=TARGET)
    plt.show()
