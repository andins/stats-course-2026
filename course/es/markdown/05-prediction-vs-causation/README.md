# Módulo 5: Predicción vs. causalidad

Con las mismas herramientas de regresión se hacen dos preguntas muy distintas, y confundirlas es uno de los errores con más consecuencias en la estadística aplicada.

## Páginas

1. [Predicción vs. explicación](./prediction-vs-explanation.md) — «¿funcionará con datos nuevos?» frente a «¿causó X a Y?».
2. [Experimentos vs. datos observacionales](./experiments-vs-observational-data.md) — por qué *cómo* se recogieron los datos cambia lo que puedes concluir.
3. [Diagramas causales](./causal-diagrams.md) — una forma sencilla de razonar sobre variables de confusión, mediadoras y colisionadores.

## Por qué esta distinción tiene su propio módulo

Un modelo que predice bien no es lo mismo que un modelo que te dice qué pasará si *intervienes*: cambiar una política, dar un tratamiento, modificar la dosis de un fármaco. Confundirlos lleva a errores prácticos: actuar sobre una correlación como si fuera algo que se puede cambiar, cuando en realidad es un subproducto de otra cosa muy distinta.

## Guías prácticas

- [Cómo: dibujar un diagrama causal](./how-to/draw-and-use-a-causal-diagram.md), con un [cuaderno sobre variable de confusión, mediadora y colisionador](../notebooks/confounder-mediator-collider.ipynb)

> **Para saber más**
>
> - Shmueli (2010), "To explain or to predict?," *Statistical Science* 25(3), 289–310.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §18.1–18.3 "Basics of causal inference" a "Randomized experiments", pp. 339–346.

---
**Módulo anterior:** [Fundamentos de regresión](../04-regression-basics/README.md) · **Siguiente:** [Construir modelos →](../06-building-models/README.md) · [Inicio](../README.md) · [Glosario](../glossary.md)
