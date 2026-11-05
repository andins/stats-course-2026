# Cómo: explorar un conjunto de datos antes de analizarlo

**Úsalo cuando:** tengas un conjunto de datos nuevo y quieras entenderlo antes de contrastar o modelar nada. El razonamiento está en la página [Fundamentos del EDA](../eda-basics.md); para la frontera entre mirar sin hacer daño y elegir tu hipótesis a partir de los datos, consulta [Exploratorio vs. confirmatorio](../exploratory-vs-confirmatory.md).

Para una visita guiada con gráficos sobre un conjunto de datos inventado que tiene algunos problemas incluidos a propósito, trabaja el [cuaderno de EDA paso a paso](../../notebooks/eda-walkthrough.ipynb) (descárgalo y ábrelo en Jupyter, VS Code o Colab). Puedes aplicarlo a tu propio CSV cambiando una sola línea.

## Pasos

1. **Comprueba lo básico y la calidad de los datos:** tamaño, tipos de columna, rangos, duplicados, valores faltantes. Esto es higiene, no espiar la hipótesis, y debes hacerlo en cualquier análisis.
2. **Mira una variable cada vez.** Histogramas para los números, recuentos para las categorías. Busca valores imposibles, picos extraños (p. ej., un valor por defecto de 0 o 999) y asimetría.
3. **Mira pares de variables.** Diagramas de dispersión para número frente a número, diagramas de cajas con los puntos originales para número frente a categoría.
4. **Busca estructura por subgrupos y tendencias en el tiempo.** ¿Cambia el patrón según el grupo? ¿Se desplaza la variable de respuesta con la fecha?
5. **Anota lo que has notado como preguntas**, no como conclusiones. Todo lo que hayas encontrado mirando es una hipótesis que comprobar con datos nuevos, no un resultado.

## Código: lo básico, la calidad de los datos y los datos faltantes

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

La última línea es la comprobación más importante para los datos faltantes: si las filas con la variable de respuesta faltante difieren sistemáticamente de las demás (aquí, quizá pacientes de más edad), eliminarlas no es inocuo. Véase [Datos faltantes](../missing-data.md).

## Código: los gráficos

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

## Qué buscar

- **Histogramas:** valores imposibles o inverosímiles (valores negativos de LDL, un valor atípico 10 veces mayor que parece un error de decimales), acumulaciones en un número redondo, dos jorobas (un subgrupo oculto), una cola larga a la derecha (a menudo señal de que una escala logarítmica sería más natural).
- **Diagramas de dispersión:** curvas en lugar de rectas, unos pocos puntos que determinan todo el patrón, forma de abanico (una variabilidad que crece con el nivel), grupos.
- **Diagramas de cajas con puntos:** grupos de tamaños muy distintos, un grupo con mucha más dispersión, grupos solapados frente a claramente separados, valores atípicos que pertenecen a una clínica o a una fecha.
- **A lo largo del tiempo:** una deriva o un cambio brusco (un instrumento nuevo, una persona operadora nueva, otra estación del año).
- **Datos faltantes:** qué columnas, cuántos y si dependen de otras variables.

## Si encuentras algo

- **Un error claro en los datos (una errata, un valor imposible):** corrígelo en origen si puedes; si no, exclúyelo e indícalo explícitamente en tus métodos, con el número de filas afectadas.
- **Un valor atípico sin explicación:** no lo elimines solo porque resulte incómodo. Presenta el análisis con y sin él si importa.
- **Subgrupos o curvas:** anótalos como cosas que modelar. Si los encontraste mirando, dilo; son pistas, no hallazgos confirmados.
- **Muchos datos faltantes:** informa de cuántos y dónde, y consulta [Datos faltantes](../missing-data.md) antes de elegir una solución.
- **Antes de contrastar nada,** decide tu comparación e, idealmente, déjala por escrito, *sin* elegirla a partir de los gráficos. Si los gráficos sugieren una comparación nueva, etiquétala como exploratoria.
