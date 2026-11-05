# Cómo: analizar datos agrupados

**Úsalo cuando:** tus observaciones vienen en grupos (familiares dentro de una familia, pacientes dentro de una clínica, medidas repetidas en el mismo paciente), de modo que las filas de un mismo grupo se parecen entre sí. Las ideas están en la página [Datos agrupados y jerárquicos](../clustered-and-hierarchical-data.md).

Para ver cuánto puede engañarte un análisis simple y qué hace el agrupamiento parcial con los grupos pequeños, usa el [cuaderno sobre datos agrupados](../../notebooks/clustered-data-overconfidence.ipynb) (descárgalo y ábrelo en Jupyter, VS Code o Colab).

## Pasos

1. **Identifica la columna de grupo y el nivel de cada predictor.** ¿El predictor de interés varía *entre* grupos (una variante que portan familias enteras) o *dentro* de ellos (una medida en cada familiar, como la edad)? Esto determina qué opciones tienes.
2. **Mide cuánto importa la agrupación:** la correlación intraclase (ICC) y el efecto de diseño (*design effect*). Una ICC cercana a 0 significa que la agrupación apenas importa; una ICC alta significa que 300 filas pueden contener la información de muchas menos observaciones independientes.
3. **Ajusta el modelo por defecto:** la regresión simple con **errores estándar robustos a los grupos** (agrupamiento completo). Deja la estimación como está y corrige el intervalo.
4. **Compáralo con una alternativa** que se adapte a tu situación (tabla más abajo): medias por grupo, efectos fijos de familia (sin agrupamiento) o un modelo multinivel (agrupamiento parcial).
5. **Presenta la estimación con su intervalo e indica cuántos grupos había.** El número de grupos, no de filas, es lo que determina la precisión para un predictor a nivel de grupo.

## Código: ¿cuánto importa la agrupación?

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

## Código: un predictor que varía entre grupos

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

## Código: un predictor que varía dentro de los grupos

Cuando el predictor varía de un familiar a otro dentro de cada familia (aquí `age`), puedes dar a cada familia su propia ordenada en el origen:

```python
within = smf.ols(f"{outcome} ~ age + C({cluster})", data=df).fit()      # no pooling
within_robust = smf.ols(f"{outcome} ~ age", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df[cluster]}, use_t=True,
)                                                                        # complete pooling
for label, model in [("family fixed effects", within), ("cluster-robust SE", within_robust)]:
    low, high = model.conf_int().loc["age"]
    print(f"{label:21s} {model.params['age']:.3f} (95% CI {low:.3f} to {high:.3f})")
```

Los efectos fijos de familia comparan familiares *dentro* de la misma familia, lo que elimina de la comparación todo lo que es propio de las familias (genes compartidos, dieta, hogar). No pueden estimar el efecto de algo que es constante dentro de una familia, como el estado de portador de arriba: las variables ficticias (*dummies*) de familia lo absorben por completo.

## Cómo leer el resultado

Resultado de ejemplo con datos inventados (15 familias de 20 familiares, la variante portada por familias enteras, efecto verdadero 0.3 mmol/L):

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

- **Las estimaciones coinciden; los intervalos no.** «Ignoring clusters» trata a los 300 pacientes como independientes y da un intervalo que excluye el cero. Los tres análisis honestos dan intervalos más de tres veces más anchos, que incluyen el cero. Con solo 15 familias, los datos no permiten precisar el efecto del estado de portador, y el análisis ingenuo lo ocultaba.
- **La ICC y el efecto de diseño** te dicen cuán grave habría sido. Un efecto de diseño de aproximadamente 11 significa que las 300 filas contienen aproximadamente la información de 28 observaciones independientes.
- **Con grupos del mismo tamaño, las medias por grupo y el modelo multinivel dan la misma estimación;** difieren cuando los tamaños de grupo son desiguales, porque el modelo multinivel pondera los grupos según lo bien medido que está cada uno.
- **Para el predictor intrafamiliar,** el intervalo de los efectos fijos de familia (0.015 a 0.025) es más estrecho que el del modelo agrupado (0.015 a 0.031), porque comparar familiares dentro de la misma familia elimina de la comparación la variación entre familias.

## Qué enfoque usar en cada caso

| Tu situación | Usa |
|---|---|
| Los grupos son una molestia; hay muchos (unas pocas decenas o más) | Agrupamiento completo con errores estándar robustos a los grupos |
| Predictor asignado a grupos enteros; pocos grupos | Análisis de medias por grupo o un modelo multinivel. Los errores estándar robustos a los grupos son demasiado optimistas con pocos grupos, incluso con `use_t=True` |
| Pocos grupos que son el centro de interés (estas 4 clínicas), predictor que varía dentro de ellos | Efectos fijos de familia/clínica (sin agrupamiento) |
| Muchos grupos de tamaño desigual, o quieres generalizar a grupos nuevos | Modelo multinivel (agrupamiento parcial) |
| Medidas repetidas en el tiempo sobre la misma unidad | Las mismas ideas; comprueba también la dependencia temporal, véase [Series temporales](../time-series-data.md) |

## Si algo sale mal

- **El modelo multinivel avisa de un problema de convergencia o de un ajuste singular:** probablemente la varianza entre grupos es casi nula (ICC cercana a 0), así que no hace falta la complejidad adicional; vuelve a la regresión robusta a los grupos.
- **Muy pocos grupos (menos de unos 10):** ningún método salva una comparación a nivel de grupo. Indica cuán pocos grupos había y trata el intervalo como aproximado.
- **Quieres un modelo multinivel bayesiano:** véase [Métodos bayesianos](../bayesian-methods.md); es una maquinaria más pesada y no hace falta para los casos anteriores.
- **Un desenlace binario o de recuentos:** se aplica la misma estructura con `smf.logit` / `smf.glm` y errores estándar robustos a los grupos; un GLM multinivel necesita una herramienta específica (`BinomialBayesMixedGLM` de `statsmodels`, o `lme4`/`glmmTMB` de R).
