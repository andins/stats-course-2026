# Organize Your Project

**In plain terms:** a statistical analysis is a small software project. Give it one folder, keep the original data untouched, keep code, results and notes in separate places, and write down how to rerun it. Six months from now (or when a reviewer asks for a change) you, or a colleague, should be able to reproduce every number and figure by running the code from the top.

This page assumes you have [set up your computer](./setup-environment.md).

## The folder layout

One folder per project, with a layout like this:

```text
my-first-analysis/
├── README.md             what the project is and how to rerun it
├── AGENTS.md             optional house rules for an AI agent (see "Work with an AI agent")
├── pyproject.toml        the libraries the project needs (made by uv)
├── uv.lock               the exact versions installed (made by uv; keep it)
├── .gitignore            files Git should not track
├── data/
│   ├── raw/              original data exactly as received: never edited
│   └── processed/        cleaned data produced by your code
├── notebooks/            01_explore.ipynb, 02_model.ipynb, ...
├── src/                  reusable code (functions) and scripts
├── results/
│   ├── figures/          plots produced by your code
│   └── tables/           tables produced by your code
└── docs/
    ├── analysis-plan.md  what you planned to do, written before looking at the data
    └── data-dictionary.md  what each column means, its units, and its allowed values
```

To create the folders, save this as `make_folders.py` in your project folder and run `uv run python make_folders.py` (or paste it into a notebook cell opened in that folder):

```python
from pathlib import Path

for folder in ["data/raw", "data/processed", "notebooks", "src", "results/figures", "results/tables", "docs"]:
    Path(folder).mkdir(parents=True, exist_ok=True)
```

You don't need all of these for a small analysis. A project with just `data/raw`, `notebooks` and `results` already beats a folder full of `final_v3_REALLY_final.xlsx`.

## The rules that matter most

1. **Never edit the raw data.** Keep the file exactly as it came from the instrument, the collaborator or the database, in `data/raw`. Do all cleaning in code that reads the raw file and writes a new file to `data/processed`. Then every change you made is visible and repeatable, and you can fix a mistake by changing a line instead of redoing it by hand in a spreadsheet.
2. **Everything is produced by code.** Every figure and table in a report should come from a notebook or script, not from copying and pasting. If you change the data or a decision, rerun and everything updates.
3. **One question, one notebook, in order.** Number the notebooks (`01_explore.ipynb`, `02_clean.ipynb`, `03_model.ipynb`) so the order of the analysis is obvious. A notebook should do one job and read its input from the previous step's output.
4. **Notebooks explore; scripts repeat.** A notebook is the right place to look at plots and try ideas. When some code is used by several notebooks, or takes a long time, move it into a function in `src/` and import it.
5. **Write down decisions.** Record which rows you excluded and why, how you handled missing values, and which analyses you ran. The count of rows dropped is something a reader will ask for. See [Missing data](./02-exploring-data/missing-data.md).
6. **Write the analysis plan before you look.** For a confirmatory analysis, put the comparison you will test, the outcome, the model and the exclusion rules in `docs/analysis-plan.md` *before* exploring the data. Later, anything you added after looking is exploratory and should be labelled that way. See [Exploratory vs. confirmatory](./02-exploring-data/exploratory-vs-confirmatory.md).

## Habits for notebooks

- **Put the settings at the top**: file paths, the random seed, thresholds, column names. Then someone can see and change them in one place.
- **Set a random seed** wherever randomness is used (`rng = np.random.default_rng(0)`, `random_state=0`), so a rerun gives the same numbers.
- **Run from the top before you trust it.** Use **Restart** and then **Run All**. A notebook that only works when its cells are run in a particular order is a bug waiting to happen.
- **Keep file paths relative to the project**, not to your computer (`C:\Users\you\...` stops working for anyone else). This snippet finds the project folder whether the notebook is in `notebooks/` or in the project root:

```python
from pathlib import Path

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "results" / "figures"

print("Project folder:", ROOT)
# df = pd.read_csv(RAW / "ldl_2024.csv")
# fig.savefig(FIGURES / "ldl_by_genotype.png", dpi=200, bbox_inches="tight")
```

- **Save outputs from code**, with descriptive names (`ldl_by_genotype.png`, not `Figure 3.png`).
- **Keep file names plain:** lowercase, no spaces, with dates as `2024-06-15` so they sort correctly.

## A README worth writing

A short `README.md` at the top of the project answers the first questions of anyone who opens it:

```text
# LDLR variant study 2024

Is a variant in the LDLR gene linked to LDL cholesterol? Lipid-clinic cohort, 15 families x 20 relatives.

## How to rerun
1. Install uv (see the course page "Set up your computer").
2. In this folder run:  uv sync
3. Open the notebooks in notebooks/ in order (01, 02, ...) and run each one.

## Data
data/raw/ldl_2024.csv  from the clinic team, received 2024-09-12, not modified.
Columns are described in docs/data-dictionary.md.

## Contact
Your name, your email.
```

## Version control with Git (optional)

This section is optional: do it only if you want to spend a bit more time learning Git.

Git records every version of your files, so you can see what changed, undo a mistake, and work with others. It is also a good backup for text files and notebooks. Install it once:

- **Windows:** `winget install --id Git.Git -e` (or download it from [git-scm.com](https://git-scm.com/)).
- **macOS:** run `git --version` in a terminal; if Git is missing, macOS offers to install it.
- **Linux:** `sudo apt install git` (Debian, Ubuntu) or `sudo dnf install git` (Fedora).

Tell Git who you are (once per computer), then start tracking the project:

```text
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

git init
git add .
git commit -m "Start the project"
```

After that, `git add .` and `git commit -m "short description of what changed"` save a new snapshot. Commit when something works, with a message that says what and why.

Create a `.gitignore` file in the project folder so Git skips what shouldn't be tracked:

```text
# the environment is rebuilt with `uv sync`; never commit it
.venv/
__pycache__/
.ipynb_checkpoints/
.DS_Store

# raw data: keep out of Git if it is large or confidential, and back it up elsewhere
# (remove this line if the data is small, public, and you want it versioned too)
data/raw/

# generated by the code, can be recreated
data/processed/
results/
```

A few cautions:

- **Never put confidential data in Git**, in particular patient data or anything under a data-sharing agreement, and never passwords or keys. A file removed from a later commit is still in the history. Keep sensitive raw data in a secure place approved by your institution, and describe in the README where it lives.
- **Do commit** `pyproject.toml` and `uv.lock`, so the environment can be rebuilt.
- **Notebook outputs can contain data** (printed tables, plots of individual records). Before sharing a notebook, clear its outputs (VS Code: **Clear All Outputs** in the notebook toolbar) unless you mean to share them.
- To keep a copy in the cloud and share with colleagues, create an empty repository on a service such as GitHub or GitLab (your institution may run its own) and follow the instructions it shows for connecting it.

## Rebuild the project on another computer

Because the project records its environment, getting going elsewhere takes a few steps: install [VS Code and uv](./setup-environment.md), get the project folder (`git clone <address>`, or copy it without `.venv`), place the raw data in `data/raw`, and run `uv sync` in the folder. Then open the notebooks and Run All.

## A few things to avoid

- **Analyzing in a spreadsheet and in code at the same time.** Pick one place where the analysis lives; use the spreadsheet only to look at or enter data.
- **Several copies of the data with different names.** If a file changes, it belongs in `data/processed` with the code that made it.
- **One giant notebook that does everything.** Split it when it stops fitting on a few screens.
- **Environments shared between projects.** A separate environment per project means upgrading a library for one analysis can never change the results of another.

---
**Previous:** [Set up your computer](./setup-environment.md) · **Next:** [Work with an AI agent →](./use-an-agent.md) · [Home](./README.md) · [Glossary](./glossary.md)
