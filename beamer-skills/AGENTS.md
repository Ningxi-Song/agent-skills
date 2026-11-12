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

## Default research presentation narrative

For academic research presentations, use `research-slide-narrative/SKILL.md` by default unless the user chooses another structure. It governs narrative and content density; pair it with the selected layout skill. Merge thin pages, keep results beside their interpretation, and preserve the user's required evidence and appendix policy.
