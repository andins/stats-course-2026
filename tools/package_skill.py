"""Package the statistics-advisor skill for tools that can't read the skill folder directly.

Run from anywhere; the skill is found relative to this file (../statistics-advisor). Two outputs
are written to `dist/` at the repository root (or to --out):

- statistics-advisor.zip: the skill as a zip with the skill folder at its root, ready to upload
  in the Claude web app (Customize > Skills). Contains SKILL.md, references/ and the Python
  helper scripts.
- statistics-advisor-single-file.md: SKILL.md plus its reference files in one markdown file, to
  attach to a chat in tools without skill support (ChatGPT, Gemini, Copilot or Claude chat
  without Skills, ...). The helper scripts can't be bundled in a single text file.

Usage:
    python3 tools/package_skill.py [--out DIR]

Needs only the Python standard library.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import zipfile

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_ROOT = REPO_ROOT / "statistics-advisor"
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Files that never belong in a package, wherever they are found.
EXCLUDED_NAMES = {"__pycache__", ".DS_Store", "dist", ".git"}
SINGLE_FILE_REFERENCES = [
    "analysis-triage.md", "test-regression-equivalents.md", "core-references.md", "course-topics.md",
]
ZIP_TIMESTAMP = (2020, 1, 1, 0, 0, 0)   # fixed, so rebuilding gives an identical zip


def read_frontmatter(skill_md: pathlib.Path) -> tuple[dict[str, str], str]:
    """Return (name/description fields, markdown body). Validates the Agent Skills limits."""
    text = skill_md.read_text()
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"{skill_md} does not start with YAML frontmatter.")
    fields: dict[str, str] = {}
    for key in ("name", "description"):
        found = re.search(rf"^{key}:\s*(.+)$", match.group(1), re.MULTILINE)
        if not found:
            raise ValueError(f"{skill_md}: frontmatter has no '{key}'.")
        value = found.group(1).strip()
        if value[:1] == value[-1:] and value[:1] in ("'", '"'):
            value = value[1:-1].replace("''", "'")
        fields[key] = value
    if len(fields["name"]) > 64 or not NAME_RE.match(fields["name"]):
        raise ValueError(f"Invalid skill name {fields['name']!r}: use lowercase letters, digits and single hyphens (max 64).")
    if not 1 <= len(fields["description"]) <= 1024:
        raise ValueError(f"The description is {len(fields['description'])} characters; the Agent Skills limit is 1024.")
    return fields, text[match.end():]


def skill_files(root: pathlib.Path = SKILL_ROOT) -> list[pathlib.Path]:
    """Every file that goes into the zip, as paths relative to the skill folder, sorted."""
    return [
        path.relative_to(root)
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and not any(part in EXCLUDED_NAMES for part in path.relative_to(root).parts)
        and path.suffix != ".pyc"
    ]


def build_zip(out_dir: pathlib.Path, root: pathlib.Path = SKILL_ROOT) -> pathlib.Path:
    fields, _ = read_frontmatter(root / "SKILL.md")
    target = out_dir / f"{fields['name']}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for relative in skill_files(root):
            info = zipfile.ZipInfo(f"{fields['name']}/{relative.as_posix()}", ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, (root / relative).read_bytes())
    return target


def build_single_file(out_dir: pathlib.Path, root: pathlib.Path = SKILL_ROOT) -> pathlib.Path:
    fields, body = read_frontmatter(root / "SKILL.md")
    parts = [
        f"# {fields['name']}: instructions for a statistics advisor\n",
        "You are a statistics advisor. Follow the instructions in this file for the whole conversation.\n",
        "Notes on this single-file version:\n"
        "- Links such as `./references/analysis-triage.md` point to the sections named "
        "\"Reference file: ...\" at the end of this file.\n"
        "- The Python helper scripts mentioned in the instructions are not included. When the instructions point "
        "to a script, write equivalent code yourself (pandas, statsmodels, scikit-learn, scipy, matplotlib) "
        "and show it to the user, who will run it.\n"
        "- You cannot see the user's files. Ask for column names, units, a few example rows and the study "
        "design instead of guessing, and remind the user not to paste confidential data.\n",
        "---\n",
        f"## Instructions (SKILL.md)\n\n{body.strip()}\n",
    ]
    for name in SINGLE_FILE_REFERENCES:
        reference = (root / "references" / name).read_text().strip()
        parts.append(f"---\n\n## Reference file: references/{name}\n\n{reference}\n")
    target = out_dir / f"{fields['name']}-single-file.md"
    target.write_text("\n".join(parts))
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=pathlib.Path, default=REPO_ROOT / "dist", help="output folder (default: dist/)")
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        outputs = [build_zip(args.out), build_single_file(args.out)]
    except (ValueError, FileNotFoundError) as error:
        print(f"Cannot package the skill: {error}", file=sys.stderr)
        return 1
    for path in outputs:
        print(f"{path}  ({path.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
