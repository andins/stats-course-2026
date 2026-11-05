# Tamaño muestral y potencia

**En pocas palabras:** la potencia es la probabilidad de que tu estudio detecte un efecto real, *si de verdad existe*. Planificar el tamaño muestral es trabajar hacia atrás, desde «con cuánta seguridad quiero estar» hasta «cuántos sujetos necesito».

## El ejemplo de Mia

Mia cree que portar su variante de LDLR aumenta el colesterol LDL en torno a un 10%, a partir de una pequeña serie clínica previa (6 portadores y 6 no portadores). Antes de poner en marcha el estudio de cohortes completo, necesita saber: ¿cuántos pacientes necesita por grupo para detectar de forma fiable una diferencia del 10%, si es real?

## Los cuatro ingredientes de un cálculo de potencia

Todo cálculo de tamaño muestral necesita cuatro números, y fijando tres de ellos queda determinado el cuarto:

1. **Tamaño del efecto** — qué diferencia tan grande intentas detectar (véase [Tamaño del efecto](./effect-size.md)). Suele ser el más difícil de concretar.
2. **Alfa (nivel de significación)** — tu tolerancia a los falsos positivos, por convención 0.05.
3. **Potencia** — tu tolerancia a los falsos negativos, por convención 0.80 (un 80% de probabilidad de detectar el efecto si es real).
4. **Tamaño muestral** — lo que normalmente quieres calcular.

Como regla general: efectos más pequeños, menor tolerancia a los errores y datos más variables exigen todos *más* muestra.

## Usar directamente el tamaño del efecto de un estudio piloto

Los estudios piloto pequeños dan estimaciones ruidosas del tamaño del efecto, y las estimaciones ruidosas de muestras pequeñas tienden a ser, de media, mayores que el efecto real (a veces se llama «la maldición del ganador», *winner's curse*). Si la serie clínica previa de Mia tenía solo 6 pacientes por grupo, el «aumento del 10%» que mostró podría estar más cerca del 3%, o de cero. Introducir en una calculadora de tamaño muestral el número bruto del piloto puede producir un estudio que sobre el papel parece tener potencia suficiente pero que en la práctica no la tiene.

**Mejores alternativas**: usa el menor tamaño del efecto que *resultaría útil* detectar (p. ej. «un aumento del LDL inferior al 5% no cambiaría cómo se trata a un portador en la clínica»), consulta tamaños del efecto de estudios publicados, o calcula el tamaño muestral para un pequeño rango de tamaños del efecto plausibles y compara los resultados.

## La potencia no es solo para experimentos

Si no hay una única prueba planificada de antemano —p. ej. Mia hace en cambio una encuesta abierta del colesterol LDL en muchas clínicas—, la pregunta adecuada pasa a ser de **precisión**: «¿qué tamaño de muestra necesito para estimar el LDL medio con un margen de, digamos, ±5%?». Se responde del mismo modo (más datos → intervalo más estrecho) pero no exige elegir una única hipótesis que contrastar.

## La trampa en sentido contrario: la «potencia observada»

Es tentador, una vez terminado el estudio, calcular «la potencia que alcanzamos» a partir del propio resultado. Ese número es un reempaquetado del valor p que ya tienes y no aporta información nueva. Para valorar el resultado de un estudio ya terminado, mira la anchura de su intervalo de confianza y comprueba si el signo o el tamaño del efecto podrían estar exagerados (una comprobación de **error de tipo S/tipo M**, *Type S/Type M error*), en lugar de calcular la potencia a posteriori.

> **Hazlo tú mismo**
>
> - [Cómo: planificar un tamaño muestral](./how-to/plan-a-sample-size.md) — cálculos de potencia y de precisión en Python, con una tabla de sensibilidad.
> - [Cuaderno: potencia y estudios piloto](../notebooks/power-and-pilot-studies.ipynb) — comprueba por qué el tamaño del efecto de un piloto pequeño engaña.

> **Para saber más**
>
> - [Gelman, Hill & Vehtari (2020)](https://avehtari.github.io/ROS-Examples/), *Regression and Other Stories*, §16.1 "The problem with statistical power" (pp. 291–293) y §16.5 "Design calculations after the data have been collected" (pp. 304–306) — la alternativa del error de tipo S/tipo M a la potencia retroactiva.
> - [Lakens (2022)](https://lakens.github.io/statistical_inferences/), *Improving Your Statistical Inferences*, Ch. 8 "Sample Size Justification" — el análisis de potencia y otras justificaciones defendibles.
> - Hoenig & Heisey (2001), "The abuse of power," *The American Statistician* 55(1), 19–24 — por qué la «potencia observada» es solo una reformulación del valor p.

---
**Anterior:** [Inicio del módulo](./README.md) · **Siguiente:** [Tamaño del efecto →](./effect-size.md) · [Glosario](../glossary.md)
