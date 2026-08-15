"""Generate and validate the Beamer skills section of the repository README."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT.parent / "README.md"
CATALOG = ROOT / "catalog" / "skills.json"
START = "### beamer-skills/"
END = "### economics/"


def load_entries():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def render(entries):
    tree = [
        "beamer-skills/          Beamer & LaTeX/TikZ skills",
    ]
    for index, entry in enumerate(entries):
        branch = "├──"
        tree.append(f"{branch} {entry['id']}")
    tree.extend([
        "├── tests/verify-tikz-layout",
        "└── docs/superpowers",
    ])

    table = [
        "### beamer-skills/",
        "",
        "| Skill | Description | Creator / Source |",
        "|-------|-------------|------------------|",
    ]
    table.extend(
        f"| [**{entry['id']}**]({entry['link']}) | {entry['description']} | {entry['creator']} |"
        for entry in entries
    )
    return tree, table


def replace_readme(text, entries):
    tree, table = render(entries)
    structure_start = text.index("beamer-skills/          Beamer & LaTeX/TikZ skills")
    structure_end = text.index("economics/              Economics research")
    text = text[:structure_start] + "\n".join(tree) + "\n" + text[structure_end:]

    section_start = text.index(START)
    section_end = text.index(END, section_start)
    return text[:section_start] + "\n".join(table) + "\n\n" + text[section_end:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if README is stale")
    args = parser.parse_args()

    entries = load_entries()
    current = README.read_text(encoding="utf-8")
    expected = replace_readme(current, entries)
    if args.check:
        if current != expected:
            print("README.md is out of date. Run: python scripts/update_catalog.py")
            return 1
        print("README.md catalog is up to date.")
        return 0

    README.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Updated {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
