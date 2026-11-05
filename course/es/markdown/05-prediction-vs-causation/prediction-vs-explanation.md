# Predicción vs. explicación

**En pocas palabras:** un modelo predictivo responde a «¿qué es probable que ocurra?». Un modelo explicativo o causal responde a «¿qué ocurriría *si cambiara algo*?». Se juzgan con criterios completamente distintos.

## Un ejemplo: correlación sin causalidad

Las ventas de helados y las muertes por ahogamiento están muy correlacionadas a lo largo del año: ambas suben en verano. Un modelo que usara las ventas de helados para *predecir* las tasas de ahogamiento funcionaría razonablemente bien. Prohibir los helados no evitaría ni un solo ahogamiento: la causa de fondo (el calor, más gente nadando) afecta a ambas cosas. Las ventas de helados son un buen **predictor** del riesgo de ahogamiento, pero no una variable que, si se modificara, cambiaría ese riesgo.

## Los ejemplos de Mia y Theo

- **Predicción**: Mia quiere un modelo que prediga el riesgo de enfermedad coronaria precoz de un paciente a partir de características clínicas y genéticas (edad, colesterol, antecedentes familiares, genotipos de las variantes); no necesita saber *por qué* estas características predicen el riesgo, solo que lo hacen, de forma fiable, en pacientes nuevos.
- **Causalidad**: Theo quiere saber si *administrar* el fármaco *causa* un descenso de la presión arterial; le importa específicamente si intervenir (recetarlo) cambiaría el resultado, y no solo si quienes toman el fármaco tienen, por algún otro motivo, la presión arterial más baja.

## Por qué no siempre se puede saber qué responde un modelo con solo mirarlo

La misma ecuación de regresión puede ajustarse de ambas maneras: las matemáticas no conocen tu intención. Lo que cambia es:

- **Cómo juzgas el éxito.** Un modelo predictivo se juzga por lo bien que predice datos *nuevos* que no ha visto (consulta [Validación cruzada y revisión del modelo](../06-building-models/cross-validation-and-model-checking.md)); cualquier predictor que ayude vale, incluidas las ventas de helados. Un modelo causal se juzga por si aísla correctamente el efecto de *intervenir* sobre una variable, lo que exige mucho más cuidado con *qué* otras variables incluyes (consulta [Diagramas causales](./causal-diagrams.md)); meter «todos los predictores disponibles» puede perjudicarlo de verdad.
- **Lo que necesitas antes de fiarte de la respuesta.** Una afirmación causal necesita una **estrategia de identificación** (*identification strategy*): alguna razón para creer que has tenido en cuenta (o descartado) las demás explicaciones de la asociación. Consulta [Experimentos vs. datos observacionales](./experiments-vs-observational-data.md).

## Una pregunta que distingue ambos casos

Pregúntate: *¿necesito que la respuesta de este modelo siga valiendo si cambio la entrada, o solo necesito que genere previsiones fiables sobre datos que aún no he visto?* Lo primero es causal; lo segundo es predictivo. Decídelo antes de construir nada.

> **Para saber más**
>
> - Shmueli (2010), "To explain or to predict?," *Statistical Science* 25(3), 289–310 — por qué los dos objetivos exigen decisiones de modelización distintas.
> - Hernán, Hsu & Healy (2019), "A second chance to get causal inference right: a classification of data science tasks," *CHANCE* 32(1), 42–49 — descripción vs. predicción vs. inferencia causal.
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §6.3 "Interpret coefficients as comparisons, not effects", pp. 84–85.

---
**Anterior:** [Inicio del módulo](./README.md) · **Siguiente:** [Experimentos vs. datos observacionales →](./experiments-vs-observational-data.md) · [Glosario](../glossary.md)
