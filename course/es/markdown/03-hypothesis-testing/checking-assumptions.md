# Comprobar los supuestos

**En pocas palabras:** toda prueba clásica viene con condiciones en letra pequeña. La mayoría se comprueban mejor mirando un gráfico que ejecutando una segunda prueba.

## Supuestos habituales

- **Independencia**: cada observación no debería aportar información sobre otra (dos mediciones del mismo paciente *no* son independientes entre sí). Suele ser una cuestión de cómo se recogieron los datos, no algo que un gráfico pueda arreglar a posteriori; consulta [Datos agrupados y jerárquicos](../07-special-data-structures/clustered-and-hierarchical-data.md) y [Series temporales](../07-special-data-structures/time-series-data.md) si sospechas que no se cumple.
- **Normalidad**: muchas pruebas suponen que los datos (o los errores del modelo) tienen forma aproximada de campana. Compruébalo con un histograma o con un "gráfico QQ" (un gráfico que es una diagonal recta si los datos son normales y se curva alejándose de ella si no lo son).
- **Variabilidad igual entre grupos** (homogeneidad de la varianza): se comprueba comparando la dispersión visualmente (diagramas de cajas) o con la prueba de Levene.

## Por qué un gráfico suele ser mejor que una "prueba del supuesto"

Es tentador ejecutar una prueba formal (como Shapiro-Wilk para la normalidad) y tratar su valor p como un veredicto de sí o no sobre si "te está permitido" usar una prueba determinada. Esto no funciona bien en ninguno de los dos sentidos:
- Con una muestra **pequeña**, estas pruebas de supuestos tienen muy poca potencia para detectar una desviación real, así que "la ha superado" no significa gran cosa.
- Con una muestra **grande**, se vuelven hipersensibles y marcarán como "significativas" incluso desviaciones triviales e inofensivas.

Echar un vistazo rápido al gráfico, junto con preguntarte "¿cambiaría esta desviación mi conclusión?", suele ser más informativo que un único valor p sobre un supuesto.

## Qué hacer si un supuesto parece dudoso

Rara vez te quedas atascado: casi siempre hay una alternativa estándar y bien conocida:

- Varianzas desiguales → usa la prueba t de Welch (o el ANOVA de Welch) en lugar de la versión estándar.
- Lejos de la normalidad o con valores atípicos → usa una prueba no paramétrica (Mann-Whitney, Kruskal-Wallis), un enfoque de media recortada o *bootstrap*, o una alternativa bayesiana.
- Recuentos esperados pequeños en una tabla de chi-cuadrado → usa en su lugar la prueba exacta de Fisher.

La respuesta correcta a "un supuesto parece incumplido" es casi siempre "cambiar a la alternativa conocida y más robusta", no "entrar en pánico" ni "ignorarlo y esperar que todo vaya bien".

> **Hazlo tú mismo**
>
> [Cómo: comprobar los supuestos de una prueba](./how-to/check-test-assumptions.md) — los gráficos que hay que hacer, qué aspecto deberían tener y qué hacer cuando no lo tienen.

> **Para saber más**
>
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §11.1–11.3 "Assumptions of regression analysis" hasta "Residual plots", pp. 153–163 — qué supuestos importan más y cómo comprobarlos gráficamente.
> - Rochon, Gondan & Kieser (2012), "To test or not to test: preliminary assessment of normality when comparing two independent samples," *BMC Medical Research Methodology* 12, 81 — por qué contrastar los supuestos de antemano es una mala opción por defecto.
> - Delacre, Lakens & Leys (2017), *International Review of Social Psychology* 30(1), 92–101 — el argumento a favor de la prueba de Welch como opción robusta por defecto.

---
**Anterior:** [Pruebas habituales](./common-tests.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Comparaciones múltiples →](./multiple-comparisons.md) · [Glosario](../glossary.md)
