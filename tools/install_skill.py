"""Install the statistics-advisor skill into an AI tool's skills folder.

Run from anywhere; the skill is found relative to this file (../statistics-advisor), so it does
not matter what the repository folder is called (for example after downloading a ZIP).

Examples:
    python3 tools/install_skill.py --tool claude              # for Claude Code, all your projects
    python3 tools/install_skill.py --tool copilot             # for VS Code chat (GitHub Copilot)
    python3 tools/install_skill.py --tool agents              # for Codex (and other tools reading ~/.agents)
    python3 tools/install_skill.py --tool claude --project ~/projects/my-first-analysis
    python3 tools/install_skill.py --tool gemini --dry-run    # show what would happen

Update: `git pull`, then run the same command again; the old copy is replaced.

Needs only the Python standard library.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

import package_skill

# tool -> (folder under your home directory, folder under a project)
TOOLS = {
    "copilot": (".copilot/skills", ".github/skills"),    # VS Code chat with GitHub Copilot
    "claude": (".claude/skills", ".claude/skills"),      # Claude Code and Claude in VS Code
    "agents": (".agents/skills", ".agents/skills"),      # Codex, and tools that read the shared folder
    "gemini": (".gemini/skills", ".gemini/skills"),      # Gemini CLI
    "cursor": (".cursor/skills", ".cursor/skills"),      # Cursor
}
IGNORED = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def destination_for(tool: str, project: pathlib.Path | None, home: pathlib.Path, skill_name: str) -> pathlib.Path:
    user_folder, project_folder = TOOLS[tool]
    base = (project / project_folder) if project is not None else (home / user_folder)
    return base / skill_name


def install(tool: str, project: pathlib.Path | None = None, home: pathlib.Path | None = None,
            dry_run: bool = False, source: pathlib.Path | None = None) -> pathlib.Path:
    """Copy the skill folder to the tool's skills folder, replacing an older copy. Returns the destination."""
    if tool not in TOOLS:
        raise ValueError(f"Unknown tool {tool!r}; choose one of: {', '.join(TOOLS)}.")
    source = source or package_skill.SKILL_ROOT
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(
            f"Cannot find SKILL.md in {source}. Run this script from inside the downloaded repository, "
            "which should contain a 'statistics-advisor' folder next to 'tools'."
        )
    fields, _ = package_skill.read_frontmatter(source / "SKILL.md")
    if project is not None and not project.is_dir():
        raise FileNotFoundError(f"The project folder {project} does not exist.")
    destination = destination_for(tool, project, home or pathlib.Path.home(), fields["name"])
    if destination.resolve() == source.resolve():
        raise ValueError("The source and destination are the same folder; nothing to do.")
    if dry_run:
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, ignore=IGNORED)
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--tool", required=True, choices=sorted(TOOLS),
                        help="which tool to install for (copilot = VS Code chat, claude = Claude Code, "
                             "agents = Codex, gemini = Gemini CLI, cursor = Cursor)")
    parser.add_argument("--project", type=pathlib.Path,
                        help="install into this project folder instead of your home folder")
    parser.add_argument("--dry-run", action="store_true", help="show the destination without copying anything")
    args = parser.parse_args(argv)
    try:
        destination = install(args.tool, args.project, dry_run=args.dry_run)
    except (ValueError, FileNotFoundError) as error:
        print(f"Cannot install the skill: {error}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"Would install the skill to: {destination}")
        return 0
    print(f"Installed the skill to: {destination}")
    print("Next: open a NEW chat in your tool (restart Gemini CLI or Codex if it does not appear) and ask a "
          "statistics question, or call the skill by name: statistics-advisor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
