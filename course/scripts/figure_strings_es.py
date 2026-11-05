"""Spanish text for the figures drawn by make_figures.py (dict: English string -> Spanish string).

Keys must match, character for character, the strings passed to _() in make_figures.py. Strings with
{placeholders} are format templates: keep the placeholders (and their format specs) unchanged.
Terminology follows the course's Spanish translation spec.
"""

STRINGS = {
    # causal_roles
    "ancestry": "ascendencia",
    "gene\nvariant": "variante\ngenética",
    "Confounder": "Variable de confusión",
    "Adjust for it": "Ajusta por ella",
    "receptor\nactivity": "actividad del\nreceptor",
    "Mediator": "Variable mediadora",
    "Don't adjust for it\n(you would explain away the effect)":
        "No ajustes por ella\n(harías desaparecer el efecto)",
    "clinic\nreferral": "derivación\na la clínica",
    "Collider": "Colisionador",
    "Never adjust for it\n(it can create a fake association)":
        "Nunca ajustes por él\n(puede crear una asociación falsa)",
    "exposure": "exposición",
    "outcome": "variable de respuesta",
    "effect path we want to measure": "camino del efecto que queremos medir",
    "other causal arrow": "otra flecha causal",
    "possibly no effect at all": "quizá no haya ningún efecto",

    # causal_diagram_mia
    "confounder": "variable de confusión",
    "unmeasured confounder": "confusor no medido",
    "mediator": "mediadora",
    "collider": "colisionador",
    "Adjust for: ancestry     Leave out: receptor_activity, clinic_referral\n"
    "Cannot adjust for: linked_variant (state it as an assumption)":
        "Ajustar por: ancestry     Dejar fuera: receptor_activity, clinic_referral\n"
        "No se puede ajustar por: linked_variant (decláralo como supuesto)",

    # randomized_vs_observational
    "ancestry, diet, ...": "ascendencia, dieta, ...",
    "other causes of LDL": "otras causas del LDL",
    "gene variant": "variante genética",
    "Observational data": "Datos observacionales",
    "Exposure arrives bundled with its confounders:\nyou must adjust for them (and hope you got them all)":
        "La exposición llega mezclada con sus variables de confusión:\n"
        "debes ajustar por ellas (y confiar en no haberte dejado ninguna)",
    "age, diet, baseline health": "edad, dieta, salud basal",
    "other causes of blood pressure": "otras causas de la presión arterial",
    "drug or placebo": "fármaco o placebo",
    "blood pressure": "presión arterial",
    "coin flip": "moneda\nal aire",
    "Randomized experiment": "Experimento aleatorizado",
    "Only the coin flip decides the exposure, so the other\ncauses cannot differ systematically between groups":
        "Solo la moneda decide la exposición, así que las demás\n"
        "causas no pueden diferir sistemáticamente entre grupos",

    # p_value
    "Difference in mean blood pressure, drug minus placebo (mmHg)":
        "Diferencia de presión arterial media, fármaco menos placebo (mmHg)",
    "What if the drug did nothing? How surprising would Theo's result be?":
        "¿Y si el fármaco no hiciera nada? ¿Cuánto sorprendería el resultado de Theo?",
    "If the drug does nothing, differences scatter around 0\njust from random sampling":
        "Si el fármaco no hace nada, las diferencias se reparten\nen torno a 0 solo por el muestreo aleatorio",
    "Theo's observed\ndifference: \u22125 mmHg": "Diferencia observada\npor Theo: \u22125 mmHg",
    "equally extreme\nin the other direction": "igual de extrema\nen el otro sentido",
    "p = {p:.2f}: the shaded area. If the drug did nothing, a difference at least this large\n"
    "(in either direction) would show up in about {pct:.0f}% of repeated experiments.":
        "p = {p:.2f}: el área sombreada. Si el fármaco no hiciera nada, una diferencia al menos tan grande\n"
        "(en cualquier sentido) aparecería en torno al {pct:.0f}% de los experimentos repetidos.",

    # cross_validation
    "Train/test split": "División entrenamiento/prueba",
    "train: the model is built here": "entrenamiento: aquí se construye el modelo",
    "test: held back": "prueba: se reserva",
    "\u2192  score once": "\u2192  una sola puntuación",
    "5-fold cross-validation": "Validación cruzada de 5 pliegues",
    "held out": "reservado",
    "train": "entrenamiento",
    "\u2192  score {n}": "\u2192  puntuación {n}",
    "every observation is held out exactly once": "cada observación se reserva exactamente una vez",
    "\u2192  average the 5 scores": "\u2192  media de las 5 puntuaciones",
    "used to fit the model": "se usa para ajustar el modelo",
    "used only to check it (the model has never seen it)":
        "se usa solo para comprobarlo (el modelo nunca la ha visto)",

    # forest_plot
    "Study {n}": "Estudio {n}",
    "Pooled (random effects)": "Combinado (efectos aleatorios)",
    "Prediction interval": "Intervalo de predicción",
    "Extra LDL cholesterol in carriers (mmol/L)": "LDL extra en portadores (mmol/L)",
    "no effect": "sin efecto",
    "Forest plot of ten (made-up) studies": "Diagrama de bosque de diez estudios (inventados)",
    "Line: the study's 95% confidence interval.\nA wide line means an imprecise study":
        "Línea: intervalo de confianza del 95% del estudio.\nUna línea ancha indica un estudio poco preciso",
    "Square: the study's estimate. Bigger square =\nmore weight, so precise studies count more":
        "Cuadrado: estimación del estudio. Cuadrado más grande =\nmás peso, así que los estudios precisos cuentan más",
    "Diamond: the pooled average effect\nand its 95% confidence interval":
        "Rombo: el efecto medio combinado\ny su intervalo de confianza del 95%",
    "Bar: 95% prediction interval, where a new study's\ntrue effect would likely fall. The honest summary\nof how much the studies disagree":
        "Barra: intervalo de predicción del 95%, donde probablemente\ncaería el efecto real de un estudio nuevo. El resumen\nhonesto de cuánto discrepan los estudios",
    "Pooled {pooled:.2f} mmol/L (95% CI {ci_lo:.2f} to {ci_hi:.2f}); "
    "prediction interval {pi_lo:.2f} to {pi_hi:.2f}.":
        "Combinado {pooled:.2f} mmol/L (IC del 95% {ci_lo:.2f} a {ci_hi:.2f}); "
        "intervalo de predicción {pi_lo:.2f} a {pi_hi:.2f}.",

    # overfitting
    "true pattern": "patrón real",
    "simple model (cubic)": "modelo simple (cúbico)",
    "flexible model (degree 12)": "modelo flexible (grado 12)",
    "training data (model sees these)": "datos de entrenamiento (el modelo los ve)",
    "new data (model has not seen these)": "datos nuevos (el modelo no los ha visto)",
    "predictor": "predictor",
    "Fitting the training data perfectly is not the goal":
        "Ajustar a la perfección los datos de\nentrenamiento no es el objetivo",
    "error on training data": "error en los datos de entrenamiento",
    "error on new data": "error en los datos nuevos",
    "best on\nnew data": "mejor con\ndatos nuevos",
    "model flexibility (polynomial degree)": "flexibilidad del modelo (grado del polinomio)",
    "typical prediction error": "error de predicción típico",
    "More flexibility: training error keeps falling,\nerror on new data turns upward":
        "Más flexibilidad: el error de entrenamiento sigue bajando,\nel error en datos nuevos vuelve a subir",

    # glm_logistic
    "impossible: probability above 100%": "imposible: probabilidad superior al 100%",
    "impossible: probability below 0%": "imposible: probabilidad inferior al 0%",
    "straight line (ordinary regression)": "recta (regresión lineal ordinaria)",
    "logistic curve (GLM)": "curva logística (MLG)",
    "0\n(no event)": "0\n(sin evento)",
    "1\n(event)": "1\n(evento)",
    "LDL cholesterol (mmol/L)": "colesterol LDL (mmol/L)",
    "coronary event before age 60": "evento coronario antes de los 60 años",
    "A yes/no outcome: the line leaves the possible range, the curve cannot":
        "Un resultado sí/no: la recta se sale del rango posible, la curva no",

    # regression_anatomy
    "Intercept ({intercept:.1f}): where the line crosses age 0.\nOften just an anchor, not a real person":
        "Ordenada en el origen ({intercept:.1f}): donde la\n"
        "recta cruza la edad 0. A menudo es solo\n"
        "un ancla, no una persona real",
    "20 years older": "20 años más",
    "Slope ({slope:.2f} per year): a patient 20 years older\nhas on average {gain:.1f} mmol/L more LDL":
        "Pendiente ({slope:.2f} por año): un paciente\n"
        "20 años mayor tiene de media\n"
        "{gain:.1f} mmol/L más de LDL",
    "Residual: gap between the observed\npatient and the line's prediction":
        "Residuo: diferencia entre el paciente\nobservado y la predicción de la recta",
    "age (years)": "edad (años)",
    "A regression line, taken apart (70 simulated patients)":
        "Una recta de regresión, desmontada (70 pacientes simulados)",

    # funnel_plots
    "No publication bias": "Sin sesgo de publicación",
    "Publication bias": "Con sesgo de publicación",
    "effect estimate": "estimación del efecto",
    "standard error (small = precise study)": "error estándar (pequeño = estudio preciso)",
    "Symmetric funnel: precise studies cluster at the top,\nimprecise ones scatter evenly on both sides":
        "Embudo simétrico: los estudios precisos se agrupan arriba,\nlos imprecisos se reparten por igual a ambos lados",
    "missing: small studies with\nnull or negative results": "faltan: estudios pequeños\ncon resultados nulos o negativos",
    "Lopsided funnel: a corner is empty,\nso the pooled estimate is pushed up":
        "Embudo asimétrico: una esquina está vacía,\npor lo que la estimación combinada sube",

    # missing_data_mechanisms
    "Missing completely at random": "Faltan completamente al azar",
    "Gaps ignore your data entirely.\nDropping rows loses precision, not accuracy.":
        "Los huecos ignoran por completo tus datos.\nEliminar filas resta precisión, no exactitud.",
    "Missing at random": "Faltan al azar",
    "Gaps depend on something you measured.\nDropping rows can bias the result.":
        "Los huecos dependen de algo que mediste.\nEliminar filas puede sesgar el resultado.",
    "Missing not at random": "Faltan no al azar",
    "Gaps depend on the missing value itself.\nDropping rows biases the result.":
        "Los huecos dependen del propio valor faltante.\nEliminar filas sesga el resultado.",
    "age": "edad",
    "LDL\n(true value)": "LDL\n(valor real)",
    "LDL missing?": "¿LDL faltante?",
    "chance": "azar",

    # time_series_autocorrelation
    "Residuals with no time pattern": "Residuos sin patrón temporal",
    "Residuals that remember yesterday": "Residuos que recuerdan el día anterior",
    "time": "tiempo",
    "residual": "residuo",
    "lag (steps back in time)": "retardo (pasos hacia atrás en el tiempo)",
    "autocorrelation": "autocorrelación",
    "grey band: what chance alone produces": "banda gris: lo que produce el azar por sí solo",
    "bars far outside the band: not chance": "barras muy fuera de la banda: no es azar",

    # clustered_families
    "What the test assumes:\n300 independent patients": "Lo que supone la prueba:\n300 pacientes\nindependientes",
    "family (sorted by its average)": "familia (ordenada por su media)",
    "What the data look like: 15 families of 20 relatives,\nwho resemble each other more than they resemble other families":
        "Cómo son realmente los datos: 15 familias de 20 familiares,\nque se parecen entre sí más que a otras familias",
    "family average": "media de la familia",
    "overall average": "media global",

    # partial_pooling
    "no pooling: each group's own average (bar = \u00b11 standard error)":
        "sin agrupamiento: la media de cada grupo (barra = \u00b11 error estándar)",
    "partial pooling: pulled toward the overall average":
        "agrupamiento parcial: atraída hacia la media global",
    "complete pooling: one average for everyone": "agrupamiento completo: una sola media para todos",
    "{n} patients": "{n} pacientes",
    "estimated average LDL cholesterol (mmol/L)": "colesterol LDL medio estimado (mmol/L)",
    "Small, noisy groups are pulled toward the overall average the most":
        "Los grupos pequeños y ruidosos son los que más se acercan a la media global",
}
