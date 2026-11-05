# Statistics Course for Life Scientists

A practical statistics course for master's students in the life sciences.

Each topic is a short, self-contained page. You don't need to follow the order in the side bar. Actually the best way to navigate the course is probably to go straight to the [Workflow cheatsheet](./workflow-cheatsheet.md), following the decision tree choose the topics that are more relevant to you. You can also just search any topic in the search bar and then follow the links to learn about connected topics. There's also a [Glossary](./glossary.md) for any term you don't recognize.
Also follow the setup instructions in [Set up your computer](./setup-environment.md) to get everything installed and ready for the course. And if you want create a project folder for your analyses, see [Organize your project](./project-structure.md). The course comes with a specialized AI assistant to help you with the analyses. If you want to use it, see [Work with an AI agent](./use-an-agent.md).

Throughout, we'll follow two running examples:
- **Mia**, a clinical-genetics student studying whether a variant in a cholesterol gene (LDLR) is linked to LDL cholesterol.
- **Theo**, who is testing whether a new drug lowers blood pressure.

Their stories get more specific as the modules go on, so the same concepts keep showing up in a familiar setting.

> **Suggestion** See the [Workflow cheatsheet](./workflow-cheatsheet.md) for a one-page decision-tree view of the whole process before diving into individual modules.

## Apply what you learn

The topic pages explain *why*. Where there is a practical recipe, the page ends with a **Do it yourself** box linking to a short how-to guide (steps, copy-paste Python, how to read the output, what to do if it goes wrong) and sometimes to a notebook for exploring the idea hands-on. The how-to guides contain the procedures to follow while the notebooks showcase them in action with example data. You may want to follow the guide and the notebook together as they complement each other (and of course also go back to the topic pages to refresh the concepts). The how-to guides are also listed on each module's home page. They currently cover:

- [Planning a sample size](./01-planning-your-study/how-to/plan-a-sample-size.md)
- [Exploring a dataset](./02-exploring-data/how-to/explore-a-dataset.md)
- [Running a common test](./03-hypothesis-testing/how-to/run-a-common-test.md) and [checking its assumptions](./03-hypothesis-testing/how-to/check-test-assumptions.md)
- [Running a test as a regression](./04-regression-basics/how-to/run-a-test-as-a-regression.md)
- [Drawing and using a causal diagram](./05-prediction-vs-causation/how-to/draw-and-use-a-causal-diagram.md)
- [Validating a predictive model](./06-building-models/how-to/validate-a-predictive-model.md), [checking multicollinearity](./06-building-models/how-to/check-multicollinearity.md) and [correcting measurement error](./06-building-models/how-to/handle-measurement-error.md)
- [Analyzing clustered data](./07-special-data-structures/how-to/analyze-clustered-data.md) and [running a meta-analysis](./07-special-data-structures/how-to/run-a-meta-analysis.md)

Code is Python (`pandas`, `statsmodels`, `scikit-learn`, `matplotlib`). New to running it? [Set up your computer](./setup-environment.md) walks you through installing everything on Windows, macOS or Linux, and [Organize your project](./project-structure.md) suggests how to structure an analysis. To use an AI assistant (and the statistics-advisor skill) with it, see [Work with an AI agent](./use-an-agent.md). Notebooks live in [notebooks/](./notebooks/); download one and open it in Jupyter, VS Code or Google Colab.
