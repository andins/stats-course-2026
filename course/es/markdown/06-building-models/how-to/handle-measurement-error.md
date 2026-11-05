# Cómo: estimar y corregir el error de medición

**Úsalo cuando:** un predictor es una medición ruidosa de lo que te interesa y puedes hacerte una idea de cuánto ruido tiene. El razonamiento está en la página [Error de medición](../measurement-error.md).

Para ver cómo aparece el sesgo y cómo persiste al crecer la muestra, juega primero con el [cuaderno sobre la atenuación](../../notebooks/measurement-error-attenuation.ipynb) (descárgalo y ábrelo en Jupyter, VS Code o Colab).

## Pasos

1. **Averigua el tamaño del error.** La mejor fuente son las **réplicas**: dos o más mediciones independientes de la misma unidad (Theo mide dos veces a cada paciente). La alternativa es una desviación típica del error tomada de la documentación del instrumento o de un estudio de validación; usa una desviación típica, no un rango "±".
2. **Calcula la fiabilidad** (*reliability*) de tu predictor: la proporción de su variación que es señal real y no ruido. 1 significa que no hay error de medición; 0.5 significa que la mitad de la varianza es ruido.
3. **Corrige la pendiente.** Con un único predictor ruidoso, la pendiente ingenua es la pendiente verdadera multiplicada por la fiabilidad, así que dividir entre la fiabilidad deshace la atenuación.
4. **Obtén un intervalo aplicando *bootstrap* a todo el procedimiento**, incluida la estimación de la fiabilidad. El intervalo de confianza ingenuo no recoge la incertidumbre adicional que introduce la corrección.

## Código

Dos lecturas replicadas por paciente, `bp_1` y `bp_2`, y una columna `outcome`:

```python
import numpy as np
import pandas as pd

df = pd.read_csv("my_data.csv")  # columns: bp_1, bp_2, outcome


def corrected_slope(d):
    r1, r2, y = d["bp_1"], d["bp_2"], d["outcome"]
    x = (r1 + r2) / 2                                  # average of the replicates
    var_error = ((r1 - r2) ** 2).mean() / 2            # measurement-error variance of one reading
    reliability = 1 - (var_error / 2) / x.var()        # share of var(x) that is signal
    naive = np.cov(x, y)[0, 1] / x.var()               # ordinary regression slope
    return naive, reliability, naive / reliability


naive, reliability, corrected = corrected_slope(df)
boot = [corrected_slope(df.sample(frac=1, replace=True, random_state=i))[2] for i in range(1000)]
low, high = np.percentile(boot, [2.5, 97.5])
print(f"reliability {reliability:.2f}; naive slope {naive:.2f}; "
      f"corrected {corrected:.2f} (95% CI {low:.2f} to {high:.2f})")
```

Si no tienes réplicas pero conoces la desviación típica del error de una sola lectura, omite el promediado: usa `x = df["bp"]` y `reliability = 1 - sd ** 2 / x.var()`.

## Cómo leer los resultados

Ejemplo de salida con datos inventados, donde la pendiente verdadera es 0.50:

```text
reliability 0.80; naive slope 0.41; corrected 0.52 (95% CI 0.44 to 0.60)
```

- **La fiabilidad** te dice cuánta atenuación cabe esperar. Con 0.80, la pendiente ingenua es un 20% menor de lo debido; con 0.5, es la mitad del valor verdadero.
- **La pendiente corregida** es la estimación que debes comunicar, junto con su intervalo *bootstrap* y una declaración explícita del supuesto en que se apoya: los errores son aleatorios y no guardan relación con el valor verdadero ni con la variable de respuesta.
- Si la fiabilidad es cercana a 1, la corrección es despreciable y el resultado ingenuo sirve.

## Límites de esta receta

- Es válida para **un** predictor ruidoso, con un error no relacionado con nada más. Con varios predictores (o covariables por las que ajustas), la corrección es más compleja (calibración de la regresión, SIMEX o un modelo bayesiano con un valor verdadero latente); ese es el momento de contar con un estadístico.
- No sirve para el error **sistemático** (un aparato que siempre marca 5 mmHg de más), que una pendiente no detecta.
- El error en la **variable de respuesta** no sesga la pendiente; solo ensancha el intervalo, así que no hace falta corrección.
- No se arregla recogiendo más de los mismos datos ruidosos. Lo que ayuda son mejores mediciones o réplicas, y lo más barato es planificarlas en la fase de diseño (véase [Consideraciones de diseño](../../01-planning-your-study/design-considerations.md)).
