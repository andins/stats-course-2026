# Cómo: dibujar y usar un diagrama causal

**Úsalo cuando:** quieras conocer el efecto de una variable sobre otra a partir de datos *observacionales* (nadie aleatorizó la exposición) y necesites decidir por qué otras variables ajustar. Si la exposición se aleatorizó, no necesitas esto; consulta [Experimentos vs. datos observacionales](../experiments-vs-observational-data.md). Las ideas están en la página [Diagramas causales](../causal-diagrams.md).

Para ver, con números, qué ocurre cuando ajustas por la variable equivocada, usa el [cuaderno sobre variable de confusión, mediadora y colisionador](../../notebooks/confounder-mediator-collider.ipynb) (descárgalo y ábrelo en Jupyter, VS Code o Colab).

## Pasos

1. **Anota la exposición y el resultado**: el efecto que quieres, como «X sobre Y».
2. **Haz una lista de todas las demás variables que podrían importar**, incluidas las que *no* mediste. Usa las preguntas de la página del curso: ¿causa la exposición?, ¿el resultado?, ¿ambos?, ¿es consecuencia de alguno de los dos? Comprueba el orden temporal: las causas van antes que los efectos.
3. **Escribe cada creencia como una flecha** `(causa, efecto)` en una lista. Una flecha significa «causa directamente». Omite una flecha solo cuando aceptes suponer que no hay efecto directo.
4. **Deja que el código etiquete el papel de cada variable** y sugiera por qué ajustar.
5. **Comprueba el resultado con una herramienta adecuada** (DAGitty, más abajo), sobre todo si el diagrama tiene más que un puñado de variables.
6. **Estima el efecto** con una regresión que incluya la exposición más el conjunto de ajuste, y enuncia los supuestos que hiciste.

## Código: papeles y un primer conjunto de ajuste

El diagrama de aquí es el de Mia: ¿llevar la variante de LDLR eleva el colesterol LDL? La ascendencia afecta a ambos (variable de confusión); la variante reduce la actividad del receptor de LDL, lo que eleva el LDL (mediadora); un paciente es derivado a la clínica de lípidos cuando lleva la variante o tiene el LDL alto (consecuencia de ambos); y una variante cercana en desequilibrio de ligamiento con la de Mia, que nadie genotipó, afecta al LDL y viaja junto con la variante estudiada (variable de confusión no medida):

![Diagrama causal completo de Mia. La ascendencia y una variante ligada no medida apuntan cada una tanto al estado de portador como al LDL. El estado de portador apunta directamente al LDL y también a través de la actividad del receptor. El estado de portador y el LDL apuntan ambos a la derivación a la clínica. Una nota debajo indica que hay que ajustar por la ascendencia, dejar fuera la actividad del receptor y la derivación a la clínica, y enunciar la variante ligada no medida como un supuesto.](../../figures/causal_diagram_mia.png)

*El diagrama que codifica el código siguiente, con el papel de cada variable. Verde = variable de confusión (ajusta por ella si está medida), morado = mediadora, rojo = colisionador, discontinuo = no medida.*

```python
from collections import defaultdict

exposure, outcome = "carrier", "ldl_mmol"
unmeasured = {"linked_variant"}
edges = [   # (cause, effect)
    ("ancestry", "carrier"), ("ancestry", "ldl_mmol"),
    ("carrier", "receptor_activity"), ("receptor_activity", "ldl_mmol"), ("carrier", "ldl_mmol"),
    ("carrier", "clinic_referral"), ("ldl_mmol", "clinic_referral"),
    ("linked_variant", "carrier"), ("linked_variant", "ldl_mmol"),
]

children, parents = defaultdict(set), defaultdict(set)
for cause, effect in edges:
    children[cause].add(effect)
    parents[effect].add(cause)


def reachable(start, graph):
    seen, stack = set(), [start]
    while stack:
        for nxt in graph[stack.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


common_causes = reachable(exposure, parents) & reachable(outcome, parents)
after_exposure = reachable(exposure, children)
after_outcome = reachable(outcome, children)

roles = {}
for v in sorted({name for edge in edges for name in edge} - {exposure, outcome}):
    if v in common_causes:
        roles[v] = "confounder"
    elif v in after_exposure and outcome in reachable(v, children):
        roles[v] = "mediator"
    elif v in after_exposure and v in after_outcome:
        roles[v] = "collider (consequence of both)"
    elif v in after_exposure or v in after_outcome:
        roles[v] = "consequence of exposure or outcome"
    else:
        roles[v] = "unrelated / other"

for v, role in roles.items():
    print(f"{v:18s} {role}{'  (UNMEASURED)' if v in unmeasured else ''}")

confounders = {v for v, role in roles.items() if role == "confounder"}
adjust_for = sorted(confounders - unmeasured)
print("\nadjust for:", adjust_for)
print("unmeasured confounders you cannot adjust for:", sorted(confounders & unmeasured))
```

## Código: estimar el efecto

```python
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("my_data.csv")

naive = smf.ols(f"{outcome} ~ {exposure}", data=df).fit()
adjusted = smf.ols(f"{outcome} ~ {' + '.join([exposure] + adjust_for)}", data=df).fit(cov_type="HC3")

for label, model in [("unadjusted", naive), ("adjusted", adjusted)]:
    low, high = model.conf_int().loc[exposure]
    print(f"{label:10s} effect of {exposure}: {model.params[exposure]:.2f} (95% CI {low:.2f} to {high:.2f})")
```

## Cómo leer los resultados

Ejemplo de salida con datos inventados en los que el efecto real de llevar la variante es 0.5 mmol/L:

```text
ancestry           confounder
clinic_referral    collider (consequence of both)
linked_variant     confounder  (UNMEASURED)
receptor_activity  mediator

adjust for: ['ancestry']
unmeasured confounders you cannot adjust for: ['linked_variant']
unadjusted effect of carrier: 1.10 (95% CI 0.96 to 1.24)
adjusted   effect of carrier: 0.49 (95% CI 0.39 to 0.59)
```

- **Las dos estimaciones difieren mucho.** La ascendencia eleva tanto la probabilidad de llevar la variante *como* el LDL (a través de la dieta y el entorno), lo que infla el efecto aparente cuando simplemente comparas portadores con no portadores; ajustar por la ascendencia recupera el efecto real. (En estos datos inventados la variante ligada en realidad no existe; con datos reales, una variable de confusión no medida sesgaría también la estimación ajustada.)
- **Las variables de confusión** (causas comunes) son aquello por lo que se ajusta. Omitir una sesga la estimación; aquí la estimación sin ajustar es más del doble del 0.5 real.
- **Las mediadoras** *no* se ajustan si quieres el efecto total de la exposición: llevan parte del efecto que intentas medir.
- **Los colisionadores** (consecuencias de ambos) no se ajustan nunca: hacerlo crea una asociación falsa entre exposición y resultado.
- **Las variables de confusión no medidas** no se pueden ajustar. Dilo de forma explícita: la estimación solo es causal si su influencia es despreciable o si puedes razonar sobre su dirección. Este supuesto no se puede comprobar con los datos, por lo que el diagrama se escribe antes del análisis.

## Compruébalo con DAGitty

El código anterior es una **heurística de primera pasada** (causas comunes de la exposición y el resultado, menos todo lo que viene después de la exposición). No es el criterio de la puerta trasera (*backdoor criterion*) completo y puede pasar por alto casos, como variables que bloquean un camino solo en combinación o sesgos inducidos por colisionadores que no encajan en este patrón sencillo.

Para cualquier cosa más grande que un diagrama pequeño, pega tus flechas en [DAGitty](https://www.dagitty.net/) (gratuito, funciona en el navegador; también disponible como paquete de R, `dagitty`). Dibuja el diagrama, enumera los conjuntos de ajuste mínimos y señala los caminos que siguen abiertos. Es también la forma más fácil de ver la imagen.

## Si algo sale mal

- **No logras decidir si hay una flecha:** conserva ambas versiones, ejecuta el análisis con cada una y comprueba si cambia la conclusión.
- **El conjunto de ajuste incluye una variable no medida:** el ajuste no puede identificar el efecto solo con estos datos. Las opciones son un mejor diseño (aleatorización), otra estrategia de identificación (un instrumento, un experimento natural) o una declaración honesta de que la estimación es solo una asociación.
- **Te tentó ajustar por todo lo disponible:** así es exactamente como se cuelan las mediadoras y los colisionadores. Ajusta por lo que dice el diagrama, nada más.
- **Diagrama dibujado después de ver los resultados:** tenderá a justificar lo que encontraste. Dibújalo antes, a partir del conocimiento del tema, idealmente con alguien que conozca la biología.
- **El objetivo es la predicción, no un efecto:** no necesitas nada de esto; consulta [Predicción vs. explicación](../prediction-vs-explanation.md).
