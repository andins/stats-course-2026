# Validación cruzada y revisión del modelo

**En pocas palabras:** la forma fiable de saber si un modelo predictivo es bueno es comprobar su rendimiento con datos que no ha visto.

## Por qué engaña comprobar el ajuste con los mismos datos con los que construiste el modelo

El rendimiento de un modelo sobre los mismos datos que se usaron para construirlo (su "ajuste de entrenamiento") siempre parece al menos tan bueno como su verdadera capacidad de generalizar, y a menudo mucho mejor, sobre todo en modelos flexibles que pueden sobreajustarse (véase [Sobreajuste y regularización](./overfitting-and-regularization.md)). Presentar el rendimiento de entrenamiento como si indicara cómo se comportará el modelo en el mundo real es uno de los errores más comunes del modelado aplicado.

## La solución: reservar una parte de los datos

- **División entrenamiento/prueba** (*train/test split*): aparta una porción de los datos (p. ej., el 25%) que el modelo no ve mientras se construye y comprueba el rendimiento únicamente en esa porción reservada.
- **Validación cruzada** (*cross-validation*): una versión que aprovecha mejor los datos. Divide los datos en varios "pliegues" (*folds*), entrena repetidamente con todos los pliegues menos uno y evalúa con el pliegue que queda fuera, y después promedia el rendimiento de todas las divisiones. Así cada dato se usa tanto para entrenar como para evaluar (aunque nunca a la vez), algo importante cuando los datos son escasos.

![Arriba: una barra dividida en una parte grande de entrenamiento y una parte pequeña de prueba reservada. Abajo: cinco barras, cada una dividida en cinco pliegues; en cada barra se reserva un pliegue distinto y los otros cuatro se usan para entrenar, lo que da cinco puntuaciones que se promedian.](../figures/cross_validation.png)

*Una única división entrenamiento/prueba puntúa el modelo una sola vez; la validación cruzada con 5 pliegues lo repite cinco veces, de modo que cada observación queda reservada exactamente una vez.*

## Qué significa "rendimiento" depende de la variable de respuesta

- Variable de respuesta continua (colesterol LDL en mmol/L): RMSE (el error de predicción típico, en las propias unidades de la variable de respuesta) o R² (fracción de la variación explicada).
- Variable de respuesta sí/no (sobrevive o no): AUC (lo bien que el modelo ordena los casos positivos frente a los negativos) o exactitud (*accuracy*).

## Cómo se relaciona esto con la distinción entre predicción y causalidad

La validación cruzada es la forma adecuada de juzgar un modelo **predictivo** (módulo 5): mide directamente lo que te interesa, la generalización a datos nuevos. *No* es la forma adecuada de juzgar si una estimación **causal** es correcta: un modelo puede predecir de maravilla con datos reservados y, aun así, estimar muy mal el efecto causal de una variable concreta si no ha tenido en cuenta adecuadamente la confusión (véase [Diagramas causales](../05-prediction-vs-causation/causal-diagrams.md)). Un buen rendimiento predictivo y una estimación causal válida son objetivos distintos, que se comprueban de formas distintas.

> **Hazlo tú mismo**
>
> [Cómo: validar un modelo predictivo](./how-to/validate-a-predictive-model.md) — división entrenamiento/prueba, validación cruzada y un modelo regularizado, paso a paso en Python.

> **Para saber más**
>
> - [James, Witten, Hastie & Tibshirani (2021)](https://www.statlearning.com/), *An Introduction to Statistical Learning* (2.ª ed.), §5.1 "Cross-Validation", pp. 198–209 (el *k-fold* está en §5.1.3, p. 203).
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §11.7 "External validation" y §11.8 "Cross validation", pp. 171–180.
> - McElreath (2020), *Statistical Rethinking* (2.ª ed.), cap. 7, §7.4 "Predicting predictive accuracy" — comparación entre la validación cruzada y los criterios de información.

---
**Anterior:** [Sobreajuste y regularización](./overfitting-and-regularization.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Multicolinealidad →](./multicollinearity.md) · [Glosario](../glossary.md)
