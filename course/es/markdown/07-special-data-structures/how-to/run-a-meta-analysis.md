# Cómo: realizar un metaanálisis

**Úsalo cuando:** tienes una estimación del efecto y su error estándar de cada uno de varios estudios sobre la misma pregunta (estudios de una variante génica, ensayos de un fármaco) y quieres una única respuesta combinada. Las ideas están en la página [Metaanálisis](../meta-analysis.md); las trampas, en [Metaanálisis: sesgos y trampas](../meta-analysis-pitfalls.md).

## Pasos

1. **Fija la pregunta y los criterios de elegibilidad antes de mirar los resultados.** ¿Qué tratamiento, qué desenlace, qué tipos de estudio cuentan? Déjalo por escrito; buscar y seleccionar estudios es la parte que más afecta a la respuesta.
2. **Pon todos los estudios en la misma escala.** Una fila por estudio con un `effect` y su error estándar `se`. El último bloque de código de abajo muestra cómo obtenerlos a partir de medias de grupo o de recuentos.
3. **Combina con un modelo de efectos aleatorios.** Presenta la estimación combinada con su intervalo.
4. **Presenta la dispersión de los efectos verdaderos:** la heterogeneidad (τ, I²) y el intervalo de predicción, no solo la media combinada.
5. **Dibuja el diagrama de bosque** y míralo antes de fiarte de ningún número.
6. **Comprueba cuán frágil es el resultado:** deja fuera un estudio cada vez y compara con la estimación de efecto fijo.
7. **Busca sesgo de publicación** (gráfico de embudo, regresión de Egger), teniendo en cuenta que con menos de unos 10 estudios no puede decirte gran cosa.
8. **Presenta** el número de estudios, cómo se encontraron y las limitaciones anteriores.

## Código: combinar los estudios

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.meta_analysis import combine_effects

df = pd.read_csv("my_data.csv")    # one row per study: study, effect (difference in LDL, mmol/L), se (its standard error)
k = len(df)

res = combine_effects(df["effect"].to_numpy(), (df["se"] ** 2).to_numpy(), method_re="iterated", row_names=list(df["study"]))
pooled, pooled_se = res.mean_effect_re, res.sd_eff_w_re              # random effects
fixed, fixed_se = res.mean_effect_fe, res.sd_eff_w_fe                # one common true effect
tau2, i2 = res.tau2, max(0.0, res.i2)                                # between-study variance; share of spread beyond chance
q_p = stats.chi2.sf(res.q, k - 1)
pi_half = stats.t.ppf(0.975, k - 2) * np.sqrt(tau2 + pooled_se ** 2)

print(f"{k} studies")
print(f"random effects: {pooled:.2f} (95% CI {pooled - 1.96 * pooled_se:.2f} to {pooled + 1.96 * pooled_se:.2f})")
print(f"fixed effect:   {fixed:.2f} (95% CI {fixed - 1.96 * fixed_se:.2f} to {fixed + 1.96 * fixed_se:.2f})")
print(f"tau = {np.sqrt(tau2):.2f}, I2 = {100 * i2:.0f}%, heterogeneity test p = {q_p:.3f}")
print(f"95% prediction interval for a new study: {pooled - pi_half:.2f} to {pooled + pi_half:.2f}")

res.plot_forest()
plt.show()
```

## Código: ¿pocos estudios? Ensancha el intervalo con honestidad

Con un puñado de estudios, τ² se estima mal y el intervalo habitual es demasiado estrecho. El ajuste de Hartung-Knapp (HKSJ) usa la dispersión observada de los estudios y una distribución t:

```python
w = 1 / (df["se"] ** 2 + tau2)
mu = (w * df["effect"]).sum() / w.sum()
se_hksj = np.sqrt((w * (df["effect"] - mu) ** 2).sum() / ((k - 1) * w.sum()))
se_hksj = max(se_hksj, np.sqrt(1 / w.sum()))                   # never narrower than the usual interval
t_crit = stats.t.ppf(0.975, k - 1)
print(f"random effects, Hartung-Knapp: {mu:.2f} (95% CI {mu - t_crit * se_hksj:.2f} to {mu + t_crit * se_hksj:.2f})")
```

## Código: ¿cuán frágil es el resultado?

```python
rows = []
for name in df["study"]:
    rest = df[df["study"] != name]
    r = combine_effects(rest["effect"].to_numpy(), (rest["se"] ** 2).to_numpy(), method_re="iterated")
    rows.append({"left out": name, "estimate": r.mean_effect_re, "tau": np.sqrt(r.tau2)})
leave_one_out = pd.DataFrame(rows).round(2)
print(leave_one_out.to_string(index=False))
```

## Código: sesgo de publicación

```python
precision = (1 / df["se"]).rename("precision")
egger = sm.OLS(df["effect"] / df["se"], sm.add_constant(precision)).fit()     # Egger's regression
print(f"Egger intercept = {egger.params['const']:.2f} (p = {egger.pvalues['const']:.2f}); "
      f"{k} studies, so treat this as a weak check")

fig, ax = plt.subplots()
ax.scatter(df["effect"], df["se"])
ax.axvline(pooled, color="grey", linestyle="--")
ax.invert_yaxis()                                                # the most precise studies at the top
ax.set_xlabel("effect")
ax.set_ylabel("standard error")
plt.show()
```

## Código: obtener un efecto y un error estándar de cada estudio

Si un artículo da resúmenes por grupo en lugar de un efecto y un error estándar, calcúlalos tú. Usa la misma escala para todos los estudios.

```python
from statsmodels.stats.meta_analysis import effectsize_2proportions, effectsize_smd

# Continuous outcome, same unit in every study: the raw mean difference and its standard error
means = pd.DataFrame({
    "mean_t": [24.1, 22.8, 25.0], "sd_t": [3.2, 2.9, 3.6], "n_t": [30, 45, 28],
    "mean_c": [22.0, 22.1, 22.7], "sd_c": [3.0, 3.1, 3.3], "n_c": [30, 44, 29],
})
diff = means["mean_t"] - means["mean_c"]
se_diff = np.sqrt(means["sd_t"] ** 2 / means["n_t"] + means["sd_c"] ** 2 / means["n_c"])

# Different units or instruments across studies: the standardized mean difference (Hedges' g)
g, var_g = effectsize_smd(means["mean_t"], means["sd_t"], means["n_t"],
                          means["mean_c"], means["sd_c"], means["n_c"])

# Yes/no outcome: the log odds ratio (pool on the log scale, then exponentiate)
counts = pd.DataFrame({"events_t": [12, 9, 20], "n_t": [60, 40, 90], "events_c": [20, 15, 31], "n_c": [60, 42, 88]})
log_or, var_log_or = effectsize_2proportions(counts["events_t"], counts["n_t"], counts["events_c"], counts["n_c"],
                                             statistic="odds-ratio")

print(pd.DataFrame({"difference": diff, "se": se_diff, "g": g, "se_g": np.sqrt(var_g),
                    "log_or": log_or, "se_log_or": np.sqrt(var_log_or)}).round(2))
```

## Cómo leer el resultado

Resultado de ejemplo con datos inventados (10 estudios de una variante de LDLR, efecto en mmol/L de colesterol LDL adicional en portadores):

```text
10 studies
random effects: 0.34 (95% CI 0.23 to 0.45)
fixed effect:   0.30 (95% CI 0.23 to 0.38)
tau = 0.13, I2 = 66%, heterogeneity test p = 0.002
95% prediction interval for a new study: 0.01 to 0.67
random effects, Hartung-Knapp: 0.34 (95% CI 0.21 to 0.47)
left out  estimate  tau
 Study 1      0.32 0.14
 ...
 Study 9      0.39 0.02
Study 10      0.33 0.14
Egger intercept = 3.17 (p = 0.11); 10 studies, so treat this as a weak check
```

- **La estimación combinada es el efecto promedio, no el efecto en todas partes.** De media, portar la variante añade unos 0.34 mmol/L de LDL. Pero τ = 0.13 mmol/L e I² = 66 % indican que los estudios difieren de verdad, y el intervalo de predicción (0.01 a 0.67 mmol/L) indica que un estudio nuevo podría mostrar desde ningún efecto hasta el doble del promedio. Ese es el resumen honesto; el intervalo de confianza de la media por sí solo suena mucho más seguro.
- **Los efectos aleatorios dieron un intervalo más ancho que el efecto fijo** (0.23 a 0.45 frente a 0.23 a 0.38) porque cuentan las diferencias entre estudios como incertidumbre. Cuando la heterogeneidad es baja, ambos coinciden.
- **El intervalo de Hartung-Knapp es aún más ancho** (0.21 a 0.47), como cabía esperar con solo 10 estudios. Preséntalo si tienes pocos estudios.
- **Dejar fuera el Study 9 reduce τ de 0.13 a 0.02** y mueve la estimación a 0.39. Gran parte de la heterogeneidad procede de un solo estudio. Mira qué tenía de distinto (¿otra ascendencia?, ¿otra técnica de laboratorio?) antes de decidir si pertenece al conjunto combinado. No lo descartes solo porque resulte incómodo: presenta ambos resultados.
- **La ordenada en el origen de Egger apunta a estudios pequeños con efectos mayores** (3.17), aunque no «significativamente» (p = 0.11). Con 10 estudios esta prueba tiene poca potencia, así que la ausencia de significación no es evidencia de que no haya sesgo de publicación. Mira el gráfico de embudo y trata la estimación combinada como posiblemente optimista.

## Qué enfoque usar en cada caso

| Tu situación | Usa |
|---|---|
| Los estudios midieron lo mismo en la misma escala | Diferencia de medias sin estandarizar (o logaritmo de la razón de odds) y efectos aleatorios |
| Los estudios usaron instrumentos o unidades distintos | Diferencia de medias estandarizada, con la salvedad de que también depende de lo variable que fuera cada muestra |
| Menos de unos 5-10 estudios | Efectos aleatorios con el intervalo de Hartung-Knapp, o un modelo bayesiano; indica cuán pocos estudios había |
| Varios efectos del mismo estudio (dos dosis frente a un control, varios desenlaces) | No son independientes: elige uno por estudio o trata el estudio como un grupo (véase [Datos agrupados y jerárquicos](../clustered-and-hierarchical-data.md)) |
| Tienes los datos en bruto de cada centro | No es un problema de metaanálisis: analízalos como datos agrupados con el centro como grupo, véase [Cómo: analizar datos agrupados](./analyze-clustered-data.md) |
| Quieres saber por qué difieren los estudios | Una metarregresión sobre características a nivel de estudio, interpretada como exploratoria: las características no están aleatorizadas |

## Si algo sale mal

- **τ² sale cero pero el diagrama de bosque claramente se dispersa:** con pocos estudios, o poco precisos, τ² se estima muy mal. Presenta el intervalo de predicción y el intervalo de Hartung-Knapp en lugar de concluir que los estudios coinciden.
- **I² es muy alta (por encima de aproximadamente el 75 %):** el promedio puede no describir ningún contexto real. Busca qué difiere entre estudios (dosis, ascendencia, técnica de laboratorio, diseño) antes de presentar una única cifra.
- **Un estudio domina los pesos, o dejarlo fuera cambia la respuesta:** dilo y presenta el resultado con y sin él.
- **El gráfico de embudo está desequilibrado:** estudios pequeños con efectos grandes y ausencia de estudios pequeños con efectos nulos sugieren sesgo de publicación, pero también diferencias reales entre estudios pequeños y grandes. La estimación combinada puede ser demasiado optimista; dilo.
- **Los estudios presentan cosas distintas (medianas, sin errores estándar):** existen fórmulas de conversión (véase el Cochrane Handbook), pero cada conversión añade supuestos; explícitalos.
- **Un desenlace binario con cero eventos en un grupo:** el logaritmo de la razón de odds no está definido; usa `zero_correction` en `effectsize_2proportions` y comprueba que el resultado no depende de la corrección.
