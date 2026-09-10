# Push Preflight

Run within the selected repository before any push governed by this skill. This is a review procedure, not an automatic history-rewriting or file-deletion tool.

## Inspect the actual publication range

Resolve the exact remote, destination branch, and local source commit. Refresh destination refs. For an existing branch, inspect objects reachable from the source but not the verified destination history. For a new branch, inspect source history excluding only refs verified as already present in that same destination repository. Do not exclude arbitrary local branches, stale tracking refs, or a different fork's refs merely because they contain the objects.

Useful Git primitives are `git rev-list --objects <source> ^<verified-destination-ref>` and `git cat-file --batch-check` to identify object type and blob size. Supply exact verified refs; omit exclusions that cannot be verified, accepting a conservative review instead. New-branch publication must include historical blobs, not just files currently present. Avoid relying on `--all` or pushing tags/other branches that were not requested.

Inspect the changed paths and file modes across the outgoing commits as well as object sizes. A blob can appear under multiple paths, so the representative name from an object listing alone cannot classify every PDF or detect all literature-path associations. Filenames can contain spaces or non-ASCII characters; use structured/NUL-safe Git output where available rather than splitting on whitespace.

## Apply the defaults

- Block new publication of any file blob larger than 10,000,000 bytes unless specifically allowed.
- Review source-literature PDF provenance for every relevant outgoing version/path regardless of size. Renaming a paper does not change its role. If provenance is unknown, inspect project context or ask before publication.
- Check staged candidates separately before committing. Do not stage excluded files and expect push to filter them later: Git pushes commit history, not a selected file list.
- A Git LFS pointer or submodule entry is not an ordinary content blob. Check any upload hook/associated content that would be published; do not use indirection to evade the defaults. Do not assume parent-repository push also publishes submodule content.

Report blocked paths, sizes/roles, and containing outgoing commits. If historical content must be removed, preserve the local files and obtain authority for that precise history repair. A later deletion commit, ignore entry, or smaller latest version does not remove earlier blobs.

If ref visibility or classification is incomplete, say the preflight is incomplete and do not assert a clean push. After the check, ensure the source commit has not changed before pushing an explicit branch refspec without force. Recheck changed outgoing content if a new commit or remote update changes the reviewed range.

These defaults concern user upload preferences; an exception does not bypass repository restrictions, secrets checks, or the destination's technical limits.
