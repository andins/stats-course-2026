# Multicolinealidad

**En pocas palabras:** si dos de tus predictores están muy correlacionados entre sí, un modelo puede tener dificultades para distinguir sus efectos individuales, aunque siga prediciendo la variable de respuesta perfectamente bien en conjunto.

## Una imagen concreta

Supón que Mia registra los genotipos de dos variantes, A y B, que están muy próximas en el mismo cromosoma. Las variantes tan cercanas tienden a heredarse juntas (un patrón llamado **desequilibrio de ligamiento**, *linkage disequilibrium*, LD), de modo que el número de copias de A y de B acaba estando casi perfectamente correlacionado entre sus pacientes. Una regresión que intente estimar los efectos separados de la variante A y de la variante B sobre el colesterol LDL tendrá problemas: los datos no contienen muchas personas que lleven una sin la otra, así que queda poca información para distinguir entre "el LDL responde específicamente a la variante A" y "el LDL responde específicamente a la variante B". Las estimaciones de los coeficientes individuales se vuelven inestables: pequeños cambios en los datos pueden dispararlas o incluso invertir su signo.

## Qué estropea y qué no

- **Lo que estropea**: la confianza en cualquier coeficiente *individual* y en su error estándar/intervalo de confianza, que dejan de ser fiables.
- **Lo que no estropea**: el ajuste global del modelo y sus predicciones. Un modelo con multicolinealidad grave puede seguir prediciendo bien el LDL; lo único que no puede es decirte con fiabilidad *cuál* de los dos predictores solapados "hace el trabajo".

Esto significa que la multicolinealidad importa sobre todo cuando tu objetivo es **interpretar coeficientes individuales** (un uso explicativo/causal), y importa mucho menos cuando tu único objetivo es la **predicción**.

## Cómo comprobarla: el VIF

El **factor de inflación de la varianza** (*Variance Inflation Factor*, VIF) cuantifica, para cada predictor, cuánto se infla su incertidumbre por su correlación con los demás predictores. Un VIF cercano a 1 indica que no hay problema; por convención, un VIF superior a 5 merece una revisión más atenta y uno superior a 10 es una señal de alarma clara. Trata estos valores como orientaciones aproximadas, no como umbrales estrictos.

## Qué hacer al respecto

- Elimina uno de los predictores solapados, si miden la misma realidad subyacente.
- Combínalos en una única variable compuesta, si tiene sentido desde el punto de vista sustantivo.
- Recoge más datos, o datos distintos, en los que los predictores varíen con más independencia entre sí, si es factible.
- O, si el verdadero objetivo es la predicción (no la interpretación), plantéate dejarlo tal cual y usar en su lugar la [regularización](./overfitting-and-regularization.md), que maneja los predictores correlacionados mejor que la regresión simple.

> **Hazlo tú mismo**
>
> [Cómo: comprobar la multicolinealidad](./how-to/check-multicollinearity.md) — calcula e interpreta los VIF en unas pocas líneas de Python.

> **Para saber más**
>
> - [James, Witten, Hastie & Tibshirani (2021)](https://www.statlearning.com/), *An Introduction to Statistical Learning* (2.ª ed.), §3.3.3 "Potential Problems", el apartado "Collinearity" (pp. 100–103), que incluye el VIF.
> - O'Brien (2007), "A caution regarding rules of thumb for variance inflation factors," *Quality & Quantity* 41(5), 673–690 — por qué los umbrales de VIF de 5 o 10 son heurísticos.
> - McElreath (2020), *Statistical Rethinking* (2.ª ed.), cap. 6, §6.1 "Multicollinearity".

---
**Anterior:** [Validación cruzada y revisión del modelo](./cross-validation-and-model-checking.md) · [Inicio del módulo](./README.md) · **Siguiente:** [Error de medición →](./measurement-error.md) · [Glosario](../glossary.md)
