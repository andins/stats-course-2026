# Pruebas como regresiones

**En pocas palabras:** las pruebas «con nombre» del Módulo 3 no son una caja de herramientas aparte: cada una es una regresión con otro sombrero.

## Algunas equivalencias concretas

| Prueba con nombre | Equivalente en regresión |
|---|---|
| Prueba t de dos muestras | Regresa el resultado sobre un único predictor sí/no (0/1) que indica el grupo. La pendiente *es* la diferencia de medias. |
| ANOVA de una vía | Regresa el resultado sobre un predictor categórico con una variable ficticia (*dummy*) por grupo (menos uno). La prueba global *es* la prueba F del ANOVA. |
| Prueba de independencia chi-cuadrado | Regresión logística de una variable categórica sobre la otra. |
| Prueba de significación de la correlación | La prueba de la pendiente en una regresión simple de y sobre x. |

Esto refleja que todas estas pruebas plantean la misma pregunta de fondo («¿explica este agrupamiento o esta variable parte de la variación del resultado?»), empaquetada para casos concretos y sencillos.

## Por qué importa en la práctica

Cuando una prueba se escribe como «una regresión con un predictor», ampliarla resulta sencillo:

- **¿Necesitas añadir una covariable?** (p. ej., controlar por la edad al comparar clases de genotipo). Basta con añadirla como un término más de la regresión. No hay que buscar una «prueba ANCOVA» aparte: es la misma regresión con un predictor más.
- **¿Variabilidad desigual entre grupos?** Ajusta la misma regresión pero pide *errores estándar robustos*: así se reproduce la prueba t de Welch sin necesidad de un procedimiento con otro nombre.
- **¿Datos agrupados o repetidos?** La misma regresión con otro cálculo del error estándar, o una versión de efectos mixtos; consulta [Datos agrupados y jerárquicos](../07-special-data-structures/clustered-and-hierarchical-data.md).

## La idea clave

Si una prueba clásica te parece un callejón sin salida (no te deja añadir la covariable que necesitas o gestionar la complicación que tienen tus datos), la solución casi siempre es «escríbela como una regresión y modifícala desde ahí», no «busca una prueba con nombre más exótico».

> **Hazlo tú mismo**
>
> [Cómo: ejecutar una prueba como regresión](./how-to/run-a-test-as-a-regression.md) — cada prueba clásica junto a su forma de regresión, con números que coinciden.

> **Para saber más**
>
> - [Lindeløv (2019)](https://lindeloev.github.io/tests-as-linear/), "Common statistical tests are linear models" (gratis en línea) — cada prueba con nombre junto a su equivalente con `lm()`, con código en R.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §7.3 (pp. 99–101) y §10.5 "Formulating paired or blocked designs as a regression problem" (pp. 139–140).

---
**Anterior:** [Qué es la regresión](./what-is-regression.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Modelos lineales generalizados →](./generalized-linear-models.md) · [Glosario](../glossary.md)
