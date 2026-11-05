# How to: explore a dataset before analyzing it

**Use this when:** you have a new dataset and want to understand it before testing or modeling anything. The reasoning is on the [EDA basics](../eda-basics.md) page; for the line between harmless looking and picking your hypothesis from the data, see [Exploratory vs. confirmatory](../exploratory-vs-confirmatory.md).

For a guided tour with plots on a made-up dataset that has some planted problems, work through the [EDA walkthrough notebook](../../notebooks/eda-walkthrough.ipynb) (download it and open it in Jupyter, VS Code or Colab). You can point it at your own CSV by changing one line.

## Steps

1. **Check the basics and data quality:** size, column types, ranges, duplicates, missing values. This is hygiene, not hypothesis-peeking, and you should do it for any analysis.
2. **Look at one variable at a time.** Histograms for numbers, counts for categories. Look for impossible values, odd spikes (e.g. a default of 0 or 999), and skew.
3. **Look at pairs of variables.** Scatterplots for number vs. number, boxplots with the raw points for number vs. category.
4. **Look for subgroup structure and trends over time.** Does the pattern differ by group? Does the outcome drift with date?
5. **Write down what you noticed as questions**, not conclusions. Anything you found by looking is a hypothesis to check on new data, not a result.

## Code: basics, data quality, missingness

```python
import pandas as pd

df = pd.read_csv("my_data.csv", parse_dates=["sample_date"])  # list your date columns, if any

print(df.shape)
print(df.dtypes)
print(df.describe(include="number").T[["count", "mean", "std", "min", "max"]])  # ranges: anything impossible?
print("duplicate rows:", df.duplicated().sum())
print(df.isna().mean().sort_values(ascending=False).round(2))  # share missing per column

outcome = "ldl_mmol"
print(df[df[outcome] < 0])                                        # inspect suspicious rows directly
print(df.groupby(df[outcome].isna()).mean(numeric_only=True))     # do rows with a missing outcome look different?
```

The last line is the most important check for missing data: if the rows with a missing outcome differ systematically from the others (here, perhaps older patients), dropping them is not harmless. See [Missing data](../missing-data.md).

## Code: the plots

```python
import matplotlib.pyplot as plt
import seaborn as sns

numeric = df.select_dtypes("number").columns.tolist()
categories = df.select_dtypes(exclude=["number", "datetime"]).columns.tolist()

# 1. One variable at a time
df[numeric].hist(bins=30, figsize=(10, 6))
plt.show()

# 2. Pairs of numeric variables (scatter matrix); colour by a category to spot subgroups
sns.pairplot(df, vars=numeric, hue=categories[0] if categories else None, corner=True)
plt.show()

# 3. The outcome by each category, with the raw points on top of the boxes
for cat in categories:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x=cat, y=outcome, ax=ax)
    sns.stripplot(data=df, x=cat, y=outcome, color="black", alpha=0.3, ax=ax)
    plt.show()

# 4. Trend over time
df.sort_values("sample_date").plot(x="sample_date", y=outcome, style=".", figsize=(8, 3))
plt.show()
```

## What to look for

- **Histograms:** impossible or implausible values (negative LDL values, a 10x outlier that looks like a decimal slip), pile-ups at a round number, two humps (a hidden subgroup), a long right tail (often a sign that a log scale would be more natural).
- **Scatterplots:** curves instead of straight lines, a few points driving the whole pattern, a fan shape (variability that grows with the level), clusters.
- **Boxplots with points:** groups of very different sizes, one group with much more spread, overlapping vs. clearly separated groups, outliers that belong to one clinic or one date.
- **Over time:** a drift or step change (new instrument, new operator, a different season).
- **Missingness:** which columns, how many, and whether it depends on other variables.

## If you find something

- **A clear data error (a typo, an impossible value):** fix it at the source if you can, otherwise exclude it and say so explicitly in your methods, with the number of rows affected.
- **An unexplained outlier:** don't delete it just because it is inconvenient. Report the analysis with and without it if it matters.
- **Subgroups or curves:** note them as things to model. If you found them by looking, say so; they are leads, not confirmed findings.
- **Substantial missing data:** report how much and where, and see [Missing data](../missing-data.md) before choosing a fix.
- **Before testing anything,** decide your comparison, and ideally write it down, *without* choosing it from the plots. If the plots suggest a new comparison, label it exploratory.
