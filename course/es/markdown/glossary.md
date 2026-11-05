# Glosario

Definiciones breves y en lenguaje sencillo de los términos que aparecen en estas explicaciones. En orden alfabético (según el término en español; entre paréntesis figura el término en inglés para que puedas buscarlo). Cada término enlaza con la página que lo explica con más detalle, cuando existe.

**Agrupamiento (*pooling*; nulo/completo/parcial)** — tres estrategias para datos agrupados: analizar cada grupo por separado (sin agrupamiento), ignorar la agrupación (agrupamiento completo) o compartir información entre grupos mediante contracción (*shrinkage*) (agrupamiento parcial/multinivel). Consulta [Datos agrupados y jerárquicos](./07-special-data-structures/clustered-and-hierarchical-data.md).

**Alelo (*allele*)** — una versión de un gen. Una persona hereda dos copias de la mayoría de los genes, así que tiene dos alelos de cada uno; una variante es un alelo que difiere del habitual (el de referencia).

**Alfa (nivel de significación) (*alpha, significance level*)** — la tasa de falsos positivos que aceptas asumir, elegida *antes* de mirar los datos. Por convención es 0.05 (una probabilidad de 1 entre 20). Consulta [Valores p y significación](./03-hypothesis-testing/p-values-and-significance.md).

**Análisis exploratorio vs. confirmatorio (*exploratory vs. confirmatory analysis*)** — si buscas patrones que aún no has decidido de antemano (exploratorio) o pones a prueba una única comparación específica decidida de antemano (confirmatorio). Consulta [Exploratorio vs. confirmatorio](./02-exploring-data/exploratory-vs-confirmatory.md).

**Autocorrelación (*autocorrelation*)** — cuando un valor de una serie ordenada en el tiempo está correlacionado con sus propios valores pasados (la temperatura de hoy predice la de mañana). Consulta [Series temporales](./07-special-data-structures/time-series-data.md).

**Colisionador (*collider*)** — una variable causada *tanto* por tu exposición *como* por tu resultado. Condicionar por ella puede crear una asociación falsa donde no existe ninguna. Consulta [Diagramas causales](./05-prediction-vs-causation/causal-diagrams.md).

**Conjunto de ajuste (*adjustment set*)** — la lista de variables por las que "controlas" estadísticamente en un modelo para intentar aislar el efecto de una variable sobre otra. Consulta [Diagramas causales](./05-prediction-vs-causation/causal-diagrams.md).

**DAG (grafo acíclico dirigido, *Directed Acyclic Graph*)** — un diagrama de flechas entre variables que muestra las direcciones de causa y efecto supuestas, sin bucles. Consulta [Diagramas causales](./05-prediction-vs-causation/causal-diagrams.md).

**Datos observacionales (*observational data*)** — datos en los que la "exposición" de interés no la asignó nadie mediante un experimento: es simplemente lo que ocurrió. Consulta [Experimentos vs. datos observacionales](./05-prediction-vs-causation/experiments-vs-observational-data.md).

**Desequilibrio de ligamiento (LD, *linkage disequilibrium*)** — la tendencia de las variantes genéticas que están próximas en un cromosoma a heredarse juntas, de modo que sus genotipos están fuertemente correlacionados. Es una fuente de multicolinealidad entre variantes. Consulta [Multicolinealidad](./06-building-models/multicollinearity.md).

**Diagrama de bosque (*forest plot*)** — la imagen estándar de un metaanálisis: una fila por estudio (su estimación y su intervalo) y un rombo para la estimación combinada. Consulta [Metaanálisis](./07-special-data-structures/meta-analysis.md).

**Error de medición (*measurement error*)** — la diferencia entre un valor observado y registrado y la cantidad real a la que pretende representar (p. ej., un instrumento ruidoso o un indicador indirecto autodeclarado). El error en un predictor sesga hacia cero la pendiente de una regresión (véase Sesgo de atenuación); el error en una variable de respuesta sobre todo añade ruido. Consulta [Error de medición](./06-building-models/measurement-error.md).

**Error de tipo I (*Type I error*)** — un falso positivo: concluir que hay un efecto cuando no lo hay.

**Error de tipo II (*Type II error*)** — un falso negativo: no detectar un efecto real.

**Error de tipo S / tipo M (*Type S / Type M error*)** — equivocarse en el *signo* (S) o en la *magnitud* (M) de un efecto; una forma más útil de pensar en los errores en estudios pequeños o ruidosos que la potencia por sí sola. Consulta [Tamaño muestral y potencia](./01-planning-your-study/sample-size-and-power.md).

**Experimento aleatorizado (*randomized experiment*)** — un estudio en el que la exposición o el tratamiento se asigna a las unidades mediante un mecanismo de azar controlado por quien investiga, que es lo que hace creíbles las afirmaciones causales. Consulta [Experimentos vs. datos observacionales](./05-prediction-vs-causation/experiments-vs-observational-data.md).

**Factor de inflación de la varianza (VIF, *Variance Inflation Factor*)** — un número que cuantifica cuánto se infla la incertidumbre de un predictor por su correlación con otros predictores. Consulta [Multicolinealidad](./06-building-models/multicollinearity.md).

**Genotipo (*genotype*)** — qué versiones (alelos) de un gen o variante tiene una persona, p. ej., ninguna copia, una copia o dos copias de una variante. A menudo se codifica como 0, 1 o 2 para el análisis.

**Heterogeneidad (*heterogeneity*)** — en un metaanálisis, las diferencias reales entre los efectos verdaderos de los estudios, más allá del azar. Se mide con τ (su desviación típica) e I² (la proporción de la variabilidad que es real y no debida al azar). Consulta [Metaanálisis](./07-special-data-structures/meta-analysis.md).

**Imputación (*imputation*)** — rellenar los valores faltantes con una estimación plausible en lugar de descartar la fila. Consulta [Datos faltantes](./02-exploring-data/missing-data.md).

**Inferencia bayesiana (*Bayesian inference*)** — un marco que trata las cantidades desconocidas como distribuciones de probabilidad que se actualizan a medida que llegan datos, en lugar de producir un único valor p. Consulta [Métodos bayesianos](./07-special-data-structures/bayesian-methods.md).

**Intervalo de confianza (IC) (*confidence interval, CI*)** — un rango de valores plausibles para una cantidad desconocida (como un tamaño del efecto verdadero), construido de modo que, si repitieras el estudio muchas veces, alrededor del 95 % de esos intervalos contendrían el valor verdadero. Consulta [Valores p y significación](./03-hypothesis-testing/p-values-and-significance.md).

**Intervalo de predicción (metaanálisis) (*prediction interval*)** — el rango donde se esperaría que cayera el efecto verdadero de un estudio *nuevo*. Es más ancho que el intervalo de confianza del efecto promedio y, a menudo, el resumen más honesto cuando los estudios difieren. Consulta [Metaanálisis](./07-special-data-structures/meta-analysis.md).

**Jardín de los senderos que se bifurcan (*garden of forking paths*)** — las muchas decisiones pequeñas y sin registrar (qué valores atípicos descartar, qué subgrupo mirar) que pueden convertir el ruido en un resultado aparentemente "significativo", incluso con buena intención. Consulta [Exploratorio vs. confirmatorio](./02-exploring-data/exploratory-vs-confirmatory.md).

**Metaanálisis (*meta-analysis*)** — combinar las estimaciones del efecto (y sus errores estándar) de varios estudios sobre la misma pregunta en una única estimación combinada, dando más peso a los estudios más precisos y midiendo cuánto discrepan los estudios. Consulta [Metaanálisis](./07-special-data-structures/meta-analysis.md).

**Modelo de efectos aleatorios (metaanálisis) (*random-effects model*)** — supone que cada estudio tiene su propio efecto verdadero, disperso alrededor de un promedio, en lugar de un único efecto verdadero común. Es la opción por defecto habitual para combinar estudios de ciencias de la vida. Consulta [Metaanálisis](./07-special-data-structures/meta-analysis.md).

**Modelo lineal generalizado (GLM, *Generalized Linear Model*)** — la familia de regresión que extiende la regresión ordinaria a variables de respuesta que no son simples números continuos (sí/no, recuentos). Consulta [Modelos lineales generalizados](./04-regression-basics/generalized-linear-models.md).

**Modelo multinivel / de efectos mixtos (*multilevel / mixed-effects model*)** — un modelo para datos agrupados que comparte parcialmente (“agrupa”) información entre grupos en lugar de tratarlos como totalmente separados o totalmente idénticos. Consulta [Datos agrupados y jerárquicos](./07-special-data-structures/clustered-and-hierarchical-data.md).

**Multicolinealidad (*multicollinearity*)** — cuando los predictores de un modelo están muy correlacionados entre sí, lo que dificulta distinguir sus efectos individuales. Consulta [Multicolinealidad](./06-building-models/multicollinearity.md).

**Portador (*carrier*)** — una persona que tiene al menos una copia de una variante génica concreta. Los portadores "heterocigotos" tienen una copia y los "homocigotos" tienen dos.

**Potencia (estadística) (*power*)** — la probabilidad de que un estudio detecte un efecto verdadero de un tamaño dado, si existe. Una potencia baja significa que incluso los efectos reales suelen pasar desapercibidos. Consulta [Tamaño muestral y potencia](./01-planning-your-study/sample-size-and-power.md).

**Puntuación poligénica (*polygenic score*)** — un único número de riesgo para una persona, construido sumando los pequeños efectos de muchas variantes genéticas. Ajustarla con una muestra pequeña es un riesgo de sobreajuste de manual. Consulta [Sobreajuste y regularización](./06-building-models/overfitting-and-regularization.md).

**Regularización (*regularization*)** — reducir deliberadamente los coeficientes de un modelo hacia cero para disminuir el sobreajuste, a costa de un pequeño sesgo. Consulta [Sobreajuste y regularización](./06-building-models/overfitting-and-regularization.md).

**Residuo (*residual*)** — la diferencia entre lo que predijo un modelo y lo que se observó, para un único dato.

**Sesgo de atenuación (*attenuation bias*)** — la tendencia de la pendiente de una regresión a sesgarse hacia cero cuando un predictor se mide con error aleatorio. No disminuye con más datos. Consulta [Error de medición](./06-building-models/measurement-error.md).

**Sesgo de publicación (*publication bias*)** — la literatura publicada exagera los efectos porque los estudios con resultados llamativos tienen más probabilidades de publicarse que los que no encontraron nada. Consulta [Metaanálisis: sesgos y trampas](./07-special-data-structures/meta-analysis-pitfalls.md).

**Sobreajuste (*overfitting*)** — cuando un modelo aprende el ruido de tu muestra concreta en lugar del patrón general, y rinde bien con los datos con los que se construyó y mal con datos nuevos. Consulta [Sobreajuste y regularización](./06-building-models/overfitting-and-regularization.md).

**Tamaño del efecto (*effect size*)** — cuán *grande* es una diferencia o una relación, en unidades con significado, y no solo si es "significativa". Consulta [Tamaño del efecto](./01-planning-your-study/effect-size.md).

**Validación cruzada (*cross-validation*)** — dividir los datos repetidamente en porciones de "ajuste" y de "prueba" para ver cómo de bien generaliza un modelo a datos que no ha visto. Consulta [Validación cruzada y revisión del modelo](./06-building-models/cross-validation-and-model-checking.md).

**Valor p (*p-value*)** — la probabilidad de ver un resultado al menos así de extremo *si de verdad no hubiera ningún efecto*. No es la probabilidad de que el efecto sea real, y solo está bien calibrado para una única hipótesis decidida antes de ver los datos, idealmente procedente de un experimento bien diseñado; incluso entonces, una estimación del tamaño del efecto con un intervalo de confianza es más informativa que el veredicto por sí solo. Consulta [Valores p y significación](./03-hypothesis-testing/p-values-and-significance.md).

**Variable de confusión (confusor) (*confounder*)** — una variable que afecta causalmente *tanto* a tu exposición *como* a tu resultado, creando una asociación entre ambos aunque ninguno cause directamente al otro. Consulta [Diagramas causales](./05-prediction-vs-causation/causal-diagrams.md).

**Variable mediadora (mediador) (*mediator*)** — una variable situada *en la vía causal* entre tu exposición y tu resultado (la exposición la causa, y ella causa el resultado). No ajustes por ella si quieres el efecto total. Consulta [Diagramas causales](./05-prediction-vs-causation/causal-diagrams.md).

**Variante de significado incierto (VUS, *variant of uncertain significance*)** — una variante genética cuyo significado clínico aún se desconoce, por ejemplo, si aumenta el riesgo de enfermedad. Estudios como el de Mia intentan aportar la evidencia.
