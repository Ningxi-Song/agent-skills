# Shared Data Manifest

Use the project's existing data registry/configuration when it provides these semantics. Otherwise use a small version-controlled JSON manifest per task, for example `data-manifests/<task-id>.json`. Create one only for a task that uses external data; do not impose a new data system on code-only work.

## Storage and ownership

Choose a stable task ID, normally derived from the task branch. Resolve a project-specific local data root through existing configuration or an environment variable such as `PROJECT_DATA_ROOT`; keep machine-specific absolute paths out of committed manifests. If the root cannot be inferred, resolve that one choice before writing outputs. Existing data can remain in their established location, including the primary checkout if necessary, provided they are outside the removable task worktree and excluded from upload as applicable.

Suggested layout beneath that root:

```text
raw/                              shared inputs, read-only by default
tasks/<task-id>/intermediate/      task-owned temporary data
tasks/<task-id>/outputs/           task results, retained in place when accepted
```

Output paths do not need to change when a result becomes a mainline result. Do not overwrite retained outputs: create a new version/path and update the manifest. Shared data are not automatically backed up or available on another computer simply because the manifest is on GitHub.

## Manifest contract

Record `schema_version`, `task_id`, `branch`, `data_root_key`, and an `entries` array. Each entry contains:

| Field | Meaning |
|---|---|
| `path` | Relative file path under the configured data root; no absolute paths or parent traversal. |
| `role` | `input`, `result`, or `intermediate`. |
| `retention` | `keep` or `disposable`; input/result entries default to keep. |
| `owner_task` | Task ID for task-owned outputs; `shared` for shared inputs. |
| `purpose` | Short description explaining the file's consumer/use. |
| `size_bytes` | Exact size of a finalized retained file. |
| `sha256` | SHA-256 of a finalized retained file. |

Intermediate entries can omit size/checksum until finalized. Use per-file entries or a referenced per-file inventory for large collections, not deletion globs. Do not silently omit inventory content because it is inconveniently large; keep the summary manifest small and resolve storage of the detailed inventory explicitly.

Before publishing results, compute sizes and checksums from actual files. Never invent checksum values. Validate that each kept result exists, resolves inside the intended root, and matches its recorded identity. Results required by mainline must be marked `keep` before integration. A `disposable` marker indicates a potential cleanup candidate, not permission for deletion during ordinary synchronization.

## Mainline handoff and cleanup

Merge the manifest with task code through GitHub, then fast-forward local mainline. Verify mainline can resolve its retained result paths with local configuration. If checksum verification for very large data is expensive, finalize hashes once and reuse them only when file immutability is established; uncertainty is not a passing validation.

At cleanup, inspect manifests from current mainline and other retained task branches/worktrees, including unpublished manifests. Keep anything another task references, even if this task labels it disposable. If reference coverage or ownership is uncertain, preserve the candidate and report it. Original shared inputs are never task intermediates.

The phrase "delete this task worktree" in this agreed workflow covers its confirmed disposable intermediates, but not retained results, unknown data, or branch deletion. Validate the inventory before removing the worktree, since unpublished information in that directory may otherwise disappear. Do not remove a retained result from a shared directory merely because its producing task directory is gone.
