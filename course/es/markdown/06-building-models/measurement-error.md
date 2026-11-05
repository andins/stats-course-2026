# Error de medición

**En pocas palabras:** si lo que registraste no es exactamente lo que querías medir (un sustituto ruidoso en lugar de la cantidad verdadera), el modelo no solo se vuelve más ruidoso: se vuelve sesgado, normalmente hacia el "ningún efecto".

## Una imagen concreta

Theo mide la tensión arterial con un tensiómetro doméstico preciso solo hasta ±5 mmHg, en lugar de un aparato de calidad clínica. Cada lectura es la tensión arterial real más un error aleatorio. Si Theo hace una regresión de una variable de respuesta sobre estas lecturas ruidosas, la pendiente estimada resulta sistemáticamente menor que la relación real, incluso con una muestra enorme, simplemente porque el predictor es una versión borrosa de lo que de verdad importa.

## Por qué no es "solo ruido"

- El error aleatorio en la **variable de respuesta** infla sobre todo la varianza residual y ensancha el intervalo de confianza; no sesga la pendiente en promedio.
- El error aleatorio en un **predictor** es distinto: sesga la pendiente estimada hacia cero, un patrón llamado **sesgo de atenuación** (*attenuation bias*, o *regression dilution*, dilución de la regresión). Es un sesgo, no un problema de varianza: **no** disminuye al crecer el tamaño muestral.
- En la práctica, esto puede parecer "no se encontró ninguna relación" cuando existe una relación real que quedó diluida por una medición imprecisa.

## Fuentes habituales

- Cantidades autodeclaradas (recuerdo de la dieta, ejercicio o adherencia autodeclarados, cuestionarios).
- Ensayos de laboratorio o sensores con una variabilidad de medición conocida.
- Un sustituto (*proxy*) que representa el constructo que de verdad te interesa (p. ej., el IMC como sustituto de la grasa corporal).

## Qué hacer al respecto

- Nómbralo explícitamente cuando una variable sea un sustituto impreciso conocido, en lugar de tratar el valor observado como si fuera exacto.
- Si tienes una idea del tamaño del error (a partir de la precisión documentada del instrumento o de mediciones repetidas sobre la misma unidad), un **modelo de error de medición / de errores en las variables** (*errors-in-variables*), como la calibración de la regresión, SIMEX o un modelo bayesiano con un "valor verdadero" latente explícito, puede corregir el sesgo; los mínimos cuadrados ordinarios (OLS) sobre el valor observado no pueden (FULLER_MEASUREMENT_ERROR).
- Si existen mediciones replicadas, úsalas para estimar la varianza del error en lugar de suponerla.
- Más datos por sí solos no lo arreglan: el sesgo de atenuación persiste con cualquier tamaño muestral, así que no lo trates como un problema de potencia.

## La conclusión

Un coeficiente es tan bueno como la variable que entró en él. Si un predictor (o una variable de respuesta) es un sustituto ruidoso conocido de lo que de verdad te interesa, dilo, y plantéate un modelo que tenga en cuenta el error de medición en lugar de presentar como respuesta final la estimación ingenua, probablemente atenuada.

> **Hazlo tú mismo**
>
> - [Cómo: corregir el error de medición](./how-to/handle-measurement-error.md) — estima la fiabilidad a partir de réplicas y corrige la pendiente.
> - [Cuaderno: observa cómo se encoge la pendiente](../notebooks/measurement-error-attenuation.ipynb) — simula el sesgo y comprueba que tener más datos no lo elimina.

> **Para saber más**
>
> - [Hernán & Robins (2020)](https://miguelhernan.org/whatifbook), *Causal Inference: What If* (de acceso libre en línea), §9.1–9.2 "Measurement error" y "The structure of measurement error", pp. 125–128.
> - Fuller (1987), *Measurement Error Models*, cap. 1 "A Single Explanatory Variable" — el tratamiento clásico del sesgo de atenuación y de sus correcciones.
> - McElreath (2020), *Statistical Rethinking* (2.ª ed.), cap. 15, §15.1 "Measurement error" — un modelo bayesiano que tiene en cuenta el error de medición.

---
**Anterior:** [Multicolinealidad](./multicollinearity.md) · **Inicio del módulo:** [Construir modelos](./README.md) · **Módulo siguiente:** [Estructuras de datos especiales →](../07-special-data-structures/README.md) · [Glosario](../glossary.md)
