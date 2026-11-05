# Workflow Cheatsheet

A one-page map of the whole decision process — the same logic the `statistics-advisor` skill's workflow follows, drawn out so you can see the whole arc at a glance. In the generated HTML course the map is redrawn in a wide layout with one band per step, and every box is a link to its explainer page (Tab and Enter work too). In plain markdown previews the diagram renders as a Mermaid flowchart instead, and the node links won't resolve — use the node IDs (A, B, C, ...) to cross-reference if needed.

```mermaid
flowchart TD
    subgraph S0["Step 0 — Design phase"]
        A{"A: Has data already\nbeen collected?"}
        A -->|No| B["B: Plan sample size:\npower (test) or precision (CI width)"]
        B --> B1["B1: Reduce measurement noise upfront\n+ check all relevant variables are recorded"]
    end

    A -->|"Yes"| C

    subgraph S1["Step 1 — Exploratory or confirmatory?"]
        C{"C: Exploratory or\nconfirmatory?"}
        C -->|Exploratory| D["D: EDA first:\nvisualize before testing anything"]
        C -->|Confirmatory| F["F: Pick the test,\ncheck its assumptions"]
        F --> F1{"F1: Causal (exposure/treatment's\neffect) or descriptive (e.g. a QC/spec check)?"}
    end

    D --> E
    F1 -->|"Descriptive comparison\n"| Z1(["Z1: Report the estimate + CI\n(done)"])
    F1 -->|"Causal"| H

    subgraph S2["Step 2 — Prediction or causal?"]
        E{"E: Prediction or\ncausal interpretation?"}
        E -->|Prediction| G["G: Predictive modeling:\nout-of-sample validation, regularization"]
        E -->|Causal| H{"H: Was the exposure assigned by a\nwell-designed experiment?"}
        H -->|Yes| I["I: Experimental causal mode:\nunadjusted, or + precision covariates"]
        H -->|No| J["J: Build a causal DAG\nwith the user"]
        J --> K["K: Observational causal mode:\nadjust for the DAG-identified set"]
    end

    subgraph S3["Step 3 — Model & check"]
        L["L: Check: multicollinearity, measurement error,\nclustering / time-dependence, missing data"]
    end

    G --> L
    I --> L
    K --> L
    L -->|"Predictive mode"| Z3(["Z3: Serve predictions on new data\n(done)"])
    L -->|"Causal mode"| Z2(["Z2: Report the effect-size estimate + CI\n(done)"])

    B1 -.->|"once collected"| C

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

    click A "01-planning-your-study/README.md" "Planning your study"
    click B "01-planning-your-study/sample-size-and-power.md" "Sample size and power"
    click B1 "01-planning-your-study/design-considerations.md" "Design considerations: measurement noise & variable coverage"
    click C "02-exploring-data/exploratory-vs-confirmatory.md" "Exploratory vs. confirmatory"
    click D "02-exploring-data/eda-basics.md" "EDA basics"
    click F "03-hypothesis-testing/README.md" "Hypothesis testing"
    click F1 "03-hypothesis-testing/README.md" "Hypothesis testing"
    click E "05-prediction-vs-causation/prediction-vs-explanation.md" "Prediction vs. explanation"
    click G "06-building-models/cross-validation-and-model-checking.md" "Cross-validation and model checking"
    click H "05-prediction-vs-causation/experiments-vs-observational-data.md" "Experiments vs. observational data"
    click I "05-prediction-vs-causation/experiments-vs-observational-data.md" "Experiments vs. observational data"
    click J "05-prediction-vs-causation/causal-diagrams.md" "Causal diagrams"
    click K "05-prediction-vs-causation/causal-diagrams.md" "Causal diagrams"
    click L "06-building-models/multicollinearity.md" "Multicollinearity (also see: measurement error, clustered/time-series data, missing data)"
    click Z1 "03-hypothesis-testing/p-values-and-significance.md" "P-values and significance"
    click Z2 "03-hypothesis-testing/p-values-and-significance.md" "P-values and significance"
    click Z3 "06-building-models/cross-validation-and-model-checking.md" "Cross-validation and model checking"
```

## Rules of thumb that apply at every node

- **Lead with the estimate and its confidence interval**, not a bare significant/non-significant verdict — true even in the best-case confirmatory/experimental branch. See [P-values and significance](./03-hypothesis-testing/p-values-and-significance.md).
- **Design-phase mistakes (noise, missing variables) can't be fixed by a better model later** — get instrument choice and variable coverage right before collecting data. See [Design considerations](./01-planning-your-study/design-considerations.md).
- **A well-fitting model is not automatically a causal one** — causal claims need an identification strategy (experiment or DAG-based adjustment), not just good fit. See [Prediction vs. explanation](./05-prediction-vs-causation/prediction-vs-explanation.md).
- **A predictive model isn't done once it validates well** — the final step is serving its predictions on genuinely new data, and that deployment setting should keep being checked against the out-of-sample performance it was validated on. See [Cross-validation and model checking](./06-building-models/cross-validation-and-model-checking.md).
- **One study is rarely the last word** — when several studies answer the same question, combine their *estimates* (not their significant/non-significant verdicts), report how much they disagree, and say how they were selected and what may be missing. See [Meta-analysis](./07-special-data-structures/meta-analysis.md) and [Meta-analysis: bias and pitfalls](./07-special-data-structures/meta-analysis-pitfalls.md).

---
**Previous:** [Home](./README.md) · [Glossary](./glossary.md)
