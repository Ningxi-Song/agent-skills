---
name: project-hygiene
description: Use when a coding or analysis task leaves mixed Git changes, duplicate/versioned files, temporary outputs, redundant or stale Git worktrees, or an unclear commit scope; especially when asked to clean up, finish quickly, or commit.
---

# Project Hygiene

Keep working trees understandable without treating a clean Git status as the goal. Every uncommitted file should have a known owner, purpose, and next action.

## Operating modes

Use the lowest-cost mode that answers the question:

1. **Light check** at natural handoff points, when switching objectives, or before delivery. Run `git status --short`, note modified/untracked counts, and scan names for `v2`, `final`, `old`, `backup`, `copy`, `tmp`, or `draft`.
2. **Escalate** when a risk threshold is met: 8+ modified files, 3+ untracked files, a version/backup name, 3+ same-kind outputs, changes spanning unrelated directories, files whose ownership is unclear, or more than one non-primary worktree. A bundled audit script can calculate the score: `python scripts/audit_project_hygiene.py`.
3. **Full audit** when escalated or explicitly requested. Capture the branch and baseline, inspect the complete diff, classify every file, compare suspected duplicates by content/schema/hash, inspect registered worktrees, and identify the smallest intended change set.

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
| More than one non-primary worktree | 1 |
| Missing worktree path or stale worktree registration | 2 |

Classify files as **task change**, **pre-existing change**, **deliverable**, **generated/temp**, **duplicate candidate**, or **unknown**. Classify worktrees as **current**, **primary checkout**, **active isolated task**, **clean stale candidate**, **dirty candidate**, **missing-path registration**, or **unknown**. Preserve unknowns until the user resolves them. Newest timestamp, filename, branch name, or “final” is not proof of canonical status.

## Worktree hygiene

A Codex task list is not a worktree inventory. Never infer that seven Codex tasks means seven Git worktrees, and never delete a worktree based only on a task-list count or UI label.

When the worktree risk threshold is met or the user asks about redundant worktrees:

1. Run `git worktree list --porcelain` from the repository.
2. Record each worktree's path, branch or detached commit, and whether it is the current or primary checkout.
3. For every non-primary worktree whose path exists, inspect without mutation:
   `git -C "<path>" status --short`,
   `git -C "<path>" log -1 --oneline`, and
   `git branch --merged "<base-branch>"` from the primary checkout when the base branch is known.
4. Treat a worktree as a **cleanup candidate** only when all of these are true: it is not current, not the primary checkout, has no uncommitted or untracked changes, its branch is merged into the intended base or the user explicitly abandoned it, and no active task still owns it.
5. Treat a missing path as a **stale registration**, not proof that its branch is disposable. Inspect the registration with `git worktree list --porcelain` and use `git worktree prune --dry-run` before any pruning.
6. Report worktrees in four buckets: **keep**, **remove with approval**, **stale registration to prune**, and **needs user decision**. Include exact paths, branches, dirty status, merge evidence, and the proposed command.
7. Do not run `git worktree remove`, `git worktree prune`, branch deletion, or broad directory deletion without explicit authorization for the named target. A clean worktree is not automatically redundant.

The skill may identify candidates and prepare commands, but it cannot reliably infer Codex task ownership from Git metadata alone. If the task-to-worktree mapping is unavailable, ask the user before removal.

## Safe cleanup and commits

- Never use `git reset --hard`, broad deletion, broad overwrites, or `git add .` merely because the tree is messy or the user wants speed.
- Do not delete, rename, overwrite, ignore, or commit ambiguous files without explicit authorization and a named target.
- Prefer reversible moves to an explicitly named archive only after approval; do not hide uncertainty in `.gitignore`.
- For worktrees, prefer `git worktree remove "<exact-path>"` only after the candidate checks above and explicit approval. Use `git worktree prune --dry-run` first for missing-path registrations; pruning removes stale administrative metadata, not a substitute for deciding whether a branch or existing directory is safe to remove.
- For commits, selectively stage the intended files, inspect `git diff --cached` and `git diff --cached --name-status`, run relevant checks, then commit only when requested or required by the established workflow.
- Binary files and generated data require role/consumer checks, not text-diff assumptions. Check for secrets and sensitive data before staging.
- After any approved cleanup or commit, rerun status and report remaining changes, excluded files, and unresolved questions.

## Handoff report

Report four buckets: **keep**, **archive/remove with approval**, **ignore or regenerate**, and **needs user decision**. For worktree audits, include a fifth explicit field for **stale registrations**. Include the risk score, exact paths, why each path was classified, the proposed next command, and whether the working tree was mutated. If pre-existing changes are mixed in, state how they were kept out of the proposed commit.

## Red flags

Stop and re-check when thinking: “the newest file must be right,” “clean means delete backups,” “the user said quickly,” “the diff is too large to inspect,” “Git can recover untracked files,” “a Codex task count equals a worktree count,” or “a clean worktree must be unused.” Do not turn any of these assumptions into a deletion.

## Common commands

```text
git status --short
git diff --stat
git diff --name-only
git diff --cached --name-status
git diff --cached
git ls-files --others --exclude-standard
git worktree list --porcelain
git -C "<worktree-path>" status --short
git -C "<worktree-path>" log -1 --oneline
git worktree prune --dry-run
```

The audit script is read-only and advisory. Run `python scripts/audit_project_hygiene.py --help` for JSON output and threshold options.
