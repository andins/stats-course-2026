# Fundamentos del EDA (análisis exploratorio de datos)

**En pocas palabras:** antes de modelar o contrastar nada, mira tus datos —literalmente, con gráficos— desde varios ángulos.

## Por qué gráficos antes que modelos

Los estadísticos resumen pueden ocultar mucho. Un ejemplo (el cuarteto de Anscombe) muestra cuatro conjuntos de datos con medias, varianzas y correlaciones *idénticas*; sin embargo, al representarlos, uno es una recta, otro una curva, otro tiene un único valor atípico que lo determina todo y el último es casi constante salvo por un punto extremo. Los números resumen no distinguen estos casos; los gráficos, sí.

## Qué mirar

Una primera pasada minuciosa suele cubrir:

- **Datos faltantes** — ¿qué columnas tienen huecos y cuántos? (véase [Datos faltantes](./missing-data.md))
- **Variables individuales** — histogramas para las columnas numéricas, recuentos de barras para las categóricas. ¿Los valores parecen plausibles, o hay erratas o valores imposibles (valores negativos de LDL, edades de 200 años)?
- **Pares de variables** — diagramas de dispersión entre variables numéricas, diagramas de cajas de una variable numérica separada por una categoría. Lo que buscas: ¿la relación parece lineal o curva? ¿Hay valores atípicos? ¿El patrón cambia según el subgrupo?
- **Tendencias a lo largo del tiempo**, si hay una columna de tiempo o fecha.

## El ejemplo de Mia

Antes de contrastar nada, Mia representa el colesterol LDL según el estado de portador (diagrama de cajas), comprueba si el LDL tiene forma aproximadamente de campana dentro de cada grupo (histograma), dibuja el LDL frente a la edad en un diagrama de dispersión para ver si la edad pesa más que el estado de portador, y revisa qué muestras tienen genotipos o mediciones de LDL faltantes y por qué.

## Esto no es "hacer trampas"

Aquí importa una distinción: comprobar la *calidad* de los datos (valores imposibles, datos faltantes, valores atípicos evidentes) es una práctica estándar y apropiada tanto si tu análisis es exploratorio como confirmatorio. Lo que advierte la [página anterior](./exploratory-vs-confirmatory.md) es contra espiar la *propia hipótesis* y dejar que lo que ves cambie qué comparación presentas como "la prueba". Mirar tus datos no es el problema; el problema es elegir qué comparación presentar después de ver los resultados.

> **Hazlo tú mismo**
>
> - [Cómo: explorar un conjunto de datos](./how-to/explore-a-dataset.md) — una lista de comprobación y código para la calidad de los datos, las distribuciones, los pares de variables y las tendencias.
> - [Cuaderno: EDA paso a paso](../notebooks/eda-walkthrough.ipynb) — practica con un conjunto de datos inventado con problemas incluidos a propósito, o aplícalo a tu propio CSV.

> **Para saber más**
>
> - [Wickham, Çetinkaya-Rundel & Grolemund (2023)](https://r4ds.hadley.nz/EDA.html), *R for Data Science* (2nd ed., free online), Ch. 10 "Exploratory data analysis" — un recorrido práctico por la variación y la covariación.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §2.3 "All graphs are comparisons", pp. 25–31 — cómo hacer gráficos que respondan a una pregunta.
> - Anscombe (1973), "Graphs in statistical analysis," *The American Statistician* 27(1), 17–21 — el argumento clásico a favor de representar los datos antes de resumirlos.

---
**Anterior:** [Exploratorio vs. confirmatorio](./exploratory-vs-confirmatory.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Datos faltantes →](./missing-data.md) · [Glosario](../glossary.md)
