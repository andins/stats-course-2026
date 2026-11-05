# Tamaño del efecto

**En pocas palabras:** el tamaño del efecto responde a «cuánto de grande», a diferencia del valor p (*p-value*), que solo responde a «cuánta seguridad hay».

## Por qué «¿hay diferencia?» no es la pregunta útil

Con datos suficientes, casi *cualquier* diferencia del mundo real se vuelve «estadísticamente significativa», incluso una trivialmente pequeña. Si el nuevo fármaco antihipertensivo de Theo reduce la presión arterial una media de 0.1 mmHg, un ensayo lo bastante grande lo declarará «significativo», aunque sea médicamente irrelevante. El tamaño del efecto es lo que te dice si un resultado es significativo *y* además lo bastante grande como para importar.

## Algunas medidas habituales del tamaño del efecto

- **Diferencia de medias** (en las unidades naturales de la variable de respuesta, p. ej. «redujo la presión arterial en 8 mmHg») — la más interpretable cuando las unidades significan algo para tu audiencia.
- **Diferencia estandarizada (d de Cohen)** — la diferencia de medias dividida entre la dispersión de los datos (desviación típica). Es útil para comparar tamaños del efecto entre estudios que midieron las cosas de forma distinta, o cuando las unidades originales de la variable de respuesta no son intuitivas. Por convención, d≈0.2 es «pequeño», d≈0.5 es «mediano» y d≈0.8 es «grande», pero tómalo como una convención aproximada, no como una ley de la naturaleza: lo que cuenta como un efecto relevante depende de la materia.
- **Correlación (r)** — intensidad de una relación lineal entre dos variables continuas, de -1 a 1.
- **Razón de odds / razón de riesgos** — para resultados de tipo sí/no (p. ej. «los pacientes tratados tuvieron el doble de probabilidades de recuperarse»).

## Dónde aparece el tamaño del efecto

- **Antes de recoger datos**: necesitas una *estimación aproximada* del tamaño del efecto para planificar el tamaño muestral (véase [Tamaño muestral y potencia](./sample-size-and-power.md)).
- **Después de recoger datos**: informa del tamaño del efecto (con un intervalo de confianza) junto a un valor p a secas, o en lugar de él. «Los portadores tenían un colesterol LDL un 6% más alto (IC del 95%: 1–11%)» dice mucho más que «p = 0.03».
- **Combinar estudios**: los tamaños del efecto (y sus errores estándar) son lo que agrupa un [metaanálisis](../07-special-data-structures/meta-analysis.md), y por eso todos los estudios deben informar en la misma escala.

## Error habitual

Tratar un resultado «significativo» como importante automáticamente, o un resultado «no significativo» como si significara automáticamente «no hay efecto». Un estudio pequeño puede dar fácilmente un resultado no significativo incluso para un efecto real y relevante: eso es un problema de potencia, no una prueba de que «no hay efecto». Pregunta siempre por el tamaño del efecto y por la incertidumbre que lo rodea, no solo por el valor p.

> **Hazlo tú mismo**
>
> [Cómo: planificar un tamaño muestral](./how-to/plan-a-sample-size.md) — convierte una diferencia bruta y una desviación típica en una d de Cohen y en un tamaño muestral.

> **Para saber más**
>
> - [Lakens (2022)](https://lakens.github.io/statistical_inferences/), *Improving Your Statistical Inferences*, Ch. 6 "Effect Sizes" — cómo calcular, interpretar y comunicar los tamaños del efecto más comunes.
> - Sullivan & Feinn (2012), "Using effect size — or why the P value is not enough," *Journal of Graduate Medical Education* 4(3), 279–282 — una introducción breve y legible.
> - Cohen (1988), *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.), Ch. 2 "The t Test for Means" — origen de las convenciones pequeño/mediano/grande para d; tómalas como convenciones, no como leyes.

---
**Anterior:** [Tamaño muestral y potencia](./sample-size-and-power.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Otras consideraciones de la fase de diseño →](./design-considerations.md) · [Glosario](../glossary.md)
