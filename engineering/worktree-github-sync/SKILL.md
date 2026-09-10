---
name: worktree-github-sync
description: Create a branch and worktree for a new development task; publish eligible files to GitHub, merge there once, fast-forward local mainline, and clean up completed task worktrees using data manifests. Use for explicit task-start, branch-sync, push, merge-and-sync, or task-worktree removal requests. Exclude files over 10 MB and original literature PDFs from upload unless specifically permitted.
---

# Worktree and GitHub Branch Sync

Synchronize committed history between a selected local worktree's branch and its corresponding GitHub branch. Success means their verified commit IDs match. Uncommitted files are a separate state, not content that Git push transfers.

## Trigger and scope

Use when the user asks to:

- Start a new development task with its own branch and worktree.
- Check whether a local branch/worktree matches its GitHub branch.
- Push local commits to GitHub or bring remote commits into a worktree.
- Synchronize the current worktree or an explicitly named set of worktrees.
- Merge a completed task and synchronize the local mainline, or remove its worktree.

Examples: "Sync this worktree with GitHub", "Push this branch", "Pull the remote changes", and "Which worktrees in this repository have unpushed commits?"

Do not activate merely because files are modified or worktrees exist. General workspace tidying is outside this skill. A task-start request starts the workflow; it does not authorize all later publishing or cleanup steps.

Default to the current worktree. Enumerate all registered worktrees only when the request covers them. Do not expand to unrelated repositories.

A status request permits inspection and fetching refs, not a push or a working-directory update. An explicit sync request authorizes ordinary non-forced push and fast-forward updates for the resolved branch pair; a push-only or pull-only request restricts direction. Honor existing authorization without asking again. Commit creation requires a request or established workflow that includes committing.

| User intent | Authorized workflow endpoint |
|---|---|
| Start a new development task | Create the local branch/worktree pair; report its location. |
| Check synchronization | Fetch and report differences only. |
| Push commits / synchronize branch | Publish existing eligible commits / synchronize the resolved pair. Do not infer PR merge or deletion. |
| Submit my task changes to GitHub | Review and commit intended eligible changes, then push. |
| Merge this task and sync mainline | Publish any authorized pending task commits, merge on GitHub, then fast-forward and verify local mainline. |
| Delete this completed task worktree | Run the cleanup gate; remove the worktree and confirmed disposable task intermediates, retain indexed results. Do not implicitly merge or delete branches. |

"The edits are finished" alone is not an instruction to merge or delete. Apply the requested step, not every later step in the lifecycle. These rules concern development work in the selected repository; do not create an app conversation merely to make a Git worktree.

## Resource routing

- For a task using external data, read [references/data-manifest.md](references/data-manifest.md) before creating or updating its manifest, and again when its data ownership is needed for cleanup.
- Before publication, read [references/push-preflight.md](references/push-preflight.md) for outgoing-history checks.
- Use [references/scenarios.md](references/scenarios.md) when reviewing this skill's decisions; it is not a checklist to run on every task.

## Agreed task lifecycle

1. For a new development task, create a local task branch and a corresponding independent worktree. Respect an existing app-created branch/worktree for that task instead of duplicating it. Resolve the base branch from context, inspect existing changes, and record the path and branch. Use the platform's supported worktree mechanism when available. Creating a task does not automatically publish a GitHub branch.
2. Develop and validate in the task worktree. Keep the local mainline worktree for receiving mainline updates; do not make routine task commits there.
3. When publication is requested, commit the intended changes if authorized, apply the file rules below, and push the task branch to its corresponding GitHub branch.
4. When integration is requested, merge the task branch into the GitHub mainline once, following the repository's PR/check requirements. Do not first merge it independently into the local mainline. If testing against the latest mainline is needed, incorporate that mainline into the task branch and validate there before publication.
5. Fetch the resulting GitHub mainline and fast-forward the clean local mainline worktree to it. Verify identical commit IDs. Dirty files or local-only mainline commits require inspection; do not hard-reset or force synchronization. The topic-branch divergence options below do not authorize rewriting the mainline or separately merging the task into it.
6. Only when cleanup is requested and the integration, mainline synchronization, and retained data have been verified, remove the task worktree using the supported worktree removal operation without force. Resolve its exact path, check for new/uncommitted work and active use, and preserve any unaccounted-for files. Remote branch deletion remains a separate action requiring authorization.

For a new task, default to the repository's resolved mainline base, refreshed from GitHub when available, rather than the current unrelated topic branch. Follow an explicitly specified base. If the refresh fails, disclose the cached base before proceeding with local task creation; do not claim it is current. Use a unique `codex/<task-slug>` branch unless the user names one. With no native lifecycle tool, create the pair with `git worktree add -b <branch> <absolute-path> <base-ref>` in the repository's established worktree location. Never reuse an occupied directory or branch from another task. Existing data remain in place; configuring a shared data root does not authorize relocating them.

After GitHub merges, verify the correct PR repository, base branch, and merged head. For squash/rebase merges, a failed ancestry check alone is not proof of missing integration: verify the merged PR head matches the published task commit. Any later task commits require separate handling before cleanup. Compare local mainline with freshly fetched remote mainline, which may include additional subsequent merges; it need not equal only this PR's merge commit.

## Cleanup gate

Treat deletion as the final, separately requested workflow step. Check all of the following immediately before acting:

- The worktree is registered to this repository, is not the mainline/primary checkout, and is not used by an active task. Move command execution to a retained directory before removing the target. If the app still requires that directory, defer removal through its supported lifecycle.
- No staged, unstaged, untracked, ignored valuable files, dirty submodules, ongoing Git operations, or unexplained locks would be lost. Inspect ignored files too; clean status alone is insufficient. Expected regenerable artifacts can be classified explicitly; unknown files stay pending.
- All task commits are accounted for by verified GitHub integration; local and remote mainline agree; retained manifest entries exist and validate. A pushed but unmerged task does not meet this completed-task cleanup gate.
- External deletion candidates are exact, task-owned entries marked disposable and not referenced by retained mainline results or any other task. Resolve symlinks/junctions and reject paths outside the configured task data directory. Do not recursively delete a whole data root or infer disposability from filenames or missing references.

Remove the worktree without force, then clean eligible external intermediates using the verified inventory. If either operation fails, report partial completion and retain remaining candidates. Keep local and remote branches unless branch deletion was also requested. Verify the removed path, remaining worktree registrations, and retained data. Report exact removed paths and recoverability: retained commits can restore code, but Git does not recover deleted untracked files or external data.

## Shared data and retained results

Keep large data in a shared directory outside removable worktrees. Commit a small result manifest with project-relative data paths (resolved against a configured data root), purpose, and checksums for the results to retain. The mainline receives this manifest through Git; the data remain in their existing locations. Do not move large files just to merge a task.

When task cleanup is requested, retain all data referenced by the mainline or another task. Remove external intermediate data only when explicitly identified as disposable task-owned outputs and covered by the cleanup request. Absence from a manifest is not evidence that a file is disposable. Validate exact deletion paths and references first; report any retained or unresolved data separately.

## Default GitHub file exclusions

- Do not upload files larger than 10 MB unless the user specifically permits those files. Interpret 10 MB as 10,000,000 bytes; exactly that size is not excluded by size alone.
- Do not upload original literature PDFs, regardless of size, unless the user specifically permits them. This covers downloaded papers, books, and other source literature. It does not automatically exclude task-generated PDF reports or figures, which still follow the size rule. Use provenance and role, not only the filename; resolve unclear PDFs before uploading them.
- A general request to push, synchronize, or finish a task is not an exception. Record any explicit exception with the named files or clearly bounded category. An exception to one rule does not silently waive the other; explicit permission to upload a named file can cover both when its size and role are clear.
- Keep excluded files local/shared and stage only eligible task files. Use narrow ignore entries where appropriate; do not blanket-ignore all PDFs. Git ignore rules do not implement size limits and do not exclude already tracked files.
- Before committing, inspect candidate file sizes and PDF roles. Before every push, inspect the file blobs in all outgoing history that would become newly reachable on GitHub, not just the current working directory or tip diff. Use Git object sizes for committed files. A large or literature PDF added and deleted in earlier outgoing commits still violates the rule.
- If excluded content is already in outgoing commits, stop that push and report the exact files/commits. Removing the file in a new commit or adding it to .gitignore does not remove historical content. Do not rewrite history without authorization covering that operation, and preserve the local data during any approved repair.
- Already published excluded content is not automatically authorization to upload new versions or permission to purge remote history. Report pre-existing exposure separately if discovered. Do not silently use Git LFS or another upload mechanism to bypass these exclusions.

## Resolve the branch pair

1. Inspect the selected worktree's absolute path, checked-out branch, HEAD, status, and any ongoing Git operation. Useful commands: `git rev-parse --show-toplevel`, `git symbolic-ref --quiet --short HEAD`, `git rev-parse HEAD`, and `git status --porcelain=v1 --untracked-files=all`. Run commands in the selected directory with `git -C <path>`.
2. Resolve the branch upstream and actual fetch/push destinations from Git configuration. Inspect `git branch -vv` and `git remote -v`; account for branch-specific push remotes and push URLs. Do not assume the remote is origin, the remote branch has the same name, or the intended branch is main.
3. In fork setups, distinguish the branch used for publication from an upstream base branch. Select the pair requested by the user. If configuration and context cannot resolve the intended GitHub repository/branch, ask for that specific missing destination before mutation.
4. With no configured upstream, infer a destination only from explicit user intent or unambiguous repository context. Publishing a new branch can use an explicit `git push -u <remote> <local-branch>:refs/heads/<remote-branch>` when publication is authorized. Do not recreate a previously deleted remote branch silently.
5. Detached HEAD has no checked-out local branch to synchronize. Report the commit and request a branch choice if absent from context; do not invent a branch as part of a status check.

For multiple worktrees, resolve each pair separately and fetch each relevant remote once where practical. Avoid modifying a worktree being actively changed by another task; report that pair as pending.

## Fetch and compare

Fetch the selected GitHub branch into an appropriate remote-tracking ref and verify that the fetch succeeded. Compare against the freshly fetched ref for the actual destination, not an unrelated upstream or stale FETCH_HEAD. If the branch is absent, distinguish a confirmed absence from a network/authentication failure.

Use `git rev-list --left-right --count HEAD...<fetched-remote-ref>`:

- First count: local-only commits (ahead).
- Second count: remote-only commits (behind).

If fetching fails, report remote state as unverified. Cached refs can inform a provisional report but cannot establish synchronization.

| State | Sync action |
|---|---|
| 0 ahead, 0 behind | No history update needed. Report any uncommitted files separately. |
| Ahead only | For push or bidirectional sync, inspect outgoing commits and push explicitly to the resolved destination without force. |
| Behind only | For pull or bidirectional sync, use `git merge --ff-only <fetched-remote-ref>` in a clean worktree. |
| Ahead and behind | Inspect divergence. Follow an already established merge/rebase policy for this same branch pair; if none exists, ask which integration strategy to use. Do not reset or force-push to erase divergence. |
| Remote branch absent | Publish only if creating that branch is authorized; otherwise report the missing destination. |

Respect direction: push-only does not authorize pulling, and pull-only does not authorize pushing. Report remaining mismatch rather than treating a one-direction operation as full synchronization.

## Uncommitted changes and interruptions

Inspect staged, unstaged, untracked, and submodule changes before updating local history. A dirty worktree does not prevent comparing refs or pushing existing commits, but those files remain local. State that explicitly.

If the request includes committing, review and selectively stage the intended changes, check for secrets, validate proportionately, and commit before comparing again. Otherwise do not auto-commit, stash, discard, or include unrelated files merely to achieve synchronization.

Defer incoming history updates while the worktree is dirty or a merge/rebase/cherry-pick is unfinished. Complete independent authorized comparisons or pushes where safe, and report the specific impediment. If an authorized integration conflicts, report the operation and affected files; do not claim synchronization or overwrite unrelated work.

On a non-fast-forward push rejection, fetch and reassess once. If the remote changes again, stop retrying and report concurrent updates. Never use force-push, hard reset, or automatic conflict-side selection as a synchronization shortcut.

## Verify and report

After an authorized mutation, reread local HEAD and verify the actual destination branch's commit ID with fresh remote evidence. If incoming history changed the worktree, rerun status and relevant project checks when warranted by the changes.

Report:

- Worktree path, local branch, and exact GitHub repository/branch.
- Action taken and ahead/behind counts, or why comparison remains unverified.
- Whether committed history matches, plus any remaining uncommitted files.
- Any unresolved destination, divergence, or operation blocking completion.

For several worktrees, use one row per branch pair. Do not label files as backed up merely because HEAD matches GitHub. Report excluded local files separately. Claim integration, mainline synchronization, or cleanup only for steps actually performed and verified.
