# Módulo 6: Construir modelos

Una vez que sabes *para qué* estás modelando (módulo 5), hay un puñado de cuestiones prácticas que se aplican casi con independencia del modelo concreto.

## Páginas

1. [Sobreajuste y regularización](./overfitting-and-regularization.md) — por qué un modelo que se ajusta perfectamente a tus datos puede ser, aun así, un mal modelo.
2. [Validación cruzada y revisión del modelo](./cross-validation-and-model-checking.md) — cómo saber si un modelo es bueno.
3. [Multicolinealidad](./multicollinearity.md) — qué ocurre cuando tus predictores se solapan demasiado.
4. [Error de medición](./measurement-error.md) — qué ocurre cuando un predictor o una variable de respuesta es un sustituto ruidoso de lo que de verdad querías medir.

## Guías prácticas

Recetas en Python para hacer estas comprobaciones por tu cuenta, sin necesidad de un asistente:

- [Cómo: validar un modelo predictivo](./how-to/validate-a-predictive-model.md)
- [Cómo: comprobar la multicolinealidad](./how-to/check-multicollinearity.md)
- [Cómo: corregir el error de medición](./how-to/handle-measurement-error.md), con un [cuaderno sobre la atenuación](../notebooks/measurement-error-attenuation.ipynb)

> **Para saber más**
>
> - [James, Witten, Hastie & Tibshirani (2021)](https://www.statlearning.com/), *An Introduction to Statistical Learning* (2.ª ed., de acceso libre en línea), cap. 5 "Resampling Methods" y cap. 6 "Linear Model Selection and Regularization", pp. 197–288.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §11.6–11.8 "Residual standard deviation" a "Cross validation", pp. 168–180.

---
**Módulo anterior:** [Predicción vs. causalidad](../05-prediction-vs-causation/README.md) · **Siguiente:** [Estructuras de datos especiales →](../07-special-data-structures/README.md) · [Inicio](../README.md) · [Glosario](../glossary.md)
