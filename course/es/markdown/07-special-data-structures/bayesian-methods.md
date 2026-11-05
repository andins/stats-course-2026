# Métodos bayesianos

**En pocas palabras:** la estadística bayesiana responde al mismo tipo de preguntas que todo lo anterior en este curso, pero las replantea como «¿cómo debería actualizar mis creencias sobre una cantidad desconocida a la vista de estos datos?» en lugar de «¿cuán sorprendentes serían estos datos si realmente no hubiera ningún efecto?».

## La idea central

En lugar de un único valor p, un análisis bayesiano produce una **distribución a posteriori** (*posterior distribution*): una distribución de probabilidad completa sobre los valores plausibles de aquello que estás estimando (un tamaño del efecto, la media de un grupo, un coeficiente de regresión), que combina tus datos con una **distribución a priori** (*prior*): tus creencias declaradas *antes* de ver los datos (que pueden ser deliberadamente vagas o poco informativas si no quieres asumir mucho). A partir de la distribución a posteriori puedes presentar un **intervalo de credibilidad** (*credible interval*): un rango que se interpreta como «hay un 95 % de probabilidad de que el valor verdadero esté aquí dentro», una afirmación más directa de lo que permite un intervalo de confianza clásico.

## Por qué resulta especialmente natural para los modelos multinivel de este módulo

El [enfoque de agrupamiento parcial / multinivel](./clustered-and-hierarchical-data.md) para datos agrupados —en el que los grupos pequeños y ruidosos se acercan a la media global— es una idea bayesiana incluso cuando se ajusta con programas clásicos («frecuentistas»): el «agrupamiento» es matemáticamente una creencia a priori incorporada de que los grupos se parecen entre sí. Una versión plenamente bayesiana del mismo modelo hace esto explícito, te permite añadir otras creencias a priori razonables y suele comportarse mejor con grupos pequeños o escasos, donde el software clásico puede tener dificultades o dar estimaciones inestables. Lo mismo vale para un [metaanálisis](./meta-analysis.md), que es un modelo multinivel con los estudios como grupos: con solo un puñado de estudios, una distribución a priori sobre cuánto difieren los efectos verdaderos entre estudios suele ser más estable que estimar esa dispersión únicamente a partir de los datos.

## Herramientas, si quieres seguir este camino

- **PyMC**: una biblioteca de Python para construir modelos bayesianos de forma directa y flexible: escribes exactamente lo que crees sobre cada cantidad desconocida. Más control, más código.
- **Bambi**: una interfaz más sencilla construida sobre PyMC, que te permite describir muchos modelos habituales (incluidos los multinivel) con una fórmula corta, de manera similar a cómo escribirías una fórmula de regresión en otras partes de este curso. Normalmente es la vía de entrada más rápida, salvo que necesites un modelo a medida, para el que PyMC ofrece un control más directo.

## ¿Deberías recurrir a esto?

No por defecto. Es una herramienta más pesada, útil cuando necesitas una distribución completa para una estimación (no solo un valor puntual y un intervalo), cuando hay muchos grupos pequeños o escasos, o cuando existe información previa que merece incorporarse de manera formal. Si no estás seguro de necesitarlo, la versión clásica (no bayesiana) del mismo modelo, descrita en [Datos agrupados y jerárquicos](./clustered-and-hierarchical-data.md), es un buen punto de partida.

> **Para saber más**
>
> - [Johnson, Ott & Dogucu (2022)](https://www.bayesrulesbook.com/), *Bayes Rules! An Introduction to Applied Bayesian Modeling* (gratuito en línea), Ch. 1–2 para la idea central y Ch. 15–17 para los modelos jerárquicos.
> - McElreath (2020), *Statistical Rethinking* (2.ª ed.), Ch. 2 "Small Worlds and Large Worlds" y Ch. 13 "Models With Memory".
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §9.5 "Uniform, weakly informative, and informative priors in regression", pp. 123–128.

---
**Anterior:** [Metaanálisis: sesgos y trampas](./meta-analysis-pitfalls.md) · [Inicio del módulo](./README.md) · [Inicio](../README.md) · [Glosario](../glossary.md)
