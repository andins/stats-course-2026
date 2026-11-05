# Cómo: validar un modelo predictivo

**Úsalo cuando:** tu objetivo es predecir una variable de respuesta para casos nuevos y quieres una estimación honesta de lo bien que lo hará el modelo. El razonamiento está en las páginas [Validación cruzada y revisión del modelo](../cross-validation-and-model-checking.md) y [Sobreajuste y regularización](../overfitting-and-regularization.md).

## Pasos

1. **Reserva primero un conjunto de prueba** (p. ej., el 25% de las filas) y no lo toques hasta el final.
2. **Mete en un *pipeline* cada paso que aprenda de los datos**: el escalado, la regularización y cualquier otra cosa que se ajuste a los datos. De lo contrario, la información de las filas de prueba se filtra al modelo y la puntuación parece mejor de lo que debería.
3. **Aplica validación cruzada sobre el conjunto de entrenamiento.** Esto te da una estimación del rendimiento, y de su dispersión, sin gastar el conjunto de prueba.
4. **Puntúa una sola vez con el conjunto de prueba.** Compara el resultado con la puntuación de validación cruzada y con la de entrenamiento.

## Código

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("my_data.csv")
outcome = "ldl_mmol"
predictors = ["variant_a", "variant_b", "age"]

data = df[[outcome] + predictors].dropna()  # listwise deletion; report how many rows this drops
X, y = data[predictors], data[outcome]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Scaling puts predictors on comparable footing; ElasticNetCV picks the amount of shrinkage by CV.
model = make_pipeline(StandardScaler(), ElasticNetCV(cv=5))
cv_rmse = -cross_val_score(model, X_train, y_train, cv=5, scoring="neg_root_mean_squared_error")
model.fit(X_train, y_train)

rmse = lambda a, b: np.sqrt(mean_squared_error(a, b))
print(f"cross-validated RMSE (training data): {cv_rmse.mean():.2f} +/- {cv_rmse.std():.2f}")
print(f"training RMSE:  {rmse(y_train, model.predict(X_train)):.2f}")
print(f"test RMSE:      {rmse(y_test, model.predict(X_test)):.2f}   (SD of outcome: {y_test.std():.2f})")
print(f"test R^2:       {r2_score(y_test, model.predict(X_test)):.2f}")
```

**¿Variable de respuesta sí/no?** Cambia a un modelo logístico y puntúa con el AUC:

```python
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_auc_score

model = make_pipeline(StandardScaler(), LogisticRegressionCV(cv=5, scoring="roc_auc", max_iter=5000))
model.fit(X_train, y_train)
print("test AUC:", roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))
```

## Cómo leer los resultados

Ejemplo de salida con datos inventados:

```text
cross-validated RMSE (training data): 0.62 +/- 0.02
training RMSE:  0.61
test RMSE:      0.65   (SD of outcome: 0.71)
test R^2:       0.15
```

- **El RMSE de prueba frente a la desviación típica de la variable de respuesta.** Predecir todos los casos con la media da un RMSE igual a la desviación típica de la variable de respuesta. Un modelo tiene que mejorarlo para ser útil, y aquí lo hace, aunque de forma modesta (R² = 0.15).
- **Puntuación de entrenamiento frente a la de validación cruzada/prueba.** Un error de entrenamiento mucho más bajo que los demás es la firma del sobreajuste. Aquí los tres son parecidos, así que el modelo no está memorizando ruido.
- **El ± de la puntuación de validación cruzada** muestra cuánto cambia el resultado entre pliegues. Con un conjunto de datos pequeño, esa dispersión (y la puntuación del conjunto de prueba) es ruidosa, así que no interpretes de más las pequeñas diferencias entre modelos.

## Si algo sale mal

- **Gran diferencia entre el rendimiento de entrenamiento y el de prueba**: el modelo es demasiado flexible para los datos. Usa menos predictores o una penalización más fuerte.
- **Pocas filas**: un conjunto de prueba del 25% es ruidoso en sí mismo. Presenta en su lugar la puntuación de validación cruzada con todos los datos (`cross_val_score(model, X, y, cv=5, ...)`).
- **Mediciones agrupadas o repetidas, o datos ordenados en el tiempo**: una división aleatoria deja casi duplicados tanto en entrenamiento como en prueba, lo que infla la puntuación. Divide por grupo (`GroupKFold`) o por tiempo (`TimeSeriesSplit`); véanse [Datos agrupados](../../07-special-data-structures/clustered-and-hierarchical-data.md) y [Series temporales](../../07-special-data-structures/time-series-data.md).
- **Quieres saber si X *causa* Y**: una buena puntuación con datos reservados no te lo dice. Véase [Predicción vs. explicación](../../05-prediction-vs-causation/prediction-vs-explanation.md).
