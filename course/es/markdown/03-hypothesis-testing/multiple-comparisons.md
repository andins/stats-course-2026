# Comparaciones múltiples

**En pocas palabras:** cuantas más pruebas ejecutes, más probable es que *al menos una* parezca "significativa" por puro azar, aunque no esté pasando nada real en ningún sitio.

## Una ilustración sencilla

Si lanzas 20 monedas justas y te preguntas "¿alguna de ellas está trucada?", contrastando cada una por separado con el umbral de significación habitual del 5%, esperarías en promedio aproximadamente un resultado "significativo", puramente por azar, aunque todas las monedas sean perfectamente justas. Si ejecutas suficientes pruebas sobre suficientes variables, *encontrarás* resultados "significativos" en puro ruido.

## Dónde aparece en la práctica

- Comparar muchos pares de grupos después de un ANOVA (p. ej., todos los pares posibles entre 5 grupos de genotipo).
- Contrastar muchos genes, muchos biomarcadores o muchas medidas de resultado frente a la misma variable de agrupación.
- Cualquier rastreo exploratorio a través de muchas variables (véase [Exploratorio vs. confirmatorio](../02-exploring-data/exploratory-vs-confirmatory.md); es el mismo problema de fondo).

## La solución clásica: las correcciones

Métodos como la corrección de Bonferroni o la de Holm hacen más estricto el umbral de cada prueba individual, en proporción al número de pruebas que ejecutas, de modo que la probabilidad *global* de algún falso positivo se mantiene controlada. Esto funciona, pero aplica la misma corrección sin atender a la estructura; por ejemplo, trata igual 20 genes no relacionados y 20 mediciones repetidas relacionadas.

## Una alternativa más moderna: el agrupamiento parcial (*partial pooling*)

Cuando comparas muchos grupos relacionados (p. ej., el colesterol LDL en 30 familias distintas, o un biomarcador en 50 pacientes), un **modelo multinivel** (véase [Datos agrupados y jerárquicos](../07-special-data-structures/clustered-and-hierarchical-data.md)) suele manejar el problema de las "comparaciones múltiples" con más elegancia que una corrección general: acerca de forma natural las estimaciones individuales ruidosas y de aspecto extremo hacia la media global, lo cual es conceptualmente parecido a lo que intenta lograr una corrección, pero tiende a producir estimaciones mejor calibradas y más útiles para cada grupo, en lugar de limitarse a un umbral más estricto.

## La conclusión

Si ejecutas —o ves— muchas pruebas a la vez, pregunta cómo se abordó el problema de las "comparaciones múltiples", igual que preguntarías por cualquier otro supuesto. "Ejecutamos 40 pruebas y 2 fueron significativas con p<0.05" se parece mucho a lo que cabría esperar solo por azar, y por sí solo no es evidencia de nada.

> **Para saber más**
>
> - Benjamini & Hochberg (1995), "Controlling the false discovery rate," *Journal of the Royal Statistical Society B* 57(1), 289–300 — el artículo que está detrás del control de la FDR (tasa de falsos descubrimientos).
> - Gelman, Hill & Yajima (2012), "Why we (usually) don't have to worry about multiple comparisons," *Journal of Research on Educational Effectiveness* 5(2), 189–211 — la alternativa del agrupamiento parcial.
> - Wasserman (2004), *All of Statistics*, Ch. 10 "Hypothesis Testing and p-values" (multiple-testing section) — un tratamiento compacto y riguroso de Bonferroni y la FDR.

---
**Anterior:** [Comprobar los supuestos](./checking-assumptions.md) · [Inicio del módulo](./README.md) · **Módulo siguiente:** [4. Fundamentos de regresión →](../04-regression-basics/README.md) · [Glosario](../glossary.md)
