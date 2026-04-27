#!/usr/bin/env python3
"""Validate one generated problem bundle or an entire corpus."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = ("problem.md", "solution.md", "metadata.json")
REQUIRED_DIRS = ("code", "testcases")
REQUIRED_METADATA_KEYS = (
    "title",
    "created_at",
    "difficulty",
    "tags",
    "time_limit",
    "memory_limit",
    "source",
)
KNOWN_CODE_SUFFIXES = {".cpp", ".py", ".java", ".js", ".c", ".go", ".rs", ".php", ".rb", ".kt", ".swift", ".txt"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_title(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def extract_h1(markdown: str) -> str | None:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, re.MULTILINE)
    return match.group(1).strip() if match else None


def has_section(markdown: str, name: str) -> bool:
    return name in markdown


def find_problem_dirs(target: Path) -> list[Path]:
    if not target.exists():
        raise FileNotFoundError(f"Path not found: {target}")
    if target.is_dir() and (target / "metadata.json").exists():
        return [target]
    return sorted(path for path in target.iterdir() if path.is_dir())


def validate_bundle(problem_dir: Path, min_testcases: int) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    for filename in REQUIRED_FILES:
        if not (problem_dir / filename).exists():
            errors.append(f"missing file: {filename}")

    for dirname in REQUIRED_DIRS:
        if not (problem_dir / dirname).is_dir():
            errors.append(f"missing directory: {dirname}")

    metadata = {}
    metadata_path = problem_dir / "metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(read_text(metadata_path))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"invalid metadata.json: {exc}")
        else:
            for key in REQUIRED_METADATA_KEYS:
                if key not in metadata:
                    errors.append(f"metadata missing key: {key}")

    problem_path = problem_dir / "problem.md"
    problem_title = None
    if problem_path.exists():
        try:
            problem_text = read_text(problem_path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"unreadable problem.md: {exc}")
            problem_text = ""
        else:
            if not problem_text.strip():
                errors.append("problem.md is empty")
            problem_title = extract_h1(problem_text)
            if not problem_title:
                warnings.append("problem.md is missing a top-level heading")
            if "##" not in problem_text:
                warnings.append("problem.md has no level-2 sections")
            if not has_section(problem_text, "输入") and not has_section(problem_text, "Input"):
                warnings.append("problem.md does not show an obvious input section")
            if not has_section(problem_text, "输出") and not has_section(problem_text, "Output"):
                warnings.append("problem.md does not show an obvious output section")

    solution_path = problem_dir / "solution.md"
    if solution_path.exists():
        try:
            solution_text = read_text(solution_path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"unreadable solution.md: {exc}")
        else:
            if not solution_text.strip():
                errors.append("solution.md is empty")
            if "```" not in solution_text:
                warnings.append("solution.md has no fenced code blocks")

    metadata_title = metadata.get("title") if isinstance(metadata, dict) else None
    if problem_title and metadata_title and normalize_title(problem_title) != normalize_title(str(metadata_title)):
        warnings.append("metadata title does not match problem.md title")

    code_dir = problem_dir / "code"
    if code_dir.is_dir():
        code_files = sorted(path for path in code_dir.iterdir() if path.is_file())
        if not code_files:
            errors.append("code directory is empty")
        elif not any(path.suffix.lower() in KNOWN_CODE_SUFFIXES for path in code_files):
            warnings.append("code directory only contains unexpected file types")
    else:
        code_files = []

    testcase_dir = problem_dir / "testcases"
    testcase_count = 0
    if testcase_dir.is_dir():
        inputs = {path.stem for path in testcase_dir.glob("*.in")}
        outputs = {path.stem for path in testcase_dir.glob("*.out")}
        testcase_count = len(inputs & outputs)
        for stem in sorted(inputs - outputs):
            errors.append(f"missing output pair for testcase: {stem}")
        for stem in sorted(outputs - inputs):
            errors.append(f"missing input pair for testcase: {stem}")
        if testcase_count < min_testcases:
            errors.append(
                f"testcase pairs below minimum: found {testcase_count}, expected at least {min_testcases}"
            )

    return {
        "path": str(problem_dir),
        "title": metadata_title or problem_title or problem_dir.name,
        "testcase_pairs": testcase_count,
        "code_files": [path.name for path in code_files],
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }


def print_human(results: list[dict]) -> None:
    for item in results:
        status = "OK" if item["ok"] else "FAIL"
        print(f"[{status}] {item['title']} :: {item['path']}")
        print(f"  testcase_pairs: {item['testcase_pairs']}")
        print(f"  code_files: {', '.join(item['code_files']) or '(none)'}")
        for error in item["errors"]:
            print(f"  error: {error}")
        for warning in item["warnings"]:
            print(f"  warning: {warning}")

    total = len(results)
    failed = sum(1 for item in results if not item["ok"])
    warnings = sum(len(item["warnings"]) for item in results)
    print("")
    print(f"validated: {total}")
    print(f"failed: {failed}")
    print(f"warnings: {warnings}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate problem bundle structure.")
    parser.add_argument("target", help="Problem folder or corpus root")
    parser.add_argument("--min-testcases", type=int, default=1, help="Minimum matched testcase pairs")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text")
    args = parser.parse_args()

    target = Path(args.target)
    try:
        problem_dirs = find_problem_dirs(target)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 2

    results = [validate_bundle(problem_dir, args.min_testcases) for problem_dir in problem_dirs]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_human(results)

    return 1 if any(not item["ok"] for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
