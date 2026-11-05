# Cómo: ejecutar una prueba clásica como regresión

**Úsalo cuando:** quieras una estimación con intervalo de confianza a partir de una prueba con nombre *y* la libertad de añadir una covariable, relajar un supuesto o gestionar datos agrupados sin cambiar de herramienta. La idea está en la página [Pruebas como regresiones](../tests-as-regressions.md); las recetas clásicas están en [Cómo: ejecutar una prueba habitual](../../03-hypothesis-testing/how-to/run-a-common-test.md).

## Pasos

1. **Escribe la comparación como una fórmula**: `outcome ~ predictor`. Un sí/no o una categoría en el lado derecho se convierte automáticamente en variables ficticias (*dummy*).
2. **Ajústala** con `statsmodels` y lee el coeficiente de interés junto con su intervalo de confianza.
3. **Comprueba que coincide con la prueba clásica** (una sola vez, para ganar confianza). Los números de abajo coinciden.
4. **Amplíala:** añade covariables, pide errores estándar robustos o agrupa por clústeres; la ampliación es un argumento más, no un procedimiento nuevo.

## Dos grupos: la prueba t como regresión

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv("my_data.csv").dropna(subset=["ldl_mmol"])
df["carrier"] = (df["carrier_status"] == "carrier").astype(int)   # 0/1 group indicator (carrier = 1)

ols = smf.ols("ldl_mmol ~ carrier", data=df).fit()
print(ols.summary().tables[1])        # the 'carrier' row IS the difference in means, with its 95% CI

# Same thing as Student's t-test (equal variances assumed):
a = df.loc[df["carrier"] == 1, "ldl_mmol"]
b = df.loc[df["carrier"] == 0, "ldl_mmol"]
print("Student p:", round(stats.ttest_ind(a, b).pvalue, 4), "| regression p:", round(ols.pvalues["carrier"], 4))

# Close to Welch's t-test (unequal variances allowed): robust standard errors
robust = smf.ols("ldl_mmol ~ carrier", data=df).fit(cov_type="HC3")
print("Welch p:  ", round(stats.ttest_ind(a, b, equal_var=False).pvalue, 4), "| robust regression p:", round(robust.pvalues["carrier"], 4))
print(robust.conf_int().loc["carrier"].round(2).tolist(), "<- 95% CI for the difference")
```

## Tres o más grupos: el ANOVA como regresión

```python
anova_model = smf.ols("ldl_mmol ~ C(genotype)", data=df).fit()
print(sm.stats.anova_lm(anova_model, typ=2))                  # the F-test of classical one-way ANOVA
print("scipy F:", stats.f_oneway(*[g for _, g in df.groupby("genotype")["ldl_mmol"]]).statistic.round(3))
print(anova_model.params.round(2))                            # differences from the reference genotype
```

## Añadir una covariable (lo que una prueba simple no puede hacer)

```python
adjusted = smf.ols("ldl_mmol ~ carrier + age", data=df).fit(cov_type="HC3")
print(adjusted.params.round(3))
print(adjusted.conf_int().round(3))
```

El coeficiente de `carrier` es ahora la diferencia entre grupos *a la misma edad*. Ajustar por una covariable medida antes de que se asignara la exposición o el tratamiento suele estrechar el intervalo (esto es lo que se llama «ANCOVA»). Para decidir *qué* covariables incluir cuando la exposición no fue aleatorizada, consulta [Cómo: dibujar un diagrama causal](../../05-prediction-vs-causation/how-to/draw-and-use-a-causal-diagram.md).

## Dos categorías: chi-cuadrado como regresión logística

```python
df["sick"] = (df["disease"] == "yes").astype(int)
logit = smf.logit("sick ~ C(treatment)", data=df).fit(disp=False)

print("odds ratios:\n", np.exp(logit.params).round(2))
print("95% CI for the odds ratios:\n", np.exp(logit.conf_int()).round(2))
print("likelihood-ratio p:", round(logit.llr_pvalue, 4))
chi2_p = stats.chi2_contingency(pd.crosstab(df["treatment"], df["disease"]), correction=False)[1]
print("chi-squared p:", round(chi2_p, 4))
```

## Dos números: la correlación como pendiente

```python
slope = smf.ols("ldl_mmol ~ age", data=df).fit()
print(slope.summary().tables[1])
print("slope p:", round(slope.pvalues["age"], 4), "| Pearson p:", round(stats.pearsonr(df["age"], df["ldl_mmol"]).pvalue, 4))
```

El valor p de la pendiente es el mismo que el de la prueba de correlación. La pendiente tiene además la ventaja de venir en unidades útiles (mmol/L por año de edad).

## Cómo leer los resultados

| Prueba clásica | Fórmula de regresión | Cantidad que hay que leer |
|---|---|---|
| Prueba t de dos muestras | `y ~ group` | el coeficiente del grupo: la diferencia de medias |
| Prueba t pareada | `diff ~ 1` | la ordenada en el origen: el cambio medio |
| ANOVA de una vía | `y ~ C(group)` | la prueba F de `anova_lm`; los coeficientes son diferencias respecto al grupo de referencia |
| Chi-cuadrado (2 categorías) | `smf.logit("outcome01 ~ C(group)")` | los odds ratios y el valor p de la razón de verosimilitudes |
| Correlación | `y ~ x` | la pendiente (estandariza ambas variables para obtener r) |

Los valores p coinciden hasta los dígitos impresos en el caso de Student, el ANOVA y la correlación. Los valores p de chi-cuadrado y de la regresión logística son asintóticamente equivalentes, así que son próximos pero no idénticos, y la versión robusta (HC3) se parece a la de Welch pero no es el mismo cálculo.

## Si algo sale mal

- **¿Qué coeficiente es la «diferencia»?** La codificación con variables ficticias compara cada grupo con una referencia; con un indicador 0/1 controlas la dirección. Para una columna de texto, `C(group, Treatment(reference="non-carrier"))` elige la referencia.
- **Los residuos tienen mala pinta:** los gráficos de [Cómo: comprobar los supuestos de una prueba](../../03-hypothesis-testing/how-to/check-test-assumptions.md) se aplican a los residuos de la regresión. Los errores estándar robustos corrigen las varianzas desiguales, no una forma funcional equivocada.
- **Las observaciones no son independientes** (varios familiares por familia, visitas repetidas): añade `cov_type="cluster", cov_kwds={"groups": df["family"]}`, o consulta [Cómo: analizar datos agrupados](../../07-special-data-structures/how-to/analyze-clustered-data.md).
- **Un coeficiente solo es una afirmación causal si el diseño la respalda.** Una regresión no convierte una asociación observacional en un efecto.
