# Metaanálisis

**En pocas palabras:** un metaanálisis combina las *estimaciones* de varios estudios sobre la misma pregunta en una única respuesta, dando más peso a los estudios más precisos, y te dice cuánto discrepan los estudios entre sí. Es estadística en la que cada «observación» es un estudio entero.

## Por qué combinar estudios

Mia no es la única persona que estudia su variante de LDLR: se han publicado diez estudios, cada uno en una clínica o población distinta y con su propia estimación del efecto de la variante sobre el colesterol LDL. Algunos encontraron una asociación clara, otros apenas nada, uno no encontró nada. Fijarse en qué estudios fueron «significativos» es una mala forma de resumirlos (los ensayos pequeños suelen ser no significativos incluso cuando el efecto es real; véase [Tamaño muestral y potencia](../01-planning-your-study/sample-size-and-power.md)). Un metaanálisis plantea en cambio dos preguntas mejores: *¿cuál es el efecto promedio y cuánto varía de un estudio a otro?*

## Qué entra: un efecto y un error estándar por estudio

Cada estudio aporta una fila: una **estimación del efecto** y su **error estándar** (cuán incierta es esa estimación). Todos los estudios deben medir el efecto en la misma escala, por ejemplo la diferencia de colesterol LDL medio en mmol/L, o un efecto *estandarizado* cuando los estudios usaron instrumentos distintos (véase [Tamaño del efecto](../01-planning-your-study/effect-size.md)). Para desenlaces de sí/no, la escala habitual es el logaritmo de la razón de odds o de la razón de riesgos. Se combinan estimaciones, nunca valores p ni veredictos de «significativo / no significativo».

## La idea central: ponderar por la precisión

La estimación combinada es una media ponderada, y el peso de cada estudio es la inversa de su varianza:

peso = 1 / (error estándar² + τ²)

Un ensayo grande y preciso cuenta más que uno pequeño y ruidoso. El término adicional τ² (que se explica a continuación) vale cero en la versión más simple del modelo.

## Efecto común o efectos aleatorios

- **Modelo de efecto común (de «efecto fijo»):** asume que hay *un único* efecto verdadero y que cada estudio se desvía de él solo por azar. La estimación combinada responde a «¿cuál es ese único efecto?». Es razonable para replicaciones casi idénticas (el mismo protocolo ejecutado en varios laboratorios).
- **Modelo de efectos aleatorios:** asume que cada estudio tiene *su propio* efecto verdadero (distinta ascendencia, dieta, mezcla de edades, técnica de laboratorio, población), y que estos efectos verdaderos se dispersan alrededor de un promedio con dispersión τ. La estimación combinada responde a «¿cuál es el efecto *promedio* en contextos como estos?». Como el intervalo incluye las diferencias entre estudios, es más ancho y más honesto.

En las ciencias de la vida los estudios casi nunca son replicaciones exactas, así que **los efectos aleatorios son la opción por defecto sensata**. Elige el modelo por lo que crees sobre los estudios, no porque uno dé un valor p menor.

## ¿Cuánto discrepan los estudios? (heterogeneidad)

- **τ (tau):** la desviación típica de los efectos verdaderos, en las mismas unidades que el efecto. «τ = 0.7 kg» significa que los efectos verdaderos suelen diferir unos 0.7 kg de la media.
- **I²:** la proporción de la variabilidad entre las estimaciones que refleja diferencias reales y no azar. Aproximadamente, 25 % es bajo, 50 % moderado y 75 % alto; estas etiquetas son convenciones, no reglas. I² además crece con el tamaño de los estudios, así que puede parecer alta con estudios precisos aunque las diferencias sean pequeñas en términos prácticos: léela junto con τ.
- **Intervalo de predicción** (*prediction interval*): el rango en el que cabría esperar que cayera el efecto verdadero de un estudio *nuevo*. Suele ser el número más útil: una media combinada de 0.34 mmol/L con un intervalo de predicción de 0 a 0.7 mmol/L cuenta una historia muy distinta de la misma media con un intervalo de 0.3 a 0.4 mmol/L. Preséntalo junto con el intervalo de confianza de la media. Hacen falta varios estudios para que sea creíble.

## El diagrama de bosque

La imagen estándar (*forest plot*): una fila por estudio (un cuadrado para su estimación, con tamaño proporcional al peso, y una línea para su intervalo) y un rombo al final para la estimación combinada. Míralo antes de leer ningún número. Si los intervalos apenas se solapan, o un estudio queda muy lejos del resto, el promedio combinado puede no describir a nadie.

![Diagrama de bosque de diez estudios inventados. Cada estudio es un cuadrado azul, con tamaño proporcional a su peso, y una línea horizontal para su intervalo de confianza del 95 %. Debajo, un rombo verde muestra la estimación combinada de 0.34 mmol/L y una barra verde muestra el intervalo de predicción de 0.01 a 0.67 mmol/L. Unas anotaciones explican cada elemento.](../figures/forest_plot.png)

*Cómo leer un diagrama de bosque. Los datos son inventados; son los mismos diez estudios que en la [guía práctica del metaanálisis](./how-to/run-a-meta-analysis.md).*

## Dónde encaja en este módulo

Un metaanálisis de efectos aleatorios es un **modelo multinivel** con los estudios como grupos: la estimación de cada estudio se acerca («se encoge») hacia la media global, y cuanto más ruidoso es el estudio, más se acerca. Véase [Datos agrupados y jerárquicos](./clustered-and-hierarchical-data.md). Con pocos estudios, una versión [bayesiana](./bayesian-methods.md) suele ser más estable, porque te permite expresar cuán grandes crees que podrían ser plausiblemente las diferencias entre estudios.

Antes de fiarte de una cifra combinada, lee [Metaanálisis: sesgos y trampas](./meta-analysis-pitfalls.md): un metaanálisis solo es tan bueno como los estudios que reúne y la forma en que se reunieron.

> **Hazlo tú mismo**
>
> - [Cómo: realizar un metaanálisis](./how-to/run-a-meta-analysis.md) — combina estudios, presenta la heterogeneidad y un intervalo de predicción, dibuja el diagrama de bosque y comprueba cuán frágil es el resultado.

> **Para saber más**
>
> - Borenstein, Hedges, Higgins & Rothstein (2009), *Introduction to Meta-Analysis*, Wiley — el capítulo "Fixed-effect versus random-effects models" y los capítulos sobre heterogeneidad.
> - [Harrer, Cuijpers, Furukawa & Ebert (2021)](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/), *Doing Meta-Analysis with R: A Hands-On Guide* (gratuito en línea) — una guía práctica, con R en lugar de Python.
> - Higgins & Thompson (2002), "Quantifying heterogeneity in a meta-analysis," *Statistics in Medicine* 21(11), 1539–1558 — de donde procede I².
> - IntHout, Ioannidis, Rovers & Goeman (2016), "Plea for routinely presenting prediction intervals in meta-analysis," *BMJ Open* 6(7), e010247.
> - [Cochrane Handbook for Systematic Reviews of Interventions](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current) (versión 6.5, gratuito en línea), Ch. 10 "Analysing data and undertaking meta-analyses".

---
**Anterior:** [Series temporales](./time-series-data.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Metaanálisis: sesgos y trampas →](./meta-analysis-pitfalls.md) · [Inicio](../README.md) · [Glosario](../glossary.md)
