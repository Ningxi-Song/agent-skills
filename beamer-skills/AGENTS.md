# Beamer Skills Repository Rules

When adding, renaming, removing, or materially changing a skill:

1. Update `catalog/skills.json`.
2. Regenerate the parent repository README with:
   `python scripts/update_catalog.py`.
3. Run `python scripts/update_catalog.py --check` and
   `python -m unittest discover -s tests -p "test_*.py"` before completing.

The catalog is the single source of truth for the Beamer skills index. Do not
manually edit the generated Beamer section or its directory listing in the
parent README.
