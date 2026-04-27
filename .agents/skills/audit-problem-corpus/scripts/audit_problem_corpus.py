#!/usr/bin/env python3
"""Audit the generated problem corpus for structural issues."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


REQUIRED_FILES = ("problem.md", "solution.md", "metadata.json")


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def collect_folder_issues(problem_dir: Path, min_testcases: int) -> dict:
    issues: list[str] = []

    for name in REQUIRED_FILES:
        if not (problem_dir / name).exists():
            issues.append(f"missing:{name}")

    code_dir = problem_dir / "code"
    code_files = sorted(path.name for path in code_dir.glob("*")) if code_dir.is_dir() else []
    if not code_dir.is_dir():
        issues.append("missing:code-dir")
    elif not code_files:
        issues.append("empty:code-dir")

    testcase_dir = problem_dir / "testcases"
    if not testcase_dir.is_dir():
        issues.append("missing:testcases-dir")
        testcase_pairs = 0
    else:
        inputs = {path.stem for path in testcase_dir.glob("*.in")}
        outputs = {path.stem for path in testcase_dir.glob("*.out")}
        testcase_pairs = len(inputs & outputs)
        if inputs != outputs:
            issues.append("mismatch:testcase-pairs")
        if testcase_pairs < min_testcases:
            issues.append(f"low:testcases<{min_testcases}")

    metadata = read_json(problem_dir / "metadata.json") if (problem_dir / "metadata.json").exists() else None
    if metadata is None:
        issues.append("invalid:metadata")
        title = problem_dir.name
    else:
        title = str(metadata.get("title") or problem_dir.name)

    return {
        "path": str(problem_dir),
        "folder": problem_dir.name,
        "title": title,
        "testcase_pairs": testcase_pairs,
        "code_files": code_files,
        "issues": issues,
        "issue_count": len(issues),
    }


def audit(root: Path, min_testcases: int) -> dict:
    items = []
    titles = defaultdict(list)

    for problem_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        item = collect_folder_issues(problem_dir, min_testcases)
        items.append(item)
        titles[item["title"]].append(item["path"])

    duplicate_titles = {
        title: paths
        for title, paths in titles.items()
        if title and len(paths) > 1
    }

    issue_counter = Counter()
    for item in items:
        issue_counter.update(item["issues"])

    return {
        "root": str(root),
        "total_folders": len(items),
        "folders_with_issues": sum(1 for item in items if item["issues"]),
        "duplicate_titles": duplicate_titles,
        "issue_counts": dict(issue_counter.most_common()),
        "items": items,
    }


def print_human(result: dict) -> None:
    print(f"root: {result['root']}")
    print(f"total_folders: {result['total_folders']}")
    print(f"folders_with_issues: {result['folders_with_issues']}")
    print("")
    print("issue_counts:")
    for issue, count in result["issue_counts"].items():
        print(f"  {issue}: {count}")

    if result["duplicate_titles"]:
        print("")
        print("duplicate_titles:")
        for title, paths in result["duplicate_titles"].items():
            print(f"  {title}:")
            for path in paths:
                print(f"    - {path}")

    print("")
    print("worst_folders:")
    worst = sorted(result["items"], key=lambda item: (-item["issue_count"], item["folder"]))[:10]
    for item in worst:
        issues = ", ".join(item["issues"]) or "(none)"
        print(f"  {item['folder']} :: issues={item['issue_count']} :: {issues}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit generated problem corpus structure.")
    parser.add_argument("root", help="Corpus root, usually problem/normal")
    parser.add_argument("--min-testcases", type=int, default=10, help="Minimum matched testcase pairs")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    root = Path(args.root)
    result = audit(root, args.min_testcases)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
