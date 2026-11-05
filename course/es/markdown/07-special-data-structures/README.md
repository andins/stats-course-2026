# Módulo 7: Estructuras de datos especiales

Tres situaciones que requieren algo más que las pruebas y los modelos básicos: observaciones que no son independientes (datos agrupados u ordenados en el tiempo) y datos que son, a su vez, una colección de estudios.

## Páginas

1. [Datos agrupados y jerárquicos](./clustered-and-hierarchical-data.md) — cuando las observaciones vienen en grupos (pacientes en hospitales, familiares en familias, medidas repetidas en el mismo sujeto).
2. [Series temporales](./time-series-data.md) — cuando las observaciones están ordenadas en el tiempo y el valor de hoy puede depender del de ayer.
3. [Metaanálisis](./meta-analysis.md) — combinar las estimaciones de varios estudios sobre la misma pregunta y medir cuánto discrepan entre sí.
4. [Metaanálisis: sesgos y trampas](./meta-analysis-pitfalls.md) — por qué una cifra combinada puede engañar: selección de estudios, sesgo de publicación, mezcla de estudios distintos.
5. [Métodos bayesianos](./bayesian-methods.md) — un marco distinto, opcional y más avanzado, relacionado con los modelos de este módulo.

## Por qué estos temas tienen su propio módulo

Nada de lo anterior en este curso se rompe cuando los datos están agrupados u ordenados en el tiempo: simplemente te da resultados demasiado optimistas (errores estándar demasiado pequeños, intervalos de confianza demasiado estrechos) si no lo tienes en cuenta. Las dos primeras páginas explican cómo reconocer cuándo ocurre y qué hacer al respecto. El metaanálisis es el siguiente paso natural: un estudio es un grupo, así que combinar estudios es un modelo multinivel cuyas observaciones son estimaciones a nivel de estudio, y es una herramienta útil cuando un solo estudio rara vez es la última palabra.

## Guías prácticas

- [Cómo: analizar datos agrupados](./how-to/analyze-clustered-data.md), con un [cuaderno sobre datos agrupados](../notebooks/clustered-data-overconfidence.ipynb)
- [Cómo: realizar un metaanálisis](./how-to/run-a-meta-analysis.md)

> **Para saber más**
>
> - Gelman & Hill (2007), *Data Analysis Using Regression and Multilevel/Hierarchical Models*, Ch. 11 "Multilevel structures" y Ch. 12 "Multilevel linear models: the basics".
> - [Hyndman & Athanasopoulos (2021)](https://otexts.com/fpp3/), *Forecasting: Principles and Practice* (3.ª ed., gratuito en línea), §2.8 "Autocorrelation" y Ch. 10 "Dynamic regression models".
> - [Harrer, Cuijpers, Furukawa & Ebert (2021)](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/), *Doing Meta-Analysis with R: A Hands-On Guide* (gratuito en línea) — para el metaanálisis.

---
**Módulo anterior:** [6. Construir modelos](../06-building-models/README.md) · [Inicio](../README.md) · [Glosario](../glossary.md)
