# Modelos lineales generalizados (GLM)

**En pocas palabras:** los GLM son la extensión de la regresión a resultados que no son un simple número continuo, como los resultados de tipo sí/no o los recuentos.

## Por qué la regresión simple no basta para todos los resultados

La regresión ordinaria supone que el resultado puede ser (en principio) cualquier número real y que el «ruido» alrededor de la recta tiene una forma aproximadamente acampanada. Esto falla en dos casos:

- **Resultados de tipo sí/no** (¿se recuperó el paciente?, ¿sobrevivieron las células?): una recta puede predecir valores absurdos como «un 120 % de probabilidad de recuperación».
- **Recuentos** (número de visitas a urgencias por paciente, número de visitas al hospital): los recuentos no pueden ser negativos y su dispersión suele crecer con su promedio, al contrario que la dispersión constante que supone la regresión simple.

![Diagrama de dispersión de un resultado sí/no de evento coronario frente al colesterol LDL. Una recta de regresión ascendente atraviesa los puntos y se sale del rango de 0 a 1 por ambos extremos, con lo que predice probabilidades imposibles, mientras que una curva logística verde se aplana suavemente hacia 0 y 1.](../figures/glm_logistic.png)

*Datos simulados. Una recta puede predecir probabilidades por debajo del 0 % o por encima del 100 %; la curva en forma de S de la regresión logística no.*

## La solución de los GLM

Un GLM conserva la idea de «ajustar una recta a través de los predictores», pero añade una **función de enlace** (*link function*) que traslada la recta a la escala adecuada para el tipo de resultado:

- **Regresión logística**: para resultados sí/no. Modela el *logaritmo de los odds* (*log-odds*) del «sí» como una función lineal de los predictores, lo que mantiene las probabilidades predichas entre 0 y 1. Los coeficientes suelen presentarse como **odds ratios** (p. ej., «los pacientes tratados tenían 2.3 veces más odds de recuperarse»).
- **Regresión de Poisson**: para recuentos. Modela el *logaritmo* del recuento esperado como una función lineal de los predictores, lo que mantiene los recuentos predichos como positivos.

## Los ejemplos de Mia y Theo

- Mia registra si cada paciente tuvo un evento coronario antes de los 60 años (sí/no): la regresión logística relaciona los odds de un evento con el estado de portador (si el paciente lleva la variante genética) y la edad.
- Theo cuenta cuántas visitas a la clínica hizo cada paciente en un año: la regresión de Poisson relaciona el número esperado de visitas con el grupo de tratamiento y la edad.

## La idea clave

No necesitas un modelo mental distinto para «una regresión para proporciones», «una regresión para recuentos» y «una regresión para números simples»: en todos los casos es la misma idea de coeficientes y predictores, solo que con una función de enlace diferente, elegida según el tipo de resultado que tengas.

> **Para saber más**
>
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, Ch. 13 "Logistic regression", §13.1–13.2 (pp. 217–222), y §15.2 "Poisson and negative binomial regression" (pp. 264–270).
> - [James, Witten, Hastie & Tibshirani (2021)](https://www.statlearning.com/), *An Introduction to Statistical Learning* (2nd ed.), §4.6 "Generalized Linear Models", pp. 164–171.

---
**Anterior:** [Pruebas como regresiones](./tests-as-regressions.md) · [Inicio del módulo](./README.md) · **Módulo siguiente:** [Predicción vs. causalidad →](../05-prediction-vs-causation/README.md) · [Glosario](../glossary.md)
