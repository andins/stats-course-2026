# Work with an AI Agent

**In plain terms:** an AI agent is a chat assistant that can also read your project files, write code and notebooks, and run commands. The **statistics-advisor skill** is a folder of instructions that makes an agent behave like a careful statistics advisor that follows this course: it asks what kind of analysis you are doing before choosing a test, checks assumptions, reports effect sizes with intervals, and cites sources. This page shows how to get both working, with the simplest route for each common provider.

You do not need an agent to use this course. The [how-to guides](./README.md#apply-what-you-learn) work on their own. An agent helps most when you want code adapted to your own data, a second pair of eyes on your plan, or an explanation of a result.

## Before you start: four cautions

1. **Agents make mistakes, sometimes confidently.** Treat the answer as a draft from a fast assistant. Check the reasoning against the course pages, run the code yourself, and look at the plots. The skill tells the agent not to invent page numbers, but still check any reference it gives.
2. **Privacy.** Anything the agent reads is usually sent to the provider's servers. Do not give a cloud agent patient data, data under a confidentiality agreement, or unpublished results without checking your institution's rules. Safer options: describe the columns and show a few invented example rows, use an anonymized subset, or ask your institution which approved tools it offers.
3. **Stay in control.** An agent that runs commands can change or delete files. Work inside your [project folder](./project-structure.md), commit to Git before a big session, keep the approval setting on **ask first** so you see each command, and never let it touch `data/raw`.
4. **Keep learning.** Ask *why*, not just *what*. A good habit is to ask the agent to point you to the course page that explains each choice it makes.

## Step 1: Choose a tool

Plans, free allowances and model names change often, so check each provider's page for the current terms.

| If you... | Use | You need |
|---|---|---|
| already followed [Set up your computer](./setup-environment.md) and want the simplest start | **VS Code chat with GitHub Copilot** | A GitHub account. Signing in starts a free plan with a limited monthly allowance. Students and teachers can apply for free access through [GitHub Education](https://github.com/education). |
| have a Claude subscription | **Claude Code**, as a VS Code extension or in a terminal | A paid Claude plan or a Claude Console account |
| have a ChatGPT subscription | **Codex**, as a VS Code extension, in a terminal, or in the ChatGPT desktop app | A ChatGPT account |
| have a Google account and are comfortable in a terminal | **Gemini CLI** | A Google account |
| already use Cursor | **Cursor** | A Cursor account |
| can only use a web browser | **A web chat**: Claude, ChatGPT, Gemini or Copilot | An account. The Claude web app accepts the skill as an upload; for the others use the [single-file workaround](#web-chat-without-an-installed-skill). |

If you have no preference, start with **VS Code and GitHub Copilot**. Everything you installed for the course is already in place.

## Step 2: Install the skill

A *skill* is a folder with a file called `SKILL.md` and supporting files. Agents read only its short description at first, and load the full instructions when your question matches. The format is an open standard, so the same folder works in all the tools below. It only has to be in the place each tool looks.

The skill lives in the `statistics-advisor` folder of the course repository, next to the course itself. Install **only that folder**, not the whole repository: a repository copied into a skills folder has no `SKILL.md` at its top, so no skill will load. The installer below takes care of this.

### 2a. Get the repository

If you have Git (see [Organize your project](./project-structure.md#version-control-with-git-optional)), open a terminal in the folder where you keep your projects and run (replace the address with the one you were given):

```text
git clone <REPOSITORY ADDRESS>
cd stats-course-2026
```

No Git? On the repository's web page choose **Code > Download ZIP**, unzip it, and open a terminal in the unzipped folder. The folder may be called `stats-course-2026-main`; the name doesn't matter.

### 2b. Run the installer

The installer copies the skill into the right folder for your tool. It needs only Python, which you set up in [Set up your computer](./setup-environment.md). Choose the line for your tool:

| Your tool | Command |
|---|---|
| VS Code chat (GitHub Copilot) | `python3 tools/install_skill.py --tool copilot` |
| Claude Code, Claude in VS Code | `python3 tools/install_skill.py --tool claude` |
| Codex (VS Code, terminal or app) | `python3 tools/install_skill.py --tool agents` |
| Gemini CLI | `python3 tools/install_skill.py --tool gemini` |
| Cursor | `python3 tools/install_skill.py --tool cursor` |

On Windows write `py tools\install_skill.py --tool copilot` instead. If neither `python3` nor `py` is found, run it through uv: `uv run --no-project python tools/install_skill.py --tool copilot`. Add `--dry-run` to see where the skill would go without copying anything.

By default the skill is installed for **all your projects**. To install it for **one project only**, add its folder, for example `--project ~/projects/my-first-analysis`; then it is kept with that project and can be committed with it.

**To update** the skill later, run `git pull` in the repository (or download the ZIP again) and run the same installer command: it replaces the old copy.

### 2c. Or copy it by hand

The installer only copies one folder. You can do the same yourself. The skill folder is `statistics-advisor` inside the repository, and it has to end up in your tool's skills folder, still named `statistics-advisor`:

| Tool | Folder for all your projects | Or, for one project only |
|---|---|---|
| VS Code chat (Copilot) | `~/.copilot/skills/` | `.github/skills/` |
| Claude Code, Claude in VS Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex, in VS Code, terminal or app | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` or `~/.agents/skills/` | `.gemini/skills/` or `.agents/skills/` |
| Cursor | `~/.cursor/skills/` or `~/.agents/skills/` | `.cursor/skills/` or `.agents/skills/` |

`~` means your home folder (`C:\Users\<you>` on Windows). Paths starting with `.` in the last column are relative to your project folder.

**macOS and Linux**, from the repository folder (replace `.copilot` with `.claude` or `.agents` as in the table):

```text
mkdir -p ~/.copilot/skills
cp -r statistics-advisor ~/.copilot/skills/
```

**Windows** (PowerShell, from the repository folder):

```text
New-Item -ItemType Directory -Force "$HOME\.copilot\skills" | Out-Null
Copy-Item -Recurse statistics-advisor "$HOME\.copilot\skills\"
```

To update by hand, delete the old copy first (`rm -r ~/.copilot/skills/statistics-advisor`, or `Remove-Item -Recurse -Force "$HOME\.copilot\skills\statistics-advisor"` on Windows) and copy the new one.

Skills may contain scripts that an agent can run, so only install skills from sources you trust.

## Step 3: Start the agent and check it sees the skill

Open a **new** chat after installing (agents read the skill list when a session starts), with your project folder open. Then either ask,

> Which skills do you have available? Is statistics-advisor one of them?

or look for it in the tool's skill list:

| Tool | Look for the skill with | Call it explicitly with |
|---|---|---|
| VS Code chat | type `/` in the chat box | `/statistics-advisor` |
| Claude Code | type `/` | `/statistics-advisor` |
| Codex | type `$`, or `/skills` | `$statistics-advisor` |
| Gemini CLI | `/skills list` | mention it: "use the statistics-advisor skill" |
| Cursor | type `/` in Agent chat | `/statistics-advisor` |

The skill also activates **by itself** when your question is about statistics, so calling it explicitly is only needed when it doesn't. Gemini CLI asks for your confirmation the first time it activates a skill.

## Tool notes

### VS Code with GitHub Copilot

1. Hover over the Copilot icon in the status bar, choose **Use AI Features**, and sign in with GitHub.
2. Open your project folder (**File > Open Folder**). If VS Code asks whether you trust it, choose **Trust**.
3. Open the Chat view with `Ctrl+Alt+I` (`Cmd+Ctrl+I` on macOS). Click `+` for a new chat.
4. Choose **Copilot** as the session target and **Agent** as the mode, and keep permissions on **Manual** so that you approve each command or tool use.
5. Install the skill in `~/.copilot/skills/` (Step 2), start a new chat, and ask your question.

If you use the **Local** session target instead, VS Code also reads `~/.claude/skills/` and `~/.agents/skills/`, and typing `/skills` opens the skills menu.

### Claude Code

Install the **Claude Code** extension from the VS Code Extensions view (`Ctrl+Shift+X`, `Cmd+Shift+X` on macOS), then open it with the Spark icon or the **✻ Claude Code** item in the status bar, and sign in. To use it in a terminal instead, open one in your project folder and install it:

```text
# macOS, Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

Open a new terminal, then run `claude` in your project folder and follow the sign-in prompts. The skill goes in `~/.claude/skills/`. See Anthropic's [setup guide](https://code.claude.com/docs/en/setup) if something fails.

### Codex (OpenAI)

Install the OpenAI Codex extension from the VS Code Extensions view, or follow the [Codex documentation](https://developers.openai.com/codex) to use it in a terminal or the ChatGPT desktop app. Sign in with your ChatGPT account. The skill goes in `~/.agents/skills/`. If it doesn't show up, restart Codex.

### Gemini CLI

Follow the [Gemini CLI documentation](https://geminicli.com/docs/) to install it and sign in with your Google account, then run `gemini` in your project folder. Put the skill in `~/.gemini/skills/` (or `~/.agents/skills/`), then run `/skills list` to confirm and `/skills reload` after adding it.

### Cursor

Put the skill in `~/.cursor/skills/` (or `~/.agents/skills/`) and type `/` in the Agent chat to find it. Cursor also loads skills from the Claude and Codex folders.

## Web chat without an installed skill

A web chat can't read a folder on your computer, but there are two easy ways to give it the same instructions. Build both files with one command from the repository folder (it needs only Python, which you set up earlier):

```text
python3 tools/package_skill.py
```

On Windows use `py tools\package_skill.py`. If the `python3` or `py` command is not found, run it through uv instead: `uv run --no-project python tools/package_skill.py`. It creates a `dist/` folder with two files.

**The Claude web app (claude.ai):** upload `dist/statistics-advisor.zip` under **Customize > Skills** ([claude.ai/customize/skills](https://claude.ai/customize/skills)). It then works like the other tools: it activates by itself on statistics questions. On Enterprise plans an administrator must enable skills first.

**ChatGPT, Gemini, Copilot chat, or any other chat:** attach `dist/statistics-advisor-single-file.md` to a new conversation (or add it to a Project, Gem or custom assistant if your tool has those) and start with:

> Follow the attached statistics-advisor instructions for this whole conversation. Start by asking me the triage questions it describes.

This single file holds the skill's instructions and its four reference documents. Two limits apply. The chat cannot run your files or the helper scripts, so it will write code for you to paste into a notebook and run yourself. And it can only work with what you tell it, so describe your columns, units and study design instead of uploading confidential data.

## Using the skill well

### Tell it the things it needs to know

The skill's first job is to ask whether your data is already collected, whether the question was decided before you saw the data, and whether you want prediction or a causal answer. You will get a better first answer if you say these up front:

- **The question** in plain words, and what you plan to decide with the answer.
- **The study design:** how the data was collected, whether the exposure was randomized, how many units, whether there are repeated measurements or groups.
- **The data:** the file name, the columns that matter and their units, how much is missing.
- **What you want back:** an explanation, a recommendation, or a notebook in your `notebooks/` folder.

### Example prompts

- *Planning:* "I'm planning a study of an LDLR gene variant and LDL cholesterol, 15 families, 20 relatives each. How many families do I need? Use the statistics-advisor skill."
- *Exploring:* "I have `data/raw/ldl_2024.csv`. I don't have a specific hypothesis yet. Help me explore it. Create a notebook in `notebooks/` and do not modify the raw file."
- *Choosing a test:* "I decided before collecting data to compare blood pressure before and after treatment in 40 patients. Which analysis, and what assumptions do I need to check?"
- *Causal:* "I want to know whether carrying a gene variant affects LDL cholesterol, but nobody assigned the genotypes and carriers differ in ancestry and in who got tested. Walk me through what I need to adjust for."
- *Checking my work:* "Here is my analysis plan and results. What did I miss? Check assumptions, multiple comparisons, and missing data."
- *Understanding:* "Explain what a confidence interval for a regression slope means, and point me to the relevant course page."

### What a good reply looks like

The skill is working if the agent:

- **asks** which kind of analysis this is before recommending a test, when that isn't clear;
- starts with a **short plain-language answer**, then gives details;
- **lists the assumptions** and says how to check each;
- reports an **estimate with a confidence interval**, not just "significant";
- warns about **exploratory p-values, multiple comparisons, missing data** when relevant;
- **cites sources** and says so when it is not sure;
- offers to build a **notebook** and names the matching **course pages** (module and title; look them up in the course's sidebar search), so you can follow the reasoning.

If it jumps straight to a p-value, say: "Use the statistics-advisor skill and start with the triage questions."

### Give the agent house rules for your project

Most agents read a short instructions file from the project folder (`AGENTS.md` for VS Code, Codex and others; `CLAUDE.md` for Claude Code; `GEMINI.md` for Gemini CLI). A few lines prevent the most common problems. Save this as `AGENTS.md` (and a copy named `CLAUDE.md` if you use Claude Code), and edit it for your project:

```text
# Project instructions

- Run all Python with `uv run`. Add libraries with `uv add <name>`; never install packages globally.
- data/raw/ is read-only: never edit, move or delete files there. Write cleaned data to data/processed/.
- Notebooks go in notebooks/ (numbered 01_, 02_, ...), figures in results/figures/, tables in results/tables/.
- Use relative paths and set random seeds.
- Report effect sizes with confidence intervals, state assumptions and how they were checked,
  and say how many rows were dropped for missing data.
- Ask me before assuming anything about the study design.
- Ask before running any command that deletes files or changes Git history.
```

If your tool doesn't read such a file, paste the same lines at the start of the chat.

### Review what the agent produces

- **Read the code** before you trust it, and run notebooks from the top (**Restart**, then **Run All**).
- **Make sure it uses your project's environment:** `uv run`, or the `.venv` kernel in VS Code. If you see `ModuleNotFoundError`, that is the usual cause.
- **Compare with the course:** the matching how-to guide shows the standard recipe. If the agent does something different, ask why.
- **Look at the data yourself.** Plots catch problems no summary does (see [How to: explore a dataset](./02-exploring-data/how-to/explore-a-dataset.md)).
- **Keep the record:** commit to Git after each working step, and write down the decisions you and the agent made in `docs/`.

## Troubleshooting

| Problem | What to try |
|---|---|
| The skill isn't listed | Check that the folder is named exactly `statistics-advisor` and that `SKILL.md` sits directly inside it. The usual mistake is copying the whole repository (or a second `statistics-advisor` folder inside the first) instead of the `statistics-advisor` folder within it; the installer (`tools/install_skill.py`) avoids this. Then open a new chat; in Gemini CLI run `/skills reload`; in Codex, restart it. |
| The skill is listed but the agent ignores it | Call it explicitly (`/statistics-advisor`, or `$statistics-advisor` in Codex), or start your message with "Use the statistics-advisor skill". |
| It says it cannot read or run files | You are probably in a web chat, or the tool's file and command permissions are off. Use the single-file route and run the code yourself, or open your project folder in VS Code. |
| The installer says it cannot find `SKILL.md` | Run it from inside the downloaded repository: the `tools` folder and the `statistics-advisor` folder must sit side by side. If you moved `install_skill.py` somewhere else, move it back. |
| `ModuleNotFoundError` when the agent runs code | Ask it to use `uv run`, or select the project's `.venv` kernel. Don't let it install packages globally. |
| The agent asks to run a command you don't understand | Say no and ask it to explain. You can always approve commands one at a time. |
| A reference or page number looks invented | Check it against `references/core-references.md` in the skill folder, or the original source. Ask the agent to say what it is unsure of. |
| You hit the provider's usage limit | Wait for the allowance to renew, switch tools (the same skill folder works in several), or use the how-to guides, which need no agent. |
| Download or sign-in errors on a university or company network | These are usually certificate or proxy settings. See the provider's network documentation, or ask your IT team. |

---
**Previous:** [Organize your project](./project-structure.md) · [Home](./README.md) · [Glossary](./glossary.md)
