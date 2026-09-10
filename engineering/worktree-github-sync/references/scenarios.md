# Synchronization Scenarios

Use these cases to review scope and decisions without modifying a live repository.

| Request and evidence | Expected behavior |
|---|---|
| "Check whether this worktree matches GitHub." Local is ahead by two commits. | Fetch and report 2 ahead / 0 behind. Do not push on a status-only request. |
| "Sync this worktree." Local is ahead, destination is unambiguous. | Inspect outgoing commits, push without force, and verify destination HEAD. No repeated permission request for the already authorized sync. |
| "Sync this worktree." Remote is ahead and local files are clean. | Fetch, fast-forward, and verify matching commits. |
| "Sync this worktree." Remote is ahead and a tracked file is modified. | Report the incoming commits and local modification; defer the local update without auto-stashing or committing. |
| "Push this branch." Local commits are ahead and untracked files exist. | Push the committed history when safe; explicitly report that untracked files were not transferred. |
| "Sync this worktree." Local and remote each have new commits, no integration policy exists. | Inspect divergence and ask for the merge/rebase choice. Do not force-push. |
| "Pull remote changes." Both sides have new commits and an established merge policy exists. | Apply the authorized integration policy if the tree is clean, but do not push the resulting local commits. Report remaining mismatch. |
| "Sync this branch." No upstream and two plausible GitHub destinations exist. | Ask for the destination repository/branch before mutation. |
| Configured upstream belongs to a base repository, while the requested publication branch is in a fork. | Compare and synchronize the requested fork branch; do not substitute the base branch. |
| "Check sync." Cached upstream matches HEAD, but fetch fails. | Mark GitHub state unverified; do not claim synchronization. |
| "Sync this worktree." Its previously tracked remote branch was deleted. | Report confirmed absence; do not recreate the branch without authority to publish it. |
| "Sync this worktree." HEAD is detached and no branch choice is given. | Report detached HEAD and ask for the intended branch. |
| "Check all worktrees in this repository." Several are registered. | Compare each resolved branch pair, fetching shared remotes efficiently; do not create or delete anything. |
| "Start a new development task." | Create a task branch and independent worktree, or reuse the platform-created pair for this task. Do not publish automatically. |
| "Merge the completed task." | Merge on GitHub when authorized, then fast-forward local mainline to the GitHub result. Do not independently merge on both sides. |
| GitHub merge succeeded, but local mainline has local-only commits. | Inspect and report divergence; do not reset mainline or force synchronization. |
| "Sync this worktree." Both commit IDs match, but local edits remain. | Report committed history synchronized and local edits not uploaded. |
| Candidate output is 10,000,001 bytes, with no explicit exception. | Exclude it from GitHub publication and retain it locally/shared. |
| Generated report is exactly 10,000,000 bytes. | Size alone does not exclude it; inspect normal scope and content before publication. |
| Downloaded source paper is a 500 KB PDF. | Exclude it as original literature even though it is small. |
| Task-generated figure is a 500 KB PDF. | Do not exclude it merely because it is a PDF. |
| User says "push everything" without specifically overriding file exclusions. | Apply both exclusions; general push language is not an exception. |
| User specifically permits uploading an identified 12 MB source paper. | Treat the informed file-specific instruction as an exception to both defaults. |
| Outgoing history added a 20 MB file and subsequently deleted it. | Block the push; tip deletion and ignore entries do not remove the historical blob. |
| Cleanup requested; mainline manifest references data in the task's external output directory. | Retain those data in place; delete only confirmed disposable outputs covered by the request. |
| New task requested while an unrelated topic branch is checked out. | Resolve the mainline base and create a separate task pair; do not silently branch from the unrelated topic. |
| Platform already created an isolated task worktree and branch. | Reuse it; do not create a second pair for the same task. |
| Squash-merged PR matches the published task head; raw ancestry check fails. | Verify PR evidence and current mainline rather than treating ancestry failure as missing work. |
| Task HEAD has new commits after the merged PR. | Retain the worktree pending integration of those commits. |
| A clean task worktree contains an ignored, unclassified local file. | Preserve it and defer removal until its disposition is known. |
| A disposable intermediate is referenced by another task's manifest. | Keep it; a reference overrides its producer's disposable classification. |
| A manifest path escapes the task data directory through a junction. | Reject it as an external deletion candidate. |
| User requests only branch synchronization, and the task is ready to merge. | Synchronize the branch; do not infer permission for GitHub integration. |
| The task worktree was removed but external intermediate deletion fails. | Report partial cleanup and the remaining paths; do not claim full completion. |
