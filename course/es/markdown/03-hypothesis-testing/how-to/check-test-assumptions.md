# Cómo: comprobar los supuestos de una prueba

**Úsalo cuando:** estés a punto de ejecutar (o ya hayas ejecutado) una prueba t, un ANOVA, una regresión o una prueba de chi-cuadrado y quieras saber si su letra pequeña supone un problema. El razonamiento está en la página [Comprobar los supuestos](../checking-assumptions.md).

## Pasos

1. **Primero la independencia, pensando, no dibujando.** ¿Hay mediciones repetidas sobre la misma unidad, familiares de la misma familia, pacientes de la misma clínica o datos ordenados en el tiempo? Si es así, una prueba simple es demasiado optimista; véanse [Datos agrupados y jerárquicos](../../07-special-data-structures/clustered-and-hierarchical-data.md) y [Series temporales](../../07-special-data-structures/time-series-data.md).
2. **Representa los datos por grupo**: diagramas de cajas con los puntos originales y un gráfico QQ por grupo (en una regresión, los residuos en su lugar).
3. **Compara la dispersión** entre grupos con los números a secas, no solo con una prueba.
4. **Pregúntate si importa.** Ejecuta el análisis estándar junto a la alternativa robusta. Si las conclusiones coinciden, el supuesto dudoso no está determinando tu resultado.
5. **Si importa, cambia** a la alternativa robusta (más abajo) e infórmalo.

## Código: grupos y una variable de respuesta numérica

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

df = pd.read_csv("my_data.csv")
outcome, group = "ldl_mmol", "carrier_status"

groups = {name: values.dropna() for name, values in df.groupby(group)[outcome]}
fig, axes = plt.subplots(1, 1 + len(groups), figsize=(4.5 * (1 + len(groups)), 4))

sns.boxplot(data=df, x=group, y=outcome, ax=axes[0])
sns.stripplot(data=df, x=group, y=outcome, color="black", alpha=0.3, ax=axes[0])
for ax, (name, values) in zip(axes[1:], groups.items()):
    stats.probplot(values, plot=ax)          # QQ-plot: points on the line = bell-shaped
    ax.set_title(f"QQ-plot: {name}")
plt.tight_layout()
plt.show()

sds = pd.Series({name: values.std() for name, values in groups.items()})
print(sds.round(2))
print("SD ratio, largest / smallest:", round(sds.max() / sds.min(), 2))
```

## Código: los residuos de una regresión

En una regresión (incluido el ANOVA con covariables), comprueba los *residuos* del modelo ajustado, no la variable de respuesta original:

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

model = smf.ols(f"{outcome} ~ C({group}) + age", data=df).fit()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sm.qqplot(model.resid, line="s", ax=axes[0])
axes[0].set_title("Residual QQ-plot")
axes[1].scatter(model.fittedvalues, model.resid, alpha=0.6)
axes[1].axhline(0, color="red", linestyle="--")
axes[1].set(xlabel="fitted values", ylabel="residuals", title="Residuals vs. fitted")
plt.tight_layout()
plt.show()
```

## Código: ¿importa? La versión estándar junto a la robusta

```python
a, b = list(groups.values())[:2]   # two groups
print("Student (equal variances):", stats.ttest_ind(a, b))
print("Welch (unequal variances):", stats.ttest_ind(a, b, equal_var=False))
print("Mann-Whitney (rank-based):", stats.mannwhitneyu(a, b))
```

## Código: tablas de chi-cuadrado

```python
table = pd.crosstab(df["treatment"], df["disease"])
chi2, p, dof, expected = stats.chi2_contingency(table)
print(pd.DataFrame(expected, index=table.index, columns=table.columns).round(1))  # expected counts
if (expected < 5).any():
    print("Small expected counts; Fisher's exact test (2x2 tables):", stats.fisher_exact(table))
```

## Cómo leer los gráficos

| Lo que ves | Qué significa | Qué hacer |
|---|---|---|
| Los puntos del gráfico QQ siguen la recta | Forma aproximada de campana | Nada |
| Los puntos se curvan alejándose en un extremo, normalmente hacia arriba a la derecha | Asimetría a la derecha (habitual en triglicéridos, concentraciones, recuentos) | Considera una prueba no paramétrica, un *bootstrap* o analizar en escala logarítmica |
| Ambos extremos se despegan (forma de S) o unos pocos puntos aislados | Colas pesadas o valores atípicos | Comprueba que los valores atípicos son reales; usa errores estándar robustos o una prueba basada en rangos |
| La caja de un grupo es mucho más alta que la de otro (regla práctica aproximada: cociente de desviaciones típicas superior a 2) | Varianzas desiguales | Prueba t de Welch / ANOVA de Welch, o una regresión con errores estándar robustos |
| Los residuos se abren en abanico al crecer los valores ajustados | La varianza aumenta con el nivel | Errores estándar robustos (`cov_type="HC3"`), o modelar el logaritmo de la variable de respuesta |
| Los residuos muestran una curva | La relación no es recta | Añade un término (p. ej., un término cuadrático) o usa otro modelo |
| Recuentos esperados inferiores a 5 | La aproximación del chi-cuadrado es mala | Prueba exacta de Fisher |

## Entrena el ojo

Los gráficos QQ son fáciles de malinterpretar la primera vez. Estas tres muestras son inventadas; fíjate en el aspecto de cada forma antes de juzgar tus propios datos:

```python
import numpy as np

rng = np.random.default_rng(0)
samples = {
    "bell-shaped": rng.normal(size=100),
    "right-skewed": rng.lognormal(size=100),
    "heavy tails": rng.standard_t(2, size=100),
}
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, (name, values) in zip(axes, samples.items()):
    stats.probplot(values, plot=ax)
    ax.set_title(name)
plt.tight_layout()
plt.show()
```

## Si algo sale mal

- **No trates una prueba de normalidad como un veredicto.** Shapiro-Wilk aprobará casi cualquier cosa con n pequeño y marcará ondulaciones triviales con n grande; úsala, si acaso, como complemento del gráfico (`stats.shapiro(values)`).
- **Las muestras grandes perdonan más.** Con suficientes datos por grupo, una no normalidad leve rara vez cambia el resultado de una prueba t; las varianzas desiguales (sobre todo con tamaños de grupo desiguales) y los valores atípicos importan más. Por eso el paso 4 (comparar con la versión robusta) es la comprobación práctica.
- **Las pruebas basadas en rangos no comparan medias ni medianas en general.** Preguntan si un grupo tiende a producir valores mayores; dilo al presentarlas.
- **Los problemas de independencia no se arreglan cambiando de prueba.** Necesitan un modelo distinto, no un valor p distinto.
