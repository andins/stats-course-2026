# Set Up Your Computer

**In plain terms:** to run the notebooks and the code in the how-to guides you need three things: a place to write and run code, Python with a handful of statistics libraries, and a way to keep those libraries separate for each project. This page gets you there from a clean computer, on Windows, macOS or Linux, in about 30 minutes. You only do it once.

We use two tools:

- **VS Code**, a free editor that can also run notebooks.
- **uv**, a free tool that installs Python for you and keeps each project's libraries in its own isolated environment. You don't have to install Python separately, and nothing you do here can break another project or your system.

If you would rather not install anything, see [No installation: Google Colab](#no-installation-google-colab) at the end. For how to organize the folders of an analysis once you are set up, see [Organize your project](./project-structure.md). To get an AI assistant to help with the analysis, see [Work with an AI agent](./use-an-agent.md).

## What you will end up with

- VS Code with the Python and Jupyter extensions.
- A project folder containing a Python 3.12 environment with `numpy`, `pandas`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn` and `jupyterlab`: everything the course's notebooks and how-to guides use.
- A file (`uv.lock`) that records the exact versions installed, so the same environment can be rebuilt on any computer.

## Step 1: Install VS Code

Download the installer for your system from [code.visualstudio.com](https://code.visualstudio.com/) and run it. If you prefer the command line:

**Windows** (in PowerShell):

```text
winget install --id Microsoft.VisualStudioCode -e
```

**macOS:** open the downloaded file and drag *Visual Studio Code* to the *Applications* folder. If you use Homebrew: `brew install --cask visual-studio-code`.

**Linux:** on Debian or Ubuntu, download the `.deb` file from the website and install it with `sudo apt install ./<file>.deb`. Many distributions also offer `sudo snap install --classic code`. For Fedora and other systems, follow the [official Linux instructions](https://code.visualstudio.com/docs/setup/linux).

Then open VS Code, click the **Extensions** icon in the left bar (or press `Ctrl+Shift+X`, `Cmd+Shift+X` on macOS) and install two extensions, both published by Microsoft: **Python** and **Jupyter**.

## Step 2: Open a terminal and install uv

A terminal is a window where you type commands. Open one:

- **Windows:** open the Start menu, type *PowerShell*, and open it.
- **macOS:** press `Cmd+Space`, type *Terminal*, and press Enter.
- **Linux:** press `Ctrl+Alt+T` on most desktops, or search for *Terminal*.

Then install uv.

**Windows** (PowerShell):

```text
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatively: `winget install --id=astral-sh.uv -e`.

**macOS and Linux:**

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On a very minimal Linux installation `curl` may be missing; install it first (`sudo apt install curl` on Debian or Ubuntu), or use `wget -qO- https://astral.sh/uv/install.sh | sh`. On macOS with Homebrew, `brew install uv` also works.

**Close the terminal and open a new one**, then check that it worked:

```text
uv --version
```

It should print a version number. If it says the command isn't found, see [Troubleshooting](#troubleshooting).

## Step 3: Create a project and its environment

These commands are the same on every system. They create a folder for your first analysis, tell uv to use Python 3.12, and install the libraries into an environment that belongs to that folder only.

```text
cd ~
mkdir projects
cd projects
mkdir my-first-analysis
cd my-first-analysis

uv init --bare
uv python pin 3.12
uv add numpy pandas scipy statsmodels scikit-learn matplotlib seaborn jupyterlab
```

The first run downloads Python and the libraries, which takes a few minutes. Afterwards the folder contains:

| File or folder | What it is |
|---|---|
| `pyproject.toml` | The list of libraries your project needs. |
| `uv.lock` | The exact versions installed. Keep it: it makes the environment reproducible. |
| `.python-version` | The Python version the project uses. |
| `.venv/` | The environment itself. Never edit it by hand, and don't copy it between computers; rebuild it with `uv sync` instead. |

The same package list is also in [requirements.txt](./notebooks/requirements.txt). If you have that file in the project folder, `uv add -r requirements.txt` does the same as the long `uv add` command above.

Keep your projects somewhere simple such as `projects` in your home folder. Folders synced by OneDrive, Dropbox or iCloud can slow down or cause conflicts with the thousands of small files in an environment. To back up and share work, use [Git](./project-structure.md#version-control-with-git-optional) instead.

## Step 4: Open the project in VS Code and run a notebook

1. In VS Code choose **File > Open Folder** and select `my-first-analysis`.
2. Create a folder called `notebooks` in it (right-click in the file list, *New Folder*).
3. Download a notebook from the course, for example the [measurement error notebook](./notebooks/measurement-error-attenuation.ipynb), and save it in that `notebooks` folder.
4. Open the notebook in VS Code. Click **Select Kernel** at the top right, choose **Python Environments**, then the entry that mentions `.venv` and Python 3.12.
5. Click **Run All**. The plots and tables appear under the cells.

Prefer the browser? In the project folder run `uv run jupyter lab`; it opens JupyterLab with the same environment.

## Step 5: Check that everything is installed

In a new notebook cell (or any notebook), run:

```python
import sys
import numpy, pandas, scipy, statsmodels, sklearn, matplotlib, seaborn

print("Python", sys.version.split()[0])
for module in (numpy, pandas, scipy, statsmodels, sklearn, matplotlib, seaborn):
    print(f"{module.__name__:12s} {module.__version__}")
```

You should see a Python 3.12 version and a version number for each library, with no error. The course code was tested with Python 3.12 and recent library versions (for example pandas 3.1, scipy 1.18, statsmodels 0.15, scikit-learn 1.9).

To run a script from the terminal instead of a notebook, use `uv run python my_script.py` inside the project folder; uv always uses the project's own environment.

## Later: add a library, or rebuild on another computer

- **Add a library:** `uv add <package-name>`. For the optional Bayesian examples: `uv add pymc bambi arviz` (these are large; install them only if you need them).
- **Rebuild the same environment** on a new computer or after a clean install: install VS Code and uv (steps 1 and 2), copy the project folder *without* `.venv`, and run `uv sync` inside it.
- **Update the libraries:** `uv lock --upgrade` and then `uv sync`. Do this between projects, not in the middle of an analysis, since new versions can change results slightly.

## Troubleshooting

| Problem | What to do |
|---|---|
| `uv: command not found` (or "not recognized") right after installing | Close the terminal and open a new one; the installer changes the search path only for new terminals. If it still fails, restart the computer. |
| `invalid peer certificate: UnknownIssuer` or another certificate error while downloading | Typical on company or university networks that inspect secure traffic. Tell uv to use the system's certificates: `export UV_SYSTEM_CERTS=1` (macOS, Linux) or `$env:UV_SYSTEM_CERTS = "1"` (Windows PowerShell), then repeat the command. Older uv versions call it `UV_NATIVE_TLS`. |
| Downloads time out or fail on a network that requires a proxy | Ask your IT team for the proxy address and set `HTTPS_PROXY` to it. |
| `ModuleNotFoundError: No module named 'pandas'` in a notebook | The notebook is using the wrong kernel. Click **Select Kernel** and choose the `.venv` of your project. |
| The `.venv` kernel is not listed in VS Code | Press `Ctrl+Shift+P` (`Cmd+Shift+P` on macOS), run **Python: Select Interpreter**, and choose the `.venv` entry. If it is missing, check that you opened the *project folder* (the one containing `pyproject.toml`) in VS Code. |
| You cannot install software on your computer | Ask IT to install VS Code and uv, or use Google Colab (below). |
| Plots do not appear in a script run from the terminal | Notebooks show plots automatically; scripts need `plt.show()` at the end, or `plt.savefig("figure.png")`. |

## If you cannot or do not want to use uv

The classic route works too: install Python 3.12 or newer, create an environment with Python's built-in `venv`, and install the libraries with `pip`, using the course's [requirements.txt](./notebooks/requirements.txt).

**Windows:** download Python from [python.org](https://www.python.org/downloads/) and tick *Add python.exe to PATH* in the installer. Then, in PowerShell inside your project folder:

```text
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell refuses to run the activation script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

**macOS and Linux:** you need `python3` version 3.12 or newer. The one that comes with macOS is often too old, so install a current one from [python.org](https://www.python.org/downloads/) or Homebrew; on Debian or Ubuntu you may also need `sudo apt install python3-venv`:

```text
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

In VS Code, select the `.venv` interpreter as described in step 4. You lose the lockfile, so record what you installed with `pip freeze > requirements-frozen.txt` once your analysis works.

## No installation: Google Colab

[Google Colab](https://colab.research.google.com/) runs notebooks in your browser with `numpy`, `pandas`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib` and `seaborn` already available. Open Colab, choose **File > Upload notebook**, and select a course notebook. It is a good way to try things out, but your files disappear when the session ends unless you save them to Google Drive, and you should **not upload confidential or patient data** to it without checking your institution's rules.

---
**Next:** [Organize your project](./project-structure.md) · [Home](./README.md) · [Glossary](./glossary.md)
