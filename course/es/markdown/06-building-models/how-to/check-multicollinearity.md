# Cómo: comprobar la multicolinealidad

**Úsalo cuando:** tu modelo tiene más de un predictor y piensas interpretar coeficientes individuales. La idea de fondo está en la página [Multicolinealidad](../multicollinearity.md).

## Pasos

1. Mira las correlaciones por pares entre tus predictores. Conviene revisar con más atención cualquier valor por encima de 0.8 aproximadamente en valor absoluto.
2. Calcula el **VIF** (factor de inflación de la varianza, *variance inflation factor*) de cada predictor. Las correlaciones solo detectan solapamientos entre pares; el VIF también detecta un predictor que queda explicado por una combinación de varios de los demás.
3. Decide qué hacer (más abajo). Repite la comprobación después de cualquier cambio.

## Código

```python
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv("my_data.csv")
predictors = ["variant_a", "variant_b", "age"]  # the numeric predictors in your model (variant columns = allele counts 0/1/2)

print(df[predictors].corr().round(2))

X = sm.add_constant(df[predictors].dropna())  # VIF needs an intercept column
vif = pd.Series(
    [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
    index=X.columns,
).drop("const")
print(vif.round(1))
```

Los predictores categóricos hay que codificarlos antes como variables ficticias (*dummy*) (`pd.get_dummies(df[col], drop_first=True)`) para poder incluirlos en el cálculo del VIF.

## Cómo leer los resultados

Ejemplo de salida con datos inventados de la cohorte de Mia, en la que las variantes A y B están muy próximas en el cromosoma y casi siempre se heredan juntas (desequilibrio de ligamiento):

```text
variant_a    29.8
variant_b    29.9
age           1.0
```

- **Alrededor de 1**: no hay solapamiento con los demás predictores.
- **Por encima de 5**: conviene mirarlo con más atención.
- **Por encima de 10**: una señal de alarma clara. Los dos valores altos de aquí pertenecen a la pareja solapada, y `age` no se ve afectada.

Estos umbrales son orientaciones aproximadas, no reglas (O'Brien 2007). Juzga según lo que quieras hacer con el modelo: el VIF solo importa para interpretar coeficientes individuales, no para predecir.

## Si un VIF es alto

- **Dos predictores miden lo mismo**: elimina uno. Aquí, quédate con `variant_a` o con `variant_b`, y explica cuál elegiste y por qué.
- **Van juntos por naturaleza**: combínalos en una única puntuación, si tiene sentido desde el punto de vista científico.
- **Solo necesitas predicciones**: puedes dejarlos y usar en su lugar la [regularización](./validate-a-predictive-model.md).
- **El VIF alto procede de `x` y `x²`, o de un término de interacción**: están correlacionados por construcción. Centrar `x` (restándole su media) antes de elevarla al cuadrado elimina la mayor parte del solapamiento.

> Eliminar una variable cambia el significado del coeficiente que queda. Si estabas ajustando por una variable de confusión, no la elimines solo para reducir un VIF; véase [Diagramas causales](../../05-prediction-vs-causation/causal-diagrams.md).
