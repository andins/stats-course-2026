# Cómo: planificar un tamaño muestral

**Úsalo cuando:** estés diseñando un estudio y necesites decidir cuántas unidades (pacientes, familias, muestras, animales, personas encuestadas) recoger. El razonamiento está en la página [Tamaño muestral y potencia](../sample-size-and-power.md).

Para ver por qué el tamaño del efecto de un piloto pequeño es una mala entrada, y para experimentar con curvas de potencia, usa el [cuaderno de potencia y estudios piloto](../../notebooks/power-and-pilot-studies.ipynb) (descárgalo y ábrelo en Jupyter, VS Code o Colab).

## Pasos

1. **Decide qué pregunta tienes.** Una prueba planificada de una diferencia o de un efecto necesita un cálculo de *potencia*. Una estimación abierta («¿cuál es el colesterol LDL medio, con un margen del 5%?») necesita un cálculo de *precisión*.
2. **Elige las entradas.** Para la potencia: alfa (0.05 por convención), potencia objetivo (0.80 por convención) y un tamaño del efecto. Para el tamaño del efecto, usa la **menor diferencia que importaría en la práctica**, o un valor de la bibliografía. No copies la estimación bruta de un piloto pequeño.
3. **Expresa el tamaño del efecto como d de Cohen:** la diferencia bruta dividida entre la desviación típica de la variable de respuesta. Necesitas una estimación para planificar esa desviación típica, a partir de datos previos o de la bibliografía.
4. **Calcula el tamaño muestral para varios tamaños del efecto plausibles**, no solo uno, y observa cuánto cambia la respuesta.
5. **Si tu análisis no es una prueba t, un ANOVA o una comparación de proporciones simples** (covariables, un GLM, datos agrupados), calcula el tamaño muestral mediante simulación.

## Código: potencia para una comparación de dos grupos

```python
import math
from statsmodels.stats.power import TTestIndPower

sd = 0.8   # planning guess for the SD of the outcome (LDL, mmol/L)
power_calc = TTestIndPower()

for diff in (0.3, 0.4, 0.6, 0.8):   # sensitivity table: raw differences worth detecting (mmol/L)
    d = diff / sd                    # Cohen's d
    n = power_calc.solve_power(effect_size=d, alpha=0.05, power=0.8)
    print(f"difference {diff:.1f} mmol/L (d = {d:.2f}): {math.ceil(n)} patients per group")
```

¿Ya sabes cuántas unidades puedes permitirte? Da la vuelta a la pregunta y averigua qué potencia te dan:

```python
print(f"power with 20 patients per group for d = 0.5: {power_calc.power(effect_size=0.5, nobs1=20, alpha=0.05):.2f}")
```

Otros diseños tienen un equivalente en el mismo módulo: `TTestPower` (una muestra o datos apareados), `FTestAnovaPower` (ANOVA de un factor, con la f de Cohen como tamaño del efecto) y `NormalIndPower` con `proportion_effectsize(p1, p2)` (dos proporciones).

## Código: precisión para una encuesta o una estimación

Cuando no hay una única prueba, planifica en su lugar la anchura del intervalo de confianza:

```python
from scipy import stats

z = stats.norm.ppf(0.975)

sd, margin = 0.8, 0.1            # estimate a mean LDL to within +/- 0.1 mmol/L
print("mean:", math.ceil((z * sd / margin) ** 2), "patients")

p_guess, margin = 0.5, 0.03      # estimate a proportion to within +/- 3 points; 0.5 is the most cautious guess
print("proportion:", math.ceil(z**2 * p_guess * (1 - p_guess) / margin**2), "respondents")
```

## Código: potencia por simulación, para cualquier otro caso

Simula tu estudio muchas veces con el efecto que quieres detectar, ejecuta tu análisis planificado en cada conjunto de datos simulado y cuenta con qué frecuencia detecta el efecto. Aquí el análisis es una regresión que ajusta por la edad:

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(0)


def power_by_simulation(n_per_group, effect=0.4, sd=0.8, n_sims=500, alpha=0.05):
    hits = 0
    for _ in range(n_sims):
        group = np.repeat([0, 1], n_per_group)          # 0 = non-carrier, 1 = carrier
        age = rng.normal(45, 12, 2 * n_per_group)
        y = 0.02 * age + effect * group + rng.normal(0, sd, 2 * n_per_group)
        fit = smf.ols("y ~ group + age", data=pd.DataFrame({"y": y, "group": group, "age": age})).fit()
        hits += fit.pvalues["group"] < alpha
    return hits / n_sims


for n in (20, 40, 60):
    print(f"{n} per group: power = {power_by_simulation(n):.2f}")
```

Cambia las líneas que generan los datos para que coincidan con tu diseño (agrupamiento, grupos desiguales, una variable de respuesta binaria con `smf.logit`) y la línea `smf.ols` para que coincida con el análisis que vayas a ejecutar de verdad.

## Cómo leer el resultado

Ejemplo de salida (debería ser parecida a esta):

```text
difference 0.3 mmol/L (d = 0.37): 113 patients per group
difference 0.4 mmol/L (d = 0.50): 64 patients per group
difference 0.6 mmol/L (d = 0.75): 29 patients per group
difference 0.8 mmol/L (d = 1.00): 17 patients per group
```

- **El tamaño muestral crece rápido a medida que el efecto se reduce.** Reducir el efecto a la mitad multiplica la muestra aproximadamente por cuatro, así que la elección del tamaño del efecto importa más que la de alfa o la de la potencia.
- **Presenta la tabla, no un único número.** Elige el tamaño muestral que puedas defender para el menor efecto que te interese, e indica qué puedes detectar si el efecto real es mayor.
- **La respuesta de la simulación tiene error de Monte Carlo** de un par de puntos porcentuales con 500 simulaciones; aumenta `n_sims` si la potencia está cerca de tu objetivo.
- **Añade un margen para las pérdidas.** Si esperas que el 10% de las unidades abandone o falle, divide el tamaño muestral entre 0.9.

## Si algo sale mal

- **Solo tienes el tamaño del efecto de un piloto:** probablemente esté inflado, así que el estudio resultante tendrá poca potencia (véase el cuaderno). Usa en su lugar el menor efecto útil, o una estimación publicada, y muestra la tabla de sensibilidad.
- **El tamaño muestral necesario es mayor del que puedes recoger:** tienes tres opciones honestas. Aceptar una potencia menor y decirlo, fijar un efecto mínimo de interés mayor, o reducir el ruido (mejor medición, una covariable, un diseño apareado o por bloques). No ajustes los supuestos hasta que el número encaje.
- **Nunca calcules la «potencia observada» después del estudio.** Reformula el valor p. Mira en su lugar la anchura del intervalo de confianza.
