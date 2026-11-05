# Metaanálisis: sesgos y trampas

**En pocas palabras:** combinar estudios hace que una respuesta parezca más sólida que la de cualquier estudio individual, pero no puede arreglar lo que falla en los estudios en sí ni en la forma en que se reunieron. Casi todo lo que puede salir mal ocurre antes de cualquier estadística.

## 1. Basura entra, basura sale

Un metaanálisis hereda las debilidades de sus estudios. Si los ensayos tenían una evaluación del desenlace sin enmascaramiento, o los estudios eran observacionales con [confusión](../05-prediction-vs-causation/causal-diagrams.md) sin controlar, combinarlos da una versión más *precisa* del mismo sesgo, con un intervalo más estrecho y por tanto más engañoso. No mezcles experimentos aleatorizados y estudios observacionales en una sola cifra sin un buen motivo; si lo haces, muéstralos también por separado. Véase [Experimentos vs. datos observacionales](../05-prediction-vs-causation/experiments-vs-observational-data.md).

## 2. Cómo se encontraron los estudios

Theo quiere resumir los ensayos de un fármaco contra la hipertensión. Si incluye los que casualmente conoce, o deja de buscar cuando la respuesta le parece correcta, el resultado refleja sus decisiones y no la evidencia: es de nuevo el [jardín de los senderos que se bifurcan](../02-exploring-data/exploratory-vs-confirmatory.md), pero a nivel de la revisión. El remedio es de procedimiento: decide la pregunta, las bases de datos, los términos de búsqueda y los criterios de inclusión **antes** de mirar los resultados, déjalos por escrito (un protocolo) e indica cuántos estudios se encontraron, se cribaron y se excluyeron, y por qué. La declaración PRISMA 2020 es una lista de comprobación pensada justo para esto.

## 3. Sesgo de publicación y efectos de los estudios pequeños

Los estudios con resultados llamativos tienen más probabilidad de redactarse y publicarse que los que no encontraron nada, de modo que la literatura publicada sobrestima los efectos (el mismo mecanismo que los [errores de tipo M](../01-planning-your-study/sample-size-and-power.md)). Dos comprobaciones habituales:

- **Gráfico de embudo** (*funnel plot*): el efecto de cada estudio frente a su precisión. Sin sesgo parece un embudo invertido simétrico; una esquina vacía (estudios pequeños con resultados nulos o negativos) sugiere que faltan algunos estudios.
- **Regresión de Egger:** una prueba estadística de esa asimetría.

Ambas son débiles. Con menos de unos 10 estudios tienen poca potencia, y la asimetría puede deberse también a otras causas (los estudios pequeños a menudo se llevan a cabo de manera distinta a los grandes, o con poblaciones distintas). Úsalas como una luz de aviso, no como prueba en ningún sentido, y di que la estimación combinada puede ser demasiado optimista. Buscar estudios no publicados (registros, preprints, contactar con los autores) es mejor que cualquier corrección estadística.

![Dos gráficos de embudo de estimaciones del efecto frente al error estándar. Izquierda: los estudios se dispersan simétricamente alrededor del efecto combinado. Derecha: el mismo tipo de datos con los estudios pequeños nulos o negativos ausentes, lo que deja una esquina sombreada vacía en un lado y una estimación combinada desplazada hacia arriba.](../figures/funnel_plots.png)

*Gráficos de embudo con estudios simulados. Sin sesgo el embudo es simétrico; cuando los estudios pequeños con resultados decepcionantes no se publican, una esquina queda vacía.*

## 4. Comparar peras con manzanas

Si los estudios difieren en dosis, especie, población o definición del desenlace, «el efecto promedio» puede no describir nada real. Eso es lo que mide la heterogeneidad, y por eso el intervalo de predicción importa más que la media combinada. Una **metarregresión** o una comparación por subgrupos puede explorar *por qué* difieren los estudios (por ejemplo, según la dosis), pero trátala como exploratoria: las características de los estudios no están aleatorizadas, están enredadas entre sí y, con pocos estudios, hay poca potencia. Además, una relación entre estudios (mayor dosis media, mayor efecto medio) puede no cumplirse dentro de ningún estudio concreto.

## 5. Los estudios no siempre son independientes

Un metaanálisis asume que cada estimación aporta información distinta. Esto falla cuando:

- un estudio aporta varias estimaciones (dos dosis frente a un mismo control, varios desenlaces), o
- varios estudios proceden del mismo laboratorio, grupo o conjunto de datos.

Contar esos resultados como independientes estrecha demasiado el intervalo, exactamente igual que con los [datos agrupados](./clustered-and-hierarchical-data.md). Elige una estimación por estudio o modela la dependencia.

## 6. No cuentes votos

«Siete de diez estudios fueron significativos, así que funciona» ignora tanto el tamaño de los efectos como la potencia de cada estudio. Combina las estimaciones, no los veredictos.

## 7. Pocos estudios

Con dos o tres estudios, τ² no puede estimarse de forma fiable, y una estimación combinada puede confundir más de lo que aclara. Indica cuán pocos estudios tienes, usa el intervalo de Hartung-Knapp o un [modelo bayesiano](./bayesian-methods.md) con una distribución a priori sensata para la dispersión entre estudios, y plantéate simplemente mostrar los estudios uno al lado del otro.

## 8. Mismos datos, otro problema

Si dispones de los datos en bruto de cada centro (cada paciente, cada familia), no necesitas un metaanálisis: analízalos como [datos agrupados](./clustered-and-hierarchical-data.md) con el centro como grupo. Es más flexible, porque puedes ajustar a nivel individual. Un metaanálisis es para cuando solo tienes el resumen de cada estudio.

## Una breve lista de comprobación

1. La pregunta y los criterios de inclusión se escribieron antes de mirar los resultados.
2. La búsqueda fue sistemática y se indica el número de estudios encontrados y excluidos.
3. Los efectos están en una escala común y el error estándar de cada estudio es correcto.
4. Efectos aleatorios, con τ, I² y un intervalo de predicción presentados.
5. Se examinaron un diagrama de bosque, una comprobación dejando uno fuera (*leave-one-out*) y un gráfico de embudo.
6. La calidad de los estudios y el sesgo de publicación se discuten como límites del resultado.

> **Para saber más**
>
> - Page et al. (2021), "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews," *BMJ* 372, n71.
> - Sterne et al. (2011), "Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials," *BMJ* 343, d4002 — incluye por qué evitar las pruebas con menos de 10 estudios.
> - Egger, Smith, Schneider & Minder (1997), "Bias in meta-analysis detected by a simple, graphical test," *BMJ* 315(7109), 629–634.
> - [Cochrane Handbook for Systematic Reviews of Interventions](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current) (versión 6.5, gratuito en línea), Ch. 13 "Assessing risk of bias due to missing evidence in a meta-analysis".
> - IntHout, Ioannidis & Borm (2014), "The Hartung-Knapp-Sidik-Jonkman method for random effects meta-analysis is straightforward and considerably outperforms the standard DerSimonian-Laird method," *BMC Medical Research Methodology* 14, 25.

---
**Anterior:** [Metaanálisis](./meta-analysis.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Métodos bayesianos →](./bayesian-methods.md) · [Inicio](../README.md) · [Glosario](../glossary.md)
