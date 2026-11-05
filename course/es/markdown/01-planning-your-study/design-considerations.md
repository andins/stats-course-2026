# Otras consideraciones de la fase de diseño

**En pocas palabras:** el tamaño muestral no es la única decisión que hay que tomar antes de empezar a recoger datos. Hay otras dos igual de importantes, y ninguna se puede arreglar después: con qué precisión mides tus variables y qué variables te molestas en registrar.

## Reduce el ruido de medición desde el principio, con mejores instrumentos

Una medición ruidosa no solo añade variación aleatoria que se pueda promediar: si está en un predictor, sesga el efecto estimado hacia cero (**sesgo por atenuación**, véase [Error de medición](../06-building-models/measurement-error.md)), y ese sesgo no disminuye con una muestra mayor. El momento más barato para ocuparse de esto es la fase de diseño, antes de empezar a recoger datos:

- Prefiere el instrumento o protocolo más preciso que te puedas permitir (un dispositivo calibrado antes que un autoinforme, un ensayo estandarizado antes que uno improvisado) en lugar de aceptar el ruido e intentar compensarlo recogiendo más datos.
- Si un instrumento más preciso no es viable, planifica **mediciones repetidas** al menos en una submuestra: permiten estimar más adelante el tamaño del error de medición y corregirlo, en lugar de tener que adivinarlo.
- Si Theo sabe que su tensiómetro doméstico es ruidoso, cambiarlo por un dispositivo de uso clínico (o tomar tres lecturas por visita y promediarlas) resuelve el problema mucho mejor que limitarse a incluir más pacientes.

## Asegúrate de que el diseño recoge lo que necesitará una pregunta causal

Si el objetivo final es interpretar un efecto de forma causal (y no solo describir una asociación), el plan de diseño y de recogida de datos tiene que anticiparlo antes de recoger los datos, no después:

- Piensa de antemano qué más puede afectar tanto a la exposición como a la variable de respuesta (**variables de confusión** — véase [Diagramas causales](../05-prediction-vs-causation/causal-diagrams.md)) y asegúrate de que esas variables se registran de verdad. Una variable de confusión que nunca se midió no se puede ajustar después, por bueno que sea el modelo.
- Esto importa menos en un experimento aleatorizado bien diseñado, donde la asignación al azar se ocupa de la confusión por diseño (véase [Experimentos vs. datos observacionales](../05-prediction-vs-causation/experiments-vs-observational-data.md)), pero aun así conviene registrar covariables **previas al tratamiento** plausibles, que mejoran la precisión incluso en ese caso.
- En un diseño observacional esto no es opcional: una lista de variables incompleta en la fase de diseño limita lo que cualquier análisis causal posterior puede afirmar con credibilidad, sea cual sea el tamaño muestral o la sofisticación del modelo.

## La idea clave

El tamaño muestral responde a «cuántos datos». La elección del instrumento y la lista de variables responden a «hasta qué punto son fiables esos datos» y a «¿puedo siquiera plantear con ellos la pregunta que quiero plantear?». Acierta con ambas cosas antes de recoger un solo dato, porque ningún análisis posterior, por bueno que sea, puede arreglarlas.

> **Para saber más**
>
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §2.2 "Validity and reliability", pp. 23–25 — qué hace fiable una medición antes de analizarla.
> - [Hernán & Robins (2020)](https://miguelhernan.org/whatifbook), *Causal Inference: What If* (gratuito en línea), §3.6 "The target trial" (p. 41 en adelante) y §7.6 "Confounding adjustment" (pp. 102–108) — decidir de antemano qué exige medir una pregunta causal.

---
**Anterior:** [Tamaño del efecto](./effect-size.md) · [Inicio del módulo](./README.md) · **Módulo siguiente:** [Explorar tus datos →](../02-exploring-data/README.md) · [Glosario](../glossary.md)
