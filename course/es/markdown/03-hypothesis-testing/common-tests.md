# Pruebas habituales: un recorrido rápido

**En pocas palabras:** la mayoría de las pruebas estadísticas "con nombre" preguntan "¿son estos números distintos de aquellos (o de un valor de referencia) de alguna manera concreta?". La tabla siguiente reúne las más habituales.

| Prueba | Úsala para preguntar... | Ejemplo |
|---|---|---|
| Prueba t de una muestra | ¿Es la media de este grupo distinta de un valor de referencia fijo? | ¿Es el colesterol LDL medio de esta clínica distinto de la media conocida de la población? |
| Prueba t de dos muestras | ¿Tienen dos grupos independientes medias distintas? | Portadores frente a no portadores de una variante génica, colesterol LDL medio. |
| Prueba t pareada | ¿Cambiaron, en promedio, las mismas unidades entre dos mediciones? | La presión arterial de cada paciente antes y después del tratamiento. |
| ANOVA de un factor | ¿Difieren las medias de tres o más grupos independientes? | Colesterol LDL en tres clases de genotipo (no portador, heterocigoto, homocigoto). |
| Prueba de chi-cuadrado | ¿Están asociadas dos variables categóricas? | ¿Está asociada la "presencia de enfermedad" con el "grupo de tratamiento"? |
| Correlación (r de Pearson) | ¿Hay una relación lineal entre dos variables continuas? | Edad frente a colesterol LDL. |

## Variantes

- **Prueba t de Welch** frente a **prueba t de Student**: la de Welch no supone que los dos grupos tengan la misma variabilidad (dispersión), mientras que la de Student sí. La de Welch es la opción por defecto más segura: apenas cuesta nada cuando las varianzas *son* iguales y te protege cuando no lo son.
- **Alternativas no paramétricas** (U de Mann-Whitney, Wilcoxon, Kruskal-Wallis): se usan cuando los datos no se parecen a una campana o tienen valores atípicos graves. Un error muy extendido: se suele pensar que comparan *medianas*; en general comparan si un grupo tiende a producir *valores mayores* que el otro (lo que se llama **dominancia estocástica**), y esto equivale a comparar medianas solo cuando las distribuciones de los dos grupos tienen una forma parecida.

## Pruebas y regresión

Toda prueba de esta tabla puede reescribirse como una **regresión**: la misma pregunta de fondo, formulada como "ajusta una recta o un modelo y mira un coeficiente" en lugar de como una receta con nombre. La versión de regresión suele ser más fácil de ampliar (añadir más variables, manejar una variabilidad desigual, etc.). Véanse [Qué es la regresión](../04-regression-basics/what-is-regression.md) y [Pruebas como regresiones](../04-regression-basics/tests-as-regressions.md).

## Cómo elegir

En lugar de memorizar esta tabla, pregúntate: *¿qué tipo de variable de respuesta tengo (un número continuo, una categoría, un recuento)?* y *¿cuántos grupos estoy comparando?* Eso lo reduce enseguida a una o dos filas.

> **Hazlo tú mismo**
>
> [Cómo: ejecutar una prueba habitual](./how-to/run-a-common-test.md) — cada prueba de la tabla en Python, presentada como una estimación con un intervalo de confianza.

> **Para saber más**
>
> - [Lindeløv (2019)](https://lindeloev.github.io/tests-as-linear/), "Common statistical tests are linear models" (free online) — una hoja de referencia y código en R resuelto para cada prueba de la tabla.
> - Delacre, Lakens & Leys (2017), "Why psychologists should by default use Welch's t-test instead of Student's t-test," *International Review of Social Psychology* 30(1), 92–101.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §7.3 "Formulating comparisons as regression models", pp. 99–101.

---
**Anterior:** [Valores p y significación](./p-values-and-significance.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Comprobar los supuestos →](./checking-assumptions.md) · [Glosario](../glossary.md)
