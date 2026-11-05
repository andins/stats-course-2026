# Guía rápida del flujo de trabajo

Un mapa de una página de todo el proceso de decisión: la misma lógica que sigue el flujo de trabajo de la skill `statistics-advisor`, dibujada para que veas todo el recorrido de un vistazo. En el curso HTML generado, el mapa se redibuja en un formato ancho con una banda por paso, y cada recuadro es un enlace a su página explicativa (también funcionan Tab y Enter). En las vistas previas de Markdown simples, el diagrama se muestra como un diagrama de flujo de Mermaid y los enlaces de los nodos no se resuelven: usa los identificadores de los nodos (A, B, C, ...) para cruzar referencias si lo necesitas.

```mermaid
flowchart TD
    subgraph S0["Paso 0 — Fase de diseño"]
        A{"A: ¿Ya se han recogido\nlos datos?"}
        A -->|No| B["B: Planifica el tamaño muestral:\npotencia (prueba) o precisión (ancho del IC)"]
        B --> B1["B1: Reduce el ruido de medición desde el principio\n+ comprueba que se registran todas las variables relevantes"]
    end

    A -->|"Sí"| C

    subgraph S1["Paso 1 — ¿Exploratorio o confirmatorio?"]
        C{"C: ¿Exploratorio o\nconfirmatorio?"}
        C -->|Exploratorio| D["D: Primero EDA:\nvisualiza antes de contrastar nada"]
        C -->|Confirmatorio| F["F: Elige la prueba,\ncomprueba sus supuestos"]
        F --> F1{"F1: ¿Causal (efecto de una exposición/tratamiento)\no descriptivo (p. ej., un control de calidad/especificación)?"}
    end

    D --> E
    F1 -->|"Comparación descriptiva\n"| Z1(["Z1: Informa de la estimación + IC\n(fin)"])
    F1 -->|"Causal"| H

    subgraph S2["Paso 2 — ¿Predicción o causalidad?"]
        E{"E: ¿Predicción o\ninterpretación causal?"}
        E -->|Predicción| G["G: Modelado predictivo:\nvalidación fuera de muestra, regularización"]
        E -->|Causal| H{"H: ¿Se asignó la exposición mediante un\nexperimento bien diseñado?"}
        H -->|Sí| I["I: Modo causal experimental:\nsin ajustar, o + covariables de precisión"]
        H -->|No| J["J: Construye un DAG causal\ncon el usuario"]
        J --> K["K: Modo causal observacional:\najusta por el conjunto que identifica el DAG"]
    end

    subgraph S3["Paso 3 — Modelar y comprobar"]
        L["L: Comprueba: multicolinealidad, error de medición,\nagrupamiento / dependencia temporal, datos faltantes"]
    end

    G --> L
    I --> L
    K --> L
    L -->|"Modo predictivo"| Z3(["Z3: Sirve predicciones con datos nuevos\n(fin)"])
    L -->|"Modo causal"| Z2(["Z2: Informa de la estimación del tamaño del efecto + IC\n(fin)"])

    B1 -.->|"una vez recogidos"| C

    classDef decision fill:#fde68a,stroke:#b45309,color:#1c1917,stroke-width:1.5px;
    classDef process fill:#bfdbfe,stroke:#1d4ed8,color:#1c1917,stroke-width:1.5px;
    classDef terminal fill:#bbf7d0,stroke:#15803d,color:#1c1917,stroke-width:1.5px;
    class A,C,F1,E,H decision;
    class B,B1,D,F,G,I,J,K,L process;
    class Z1,Z2,Z3 terminal;
    style S0 fill:#eef2ff,stroke:#c7d2fe,color:#1e1b4b
    style S1 fill:#fefce8,stroke:#fde68a,color:#422006
    style S2 fill:#ecfdf5,stroke:#a7f3d0,color:#022c22
    style S3 fill:#fdf4ff,stroke:#f0abfc,color:#4a044e

    click A "01-planning-your-study/README.md" "1. Planificar tu estudio"
    click B "01-planning-your-study/sample-size-and-power.md" "Tamaño muestral y potencia"
    click B1 "01-planning-your-study/design-considerations.md" "Consideraciones de diseño: ruido de medición y cobertura de variables"
    click C "02-exploring-data/exploratory-vs-confirmatory.md" "Exploratorio vs. confirmatorio"
    click D "02-exploring-data/eda-basics.md" "Fundamentos del EDA"
    click F "03-hypothesis-testing/README.md" "3. Contraste de hipótesis"
    click F1 "03-hypothesis-testing/README.md" "3. Contraste de hipótesis"
    click E "05-prediction-vs-causation/prediction-vs-explanation.md" "Predicción vs. explicación"
    click G "06-building-models/cross-validation-and-model-checking.md" "Validación cruzada y revisión del modelo"
    click H "05-prediction-vs-causation/experiments-vs-observational-data.md" "Experimentos vs. datos observacionales"
    click I "05-prediction-vs-causation/experiments-vs-observational-data.md" "Experimentos vs. datos observacionales"
    click J "05-prediction-vs-causation/causal-diagrams.md" "Diagramas causales"
    click K "05-prediction-vs-causation/causal-diagrams.md" "Diagramas causales"
    click L "06-building-models/multicollinearity.md" "Multicolinealidad (véase también: error de medición, datos agrupados/series temporales, datos faltantes)"
    click Z1 "03-hypothesis-testing/p-values-and-significance.md" "Valores p y significación"
    click Z2 "03-hypothesis-testing/p-values-and-significance.md" "Valores p y significación"
    click Z3 "06-building-models/cross-validation-and-model-checking.md" "Validación cruzada y revisión del modelo"
```

## Reglas generales que se aplican en todos los nodos

- **Empieza por la estimación y su intervalo de confianza**, no por un veredicto escueto de significativo/no significativo; esto vale incluso en la mejor rama posible, la confirmatoria/experimental. Consulta [Valores p y significación](./03-hypothesis-testing/p-values-and-significance.md).
- **Los errores de la fase de diseño (ruido, variables que faltan) no se arreglan después con un modelo mejor**: acierta con la elección del instrumento y con la cobertura de variables antes de recoger los datos. Consulta [Consideraciones de diseño](./01-planning-your-study/design-considerations.md).
- **Un modelo que ajusta bien no es automáticamente causal**: las afirmaciones causales necesitan una estrategia de identificación (experimento o ajuste basado en un DAG), no solo un buen ajuste. Consulta [Predicción vs. explicación](./05-prediction-vs-causation/prediction-vs-explanation.md).
- **Un modelo predictivo no está terminado cuando valida bien**: el paso final es servir sus predicciones con datos realmente nuevos, y ese entorno de despliegue debería seguir comprobándose frente al rendimiento fuera de muestra con el que se validó. Consulta [Validación cruzada y revisión del modelo](./06-building-models/cross-validation-and-model-checking.md).
- **Un solo estudio rara vez es la última palabra**: cuando varios estudios responden a la misma pregunta, combina sus *estimaciones* (no sus veredictos de significativo/no significativo), indica cuánto discrepan y cómo se seleccionaron y qué puede faltar. Consulta [Metaanálisis](./07-special-data-structures/meta-analysis.md) y [Metaanálisis: sesgos y trampas](./07-special-data-structures/meta-analysis-pitfalls.md).

---
**Anterior:** [Inicio](./README.md) · [Glosario](./glossary.md)
