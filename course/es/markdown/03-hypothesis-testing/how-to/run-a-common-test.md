# Cómo: ejecutar una prueba habitual y presentarla correctamente

**Úsalo cuando:** tengas una comparación concreta decidida *antes* de mirar los datos (véase [Exploratorio vs. confirmatorio](../../02-exploring-data/exploratory-vs-confirmatory.md)) y quieras ejecutar la prueba clásica correspondiente. La tabla de pruebas está en la página [Pruebas habituales](../common-tests.md); las advertencias sobre el valor p están en [Valores p y significación](../p-values-and-significance.md).

## Pasos

1. **Elige la receta de abajo** según el tipo de variable de respuesta y el diseño: dos grupos independientes, las mismas unidades medidas dos veces, tres o más grupos, dos categorías o dos números.
2. **Comprueba los supuestos** con los gráficos de [Cómo: comprobar los supuestos de una prueba](./check-test-assumptions.md) antes de fiarte del resultado.
3. **Presenta primero la estimación y su intervalo de confianza**, y en segundo lugar el valor p. "Los portadores tenían un colesterol LDL 0.35 mmol/L más alto (IC del 95%: 0.12 a 0.59)" dice más al lector que "p = 0.001".
4. **Si la pregunta es sobre el efecto de un tratamiento,** recuerda que una prueba solo compara grupos; que la diferencia sea *causal* depende del diseño (véase [Experimentos vs. datos observacionales](../../05-prediction-vs-causation/experiments-vs-observational-data.md)).

Todas las recetas de abajo también pueden escribirse como una regresión, que es más fácil de ampliar con covariables; véase [Cómo: ejecutar una prueba como regresión](../../04-regression-basics/how-to/run-a-test-as-a-regression.md).

## Dos grupos independientes: prueba t de Welch

```python
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import CompareMeans, DescrStatsW

df = pd.read_csv("my_data.csv")
carriers = df.loc[df["carrier_status"] == "carrier", "ldl_mmol"].dropna()
non_carriers = df.loc[df["carrier_status"] == "non-carrier", "ldl_mmol"].dropna()

diff = carriers.mean() - non_carriers.mean()
low, high = CompareMeans(DescrStatsW(carriers), DescrStatsW(non_carriers)).tconfint_diff(usevar="unequal")
welch = stats.ttest_ind(carriers, non_carriers, equal_var=False)

pooled_sd = np.sqrt(((len(carriers) - 1) * carriers.var() + (len(non_carriers) - 1) * non_carriers.var())
                    / (len(carriers) + len(non_carriers) - 2))
print(f"difference in means {diff:.2f} mmol/L (95% CI {low:.2f} to {high:.2f}); "
      f"Cohen's d = {diff / pooled_sd:.2f}; Welch p = {welch.pvalue:.3f}")

# If the data are far from bell-shaped or have outliers: rank-based alternative
print(stats.mannwhitneyu(carriers, non_carriers))
```

La versión de Welch no supone varianzas iguales y apenas cuesta nada cuando lo son, así que úsala por defecto.

## Las mismas unidades medidas dos veces: prueba t pareada

```python
paired = pd.read_csv("my_paired_data.csv")   # one row per patient
change = paired["bp_after"] - paired["bp_before"]

low, high = DescrStatsW(change).tconfint_mean()
print(f"mean change {change.mean():.1f} mmHg (95% CI {low:.1f} to {high:.1f}); "
      f"paired t-test p = {stats.ttest_rel(paired['bp_after'], paired['bp_before']).pvalue:.2g}")

# Rank-based alternative on the differences
print(stats.wilcoxon(change))
```

Analiza las *diferencias*; no ejecutes la prueba para grupos independientes con datos pareados.

## Tres o más grupos: ANOVA de un factor

```python
groups = [values.dropna() for _, values in df.groupby("genotype")["ldl_mmol"]]
print(stats.f_oneway(*groups))                      # overall: do the groups differ at all?

summary = df.groupby("genotype")["ldl_mmol"].agg(["count", "mean", "sem"])
summary["ci_low"] = summary["mean"] - stats.t.ppf(0.975, summary["count"] - 1) * summary["sem"]
summary["ci_high"] = summary["mean"] + stats.t.ppf(0.975, summary["count"] - 1) * summary["sem"]
print(summary.round(2))                              # each group's mean with its own 95% CI

from statsmodels.stats.multicomp import pairwise_tukeyhsd
clean = df.dropna(subset=["ldl_mmol"])
print(pairwise_tukeyhsd(clean["ldl_mmol"], clean["genotype"]))   # pairwise differences with CIs, adjusted for multiplicity

print(stats.kruskal(*groups))                       # rank-based alternative
```

La prueba F global solo dice que "no todos los grupos son iguales". La tabla por pares es la que responde a "cuáles, y en qué medida"; consulta [Comparaciones múltiples](../multiple-comparisons.md) para ver por qué importa el ajuste.

## Dos categorías: prueba de chi-cuadrado

```python
from statsmodels.stats.proportion import confint_proportions_2indep

table = pd.crosstab(df["treatment"], df["disease"])
chi2, p, dof, expected = stats.chi2_contingency(table)

counts = table["yes"]
totals = table.sum(axis=1)
print((counts / totals).round(3))                    # share with the disease in each group
low, high = confint_proportions_2indep(counts.iloc[0], totals.iloc[0], counts.iloc[1], totals.iloc[1],
                                       compare="diff", method="newcomb")
print(f"difference in proportions {counts.iloc[0] / totals.iloc[0] - counts.iloc[1] / totals.iloc[1]:.3f} "
      f"(95% CI {low:.3f} to {high:.3f}); chi-squared p = {p:.3f}")

if (expected < 5).any():                             # small expected counts: use the exact test (2x2 tables)
    print(stats.fisher_exact(table))
```

Presenta las proporciones de cada grupo, no solo el valor p.

## Dos números: correlación

```python
pair = df[["age", "ldl_mmol"]].dropna()
r = stats.pearsonr(pair["age"], pair["ldl_mmol"])
low, high = r.confidence_interval()
print(f"r = {r.statistic:.2f} (95% CI {low:.2f} to {high:.2f}), p = {r.pvalue:.3g}")

print(stats.spearmanr(pair["age"], pair["ldl_mmol"]))   # for curved-but-steadily-rising relationships or outliers
```

Representa siempre primero el diagrama de dispersión: una única r no distingue una recta de una curva ni de un patrón causado por un valor atípico.

## Cómo leer el resultado

Ejemplo de salida con datos inventados, de la primera receta (Welch):

```text
difference in means 0.35 mmol/L (95% CI 0.12 to 0.59); Cohen's d = 0.39; Welch p = 0.004
```

- **La diferencia y su IC** son el resultado. El IC muestra el rango de efectos compatibles con los datos; si abarca diferencias que importarían en la práctica y otras que no, el estudio no puede zanjar la cuestión, diga lo que diga el valor p.
- **La d de Cohen** expresa la diferencia en unidades de la desviación típica de la variable de respuesta, lo cual es útil para comparar entre estudios y para los [cálculos de potencia](../../01-planning-your-study/how-to/plan-a-sample-size.md). Alrededor de 0.2 se considera convencionalmente pequeña, 0.5 mediana y 0.8 grande, pero lo que cuenta es la escala de tu campo, no esas etiquetas.
- **El valor p** responde a una pregunta estrecha: ¿cuán sorprendentes serían unos datos como estos si de verdad no hubiera ninguna diferencia? No leas un valor p grande como "no hay efecto" ni uno pequeño como "importante".

## Si algo sale mal

- **Un supuesto parece dudoso:** ejecuta la alternativa que se muestra en cada receta y comprueba si cambia la conclusión.
- **Has ejecutado varias pruebas y presentas las significativas:** es el problema de las comparaciones múltiples; véase [Comparaciones múltiples](../multiple-comparisons.md).
- **Elegiste la comparación después de mirar los gráficos:** etiquétala como exploratoria. Un valor p obtenido así es una pista, no una confirmación.
- **Tus datos están agrupados o son repetidos** (familiares dentro de familias, varias visitas por paciente): estas pruebas suponen observaciones independientes; véase [Datos agrupados y jerárquicos](../../07-special-data-structures/clustered-and-hierarchical-data.md).
