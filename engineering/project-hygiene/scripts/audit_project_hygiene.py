#!/usr/bin/env python3
"""Read-only Git/project hygiene audit."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


VERSION_RE = re.compile(r"(?:^|[_ .-])(v\d+|final|old|backup|copy|tmp|draft)(?:$|[_ .-])", re.I)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], text=True, capture_output=True, check=True)
    return result.stdout.rstrip("\r\n")


def files_from_status() -> tuple[list[str], list[str]]:
    modified: list[str] = []
    untracked: list[str] = []
    for line in git("status", "--short").splitlines():
        if not line:
            continue
        code, path = line[:2], line[3:]
        if code == "??":
            untracked.append(path)
        else:
            modified.append(path)
    return modified, untracked


def normalized_stem(path: str) -> str:
    stem = Path(path).stem.lower()
    stem = re.sub(r"(?:[_ .-](?:v\d+|final|old|backup|copy|tmp|draft))+$", "", stem)
    return re.sub(r"[^a-z0-9]+", "_", stem).strip("_")


def audit() -> dict:
    root = git("rev-parse", "--show-toplevel")
    modified, untracked = files_from_status()
    paths = modified + untracked
    versioned = [p for p in paths if VERSION_RE.search(Path(p).stem)]
    groups: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        groups[normalized_stem(path)].append(path)
    duplicate_candidates = {key: value for key, value in groups.items() if key and len(value) >= 2}
    directories = {str(Path(path).parent) for path in paths}
    score = 0
    signals: list[str] = []
    if len(modified) >= 8:
        score += 1
        signals.append("8+ modified files")
    if len(untracked) >= 3:
        score += 1
        signals.append("3+ untracked files")
    if versioned:
        score += 2
        signals.append("version/backup/temp naming")
    if duplicate_candidates:
        score += 2
        signals.append("duplicate-name candidates")
    if len(directories) >= 3:
        score += 1
        signals.append("changes span 3+ directories")
    return {
        "root": root,
        "branch": git("branch", "--show-current"),
        "modified": modified,
        "untracked": untracked,
        "counts": {"modified": len(modified), "untracked": len(untracked)},
        "versioned_or_temporary_names": versioned,
        "duplicate_name_candidates": duplicate_candidates,
        "risk_score": score,
        "risk_level": "full-audit" if score >= 5 else "review" if score >= 3 else "light-check",
        "signals": signals,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a read-only project hygiene audit.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    try:
        report = audit()
    except subprocess.CalledProcessError as exc:
        print(f"Not a Git worktree or Git command failed: {exc}")
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
        return 0
    print(f"root: {report['root']}")
    print(f"branch: {report['branch'] or '(detached or unnamed)'}")
    print(f"risk: {report['risk_level']} ({report['risk_score']})")
    print(f"modified: {report['counts']['modified']}; untracked: {report['counts']['untracked']}")
    if report["signals"]:
        print("signals: " + ", ".join(report["signals"]))
    if report["versioned_or_temporary_names"]:
        print("version-like names:")
        print("\n".join(f"  - {path}" for path in report["versioned_or_temporary_names"]))
    if report["duplicate_name_candidates"]:
        print("duplicate-name candidates:")
        for key, paths in report["duplicate_name_candidates"].items():
            print(f"  - {key}: {', '.join(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
