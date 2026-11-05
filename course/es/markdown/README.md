# Curso de estadística para científicos de la vida

Un curso práctico de estadística para estudiantes de máster en ciencias de la vida.

Cada tema es una página breve y autocontenida. No hace falta que sigas el orden de la barra lateral. De hecho, probablemente la mejor manera de moverte por el curso sea ir directamente a la [Guía rápida del flujo de trabajo](./workflow-cheatsheet.md) y, siguiendo el árbol de decisión, elegir los temas que más te interesen. También puedes buscar cualquier tema en el buscador y seguir los enlaces para descubrir temas relacionados. Y si hay algún término que no reconoces, tienes el [Glosario](./glossary.md).
Sigue además las instrucciones de [Prepara tu ordenador](./setup-environment.md) para dejar todo instalado y listo para el curso. Y si quieres crear una carpeta de proyecto para tus análisis, consulta [Organiza tu proyecto](./project-structure.md). El curso incluye un asistente de IA especializado que te ayuda con los análisis. Si quieres usarlo, consulta [Trabaja con un agente de IA](./use-an-agent.md).

A lo largo del curso seguiremos dos ejemplos recurrentes:
- **Mia**, una estudiante de genética clínica que investiga si una variante de un gen del colesterol (LDLR) está asociada al colesterol LDL.
- **Theo**, que está comprobando si un nuevo fármaco reduce la presión arterial.

Sus historias se van concretando a medida que avanzan los módulos, de modo que los mismos conceptos reaparecen en un contexto familiar.

> **Sugerencia** Consulta la [Guía rápida del flujo de trabajo](./workflow-cheatsheet.md), una vista en una página del árbol de decisión de todo el proceso, antes de sumergirte en cada módulo.

## Aplica lo que aprendes

Las páginas de temas explican el *porqué*. Cuando hay una receta práctica, la página termina con un cuadro **Hazlo tú mismo** que enlaza con una guía breve (pasos, código Python para copiar y pegar, cómo leer los resultados y qué hacer si algo sale mal) y, a veces, con un cuaderno (*notebook*) para explorar la idea en la práctica. Las guías contienen los procedimientos que debes seguir, mientras que los cuadernos los muestran en acción con datos de ejemplo. Conviene que sigas la guía y el cuaderno a la vez, porque se complementan (y, por supuesto, que vuelvas a las páginas de temas para repasar los conceptos). Las guías prácticas también aparecen en la página de inicio de cada módulo. Actualmente cubren:

- [Planificar un tamaño muestral](./01-planning-your-study/how-to/plan-a-sample-size.md)
- [Explorar un conjunto de datos](./02-exploring-data/how-to/explore-a-dataset.md)
- [Ejecutar una prueba habitual](./03-hypothesis-testing/how-to/run-a-common-test.md) y [comprobar sus supuestos](./03-hypothesis-testing/how-to/check-test-assumptions.md)
- [Ejecutar una prueba como regresión](./04-regression-basics/how-to/run-a-test-as-a-regression.md)
- [Dibujar y usar un diagrama causal](./05-prediction-vs-causation/how-to/draw-and-use-a-causal-diagram.md)
- [Validar un modelo predictivo](./06-building-models/how-to/validate-a-predictive-model.md), [comprobar la multicolinealidad](./06-building-models/how-to/check-multicollinearity.md) y [corregir el error de medición](./06-building-models/how-to/handle-measurement-error.md)
- [Analizar datos agrupados](./07-special-data-structures/how-to/analyze-clustered-data.md) y [realizar un metaanálisis](./07-special-data-structures/how-to/run-a-meta-analysis.md)

El código está en Python (`pandas`, `statsmodels`, `scikit-learn`, `matplotlib`). ¿Es la primera vez que lo ejecutas? [Prepara tu ordenador](./setup-environment.md) te guía paso a paso para instalarlo todo en Windows, macOS o Linux, y [Organiza tu proyecto](./project-structure.md) propone cómo estructurar un análisis. Para usar un asistente de IA (y la skill statistics-advisor) con el curso, consulta [Trabaja con un agente de IA](./use-an-agent.md). Los cuadernos están en [notebooks/](./notebooks/); descarga uno y ábrelo en Jupyter, VS Code o Google Colab.
