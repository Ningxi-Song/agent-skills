---
name: project-hygiene
description: Use when a coding or analysis task leaves mixed Git changes, duplicate/versioned files, temporary outputs, or an unclear commit scope; especially when asked to clean up, finish quickly, or commit.
---

# Project Hygiene

Keep working trees understandable without treating a clean Git status as the goal. Every uncommitted file should have a known owner, purpose, and next action.

## Operating modes

Use the lowest-cost mode that answers the question:

1. **Light check** at natural handoff points, when switching objectives, or before delivery. Run `git status --short`, note modified/untracked counts, and scan names for `v2`, `final`, `old`, `backup`, `copy`, `tmp`, or `draft`.
2. **Escalate** when a risk threshold is met: 8+ modified files, 3+ untracked files, a version/backup name, 3+ same-kind outputs, changes spanning unrelated directories, or files whose ownership is unclear. A bundled audit script can calculate the score: `python scripts/audit_project_hygiene.py`.
3. **Full audit** when escalated or explicitly requested. Capture the branch and baseline, inspect the complete diff, classify every file, compare suspected duplicates by content/schema/hash, and identify the smallest intended change set.

## Risk and classification

Use the score as a prompt to investigate, not as permission to mutate:

| Signal | Points |
|---|---:|
| 8+ modified files | 1 |
| 3+ untracked files | 1 |
| Version/backup/temp naming | 2 |
| 3+ same-kind outputs | 2 |
| Unrelated directories | 1 |
| Unknown task ownership | 2 |

Classify files as **task change**, **pre-existing change**, **deliverable**, **generated/temp**, **duplicate candidate**, or **unknown**. Preserve unknowns until the user resolves them. Newest timestamp, filename, or “final” is not proof of canonical status.

## Safe cleanup and commits

- Never use `git reset --hard`, broad deletion, broad overwrites, or `git add .` merely because the tree is messy or the user wants speed.
- Do not delete, rename, overwrite, ignore, or commit ambiguous files without explicit authorization and a named target.
- Prefer reversible moves to an explicitly named archive only after approval; do not hide uncertainty in `.gitignore`.
- For commits, selectively stage the intended files, inspect `git diff --cached` and `git diff --cached --name-status`, run relevant checks, then commit only when requested or required by the established workflow.
- Binary files and generated data require role/consumer checks, not text-diff assumptions. Check for secrets and sensitive data before staging.
- After any approved cleanup or commit, rerun status and report remaining changes, excluded files, and unresolved questions.

## Handoff report

Report four buckets: **keep**, **archive/remove with approval**, **ignore or regenerate**, and **needs user decision**. Include the risk score, exact paths, why each path was classified, the proposed next command, and whether the working tree was mutated. If pre-existing changes are mixed in, state how they were kept out of the proposed commit.

## Red flags

Stop and re-check when thinking: “the newest file must be right,” “clean means delete backups,” “the user said quickly,” “the diff is too large to inspect,” “Git can recover untracked files,” or “the build passes, so duplicates do not matter.”

## Common commands

```text
git status --short
git diff --stat
git diff --name-only
git diff --cached --name-status
git diff --cached
git ls-files --others --exclude-standard
```

The audit script is read-only and advisory. Run `python scripts/audit_project_hygiene.py --help` for JSON output and threshold options.
